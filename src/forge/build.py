"""
Build functionality.
"""

from pathlib import Path
import datetime
import shutil
from forge.logger import log
from forge.compiler import compile_sources
from forge.linker import link_objects


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

def build(config):
    # Log basic config
    log.info(
        f"""
===============
~ FORGESCRIPT ~
===============
BUILD STARTED:         {datetime.datetime.now().strftime('%c')}
Project:               {config['project']['name']}
Profile:               {config['profile']}
Compiler:              {config['compiler']['executable']}
Compiler flags:        {config['compiler']['flags']}
Linker flags:          {config['linker']['flags']}
Libraries:             {config['linker']['libs']}
Output:                {config['output']['output_name']}
Build directory:       {config['output']['build_dir']}
Object directory:      {config['output']['obj_dir']}
Logging directory:     {config['logging']['log_dir']}
Include directories:   {config['source']['include_dirs']}
Library directories:   {config['linker']['lib_dirs']}
Source directories:    {config['source']['source_dirs']}
===============\n
        """
    )

    # Collect source files
    sources = collect_sources(config)
    
    # Compile sources
    compile_sources(config, sources)

    # Collect object files
    objects = collect_objects(config)

    # Link objects
    link_objects(config, objects)

def clean(config):
    project_root = config["project"]["root"]
    build_dir = config['output']['build_dir']
    build_dir_full = (project_root / build_dir)
    
    shutil.rmtree(build_dir_full, ignore_errors=True)
    build_dir_full.mkdir(parents=True, exist_ok=True)
    log.info("Clean complete")
