# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for driver info."""

from dataclasses import dataclass


@dataclass
class DriverInfo:
    """Structure for information about driver."""

    driver_name: str
    driver_version: str
