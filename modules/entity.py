__author__ = "Al0n1"
__version__ = "0.0.3"


class Entity:
    def __init__(self):
        self.components = {}

    def add_component(self, component):
        self.components[type(component)] = component

    def get_component(self, component_class):
        return self.components.get(component_class, None)
