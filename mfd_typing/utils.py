# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Utils."""

from typing import Union, TYPE_CHECKING
from netaddr import ipv6_verbose
from mfd_typing.exceptions import UnknownWindowsKernelVersionError, InvalidWindowsKernelError
from mfd_typing.os_values import WindowsFlavour
import re

if TYPE_CHECKING:
    from netaddr import IPAddress
    from pathlib import Path
    from ipaddress import IPv4Address, IPv6Address, IPv4Interface, IPv6Interface


def decimal_to_hex(decimal_value: Union[str, int]) -> str:
    """
    Convert decimal value to hexadecimal.

    :param decimal_value: decimal value
    :return: hexadecimal value
    """
    hex_value = f"0x{int(decimal_value):08x}"

    return hex_value


def decimal_to_bin(decimal_value: Union[str, int]) -> str:
    """
    Convert decimal value to binary number.

    :param decimal_value: decimal value
    :return: binary value in 3 bit format e.g. 011.
    """
    return str(f"{int(decimal_value):03b}")


def get_number_based_on_string(input_string: str, range_of_results: int = 100) -> int:
    """
    Get calculated number based on provided string from specific range.

    :param input_string: String to be converted to sum of its ASCII chars
    :param range_of_results: Range of results numbers
    """
    result = 0
    result = sum(ord(c) for c in input_string)

    return result % range_of_results


def compare_numbers_as_unsigned(number_1: int, number_2: int) -> bool:
    """
    Compare numbers as unsigned. This accounts for possible overflow on negative values.

    :param number_1: first value to compare
    :param number_2: second value to compare
    :return: True if unsigned representations are equal, False otherwise
    """
    if number_1 == number_2:
        return True
    else:
        numbers = (number_1, number_2)
        max_val = max(map(lambda n: abs(n if n > 0 else n + 1), numbers))  # Determine number range
        bitness = next(filter(lambda n: 1 << n > max_val, range(65))) + 1  # Calculate number of bits for number range
        unsigned_1, unsigned_2 = map(lambda n: n if n >= 0 else (1 << bitness - 1) + n, numbers)  # Shift if negative
        return unsigned_1 == unsigned_2


def compare_non_conforming_versions(version_1: str, version_2: str) -> int:
    """
    Compare versions that cannot be compared using StrictVersion class.

    :param version_1: first version to compare
    :param version_2: second version to compare
    :return: 1 if version_1 is greater, -1 if version_2 is greater, 0 if they are equal
    :raises ValueError: When any of arguments is not formatted properly
    """
    version_pattern = r"^(?:\d\.?)*\d$"

    for ver in (version_1, version_2):
        if not re.match(version_pattern, ver):
            raise ValueError(f"Version {ver} is invalid")

    raw_version_1 = version_1.split(".")
    raw_version_2 = version_2.split(".")

    # Versions are compared from first part onward. If any is greater, the version is assumed greater.
    for _ in range(max(len(raw_version_1), len(raw_version_2))):
        version_1_part = int(raw_version_1.pop(0)) if raw_version_1 else -1
        version_2_part = int(raw_version_2.pop(0)) if raw_version_2 else -1
        if version_1_part > version_2_part:
            return 1
        elif version_2_part > version_1_part:
            return -1

    return 0


def convert_port_dc_to_port_hex(port: Union[int, str]) -> str:
    """
    Convert Port number to comma separated hexadecimal port number.

    :param port: Port number
    :return: converted hexadecimal Port number value separated by comma or empty string.
    """
    new_hex = ""
    try:
        port = hex(int(port)).replace("0x", "0000")[-4:]
        for i in range(0, len(port), 2):
            new_hex += port[i : i + 2] + ","
        new_hex = new_hex.rstrip(",")
    except ValueError:
        pass
    return new_hex


def convert_ip_dc_to_ip_hex(ip: "IPAddress", pad_ipv6_len: bool = False) -> str:
    """
    Convert IP address to comma separated hexadecimal IP address.

    :param ip: IPAddress, can be IPv4 or IPv6
    :param pad_to_v6: If ipv4, add extra 00 to match the length of an ipv6 address
    :return: converted hexadecimal IP value separated by comma.
    """
    new_hex = ""
    if ip.version == 6:
        expand_ip = ip.format(ipv6_verbose).replace(":", "")
        for i in range(0, len(expand_ip), 2):
            new_hex += expand_ip[i : i + 2] + ","
        new_hex = new_hex.rstrip(",")
    else:
        for i in ip.words:
            new_hex += str(hex(int(i)).replace("0x", "")) + ","
        new_hex = new_hex.rstrip(",")
        if pad_ipv6_len:
            new_hex += ",00,00,00,00,00,00,00,00,00,00,00,00"
    return new_hex


def convert_ip_dc_to_hex_value(ip: "IPv4Address | IPv6Address | IPv4Interface | IPv6Interface") -> str:
    """
    Convert the IP value to its HEX value.

    :param ip: Holds the IP address value
    :return hex_value: HEX value of the IP address
    """
    return f"0x{ip:x}"


def convert_mac_string_to_hex(mac: str) -> str:
    """
    Convert the MAC value to its HEX value.

    :param mac: Holds the MAC address value
    :return: HEX value of the MAC address
    """
    if ":" in mac:
        hex_value = "0x"
        mac_list = mac.split(":")
        hex_value += "".join(mac_list)
        return hex_value
    else:
        return mac


