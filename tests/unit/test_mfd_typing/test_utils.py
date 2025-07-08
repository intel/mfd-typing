# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
import ipaddress

import pytest
from netaddr import IPAddress

from mfd_typing import utils
from mfd_typing.exceptions import InvalidWindowsKernelError, UnknownWindowsKernelVersionError
from mfd_typing.os_values import WindowsFlavour


class Testutils:
    def test_decimal_to_hex_pass_int(self):
        assert utils.decimal_to_hex(10) == "0x0000000a"

    def test_decimal_to_hex_pass_string(self):
        assert utils.decimal_to_hex("100") == "0x00000064"

    def test_decimal_to_bin_pass_string(self):
        assert utils.decimal_to_bin("10") == "1010"

    def test_decimal_to_bin_pass_int(self):
        assert utils.decimal_to_bin(100) == "1100100"

    def test_get_number_based_on_string(self):
        assert utils.get_number_based_on_string(input_string="A") == 65
        assert utils.get_number_based_on_string(input_string="abcdefg", range_of_results=1000) == 700

    def test_compare_numbers_as_unsigned(self):
        cases = [
            (0, 0, True),
            (-1, 1023, True),
            (1023, -1, True),
            (-1024, 0, True),
            (-1024, 1024, True),
            (-1024, 1023, False),
            (-10, 9, False),
        ]
        for number_1, number_2, expected in cases:
            assert utils.compare_numbers_as_unsigned(number_1, number_2) == expected

    def test_compare_non_conforming_versions_valid_versions(self):
        cases = [
            ("1.2.3", "1.2.3", 0),
            ("10.2.3", "1.2.3", 1),
            ("1.2.3", "1.2.30", -1),
            ("1.2", "1.2.3", -1),
            ("1.2.3.4", "1.2.3", 1),
            ("6", "7", -1),
        ]

        for version_1, version_2, expected in cases:
            assert utils.compare_non_conforming_versions(version_1, version_2) == expected

    def test_compare_non_conforming_versions_invalid_versions(self):
        cases = [("1.2.3.4", "1.2.2.a"), ("1.2.3.4", "1.2.3.4."), ("a.12.1", "b.12.1"), ("1,2,3,4", "1.2.3.4")]
        for version_1, version_2 in cases:
            with pytest.raises(ValueError):
                utils.compare_non_conforming_versions(version_1, version_2)

    def test_convert_port_dc_to_port_hex(self):
        assert utils.convert_port_dc_to_port_hex(65000) == "fd,e8"

    def test_convert_port_dc_to_port_hex_empty__pass(self):
        assert utils.convert_port_dc_to_port_hex("") == ""

    def test_convert_ip_dc_to_ip_hex_ipv6(self):
        assert (
            utils.convert_ip_dc_to_ip_hex(IPAddress("fe80::dcad:beff:fe7d:2503"))
            == "fe,80,00,00,00,00,00,00,dc,ad,be,ff,fe,7d,25,03"
        )

    def test_convert_ip_dc_to_ip_hex_ipv6_starting_2digits(self):
        assert (
            utils.convert_ip_dc_to_ip_hex(IPAddress("64:ff9b::1:108:8:3"))
            == "00,64,ff,9b,00,00,00,00,00,01,01,08,00,08,00,03"
        )

    def test_convert_ip_dc_to_ip_hex_ipv4(self):
        assert utils.convert_ip_dc_to_ip_hex(IPAddress("10.10.1.1")) == "a,a,1,1"

    def test_convert_ip_dc_to_ip_hex_pad_ipv6_len(self):
        assert (
            utils.convert_ip_dc_to_ip_hex(IPAddress("10.10.1.1"), True) == "a,a,1,1,00,00,00,00,00,00,00,00,00,00,00,00"
        )

    def test_convert_ipv4_to_brackets_colon_format_ipv4(self):
        assert utils.convert_ip_to_brackets_colon_format(ip=ipaddress.IPv4Address("1.2.1.1")) == "{0x0201,0x0101}"

    def test_convert_ipv6_to_brackets_colon_format_ipv6(self):
        expected_output = "{0x80fe,0x0000,0x0000,0x0000,0xfd3e,0xfffe,0xbcfe,0xc9b4}"
        assert (
            utils.convert_ip_to_brackets_colon_format(ip=ipaddress.IPv6Address("fe80::3efd:feff:febc:b4c9"))
            == expected_output
        )

    def test_get_windows_version_from_kernel_pass_12(self):
        kernel_version = "9600"
        expected_windows_version = WindowsFlavour.WindowsServer2012R2
        assert utils.get_windows_version_from_kernel(kernel_version=kernel_version) == expected_windows_version

    def test_get_windows_version_from_kernel_pass_16(self):
        kernel_version = "14393"
        expected_windows_version = WindowsFlavour.WindowsServer2016
        assert utils.get_windows_version_from_kernel(kernel_version=kernel_version) == expected_windows_version

    def test_get_windows_version_from_kernel_invalid(self):
        kernel_version = "14393-bla"
        with pytest.raises(InvalidWindowsKernelError):
            utils.get_windows_version_from_kernel(kernel_version=kernel_version)

    def test_get_windows_version_from_kernel_unknown(self):
        kernel_version = "14392"
        with pytest.raises(UnknownWindowsKernelVersionError):
            utils.get_windows_version_from_kernel(kernel_version=kernel_version)

    @pytest.mark.parametrize("param", ["yes", "YES", "true", "TRUE", "1", "y", "t", True])
    def test_strtobool_true(self, param):
        assert utils.strtobool(param)

    @pytest.mark.parametrize("param", ["no", "NO", "false", "False", "0", "n", "f", "off", False])
    def test_strtobool_false(self, param):
        assert not utils.strtobool(param)

    def test_strtobool_value_error(self, param="yess"):
        with pytest.raises(ValueError):
            assert utils.strtobool(param)

    def test_strtobool_type_error(self, param=["yes"]):
        with pytest.raises(TypeError):
            assert utils.strtobool(param)

    @pytest.mark.parametrize(
        "ip_address_value, expected",
        [
            (ipaddress.ip_address("192.168.1.1"), "0xc0a80101"),
            (ipaddress.ip_interface("192.168.1.1/255.255.255.0"), "0xc0a80101"),
        ],
    )
    def test_convert_ip_dc_to_hex_value(self, ip_address_value, expected):
        assert utils.convert_ip_dc_to_hex_value(ip_address_value) == expected

    @pytest.mark.parametrize(
        "mac_value, expected",
        [
            ("00:00:5e:00:53:af", "0x00005e0053af"),
            ("0x00005e0053af", "0x00005e0053af"),
        ],
    )
    def test_convert_mac_to_hex(self, mac_value, expected):
        assert utils.convert_mac_string_to_hex(mac_value) == expected

    @pytest.mark.parametrize(
        "mac, expected",
        [
            ("008041aefd7e", "00:80:41:ae:fd:7e"),
            ("00:80:41:AE:FD:7E", "00:80:41:ae:fd:7e"),
            ("00-80-41-ae-fd-7e", "00:80:41:ae:fd:7e"),
            ("0080.41ae.fd7e", "00:80:41:ae:fd:7e"),
            ("00 : 80 : 41 : ae : fd : 7e", "00:80:41:ae:fd:7e"),
            ("  00:80:41:ae:fd:7e  ", "00:80:41:ae:fd:7e"),
            ("00:80:41:ae:fd:7e\n\t", "00:80:41:ae:fd:7e"),
        ],
    )
    def test_format_mac_to_canonical(self, mac, expected):
        assert utils.format_mac_string_to_canonical(mac) == expected

    def test_get_sed_inline_cmd_no_line_idx(self):
        act_line, new_line, filename = "act_line", "new_line", "filename"
        if "/" in f"{act_line}{new_line}":
            sep = "|"
        else:
            sep = "/"
        exp_rv = sep.join(["sed -i 's", act_line, new_line, f"g' {filename}"])
        assert exp_rv == utils.get_sed_inline(act_line, new_line, filename, None)

    def test_get_sed_inline_cmd_nonempty_line_idx(self):
        act_line, new_line, filename = "act_line", "new_line", "filename"
        if "/" in f"{act_line}{new_line}":
            sep = "|"
        else:
            sep = "/"
        exp_rv = sep.join(["sed -i '1s", act_line, new_line, f"g' {filename}"])
        assert exp_rv == utils.get_sed_inline(act_line, new_line, filename, 1)

    def test_prepare_sed_string(self):
        assert '"dpcp": "notice\\.pkg"' == utils.prepare_sed_string(
            input_str='"dpcp": "notice.pkg"', pattern=r"$.*/[\]^"
        )

    def test_prepare_sed_string_replacement(self):
        assert '"dpcp": "notice"' == utils.prepare_sed_string(input_str='"dpcp": "notice"', pattern=r"\&")
