from abc import ABC, abstractmethod

named_ps = AttrDict()
named_tiles = AttrDict()


class PlatformFamily(ABC):
    @abstractmethod
    def get_platform_classes(self):
        pass

    @abstractmethod
    def get_shelter_classes(self):
        pass

    @abstractmethod
    def get_sprite(self, location, platform_class, shelter_class):
        pass


def register(pf: PlatformFmaily):
    platform_classes = pf.get_platform_classes
    shelter_classes = pf.get_shelter_classes
