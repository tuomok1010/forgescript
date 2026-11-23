"""
Build functionality.
"""

from pathlib import Path
import datetime
import time
import shutil
import subprocess
from forge.logger import log
from forge.compiler import compile_sources
from forge.linker import link_objects

class BuildStats:
    compiled: int = 0
    skipped: int = 0
    failed: int = 0
    linked: bool = False
    build_start: float = 0.0
    build_end: float = 0.0


def collect_sources(config):
    project_root = config["project"]["root"]
    sources = []
    for source_dir in config["source"]["source_dirs"]:
        source_path = (project_root / source_dir)
        sources.extend(source_path.rglob("*.cpp"))
        sources.extend(source_path.rglob("*.c"))
    return sources

def collect_objects(config):
    project_root = config["project"]["root"]
    obj_path = (project_root / config['output']['obj_dir'])
    objects = []
    objects.extend(obj_path.rglob("*.o"))
    return objects

def print_build_initial(config):
    log.info(
        f"""
================================================
BUILD STARTED:         {datetime.datetime.now().strftime('%c')}
================================================
Project:               {config['project']['name'] or "None"}
Profile:               {config['profile'] or "None"}
Compiler:              {config['compiler']['executable'] or "None"}
Compiler flags:        {" ".join(config['compiler']['flags']) or "None"}
Linker flags:          {" ".join(config['linker']['flags']) or "None"}
Libraries:             {" ".join(config['linker']['libs']) or "None"}
Output:                {config['output']['output_name'] or "None"}
Build directory:       {config['output']['build_dir'] or "None"}
Object directory:      {config['output']['obj_dir'] or "None"}
Logging directory:     {config['logging']['log_dir'] or "None"}
Include directories:   {" ".join(config['source']['include_dirs']) or "None"}
Library directories:   {" ".join(config['linker']['lib_dirs']) or "None"}
Source directories:    {" ".join(config['source']['source_dirs']) or "None"}
================================================
        """
    )

def print_build_summary(stats: BuildStats):
    log.info(
        f"""
================================================
BUILD ENDED:           {datetime.datetime.now().strftime('%c')}
================================================
Compiled:              {stats.compiled}
Skipped:               {stats.skipped}
Failed:                {stats.failed}
Linked:                {stats.linked}
Duration:              {stats.build_end - stats.build_start:.3f} s
================================================
        """
    )

def build(config):
    # Init stats for storing summary
    stats = BuildStats()
    
    # Store accurate start time
    stats.build_start = time.perf_counter()
    
    # Print initial info
    print_build_initial(config)

    # Collect source files
    sources = collect_sources(config)
    
    # Compile sources
    compile_sources(config, sources, stats)

    # Collect object files
    objects = collect_objects(config)

    # Link objects
    link_objects(config, objects, stats)

    # Store accurate end time
    stats.build_end = time.perf_counter()

    # Print summary
    print_build_summary(stats)
    

def clean(config):
    project_root = config["project"]["root"]
    build_dir = config['output']['build_dir']
    build_dir_full = (project_root / build_dir)
    
    shutil.rmtree(build_dir_full, ignore_errors=True)
    build_dir_full.mkdir(parents=True, exist_ok=True)
    log.info("Clean complete")

def run(config):
    # Output full filepath
    output_file = (
        config["project"]["root"]
        / config["output"]["build_dir"]
        / config["output"]["output_name"]
    )

    try:
        log.info(f"Running {config['output']['output_name']}")
        subprocess.run([str(output_file)], check=True)
        
    except subprocess.CalledProcessError as e:
        log.error("Running failed")
        log.error(e.stderr)