def format_mac_string_to_canonical(mac: str) -> str:
    r"""
    Format mac to different format as below.

    '008041aefd7e',  # valid
    '00:80:41:ae:fd:7e',  # valid
    '00:80:41:AE:FD:7E',  # valid
    '00:80:41:aE:Fd:7E',  # valid
    '00-80-41-ae-fd-7e',  # valid
    '0080.41ae.fd7e',  # valid
    '00 : 80 : 41 : ae : fd : 7e',  # valid
    '  00:80:41:ae:fd:7e  ',  # valid
    '00:80:41:ae:fd:7e\n\t',  # valid
    and coverts to proper canonical format.

    :param mac: Input mac address
    :return: Formatted string in canonical format
    """
    mac = re.sub("[.:-]", "", mac).lower()  # remove delimiters and convert to a lower case
    mac = "".join(mac.split())  # remove whitespaces
    assert len(mac) == 12  # length should be now exactly 12 (eg. 008041aefd7e)
    assert mac.isalnum()  # should only contain letters and numbers
    # convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
    mac = ":".join(["%s" % (mac[i : i + 2]) for i in range(0, 12, 2)])
    return mac


def convert_ip_to_brackets_colon_format(ip: "IPv4Address | IPv6Address") -> str:
    """Parse an IP address in a special way.

    The function creates a list from string and chops it to 2x 2 byte or 8x 2 byte,
    and reverses bytes order for each couple.

    :param ip: IP address as a string, e.g., '1.2.1.1' or 'fe80::3efd:feff:febc:b4c9'
    :return: IP address as string correctly parsed, e.g., '{0x0201,0x0101}' or
             '{0x80fe,0x0000,0x0000,0x0000,0xfd3e,0xfffe,0xbcfe,0xc9b4}'
    """
    hex_ip = hex(int(ip)).split("x")[1]
    hex_ip = hex_ip.zfill(8) if ip.version == 4 else hex_ip.zfill(32)
    ip_hex = [hex_ip[idx : idx + 4] for idx, _ in enumerate(hex_ip) if idx % 4 == 0]
    ip_changed_hex = [f"0x{elem[2:]}{elem[:2]}" for elem in ip_hex]
    return "{" + ",".join(ip_changed_hex) + "}"


def get_windows_version_from_kernel(kernel_version: str) -> WindowsFlavour:
    """Map Windows Kernel to Windows Flavour.

    :param kernel_version: Kernel Version
    :return: Windows OS Version
    """
    try:
        kernel_version = int(kernel_version)
    except ValueError:
        raise InvalidWindowsKernelError(f"Cannot convert '{kernel_version}' to integer.")

    if kernel_version == 9600:
        return WindowsFlavour.WindowsServer2012R2
    elif kernel_version == 14393:
        return WindowsFlavour.WindowsServer2016
    elif kernel_version == 17763:
        return WindowsFlavour.WindowsServer2019
    elif kernel_version == 20348:
        return WindowsFlavour.WindowsServer2022
    elif kernel_version == 22621:
        return WindowsFlavour.WindowsServer2022H2
    elif kernel_version == 26100:
        return WindowsFlavour.WindowsServer2025
    else:
        raise UnknownWindowsKernelVersionError(f"Cannot map {kernel_version} to any of supported Windows Flavours.")


def strtobool(param: Union[str, bool]) -> bool:
    """
    Convert strings to boolean True or False.

    "true", "yes", "1", "y", "t", "on" are cast to True,
    "false", "no", "0", "n", "f", "off" are cast to False, case insensitive
    If the param is already a boolean value - return it unchanged
    This is much more strict conversion than bool(param), ast.literal_eval(param), etc.

    :param param: value to cast
    :return: boolean representation of param
    :raise TypeError: if param is neither a boolean nor a string
    :raise ValueError: if param is a string with unsupported value
    """
    if isinstance(param, bool):
        return param
    elif isinstance(param, str):
        param = param.lower().strip()
        if param in ("true", "yes", "1", "y", "t", "on"):
            return True
        elif param in ("false", "no", "0", "n", "f", "off"):
            return False
        else:
            raise ValueError(f"'param' must be one of ('true', 'yes', '1', 'false', 'no', '0'), got {param} instead")
    else:
        raise TypeError(f"'param' must be either string or boolean value, got {type(param)} instead")


def get_sed_inline(act_line: str, new_line: str, filename: "str | Path", line_idx: int | str = 0) -> str:
    """
    Prepare sed command with all needed parameters.

    :param act_line: input line for sed.
    :param new_line: input line to be replaced with.
    :param filename: filename of the file to be edited.
    :param line_idx: pass a positive number representing the number of the line to be changed if you wish so.
    :return: sed cmd
    """
    line_idx = line_idx or ""
    if "/" in f"{act_line}{new_line}":
        sep = "|"
    else:
        sep = "/"
    return sep.join([f"sed -i '{line_idx}s", act_line, new_line, f"g' {filename}"])


def prepare_sed_string(input_str: str, pattern: str) -> str:
    """
    Prepare `str` to be parsed as a literal string by sed.

    :param input_str: parsed as a literal string by sed - that is, escape its special chars.
    :param pattern: the set of chars to be escaped
    :return: 'escaped' string
    """
    new_str = []
    for idx, c in enumerate(input_str):
        if c in pattern:
            if idx and input_str[idx - 1] != "\\" or not idx:
                new_str.append(rf"\{c}")
        else:
            new_str.append(c)
    return "".join(new_str)
