# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for PCI Device."""

import re
from dataclasses import dataclass, fields, InitVar
from typing import Optional, Union, Any

from mfd_typing import VendorID, DeviceID, SubVendorID, SubDeviceID
from mfd_typing.dataclass_utils import convert_value_field_to_typehint_type

hex_reg_4 = r"[0-9a-fA-F]{4}"
_pci_vendor_device_regex = rf"(?P<vendor_id>{hex_reg_4}):(?P<device_id>{hex_reg_4})"
pci_vendor_device_regex = rf"^{_pci_vendor_device_regex}$"
pci_device_full_regex = rf"^{_pci_vendor_device_regex}:(?P<sub_vendor_id>{hex_reg_4}):(?P<sub_device_id>{hex_reg_4})$"
int_acceptable_types = Union[int, str, bytes]


@dataclass(frozen=True)
class PCIDevice:
    """Class for handling PCI Device."""

    vendor_id: Optional[Union[VendorID, int_acceptable_types]] = None
    device_id: Optional[Union[DeviceID, int_acceptable_types]] = None
    sub_vendor_id: Optional[Union[SubVendorID, int_acceptable_types]] = None
    sub_device_id: Optional[Union[SubDeviceID, int_acceptable_types]] = None
    data: InitVar[str] = None

    def _parse_string_pci_device(self, data: str) -> None:
        if data is not None:
            match_vendor_device = re.search(pattern=pci_vendor_device_regex, string=data)
            match_pci_device_full = re.search(pattern=pci_device_full_regex, string=data)
            if match_vendor_device:
                self.__dict__["vendor_id"] = VendorID(match_vendor_device.group("vendor_id"))
                self.__dict__["device_id"] = DeviceID(match_vendor_device.group("device_id"))
                self.__dict__["sub_vendor_id"] = None
                self.__dict__["sub_device_id"] = None
            elif match_pci_device_full:
                self.__dict__["vendor_id"] = VendorID(match_pci_device_full.group("vendor_id"))
                self.__dict__["device_id"] = DeviceID(match_pci_device_full.group("device_id"))
                self.__dict__["sub_vendor_id"] = SubVendorID(match_pci_device_full.group("sub_vendor_id"))
                self.__dict__["sub_device_id"] = SubDeviceID(match_pci_device_full.group("sub_device_id"))
            else:
                raise ValueError(f"Incorrect format was provided as input to PCIDevice object creation: {data}")

    def __post_init__(self, data: str) -> None:
        self._parse_string_pci_device(data=data)
        if data is None and not all([self.__dict__["vendor_id"], self.__dict__["device_id"]]):
            raise PCIDeviceMissingData(
                (
                    f"Not enough data for PCI device: : {self.__dict__}. "
                    "VendorID and DeviceID are mandatory! Device details can be also passed in 'data' parameter"
                )
            )
        for field in fields(self):
            convert_value_field_to_typehint_type(self, field)

    def __eq__(self, other: Any):
        if other is None:
            return False

        if not isinstance(other, type(self)):
            raise PCIDeviceIncomparableObject(f"Incorrect object passed for comparison with PCIDevice: {other}")

        return (
            self.vendor_id == other.vendor_id
            and self.device_id == other.device_id
            and (not all([self.sub_vendor_id, other.sub_vendor_id]) or self.sub_vendor_id == other.sub_vendor_id)
            and (not all([self.sub_device_id, other.sub_device_id]) or self.sub_device_id == other.sub_device_id)
        )


class PCIDeviceMissingData(Exception):
    """Exception raised for wrong input data providing."""


class PCIDeviceIncomparableObject(Exception):
    """Exception raised for incorrect object passed for comparison."""
