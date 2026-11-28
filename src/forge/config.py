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

VALID_COMPILERS = ["gcc", "g++", "clang", "clang++", "clang-cl"]

def load_toml(path : str):
    with open(path, "rb") as file:
        return tomllib.load(file)

def validate_type(value: object, expected_type: type, name: str):
    if not isinstance(value, expected_type):
        raise ValueError(f"{name} must be of type {expected_type.__name__}, got {type(value).__name__}")

def validate_path(project_root: Path, path: Path, name: str):
    try:
        path.relative_to(project_root)
    except ValueError:
        raise ValueError(f"{name} must be inside the project directory")
    if path == project_root:
        raise ValueError(f"{name} cannot be the project root directory")

def validate_source_dir(project_root: Path, source_dir: Path):
    path = (project_root / source_dir)
    if not path.exists():
        raise ValueError(f"Source directory '{source_dir}' does not exist")
    if not path.is_dir():
        raise ValueError(f"Source directory '{source_dir}' is not a directory")

def validate_include_dir(project_root: Path, include_dir: Path):
    path = (project_root / include_dir)
    if not path.exists():
        raise ValueError(f"Include directory '{include_dir}' does not exist")
    if not path.is_dir():
        raise ValueError(f"Include directory '{include_dir}' is not a directory")

def validate_lib_dir(project_root: Path, lib_dir: Path):
    path = (project_root / lib_dir)
    if not path.exists():
        raise ValueError(f"Library directory '{lib_dir}' does not exist")
    if not path.is_dir():
        raise ValueError(f"Library directory '{lib_dir}' is not a directory")

def validate_schema(config: dict):
    """ Validates data types of the config file"""
    #[project]
    validate_type(config["project"]["name"], str, "project.name")

    #[compiler]
    validate_type(config["compiler"]["executable"], str, "compiler.executable")
    validate_type(config["compiler"]["flags"], list, "compiler.flags")

    # [source]
    validate_type(config["source"]["source_dirs"], list, "source.source_dirs")
    validate_type(config["source"]["include_dirs"], list, "source.include_dirs")

    # [linker]
    validate_type(config["linker"]["libs"], list, "linker.libs")
    validate_type(config["linker"]["lib_dirs"], list, "linker.lib_dirs")
    validate_type(config["linker"]["flags"], list, "linker.flags")

    # [logging]
    validate_type(config["logging"]["enabled"], bool, "logging.enabled")
    validate_type(config["logging"]["log_dir"], str, "logging.log_dir")

    # [output]
    validate_type(config["output"]["output_name"], str, "output.output_name")
    validate_type(config["output"]["build_dir"], str, "output.build_dir")
    validate_type(config["output"]["obj_dir"], str, "output.obj_dir")

def validate_compiler(config: dict):
    """Validate compiler by checking that it exists in the list VALID_COMPILERS"""
    if not config["compiler"]["executable"] in VALID_COMPILERS:
        compilers = ", ".join(VALID_COMPILERS)
        raise ValueError(f"compiler.executable ({config['compiler']['executable']}) not supported. Supported compilers: {compilers}")

def validate_paths(config: dict):
    """Validate filepaths"""
    project_root = (config["project"]["root"].resolve())
    build_dir = (project_root / config["output"]["build_dir"]).resolve()
    obj_dir = (project_root / config["output"]["obj_dir"]).resolve()
    log_dir = (project_root / config["logging"]["log_dir"]).resolve()

    # Make sure all paths are valid (ensures safe clean of log and build files)
    validate_path(project_root, build_dir, "output.build_dir")
    validate_path(project_root, obj_dir, "output.obj_dir")
    validate_path(project_root, log_dir, "logging.log_dir")

def validate_source_dirs(config: dict):
    """Validate source directories"""
    project_root = config["project"]["root"]
    for source_dir in config["source"]["source_dirs"]:
        validate_source_dir(project_root, source_dir)

def validate_include_dirs(config: dict):
    """Validate include directories"""
    project_root = config["project"]["root"]
    for include_dir in config["source"]["include_dirs"]:
        validate_include_dir(project_root, include_dir)

def validate_lib_dirs(config: dict):
    """Validate library directories"""
    project_root = config["project"]["root"]
    for lib_dir in config["linker"]["lib_dirs"]:
        validate_include_dir(project_root, lib_dir)

def validate(config: dict):
    """Validates config"""
    validate_schema(config)
    validate_compiler(config)
    validate_paths(config)
    validate_source_dirs(config)
    validate_include_dirs(config)
    validate_lib_dirs(config)

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
        raise ValueError(f"Unknown profile '{profile}'. Available profiles: {available}")
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
