'''
This scrpt is responsible for building all source files
'''
from forge.logger import log
from pathlib import Path
import subprocess

def compile_source(config, source):
    # Get source file relative path to root
    rel_src_path = source.relative_to(config["project"]["root"])

    # Create an absolute obj directory path
    obj_dir = (config["project"]["root"] / config["output"]["obj_dir"])

    # Append relative source file path to obj directory path
    obj_file = (obj_dir / rel_src_path.with_suffix(".o"))

    # Ensure that the directories exist for the obj file
    obj_file.parent.mkdir(parents=True, exist_ok=True)

    # Check if obj file exist, and skip compile if no changes
    if obj_file.exists():
        source_time = source.stat().st_mtime
        object_time = obj_file.stat().st_mtime

        if object_time >= source_time:
            log.info(f"Skipping {rel_src_path} (up-to-date)")
            return
        
    # Add compiler + flags to the compile command
    cmd = [config['compiler']['executable']]
    cmd.extend(config['compiler']['flags'])

    # Add include directories to the compile command
    for path in config['source']['include_dirs']:
        path = (config["project"]["root"] / path)
        cmd.extend(["-I", str(path)])

    # Add sources and output directories to the command
    cmd.extend(["-c", str(source), "-o", str(obj_file)])

    # Log compile
    log.info(f"Compiling {rel_src_path}")

    # Compile!
    subprocess.run(cmd, check=True)

def compile_sources(config, sources):
    for source in sources:
        compile_source(config, source)
