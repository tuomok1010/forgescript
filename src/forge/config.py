'''
This script is responsible for reading the config file.
'''

import tomllib

# Default config values
DEFAULTS = {
    "compiler": "clang++",
    "build_dir": "build",
    "source_dirs": ["src"],
    "include_dirs": ["include"],
    "intermediate_dir": "build/intermediate",
    "output_name": "program",
}

def load_toml(path : str):
    with open(path, "rb") as file:
        return tomllib.load(file)

def apply_defaults(config: dict):
    for key, value in DEFAULTS.items():
        config.setdefault(key, value)

    return config
