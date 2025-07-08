# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
from pytest import raises

from mfd_typing import PCIDevice, VendorID, DeviceID, SubVendorID, SubDeviceID
from mfd_typing.pci_device import PCIDeviceMissingData, PCIDeviceIncomparableObject


class TestPCIDevice:
    def test_init(self):
        assert PCIDevice(0x8086, 0x8086, 0x8086, 0x8086) == PCIDevice(
            VendorID(0x8086), DeviceID(0x8086), SubVendorID(0x8086), SubDeviceID(0x8086)
        )
        assert PCIDevice(0x8086, 0x8086, 0x8086, 0x8086) == PCIDevice(0x8086, 0x8086)

        assert not PCIDevice(0x8086, 0x8086, 0x8086, 0x8086) == PCIDevice(0x8086, 0x8085)

        assert PCIDevice(0x8086, 0x8086, 0x8086, 0x8086) == PCIDevice(0x8086, 0x8086, 0x8086)

        assert not PCIDevice(0x8086, 0x8086, 0x8086, 0x8086) == PCIDevice(0x8086, 0x8086, 0x8085)

        assert not PCIDevice(0x8086, 0x8086, 0x8086, 0x8086) == PCIDevice(0x8086, 0x8086, 0x8086, 0x8085)

        assert PCIDevice(data="8086:8086:8086:8086") == PCIDevice(
            VendorID(0x8086), DeviceID(0x8086), SubVendorID(0x8086), SubDeviceID(0x8086)
        )
        assert PCIDevice(data="8086:8086:0000:001A") == PCIDevice(
            VendorID(0x8086), DeviceID(0x8086), SubVendorID(0x0000), SubDeviceID(0x001A)
        )
        assert PCIDevice(data="ffff:001A") == PCIDevice(VendorID(0xFFFF), DeviceID(0x001A), None, None)
        assert PCIDevice(data="8086:001a") == PCIDevice(VendorID(0x8086), DeviceID(0x001A), None, None)

    def test_pci_device_missing_data(self):
        with raises(PCIDeviceMissingData):
            PCIDevice(None, None, None, None)
        with raises(PCIDeviceMissingData):
            PCIDevice(data=None)
        with raises(PCIDeviceMissingData):
            PCIDevice(None, None, "8086", "1572")

    def test_pci_device_missing_vendor_data_format(self):
        with raises(ValueError):
            PCIDevice(data="8086")

    def test_pci_device_incorrect_data_format(self):
        with raises(ValueError):
            PCIDevice(data="8086:aaaax")

    def test_pci_device_incorrect_comparison(self):
        with raises(PCIDeviceIncomparableObject):
            assert PCIDevice(data="8086:1572") == "PCIDevice"
