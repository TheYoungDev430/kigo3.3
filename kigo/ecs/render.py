# kigo/ecs/render.py
from kigo.ecs.system import System
from kigo.ecs.world import World
from kigo.qt.backend import QtGui
from .render import Transform, Renderable


class RenderSystem(System):
    """
    Pulls render data from ECS and issues draw calls.
    """

    def __init__(self, painter: QtGui.QPainter):
        self.painter = painter

    def update(self, world: World, dt: float):
        entities = world.get_entities_with(Transform, Renderable)

        for e in entities:
            transform = world.get_component(e, Transform)
            renderable = world.get_component(e, Renderable)

            self._draw(transform, renderable)

    def _draw(self, t: Transform, r: Renderable):
        self.painter.save()
        self.painter.translate(t.x, t.y)
        self.painter.rotate(t.rotation)
        self.painter.scale(t.scale, t.scale)

        if r.kind == "rect":
            self.painter.drawRect(0, 0, 50, 50)

        elif r.kind == "image" and r.resource:
            pix = QtGui.QPixmap(r.resource)
            self.painter.drawPixmap(0, 0, pix)

        self.painter.restore()