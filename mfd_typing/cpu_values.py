# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""CPU Values."""

from enum import Enum


class CPUBitness(str, Enum):
    """Available CPU bitnesses."""

    CPU_32BIT = "32bit"
    CPU_64BIT = "64bit"


class CPUArchitecture(str, Enum):
    """Available CPU architectures."""

    X86 = "x86"
    X86_64 = "x86-64"
    ARM = "ARM"
    ARM64 = "ARM64"
