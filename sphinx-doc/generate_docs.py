# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Generate sphinx docs."""

import os
import shutil
import logging

from sphinx.ext import apidoc
from sphinx.cmd import build


apidoc.main(["-e", "-o", "mfd_typing", os.path.join("..", "mfd_typing")])

build.main(["-b", "html", ".", "build/html"])

logging.info("Cleaning folders from build process...")
shutil.rmtree("mfd_typing")
