#!/usr/bin/env python
import shutil
from pathlib import Path

from jinja2 import Environment, PackageLoader

from mevo_comparator import run
from mevo_parser import MevoParser
from starsep_utils import healthchecks


if __name__ == "__main__":
    healthchecks("/start")
    templatesDirectory = Path("templates")
    libsDirectory = Path("libs")
    staticDirectory = Path("static")
    outputDirectory = Path("output")
    outputDirectory.mkdir(exist_ok=True)
    mevoParser = MevoParser()
    run(
        outputPath=outputDirectory / "index.html",
        mapPath=outputDirectory / "map-mevo.html",
        mevoParser=mevoParser,
    )

    environment = Environment(loader=PackageLoader("main", "templates"))
    shutil.copy(templatesDirectory / "index.js", outputDirectory / "index.js")
    shutil.copy(libsDirectory / "sorttable.js", outputDirectory / "sorttable.js")
    shutil.copy(staticDirectory / "josm.svg", outputDirectory / "josm.svg")
    healthchecks()
