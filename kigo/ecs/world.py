from collections import defaultdict
from typing import Dict, Type, Set

from .entity import EntityId
from .component import Component
from .system import System


class World:
    def __init__(self):
        self._next_entity: EntityId = 1
        self._components: Dict[Type[Component], Dict[EntityId, Component]] = defaultdict(dict)
        self._systems: list[System] = []

    # ----------------------------
    # Entity
    # ----------------------------
    def create_entity(self) -> EntityId:
        eid = self._next_entity
        self._next_entity += 1
        return eid

    def remove_entity(self, entity: EntityId):
        for comp_map in self._components.values():
            comp_map.pop(entity, None)

    # ----------------------------
    # Components
    # ----------------------------
    def add_component(self, entity: EntityId, component: Component):
        self._components[type(component)][entity] = component

    def remove_component(self, entity: EntityId, component_type: Type[Component]):
        self._components[component_type].pop(entity, None)

    def get_component(self, entity: EntityId, component_type: Type[Component]):
        return self._components[component_type].get(entity)

    def get_entities_with(self, *component_types: Type[Component]) -> Set[EntityId]:
        if not component_types:
            return set()

        entity_sets = [
            set(self._components[ct].keys())
            for ct in component_types
            if ct in self._components
        ]

        return set.intersection(*entity_sets) if entity_sets else set()

    # ----------------------------
    # Systems
    # ----------------------------
    def add_system(self, system: System):
        self._systems.append(system)

    def update(self, dt: float):
        for system in self._systems:
            system.update(self, dt)
