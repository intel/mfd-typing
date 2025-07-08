# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Misc data structures."""

from enum import Enum


class IPUHostType(Enum):
    """Structure for IPU Host Types."""

    XHC = "xhc"
    IMC = "imc"
    ACC = "acc"
    LP = "lp"
    SH = "sh"
