# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""OS Values."""

from dataclasses import dataclass
from enum import Enum


class WindowsFlavour(Enum):
    """Available Windows System Flavours."""

    WindowsServer2012R2 = "Microsoft Windows Server 2012 R2"
    WindowsServer2016 = "Microsoft Windows Server 2016"  # Windows-10.0.14393
    WindowsServer2019 = "Microsoft Windows Server 2019"  # Windows-10.0.17763
    WindowsServer2022 = "Microsoft Windows Server 2022"  # Windows-10.0.20348
    WindowsServer2022H2 = "Microsoft Windows Server 2022 H2"  # Windows-10.0.22621
    WindowsServer2025 = "Microsoft Windows Server 2025"  # Windows-10.0.26100
    AzureStackHCI22H2 = "Azure Stack HCI 22H2"  # Windows-10.0.20349
    AzureStackHCI23H2 = "Azure Stack HCI 23H2"  # Windows-10.0.22631
    AzureStackHCI24H2 = "Azure Stack HCI 24H2"  # Windows-10.0.26100


class OSName(str, Enum):
    """Available OS names."""

    WINDOWS = "Windows"
    LINUX = "Linux"
    FREEBSD = "FreeBSD"
    ESXI = "VMkernel"
    EFISHELL = "EFIShell"
    MELLANOX = "Mellanox"


class OSType(str, Enum):
    """Available OS types."""

    WINDOWS = "nt"
    POSIX = "posix"
    EFISHELL = "efishell"
    SWITCH = "switch"


class OSBitness(str, Enum):
    """Available OS bitnesses."""

    OS_32BIT = "32bit"
    OS_64BIT = "64bit"


@dataclass
class SystemInfo:
    """Generic Information about the System Under Test."""

    host_name: str | None = None  # WINDOWS-2019
    os_name: str | None = None  # Microsoft Windows Server 2019 Standard
    os_version: str | None = None  # 10.0.17763 N/A Build 17763
    kernel_version: str | None = None  # 17763
    system_boot_time: str | None = None  # 4/4/2023, 2:40:55 PM
    system_manufacturer: str | None = None  # Intel Corporation
    system_model: str | None = None  # S2600BPB
    system_bitness: OSBitness | None = None  # x64-based PC -> OSBitness.OS_64BIT
    bios_version: str | None = None  # Intel Corporation SE5C620.86B.02.01.0012.070720200218, 7/7/2020
    total_memory: str | None = None  # 130,771 MB
    architecture_info: str | None = None  # x86_64


# dict of OS names of switches and their regexes
SWITCHES_OS_NAME_REGEXES = {OSName.MELLANOX: [r"Onyx", r"SX_PPC_M460EX", r"MLNX-OS"]}
