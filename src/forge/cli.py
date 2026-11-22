'''
This script is responsible for the parsing of CLI arguments.
'''
import argparse
from forge.logger import log
from forge.config import configure

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
_ = ap.add_argument(
    "command",
    choices=["build", "clean"],
    help="Command to execute"
)

_ = ap.add_argument(
    "-f",
    "--config",
    dest="config_file",
    default="conf.toml",
    help="Path to configuration file"
)

_ = ap.add_argument(
    "-p",
    "--profile",
    choices=["debug", "release"],
    default="debug",
    help="Build profile"
)

_ = ap.add_argument(
    "-C",
    "--compiler",
    dest="compiler",
    help="Compiler executable"
)

_ = ap.add_argument(
    "-F",
    "--compiler-flags",
    nargs="*",
    dest="compiler_flags",
    help="Compiler flags"
)

_ = ap.add_argument(
    "-L",
    "--linker-flags",
    nargs="*",
    dest="linker_flags",
    help="Linker flags"
)

_ = ap.add_argument(
    "-o",
    "--output",
    dest="output_name",
    help="Executable name"
)

_ = ap.add_argument(
    "-B",
    "--build-dir",
    dest="build_dir",
    help="Build directory"
)

_ = ap.add_argument(
    "-O",
    "--obj-dir",
    dest="obj_dir",
    help="Intermediary (obj files directory"
)

_ = ap.add_argument(
    "-I",
    "--include-dirs",
    nargs="*",
    dest="include_dirs",
    help="Additional include directories"
)

_ = ap.add_argument(
    "-S",
    "--source-dirs",
    nargs="*",
    dest="source_dirs",
    help="Source code directories"
)

_ = ap.add_argument(
    "-Lg",
    "--log-dir",
    dest="log_dir",
    help="Log directory"
)

_ = ap.add_argument(
    "-Lb",
    "--lib-dirs",
    nargs="*",
    dest="lib_dirs",
    help="Library directories"
)

_ = ap.add_argument(
    "-l",
    "--libs",
    nargs="*",
    dest="libs",
    help="Libraries"
)

# Craft a dictionary matching the .toml config file structure
def make_overrides(args):
    overrides = {}
    
    if args["compiler"] is not None:
        overrides.setdefault(
            "compiler", {}
        )["executable"] = args["compiler"]

    if args["compiler_flags"] is not None:
        overrides.setdefault(
            "compiler", {}
        )["flags"] = args["compiler_flags"]

    if args["linker_flags"] is not None:
        overrides.setdefault(
            "linker", {}
        )["flags"] = args["linker_flags"]

    if args["libs"] is not None:
        overrides.setdefault(
            "linker", {}
        )["libs"] = args["libs"]

    if args["lib_dirs"] is not None:
        overrides.setdefault(
            "linker", {}
        )["lib_dirs"] = args["lib_dirs"]

    if args["source_dirs"] is not None:
        overrides.setdefault(
            "source", {}
        )["source_dirs"] = args["source_dirs"]

    if args["include_dirs"] is not None:
        overrides.setdefault(
            "source", {}
        )["include_dirs"] = args["include_dirs"]

    if args["build_dir"] is not None:
        overrides.setdefault(
            "output", {}
        )["build_dir"] = args["build_dir"]

    if args["obj_dir"] is not None:
        overrides.setdefault(
            "output", {}
        )["obj_dir"] = args["obj_dir"]

    if args["output_name"] is not None:
        overrides.setdefault(
            "output", {}
        )["output_name"] = args["output_name"]

    if args["log_dir"] is not None:
        overrides.setdefault(
            "logging", {}
        )["log_dir"] = args["log_dir"]

    return overrides

def build_project(args):
    log.debug("build_project")

def clean_project(args):
    log.debug("clean_project")


def main():
    args = vars(ap.parse_args())
    
    cli_overrides = make_overrides(args)
    config = configure(
        args["config_file"],
        args["profile"],
        cli_overrides
    )

    log.info(config)

    if args["command"] == "build":
        build_project(config)

    elif args["command"] == "clean":
        clean_project(config)


if __name__ == "__main__":
    main()
