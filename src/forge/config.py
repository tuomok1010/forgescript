'''
This script is responsible for reading the config file.
'''

import tomllib

# Default config values
DEFAULTS = {
    "compiler": "clang++",
    "compiler_flags": ["-g", "-Wall"],
    "linker_flags": ["-Wl,--verbose"],
    "output_name": "program",
    "build_dir": "build",
    "obj_dir": "build/obj",
    "include_dirs": ["include"],
    "source_dirs": ["src"],
    "log_dir": "log",
    "lib_dirs": ["libs"],
    "libs": [],
}

def load_toml(path : str):
    with open(path, "rb") as file:
        return tomllib.load(file)


def validate(config: dict):
    # TODO: implement
    None

def configure(config_overrides: dict):
    # Apply defaults to any values to config
    config = DEFAULTS.copy()

    # Load config file and replace any default values
    config_file = load_toml("../project_conf.toml")
    config.update(config_file)

    # Replace any configs with CLI overrides
    config.update(config_overrides)

    return config
