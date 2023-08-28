import math
import os
import grf
import functools
from pygorender import Config, render, hill_positor_1, compose, self_compose, produce_empty
from agrf.graphics.rotator import unnatural_dimens
from agrf.graphics.spritesheet import spritesheet_template
from copy import deepcopy
from agrf.actions import FakeReferencingGenericSpriteLayout


class LazyVoxel(Config):
    def __init__(
        self,
        name,
        *,
        prefix=None,
        voxel_getter=None,
        load_from=None,
        config=None,
    ):
        super().__init__(load_from=load_from, config=config)
        self.name = name
        self.prefix = prefix
        self.voxel_getter = voxel_getter
        self._update_dimensions()

    def _update_dimensions(self):
        if "agrf_unnaturalness" not in self.config:
            return
        bounding_box = self.config["size"]
        for x in self.config["sprites"]:
            x["width"], x["height"] = map(
                math.ceil,
                unnatural_dimens(
                    x["angle"], bounding_box, self.config["agrf_scale"], unnaturalness=self.config["agrf_unnaturalness"]
                ),
            )

    @functools.cache
    def rotate(self, delta, suffix):
        new_config = deepcopy(self.config)
        for x in new_config["sprites"]:
            x["angle"] += delta
        return LazyVoxel(
            self.name,
            prefix=os.path.join(self.prefix, suffix),
            voxel_getter=self.voxel_getter,
            config=new_config,
        )

    @functools.cache
    def change_pitch(self, delta, suffix):
        def voxel_getter():
            old_path = self.voxel_getter()
            new_path = os.path.join(self.prefix, suffix)
            hill_positor_1(old_path, new_path, delta)
            return os.path.join(new_path, f"{self.name}.vox")

        new_config = deepcopy(self.config)
        new_config["agrf_zdiff"] = new_config.get("agrf_zdiff", 0.0) + new_config["agrf_real_x"] / 2 * math.sin(
            math.radians(abs(delta))
        )

        return LazyVoxel(
            self.name,
            prefix=os.path.join(self.prefix, suffix),
            voxel_getter=voxel_getter,
            config=new_config,
        )

    def update_config(self, new_config, suffix):
        return LazyVoxel(
            self.name,
            prefix=os.path.join(self.prefix, suffix),
            voxel_getter=self.voxel_getter,
            config={**self.config, **new_config},
        )

    @functools.cache
    def flip(self, suffix):
        new_config = deepcopy(self.config)
        for x in new_config["sprites"]:
            x["flip"] = not x.get("flip", False)
        return LazyVoxel(
            self.name,
            prefix=os.path.join(self.prefix, suffix),
            voxel_getter=self.voxel_getter,
            config=new_config,
        )

    @functools.cache
    def compose(self, subvoxel, suffix, colour_map=None):
        def voxel_getter(subvoxel=subvoxel):
            old_path = self.voxel_getter()
            new_path = os.path.join(self.prefix, suffix)
            if isinstance(subvoxel, str):
                subvoxel_path = subvoxel
            else:
                subvoxel_path = subvoxel.voxel_getter()
            if colour_map is not None:
                extra_config = colour_map.positor_config()
            else:
                extra_config = {}
            compose(old_path, subvoxel_path, new_path, extra_config)
            return os.path.join(new_path, f"{self.name}.vox")

        return LazyVoxel(
            self.name,
            prefix=os.path.join(self.prefix, suffix),
            voxel_getter=voxel_getter,
            config=deepcopy(self.config),
        )

    @functools.cache
    def self_compose(self, suffix, colour_map=None):
        def voxel_getter():
            old_path = self.voxel_getter()
            new_path = os.path.join(self.prefix, suffix)
            if colour_map is not None:
                extra_config = colour_map.positor_config()
            else:
                extra_config = {}
            self_compose(old_path, new_path, extra_config)
            return os.path.join(new_path, f"{self.name}.vox")

        return LazyVoxel(
            self.name,
            prefix=os.path.join(self.prefix, suffix),
            voxel_getter=voxel_getter,
            config=deepcopy(self.config),
        )

    @functools.cache
    def produce_empty(self, suffix):
        def voxel_getter():
            old_path = self.voxel_getter()
            new_path = os.path.join(self.prefix, suffix)
            produce_empty(old_path, new_path)
            return os.path.join(new_path, f"{self.name}.vox")

        return LazyVoxel(
            self.name,
            prefix=os.path.join(self.prefix, suffix),
            voxel_getter=voxel_getter,
            config=deepcopy(self.config),
        )

    def render(self):
        voxel_path = self.voxel_getter()
        render(self, voxel_path, os.path.join(self.prefix, self.name))

    @functools.cache
    def spritesheet(self, xdiff, shift):
        return spritesheet_template(
            xdiff,
            os.path.join(self.prefix, self.name),
            [(x["width"], x.get("height", 0)) for x in self.config["sprites"]],
            [x["angle"] for x in self.config["sprites"]],
            bbox=self.config["size"],
            bbox_joggle=self.config.get("agrf_bbox_joggle", None),
            ydiff=self.config.get("agrf_zdiff", 0) * 0.5 * self.config.get("agrf_scale", 1),
            bpps=self.config["agrf_bpps"],
            scales=self.config["agrf_scales"],
            shift=shift,
        )

    @functools.cache
    def get_action(self, xdiff, shift, feature):
        return FakeReferencingGenericSpriteLayout(feature, (self.spritesheet(xdiff, shift),))

    def get_default_graphics(self):
        return self


