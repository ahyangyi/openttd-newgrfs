import os
import subprocess
import json
import tempfile
from copy import deepcopy


class Config:
    def __init__(self, load_from=None, config=None):
        if load_from is None:
            self.config = {}
        else:
            with open(load_from) as f:
                self.config = json.load(f)
        if config is not None:
            self.config.update(config)

    def copy(self):
        return Config(config=deepcopy(self.config))


def render(config, vox_path, output_path=None):
    if output_path is not None:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        output_clause = ["-o", output_path]
    else:
        output_clause = []

    if config is None:
        subprocess.run(["gorender", "-s", "4,2,1", "-p"] + output_clause + [vox_path], check=True)
        return

    with tempfile.NamedTemporaryFile("w") as f:
        json.dump(config.config, f)
        f.flush()
        subprocess.run(["gorender", "-s", "4,2,1", "-m", f.name, "-p"] + output_clause + [vox_path], check=True)


def positor(config, vox_path, new_path):
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    conf = config.copy()
    conf["files"] = [vox_path]
    with tempfile.NamedTemporaryFile("w") as f:
        json.dump(conf, f)
        f.flush()
        subprocess.run(["positor", "-o", new_path, f.name], check=True)


def hill_positor_1(vox_path, new_path, degree):
    config = {
        "operations": [
            {"name": "", "type": "rotate_y", "angle": degree},
        ],
    }

    positor(config, vox_path, new_path)


def compose(vox_path, subvox_path, new_path, extra_config):
    config = {
        "operations": [
            {"name": "", "type": "repeat", "n": 1, "file": subvox_path, **extra_config},
        ],
    }

    positor(config, vox_path, new_path)


def self_compose(vox_path, new_path, extra_config):
    config = {
        "operations": [
            {
                "name": "",
                "type": "repeat",
                "n": 1,
                "file": vox_path,
                "ignore_mask": True,
                "overwrite": True,
                **extra_config,
            },
        ],
    }

    positor(config, vox_path, new_path)


def produce_empty(vox_path, new_path):
    config = {
        "operations": [
            {"name": "", "type": "produce_empty"},
        ],
    }

    positor(config, vox_path, new_path)
