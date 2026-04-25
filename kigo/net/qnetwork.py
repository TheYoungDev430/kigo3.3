# SPDX-License-Identifier: Zlib
# kigo/net/qnetwork.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Union

from kigo.qt.backend import QtCore, QtGui  # backend chooses PyQt6/PySide6

# QtNetwork is a separate module
try:
    from PyQt6 import QtNetwork as _QtNetwork  # type: ignore
except Exception:
    from PySide6 import QtNetwork as _QtNetwork  # type: ignore


@dataclass
class Response:
    url: str
    status: int
    headers: Dict[str, str]
    data: bytes
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.error is None and 200 <= self.status < 400

    @property
    def text(self) -> str:
        # best-effort decode
        try:
            return self.data.decode("utf-8")
        except Exception:
            try:
                return self.data.decode("latin-1")
            except Exception:
                return self.data.decode(errors="replace")


class _NetClient(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.manager = _QtNetwork.QNetworkAccessManager()

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Union[str, bytes]] = None,
        timeout_ms: int = 15000,
    ) -> Response:
        method = method.upper().strip()

        qurl = QtCore.QUrl(url)
        req = _QtNetwork.QNetworkRequest(qurl)

        # headers
        if headers:
            for k, v in headers.items():
                req.setRawHeader(k.encode("utf-8"), v.encode("utf-8"))

        # body
        payload = None
        if body is not None:
            if isinstance(body, str):
                payload = body.encode("utf-8")
            else:
                payload = body

        # Fire request
        if method == "GET":
            reply = self.manager.get(req)
        elif method == "POST":
            reply = self.manager.post(req, payload or b"")
        elif method == "PUT":
            reply = self.manager.put(req, payload or b"")
        elif method == "DELETE":
            reply = self.manager.deleteResource(req)
        else:
            # generic/custom methods
            reply = self.manager.sendCustomRequest(req, method.encode("utf-8"), payload or b"")

        # Wait (sync wrapper)
        loop = QtCore.QEventLoop()

        # Timeout
        timed_out = {"flag": False}
        timer = QtCore.QTimer()
        timer.setSingleShot(True)

        def _on_timeout():
            timed_out["flag"] = True
            try:
                reply.abort()
            except Exception:
                pass
            loop.quit()

        timer.timeout.connect(_on_timeout)
        timer.start(max(1, int(timeout_ms)))

        reply.finished.connect(loop.quit)
        loop.exec()

        timer.stop()

        # Build response
        final_url = reply.url().toString()

        # status code
        status = reply.attribute(_QtNetwork.QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        status = int(status) if status is not None else 0

        # headers
        hdrs: Dict[str, str] = {}
        for h in reply.rawHeaderList():
            k = bytes(h).decode("utf-8", errors="replace")
            v = bytes(reply.rawHeader(h)).decode("utf-8", errors="replace")
            hdrs[k] = v

        # data
        data = bytes(reply.readAll())

        # error
        err = None
        if timed_out["flag"]:
            err = f"timeout after {timeout_ms}ms"
        else:
            if reply.error() != _QtNetwork.QNetworkReply.NetworkError.NoError:
                err = reply.errorString()

        reply.deleteLater()
        return Response(url=final_url, status=status, headers=hdrs, data=data, error=err)


# singleton client (simple + fast)
_client = _NetClient()


def req(url: str, *, timeout_ms: int = 15000, headers: Optional[Dict[str, str]] = None) -> Response:
    """
    Simple GET request.

    Usage:
        from kigo.net import req
        r = req("https://example.com")
        print(r.status, r.ok)
        print(r.text)
    """
    return _client.request("GET", url, headers=headers, timeout_ms=timeout_ms)


def post(url: str, body: Union[str, bytes], *, timeout_ms: int = 15000, headers: Optional[Dict[str, str]] = None) -> Response:
    return _client.request("POST", url, headers=headers, body=body, timeout_ms=timeout_ms)


def put(url: str, body: Union[str, bytes], *, timeout_ms: int = 15000, headers: Optional[Dict[str, str]] = None) -> Response:
    return _client.request("PUT", url, headers=headers, body=body, timeout_ms=timeout_ms)


def delete(url: str, *, timeout_ms: int = 15000, headers: Optional[Dict[str, str]] = None) -> Response:
    return _client.request("DELETE", url, headers=headers, timeout_ms=timeout_ms)
