# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Exceptions."""


class InvalidWindowsKernelError(Exception):
    """Raised when invalid Windows OS kernel version is passed."""


class UnknownWindowsKernelVersionError(Exception):
    """Raised when provided kernel version doesn't much any supported Windows version."""
