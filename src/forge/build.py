"""
Build functionality.
"""

from pathlib import Path
import datetime
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
    # Log config
    log.info("=" * 20)
    log.info(f"BUILD STARTED:  {datetime.datetime.now().strftime('%c')}")
    log.info(f"Project:        {config['project']['name']}")
    log.info(f"Profile:        {config['profile']}")
    log.info(f"Compiler:       {config['compiler']['executable']}")
    log.info(f"Compiler flags: {config['compiler']['flags']}")
    log.info(f"Linker flags:   {config['linker']['flags']}")
    log.info(f"Libraries:      {config['linker']['libs']}")
    
    log.info(f"output:         {config['output']['output_name']}")
    log.info(f"build dir:      {config['output']['build_dir']}")
    log.info(f"obj dir:        {config['output']['obj_dir']}")

    log.info(f"Logging dir:    {config['logging']['log_dir']}")
    log.info(f"Include dirs:   {config['source']['include_dirs']}")
    log.info(f"Library dirs:   {config['linker']['lib_dirs']}")
    log.info(f"Source dirs:    {config['source']['source_dirs']}")

    # Collect source files
    sources = collect_sources(config)

    # Log sources
    log.info("Discovered sources:")
    for source in sources:
        log.info(source)
    
    # Compile sources
    compile_sources(config, sources)

    # Collect object files
    objects = collect_objects(config)

    # Log objects
    log.info("Discovered objects:")
    for object in objects:
        log.info(object)

    # Link objects
    link_objects(config, objects)
