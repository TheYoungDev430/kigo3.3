# SPDX-License-Identifier: Zlib
# kigo/touchscreen/touch.py

from __future__ import annotations
from typing import Callable, Dict, Optional, Tuple

from kigo.qt import QtCore, QtWidgets


Point = Tuple[float, float]


class Touch:
    """
    Kivy-like touch object.
    """
    def __init__(self, uid: int, pos: Point):
        self.uid = uid
        self.pos = pos
        self.start_pos = pos
        self.last_pos = pos

        self.dx = 0.0
        self.dy = 0.0

    def update(self, pos: Point):
        self.dx = pos[0] - self.last_pos[0]
        self.dy = pos[1] - self.last_pos[1]
        self.last_pos = self.pos
        self.pos = pos


class TouchWidget(QtWidgets.QWidget):
    """
    Kivy-style touch dispatcher for Kigo.
    """

    def __init__(
        self,
        *,
        on_touch_down: Optional[Callable[[Touch], None]] = None,
        on_touch_move: Optional[Callable[[Touch], None]] = None,
        on_touch_up: Optional[Callable[[Touch], None]] = None,
        parent=None,
    ):
        super().__init__(parent)

        self.on_touch_down = on_touch_down
        self.on_touch_move = on_touch_move
        self.on_touch_up = on_touch_up

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.setMouseTracking(True)

        self._touches: Dict[int, Touch] = {}
        self._mouse_touch_id = -1

    # -----------------------------
    # Touchscreen events
    # -----------------------------
    def event(self, event):
        et = event.type()

        if et == QtCore.QEvent.Type.TouchBegin:
            return self._touch_begin(event)
        if et == QtCore.QEvent.Type.TouchUpdate:
            return self._touch_update(event)
        if et == QtCore.QEvent.Type.TouchEnd:
            return self._touch_end(event)

        return super().event(event)

    def _touch_begin(self, event):
        for p in event.points():
            pos = (p.position().x(), p.position().y())
            t = Touch(p.id(), pos)
            self._touches[p.id()] = t
            if self.on_touch_down:
                self.on_touch_down(t)
        return True

    def _touch_update(self, event):
        for p in event.points():
            t = self._touches.get(p.id())
            if not t:
                continue
            pos = (p.position().x(), p.position().y())
            t.update(pos)
            if self.on_touch_move:
                self.on_touch_move(t)
        return True

    def _touch_end(self, event):
        for p in event.points():
            t = self._touches.pop(p.id(), None)
            if t and self.on_touch_up:
                self.on_touch_up(t)
        return True

    # -----------------------------
    # Mouse fallback (as single touch)
    # -----------------------------
    def mousePressEvent(self, e):
        pos = (e.position().x(), e.position().y())
        t = Touch(self._mouse_touch_id, pos)
        self._touches[self._mouse_touch_id] = t
        if self.on_touch_down:
            self.on_touch_down(t)

    def mouseMoveEvent(self, e):
        t = self._touches.get(self._mouse_touch_id)
        if not t:
            return
        pos = (e.position().x(), e.position().y())
        t.update(pos)
        if self.on_touch_move:
            self.on_touch_move(t)

    def mouseReleaseEvent(self, e):
        t = self._touches.pop(self._mouse_touch_id, None)
        if t and self.on_touch_up:
            self.on_touch_up(t)