class LazySpriteSheet:
    def __init__(self, sprites, indices):
        self.sprites = sprites
        self.indices = indices

    def __getattr__(self, name):
        def method(*args, **kwargs):
            call = lambda x: getattr(x, name)(*args, **kwargs)
            return LazySpriteSheet(tuple(call(x) for x in self.sprites), self.indices)

        return method

    @functools.cache
    def spritesheet(self, xdiff, shift):
        spritesheets = [x.spritesheet(xdiff, shift) for x in self.sprites]
        return [spritesheets[i][j] for (i, j) in self.indices]

    @functools.cache
    def get_action(self, xdiff, shift, feature):
        return FakeReferencingGenericSpriteLayout(feature, (self.spritesheet(xdiff, shift),))

    def get_default_graphics(self):
        return self


class LazyAlternatives:
    def __init__(self, sprites, loading_sprites=None):
        self.sprites = sprites
        self.loading_sprites = loading_sprites

    def __getattr__(self, name):
        def method(*args, **kwargs):
            call = lambda x: getattr(x, name)(*args, **kwargs)
            return LazyAlternatives(
                tuple(call(x) for x in self.sprites),
                None if self.loading_sprites is None else tuple(call(x) for x in self.loading_sprites),
            )

        return method

    @functools.cache
    def get_action(self, xdiff, shift, feature):
        return FakeReferencingGenericSpriteLayout(
            feature,
            tuple(x.spritesheet(xdiff, shift) for x in self.sprites),
            None if self.loading_sprites is None else tuple(x.spritesheet(xdiff, shift) for x in self.loading_sprites),
        )

    def get_default_graphics(self):
        return self.sprites[-1]


class LazySwitch:
    def __init__(self, ranges, default, code):
        self.ranges = ranges
        self.default = default
        self.code = code

    def __getattr__(self, name):
        def method(*args, **kwargs):
            call = lambda x: getattr(x, name)(*args, **kwargs)
            new_ranges = {k: call(v) for k, v in self.ranges.items()}
            new_default = call(self.default)
            return LazySwitch(new_ranges, new_default, self.code)

        return method

    def render(self):
        for v in self.ranges.values():
            v.render()
        self.default.render()

    @functools.cache
    def get_action(self, xdiff, shift, feature):
        return grf.Switch(
            ranges={k: v.get_action(xdiff, shift, feature) for k, v in self.ranges.items()},
            default=self.default.get_action(xdiff, shift, feature),
            code=self.code,
        )

    def get_default_graphics(self):
        return self.default.get_default_graphics()
