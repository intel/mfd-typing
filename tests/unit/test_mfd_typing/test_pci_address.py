# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
import pytest

from mfd_typing import PCIAddress, PCIDevice
from mfd_typing.pci_address import PCIAddressMissingData
from mfd_typing.pci_address import PCIDAddressIncomparableObject


class TestPCIAddress:
    def test_arguments_converted_to_int(self):
        obj = PCIAddress("0", 0.0, "0", 0.0)

        assert obj.domain == 0
        assert obj.bus == 0
        assert obj.slot == 0
        assert obj.func == 0

    def test__parse_string_to_pci(self):
        obj = PCIAddress(data="1:2:3:4")

        assert obj.domain == 1
        assert obj.bus == 2
        assert obj.slot == 3
        assert obj.func == 4

    def test__parse_string_to_pci_wrong_format(self):
        with pytest.raises(ValueError):
            PCIAddress(data="1.2:3,4")

    def test___eq__(self):
        obj = PCIAddress(data="0000:1a:0a.1")
        assert obj == PCIAddress(data="0000:1a:0a.1")
        assert obj != None  # noqa: E711
        assert obj != PCIAddress(data="0000:00:0a.3")

    @pytest.mark.parametrize("values", [(-1, 0, 0, 0), (2**32, 0, 0, 0)])
    def test_domain_bounds_validated(self, values):
        with pytest.raises(ValueError):
            PCIAddress(*values)

    @pytest.mark.parametrize("values", [(0, -1, 0, 0), (0, 2**8, 0, 0)])
    def test_bus_bounds_validated(self, values):
        with pytest.raises(ValueError):
            PCIAddress(*values)

    @pytest.mark.parametrize("values", [(0, 0, -1, 0), (0, 0, 2**8, 0)])
    def test_slot_bounds_validated(self, values):
        with pytest.raises(ValueError):
            PCIAddress(*values)

    @pytest.mark.parametrize("values", [(0, 0, 0, -1), (0, 0, 0, 2**8)])
    def test_func_bounds_validated(self, values):
        with pytest.raises(ValueError):
            PCIAddress(*values)

    def test_func_lspci_upper_value(self):
        assert "ffff:ff:1f.7" == PCIAddress(0xFFFF, 0xFF, 0x1F, 0x7).lspci

    def test_func_lspci_lower_value(self):
        assert "0000:00:00.0" == PCIAddress(0, 0, 0, 0).lspci

    def test_lspci_short(self):
        assert "ff:1f.7" == PCIAddress(0, 0xFF, 0x1F, 0x7).lspci_short
        assert "ff:1f.7" == PCIAddress(data="ff:1f.7").lspci_short

    def test_func_sbdf(self):
        assert "00:094:00:01" == PCIAddress(0, 94, 0, 1).sbdf

    def test_func_pciconf(self):
        assert "pci65535:255:31:7" == PCIAddress(0xFFFF, 0xFF, 0x1F, 0x7).pciconf
        assert "pci65535:255:31:7" == PCIAddress(65535, 255, 31, 7).pciconf

    def test_func_nvmcheck_bdf(self):
        assert "026/00/01" == PCIAddress(0, 26, 0, 1).nvmcheck_bdf

    def test_frozen(self):
        with pytest.raises(AttributeError):
            PCIAddress(0, 0, 0, 0).domain = 1

    def test_pci_address_string(self):
        assert isinstance(PCIAddress(data="ffff:ff:1f.7"), PCIAddress)
        assert isinstance(PCIAddress(data="1a:0a.1"), PCIAddress)
        assert isinstance(PCIAddress(0xFFFF, 0xFF, 0x1F, 0x7), PCIAddress)

    def test___str__(self):
        assert "ffff:ff:1f.7" == str(PCIAddress(0xFFFF, 0xFF, 0x1F, 0x7))

    def test_pci_hex_to_pci_dec(self):
        assert PCIAddress(0xFFFF, 0xFF, 0x1F, 0x7).sbdf == "65535:255:31:07"
        assert PCIAddress(data="ffff:ff:1f.7").sbdf == "65535:255:31:07"

    def test_pci_dec_to_pci_hex(self):
        assert PCIAddress(0, 26, 10, 1).lspci == "0000:1a:0a.1"
        assert PCIAddress(data="0000:1a:0a.1").lspci == "0000:1a:0a.1"

    def test_pci_dec_to_pci_hex_capital_letters(self):
        assert PCIAddress(0, 26, 10, 1).lspci == "0000:1a:0a.1"
        assert PCIAddress(data="0000:1A:5C.1").lspci == "0000:1a:5c.1"

    def test_pci_address_none_input_params(self):
        with pytest.raises(PCIAddressMissingData):
            PCIAddress(0, 26, 10, None)

    def test__lt__(self):
        assert PCIAddress(data="0000:18:00.0") < PCIAddress(data="0000:20:00.0")
        assert PCIAddress(data="0000:18:00.0") < PCIAddress(data="0000:18:01.0")
        assert PCIAddress(data="0000:18:00.0") < PCIAddress(data="0000:18:00.1")

    def test__gt__(self):
        assert PCIAddress(data="0000:20:00.0") > PCIAddress(data="0000:18:00.0")
        assert PCIAddress(data="0000:20:01.0") > PCIAddress(data="0000:20:00.0")
        assert PCIAddress(data="0000:20:00.1") > PCIAddress(data="0000:20:00.0")

    def test_pci_address_error(self):
        with pytest.raises(
            PCIDAddressIncomparableObject, match="Incorrect object passed for comparison with PCIAddress"
        ):
            PCIAddress(data="0000:20:00.0") < PCIDevice(data="8086:1592")
