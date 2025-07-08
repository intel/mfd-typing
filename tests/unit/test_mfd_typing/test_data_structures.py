# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Test Data Structures."""

from mfd_typing.data_structures import IPUHostType


def test_ipu_host_type_values():
    assert IPUHostType.XHC.value == "xhc"
    assert IPUHostType.IMC.value == "imc"
    assert IPUHostType.ACC.value == "acc"
    assert IPUHostType.LP.value == "lp"
    assert IPUHostType.SH.value == "sh"


def test_ipu_host_type_names():
    assert IPUHostType.XHC.name == "XHC"
    assert IPUHostType.IMC.name == "IMC"
    assert IPUHostType.ACC.name == "ACC"
    assert IPUHostType.LP.name == "LP"
    assert IPUHostType.SH.name == "SH"


def test_ipu_host_type_members():
    assert list(IPUHostType) == [
        IPUHostType.XHC,
        IPUHostType.IMC,
        IPUHostType.ACC,
        IPUHostType.LP,
        IPUHostType.SH,
    ]
