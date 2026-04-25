from kigo.ecs import World, Component, System

class Position(Component):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Velocity(Component):
    def __init__(self, vx=0, vy=0):
        self.vx = vx
        self.vy = vy

class MovementSystem(System):
    def update(self, world, dt):
        for e in world.get_entities_with(Position, Velocity):
            pos = world.get_component(e, Position)
            vel = world.get_component(e, Velocity)
            pos.x += vel.vx * dt
            pos.y += vel.vy * dt

world = World()
e = world.create_entity()
world.add_component(e, Position())
world.add_component(e, Velocity(10, 0))
world.add_system(MovementSystem())

world.update(1.0)