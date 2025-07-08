# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for MAC address."""

import re
from typing import Union, Type

from netaddr import EUI, mac_unix_expanded, mac_eui48
from generate_mac import generate_mac
from netaddr.core import AddrFormatError


class MACAddress(EUI):
    """
    Class representing MAC address.

    It's just a wrapper around netaddr.EUI class with
    more user-friendly name and adjusted defaults

    For more information on this class please check out netaddr documentation:
    http://netaddr.readthedocs.io/en/latest/api.html#netaddr.EUI
    """

    def __init__(self, addr: Union[str, int, "MACAddress"], dialect: Type[mac_eui48] = mac_unix_expanded) -> None:
        """
        Initialize a MACAddress class.

        :param addr: MAC address in any of supported formats
        :param dialect: Style which will be used to convert the object to string, default leading zeroes
        """
        try:
            super().__init__(addr=addr, dialect=dialect)

        except AddrFormatError:
            raise ValueError(f"{addr} is not a correct MAC 48b format")

        if self.version != 48:
            raise ValueError(f"{addr} is not a correct MAC 48b format")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self}')"


def get_random_mac() -> MACAddress:
    """
    Generate a random MAC address.

    :return: MAC address object with MAC address in xx:xx:xx:xx:xx:xx format
    """
    return MACAddress(generate_mac.total_random())


def get_random_multicast_mac() -> MACAddress:
    """
    Generate multicast MAC starting from '01:00:5e:xx:xx:xx' with the last 3 octets randomize.

    :return: MAC address object with randomized multicast MAC address in format '01:00:5e:xx:xx:xx'
    """
    return MACAddress(generate_mac.vid_provided("01:00:5e"))


def get_random_unicast_mac() -> MACAddress:
    """
    Generate unicast MAC starting from 'fa:xx:xx:xx:xx:xx'.

    :return: MAC address object with randomized unicast MAC address in format 'fa:xx:xx:xx:xx:xx'
    """
    return MACAddress(generate_mac.vid_provided("fa:11:11"))


def get_random_mac_using_prefix(prefix: str = None) -> MACAddress:
    """
    Generate a random MAC address from the range prefix:xx:xx:xx - prefix:xx:xx:xx.

    If prefix is not passed the MAC address generated will be fa:11:11:xx:xx:xx.
    :param prefix: prefix for the MAC Address to be generated.
    :return: MAC address object
    """
    prefix = prefix if prefix else "fa:11:11"
    return MACAddress(generate_mac.vid_provided(prefix))


def parse_mac(mac: MACAddress) -> str:
    """Parse mac address in special way to have format like: '{0xfd3c,0xbcfe,0x68b6}'.

    The function creates a list from string and chops it to 3x 2 byte, and reverses bytes order for each couple.

    :param mac: MACAddress to be parsed in special way
    """
    mac = re.sub(":", "", str(mac))  # remove colons
    mac_hex = [mac[i : i + 4] for i in range(0, len(mac), 4)]  # split into 4-char groups
    ip_changed_hex = [f"0x{elem[2:]}{elem[0:2]}" for elem in mac_hex]  # reverse byte order
    return "{" + ",".join(ip_changed_hex) + "}"
