from kigo.qt.backend import QtWebEngineWidgets, QtWebChannel
from kigo.inspector.web.bridge import DOMBridge

def enable_dom_inspector(view: QtWebEngineWidgets.QWebEngineView):
    page = view.page()

    channel = QtWebChannel.QWebChannel(page)
    bridge = DOMBridge()
    channel.registerObject("kigoInspector", bridge)
    page.setWebChannel(channel)

    page.runJavaScript("""
        (function () {
            document.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();

                const el = e.target;
                const rect = el.getBoundingClientRect();

                kigoInspector.notify({
                    tag: el.tagName,
                    id: el.id,
                    class: el.className,
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height
                });
            }, true);
        })();
    """)

    return bridge