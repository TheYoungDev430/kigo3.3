from kigo.app import App
from kigo.ui import Window
from kigo.gpu import ShaderView

shader = smoke   # 🔁 swap fire / water / smoke

class SmokeDemo(App):
    def on_start(self):
        self.window = Window(title="Kigo Smoke Shader", size=(600, 400))
        self.view = ShaderView(fragment_shader=shader)
        self.window.set_content(self.view)
        self.window.show()

        self.t = 0.0
        self.schedule(self.update)

    def update(self, dt):
        self.t += dt
        self.view.set_uniform("time", self.t)

SmokeDemo(dev=True).run()