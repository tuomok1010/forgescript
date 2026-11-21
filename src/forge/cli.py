'''
This script is responsible for the parsing of CLI arguments.
'''
import argparse
from forge.logger import log
from forge.config import load_toml, apply_defaults

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument(
    "command",
    choices=["build", "clean"],
    help="Command to execute"
)


def build_project(args):
    log.debug("build_project")

def clean_project(args):
    log.debug("clean_project")


def main():
    args = ap.parse_args()

    if args.command == "build":
        build_project(args)

    elif args.command == "clean":
        clean_project(args)


    # Get the configuration
    config = load_toml("../project_conf.toml")
    config = apply_defaults(config)
    log.info(config)


if __name__ == "__main__":
    main()
