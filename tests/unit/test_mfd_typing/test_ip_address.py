# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
import pytest
from netaddr import IPAddress, IPNetwork
from netaddr.core import AddrFormatError


class TestIPAddress:
    @pytest.mark.parametrize("ip", ["192.10.10.1", "10.0.1.0", "2001:db8:3333:4444:5555:6666:7777:8888"])
    def test_is_ip_address(self, ip):
        assert IPAddress(ip)

    @pytest.mark.parametrize("ip", ["244.10.10.1.4", "2001:0db8:85a3:0000:0000:8a2e:0370:7334:1234"])
    def test_with_wrong_values(self, ip):
        with pytest.raises(AddrFormatError):
            assert IPAddress(ip)

    def test_get_ip_version(self):
        ver = IPAddress("10.0.1.14")
        assert str(ver.version) == "4"

    def test_ip_to_int(self):
        assert int(IPAddress("192.0.2.1")) == 3221225985

    def test_ipv6_to_int(self):
        assert int(IPAddress("fe80::dead:beef")) == 338288524927261089654018896845083623151

    def test_ip_to_hex(self):
        assert hex(IPAddress("192.0.2.1")) == "0xc0000201"

    def test_ipv6_to_hex(self):
        assert hex(IPAddress("fe80::dead:beef")) == "0xfe8000000000000000000000deadbeef"

    def test_ip_to_bin(self):
        assert IPAddress("192.0.2.1").bin == "0b11000000000000000000001000000001"

    def test_ip_to_bits(self):
        assert IPAddress("192.0.2.1").bits() == "11000000.00000000.00000010.00000001"

    def test_ipv6_to_bits(self):
        assert (
            IPAddress("fe80::dead:beef").bits()
            == "1111111010000000:0000000000000000:0000000000000000:0000000000000000:"
            "0000000000000000:0000000000000000:1101111010101101:1011111011101111"
        )

    def test_ip_to_words(self):
        assert IPAddress("192.0.2.1").words == (192, 0, 2, 1)

    def test_ip_address_packed(self):
        addr = IPAddress("10.1.1.10")
        assert addr.packed == b"\n\x01\x01\n"

    def test_ipv6_address_packed(self):
        addr = IPAddress("2001:db8:3333:4444:5555:6666:7777:8888")
        assert addr.packed == b" \x01\r\xb833DDUUffww\x88\x88"

    @pytest.mark.parametrize("ip", ["192.0.2.1", "fe80::1"])
    def test_is_unicast(self, ip):
        assert IPAddress(ip).is_unicast()

    @pytest.mark.parametrize("ip", ["239.192.0.1", "ff00::1"])
    def test_is_multicast(self, ip):
        assert IPAddress(ip).is_multicast()

    def test_is_private(self):
        assert IPAddress("172.24.0.1").is_private()

    def test_is_reserved(self):
        assert IPAddress("253.0.0.1").is_reserved()

    def test_is_loopback(self):
        assert IPAddress("127.0.0.1").is_loopback()

    def test_is_netmask(self):
        assert IPAddress("255.255.255.0").is_netmask()

    @pytest.mark.parametrize(
        "ip1, ip2",
        [
            ("192.100.100.1", "192.100.100.1"),
            ("2001:db8:3333:4444:5555:6666:7777:8888", "2001:db8:3333:4444:5555:6666:7777:8888"),
        ],
    )
    def test_compare_same_ip_addresses(self, ip1, ip2):
        assert IPAddress(ip1) == IPAddress(ip2)

    @pytest.mark.parametrize(
        "ip1, ip2",
        [
            ("192.100.100.1", "172.100.10.1"),
            ("2001:db8:3333:4444:5555:6666:7777:8888", "2002:db8:3333:4444:5555:6666:8888:8888"),
        ],
    )
    def test_compare_different_ip_addresses(self, ip1, ip2):
        assert not IPAddress(ip1) == IPAddress(ip2)


class TestIPNetwork:
    @pytest.mark.parametrize("ip", ["129.168.24.30/24", "129.168.24.30", "001:db8:a0b:12f0::1"])
    def test_get_ip_network(self, ip):
        if ip == "129.168.24.30/24":
            assert IPNetwork("129.168.24.30/24")
        elif ip == "129.168.24.30":
            assert IPNetwork("129.168.24.30/16")
        else:
            assert IPNetwork("1:db8:a0b:12f0::1/128")

    def test_get_broadcast_ip(self):
        broadcast = str(IPNetwork("192.0.2.0/24").broadcast)
        assert broadcast == "192.0.2.255"

    def test_get_netmask(self):
        netmask = str(IPNetwork("192.0.2.0/24").netmask)
        assert netmask == "255.255.255.0"

    def test_get_ip_size(self):
        size = IPNetwork("192.0.2.0/24").size
        assert size == 256

    def test_get_ip_network_class_C(self):
        assert str(IPNetwork("192.10.10.10", implicit_prefix=True)) == "192.10.10.10/24"

    def test_get_ip_network_class_B(self):
        assert str(IPNetwork("180.10.10.2", implicit_prefix=True)) == "180.10.10.2/16"

    def test_define_mask_by_class_ip(self, ip="129.168.24.1"):
        assert IPNetwork(ip, implicit_prefix=True).prefixlen == 16

    def test_define_mask_by_class_ip_ipv6(self, ip="001:db8:a0b:12f0::1"):
        assert IPNetwork(ip, implicit_prefix=True).prefixlen == 128

    def test_mask2len(self):
        val = IPNetwork("192.10.10.1/255.254.0.0")
        assert val.prefixlen == 15

    def test_len2mask(self):
        val = IPNetwork("192.10.0.0/18")
        assert str(val.netmask) == "255.255.192.0"

    def test_iterhosts(self):
        hosts = []
        val = IPNetwork("192.0.2.16/29").iter_hosts()
        for ip in val:
            hosts.append(ip)
        assert hosts == [
            IPAddress("192.0.2.17"),
            IPAddress("192.0.2.18"),
            IPAddress("192.0.2.19"),
            IPAddress("192.0.2.20"),
            IPAddress("192.0.2.21"),
            IPAddress("192.0.2.22"),
        ]
