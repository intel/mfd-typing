# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""
Module for (Sub)Vendor/Device ID representation classes.

Contains self-validating classes which are used to represent (Sub)Vendor/Device ID's.

All public classes are essentially equal to the base class, but are made separate so objects of different classes
are not comparable:
>>> VendorID(0x8086) == VendorID(0x8086)
True
>>> VendorID(0x8086) == DeviceID(0x8086)
False
"""

from typing import Any


class _VendorDeviceID:
    """
    Base class for (Sub)Vendor/Device ID representation.

    Can be initialized using string, int, or another object of this class.

    All the following objects are equal:
    >>> _VendorDeviceID(0x8086)
    _VendorDeviceID('8086')
    >>> _VendorDeviceID('8086')
    _VendorDeviceID('8086')
    >>> _VendorDeviceID(_VendorDeviceID(0x8086))
    _VendorDeviceID('8086')

    The object constructor will raise an error if the VID/DID is out of range:
    >>> _VendorDeviceID(-1)
    Traceback (most recent call last):
      ...
    ValueError: Vendor/Device ID has to be between 0 and 0xFFFF, got -0x1 instead
    >>> _VendorDeviceID(0xFFFF + 1)
    Traceback (most recent call last):
      ...
    ValueError: Vendor/Device ID has to be between 0 and 0xFFFF, got 0x10000 instead

    The objects are comparable to themselves:
    >>> _VendorDeviceID(0x8086) == _VendorDeviceID('8086')
    True
    >>> _VendorDeviceID(0x8086) != _VendorDeviceID('8087')
    True

    All the objects are represented as 4-character hex decimal
    >>> print(_VendorDeviceID(0x8086))
    8086
    >>> print(_VendorDeviceID('DA'))
    00DA

    The objects are hashable so they can be used as keys for a dictionary:
    >>> {_VendorDeviceID(0xDEAD): 'a', _VendorDeviceID('BEEF'): 'b'}
    {_VendorDeviceID('DEAD'): 'a', _VendorDeviceID('BEEF'): 'b'}
    >>> d = {_VendorDeviceID(0xDEAD): 'a', _VendorDeviceID('BEEF'): 'b'}
    >>> d[_VendorDeviceID('DEAD')]
    'a'
    """

    def __new__(cls, value: Any) -> "_VendorDeviceID":
        if isinstance(value, cls):
            return value
        else:
            return super().__new__(cls)

    def __init__(self, value: Any) -> None:
        if isinstance(value, (str, bytes)):
            self._value = int(value, base=16)
        else:
            self._value = int(value)

        if not 0 <= self._value <= 0xFFFF:
            raise ValueError(f"Vendor/Device ID has to be between 0 and 0xFFFF, got {self._value:#x} instead")

    def __str__(self) -> str:
        return f"{self._value:04X}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__!s}('{self}')"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return other._value == self._value

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __hash__(self) -> int:
        return hash(self._value)

    def __int__(self) -> int:
        return self._value


class VendorID(_VendorDeviceID):
    """Vendor ID representation."""


class DeviceID(_VendorDeviceID):
    """Device ID representation."""


class SubVendorID(_VendorDeviceID):
    """SubVendor ID representation."""


class SubDeviceID(_VendorDeviceID):
    """SubDevice ID representation."""
