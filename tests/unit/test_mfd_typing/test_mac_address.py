# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT

import pytest
from netaddr import mac_eui48
from unittest import mock

from mfd_typing import MACAddress
from mfd_typing import mac_address as mac


class TestMACAddress:
    @pytest.mark.parametrize("mac", ["abcd", "11-22-33-44", "11:22:33:44:55:66:77:88"])
    def test_with_wrong_numbers_should_raise_value_error(self, mac):
        with pytest.raises(ValueError):
            MACAddress(mac)

    def test_passing_empty_string(self):
        with pytest.raises(ValueError):
            MACAddress("")

    def test_construct_mac_from_colon_separated_string(self):
        assert str(MACAddress("d2:ee:77:91:34:a7")) == "d2:ee:77:91:34:a7"

    def test_construct_mac_from_dash_separated_string(self):
        assert str(MACAddress("d2-ee-77-91-34-a7")) == "d2:ee:77:91:34:a7"

    def test_construct_mac_from_non_separated_string(self):
        assert str(MACAddress("d2ee779134a7")) == "d2:ee:77:91:34:a7"

    def test_construct_mac_from_int(self):
        assert str(MACAddress(0xD2EE779134A7)) == "d2:ee:77:91:34:a7"

    def test_construction_must_be_idempotent(self):
        assert str(MACAddress(MACAddress(0xD2EE779134A7))) == "d2:ee:77:91:34:a7"

    def test___repr__(self):
        assert repr(MACAddress("d2:ee:77:91:34:a7")) == "MACAddress('d2:ee:77:91:34:a7')"

    def test_dialect_selection(self):
        assert str(MACAddress("d2:ee:77:91:34:a7", dialect=mac_eui48)) == "D2-EE-77-91-34-A7"

    def test_mac_int_to_str(self):
        addr = str(MACAddress(456))
        assert addr == "00:00:00:00:01:c8"

    def test_mac_str_to_int(self):
        addr = int(MACAddress("d2:ee:77:91:34:a7"))
        assert addr == 231921650054311

    def test_mac_str_to_bits(self):
        addr = MACAddress("d2:ee:77:91:34:a7").bits()
        assert addr == "11010010-11101110-01110111-10010001-00110100-10100111"

    def test_mac_str_to_bin(self):
        addr = bin(MACAddress("d2:ee:77:91:34:a7"))
        assert addr == "0b110100101110111001110111100100010011010010100111"

    def test_mac_str_to_hex(self):
        addr = hex(MACAddress("d2:ee:77:91:34:a7"))
        assert addr == "0xd2ee779134a7"

    def test_mac_int_to_words(self):
        addr = MACAddress(456).words
        assert addr == (0, 0, 0, 0, 1, 200)

    @pytest.mark.parametrize("mac1, mac2", [("d2:ee:77:91:34:a7", "d2:ee:aa:bb:cc:dd")])
    def test_compare_different_mac(self, mac1, mac2):
        with pytest.raises(AssertionError):
            assert MACAddress(mac1) == MACAddress(mac2)

    @pytest.mark.parametrize("mac1, mac2", [("d2:ee:77:91:34:a7", "d2:ee:77:91:34:a7")])
    def test_compare_same_mac(self, mac1, mac2):
        assert MACAddress(mac1) == MACAddress(mac2)

    @mock.patch("mfd_typing.mac_address.get_random_mac", return_value="62:2a:aa:90:27:97", autospec=True)
    def test_get_random_mac(self, mock_get_random_mac):
        assert str(mac.get_random_mac()) == "62:2a:aa:90:27:97"

    @mock.patch("mfd_typing.mac_address.get_random_multicast_mac", return_value="01:00:5e:50:b1:a4", autospec=True)
    def test_get_random_multicast_mac(self, mock_get_random_multicast_mac):
        assert str(mac.get_random_multicast_mac()) == "01:00:5e:50:b1:a4"

    @mock.patch("mfd_typing.mac_address.get_random_unicast_mac", return_value="fa:11:11:d6:dd:96", autospec=True)
    def test_get_random_unicast_mac(self, mock_get_random_unicast_mac):
        assert str(mac.get_random_unicast_mac()) == "fa:11:11:d6:dd:96"

    @mock.patch("mfd_typing.mac_address.get_random_mac_using_prefix", return_value="11:22:33:95:72:e3", autospec=True)
    def test_get_random_mac_using_prefix(self, mock_get_random_mac_using_prefix):
        assert str(mac.get_random_mac_using_prefix("11:22:33")) == "11:22:33:95:72:e3"

    @mock.patch("mfd_typing.mac_address.get_random_mac_using_prefix", return_value="fa:11:11:95:72:e3", autospec=True)
    def test_get_random_mac_using_prefix_with_default_prefix(self, mock_get_random_mac_using_prefix):
        assert str(mac.get_random_mac_using_prefix()) == "fa:11:11:95:72:e3"

    def test_parse_mac_success(self):
        assert mac.parse_mac(MACAddress("3c:fd:fe:bc:b7:68")) == "{0xfd3c,0xbcfe,0x68b7}"
