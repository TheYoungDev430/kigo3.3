from kigo.app import App
from kigo.ui import Window
from kigo.touchscreen import TouchArea


class TouchDemo(App):
    def on_start(self):
        self.window = Window(title="Touch Demo", size=(600, 400))

        def tap(pos):
            print("Tap:", pos)

        def drag(a, b):
            print("Drag:", a, "→", b)

        def pinch(scale):
            print("Pinch scale:", scale)

        touch = TouchArea(
            on_tap=tap,
            on_drag=drag,
            on_pinch=pinch
        )

        self.window.set_content(touch)
        self.window.show()


TouchDemo(dev=True).run()