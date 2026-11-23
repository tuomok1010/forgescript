'''
This script is responsible for reading the config file.
'''

import tomllib
from copy import deepcopy
from pathlib import Path

# Default config values
DEFAULTS = {
    "project": {
        "name": "Unnamed Project"
    },

    "compiler": {
        "executable": "clang++",
        "flags": []
    },

    "source": {
        "source_dirs": ["src"],
        "include_dirs": ["include"]
    },

    "linker": {
        "flags": [],
        "libs": [],
        "lib_dirs": []
    },

    "output": {
        "output_name": "program",
        "build_dir": "build",
        "obj_dir": "build/obj"
    },

    "logging": {
        "enabled": True,
        "log_dir": "log"
    }
}

def load_toml(path : str):
    with open(path, "rb") as file:
        return tomllib.load(file)

def validate(config: dict):
    # TODO: implement
    # Validate build_dir <-- must be inside project root, should also explicitly disallow root folder "/"
    None

def deep_merge(dst, src):
    for key, value in src.items():
        if (key in dst and isinstance(dst[key], dict) and isinstance(value, dict)):
            deep_merge(dst[key], value)
        else:
            dst[key] = value
    return dst

def configure(config_path: str, profile: str, overrides: dict):
    # Assign default values to current config
    config = deepcopy(DEFAULTS)

    # Read the toml config file
    toml_config = load_toml(config_path)

    # Extract the desired profile section from the config file
    profiles = toml_config.get("profiles", {})
    if profile not in profiles:
        available = ", ".join(profiles.keys())
        raise ValueError(
            f"Unknown profile '{profile}'. "
            f"Available profiles: {available}"
        )
    profile_config = profiles[profile]
    
    # Remove all profiles sections from the config file
    toml_config.pop("profiles", None)

    # Assign settings from the toml config into the current config
    config = deep_merge(config, toml_config)

    # Assign the desired profile section into the current config
    config = deep_merge(config, profile_config)

    # Assign any overrides to the current config
    config = deep_merge(config, overrides)

    # Resolve project root and store in config
    config_file = Path(config_path).resolve()
    config["project"]["root"] = config_file.parent

    # Store profile in config
    config["profile"] = profile
    
    # Validate
    validate(config)

    # Ready!
    return config
