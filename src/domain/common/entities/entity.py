from abc import ABC, abstractmethod


class Entity(ABC):

    @abstractmethod
    def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, **kwargs):
        raise NotImplementedError
