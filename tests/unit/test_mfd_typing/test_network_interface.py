# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
from mfd_typing.network_interface import InterfaceType


def test_interface_type():
    """Test InterfaceType enum."""
    assert InterfaceType.BOND
    assert InterfaceType.BOND_SLAVE
