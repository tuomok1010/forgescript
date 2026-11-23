'''
This script is responsible for linking all object files
'''
from forge.logger import log
from pathlib import Path
import subprocess


def link_objects(config, objects):
    # Add linker (in this case same as the compiler)
    cmd = [config["compiler"]["executable"]]

    # Add object files
    cmd.extend(str(obj) for obj in objects)

    # Add library directories
    for lib_dir in config["linker"]["lib_dirs"]:
        project_root = config["project"]["root"]
        lib_path = (project_root / lib_dir)
        cmd.extend(["-L", str(lib_path)])

    # Add libraries
    for lib in config["linker"]["libs"]:
        cmd.extend(["-l", lib])

    # Add linker flags
    cmd.extend(config["linker"]["flags"])

    # Create final output filepath
    output_file = (
        config["project"]["root"]
        / config["output"]["build_dir"]
        / config["output"]["output_name"]
    )

    # Add output
    cmd.extend(["-o", str(output_file)])

    # Link!!
    try:
        log.info(f"Linking {config['output']['output_name']}")
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        
    except subprocess.CalledProcessError as e:
        log.error("Linking failed")
        log.error(e.stderr)
        return False

    log.info("Linking complete")
