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

def build_project(args):
    log.debug("build_project")

def clean_project(args):
    log.debug("clean_project")


def main():
    args = vars(ap.parse_args())

    if args["command"] == "build":
        build_project(args)

    elif args["command"] == "clean":
        clean_project(args)

    cli_config = {
        key: value
        for key, value in args.items()
        if value is not None
    }

    config = configure(cli_config)
    log.info(config)


if __name__ == "__main__":
    main()
