# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
import pytest

from mfd_typing.os_values import OSName, OSType, OSBitness, SWITCHES_OS_NAME_REGEXES


class TestOSValues:
    @pytest.mark.parametrize("value", ["WINDOWS", "LINUX", "FREEBSD", "ESXI", "EFISHELL", "MELLANOX"])
    def test_os_names(self, value):
        assert value in OSName._member_names_

    @pytest.mark.parametrize("value", ["WINDOWS", "POSIX", "SWITCH"])
    def test_os_types(self, value):
        assert value in OSType._member_names_

    @pytest.mark.parametrize("value", ["OS_32BIT", "OS_64BIT"])
    def test_os_bitness(self, value):
        assert value in OSBitness._member_names_

    def test_switches_os_name_regexes(self):
        assert OSName.MELLANOX in SWITCHES_OS_NAME_REGEXES
