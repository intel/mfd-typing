# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Module for PCI Address representation."""

import re
from dataclasses import dataclass, InitVar, fields
from typing import Optional, Any

from .dataclass_utils import convert_value_field_to_typehint_type

hex_reg = r"[0-9a-fA-F]"
_pci_address_without_domain_hex_regex = rf"(?P<bus>{hex_reg}{{2}}):(?P<slot>{hex_reg}{{2}})\.(?P<func>\d+)"
pci_address_without_domain_hex_regex = rf"^{_pci_address_without_domain_hex_regex}$"
pci_address_full_hex_regex = rf"^(?P<domain>{hex_reg}{{4}}):{_pci_address_without_domain_hex_regex}$"


@dataclass(frozen=True)
class PCIAddress:
    """Class representing PCI address."""

    domain: Optional[int] = None
    bus: Optional[int] = None
    slot: Optional[int] = None
    func: Optional[int] = None
    data: InitVar[str] = None

    def _parse_string_to_pci(self, data: str) -> None:
        if data is not None:
            match_hex_without_domain = re.search(pattern=pci_address_without_domain_hex_regex, string=data)
            match_hex_full = re.search(pattern=pci_address_full_hex_regex, string=data)
            match_int = len(data.split(":")) == 4  # sbdf format acceptable for int values
            if match_hex_without_domain:
                self.__dict__["domain"] = 0
                self.__dict__["bus"] = int(match_hex_without_domain.group("bus"), 16)
                self.__dict__["slot"] = int(match_hex_without_domain.group("slot"), 16)
                self.__dict__["func"] = int(match_hex_without_domain.group("func"), 16)
            elif match_hex_full:
                self.__dict__["domain"] = int(match_hex_full.group("domain"), 16)
                self.__dict__["bus"] = int(match_hex_full.group("bus"), 16)
                self.__dict__["slot"] = int(match_hex_full.group("slot"), 16)
                self.__dict__["func"] = int(match_hex_full.group("func"), 16)
            elif match_int:
                pci_elements = data.split(":")
                self.__dict__["domain"] = int(pci_elements[0])
                self.__dict__["bus"] = int(pci_elements[1])
                self.__dict__["slot"] = int(pci_elements[2])
                self.__dict__["func"] = int(pci_elements[3])
            else:
                raise ValueError(f"Incorrect format was provided as input to PCIAddress object creation: {data}")

    def __post_init__(self, data: Optional[str] = None) -> None:
        self._parse_string_to_pci(data=data)
        if data is None and None in self.__dict__.values():
            raise PCIAddressMissingData(
                f"There are missing data for provided value because None are not acceptable: {self.__dict__}"
            )
        for field in fields(self):
            convert_value_field_to_typehint_type(self, field)

        self._check_domain(value=self.domain)
        self._check_bus(value=self.bus)
        self._check_slot(value=self.slot)
        self._check_func(value=self.func)

    def __eq__(self, other: Any):
        if other is None:
            return False

        if not isinstance(other, type(self)):
            raise PCIDAddressIncomparableObject(f"Incorrect object passed for comparison with PCIAddress: {other}")

        return all(getattr(self, field) == getattr(other, field) for field in vars(self).keys() - "data")

    def __lt__(self, other: Any):
        if other is None:
            return False

        if not isinstance(other, type(self)):
            raise PCIDAddressIncomparableObject(f"Incorrect object passed for comparison with PCIAddress: {other}")

        return (self.domain, self.bus, self.slot, self.func) < (other.domain, other.bus, other.slot, other.func)

    def __gt__(self, other: Any):
        if other is None:
            return False

        if not isinstance(other, type(self)):
            raise PCIDAddressIncomparableObject(f"Incorrect object passed for comparison with PCIAddress: {other}")

        return (self.domain, self.bus, self.slot, self.func) > (other.domain, other.bus, other.slot, other.func)

    def _check_domain(self, value: int) -> None:
        if not 0 <= value < 2**32:
            raise ValueError(f"domain value out of bounds: {value}")

    def _check_bus(self, value: int) -> None:
        if not 0 <= value < 2**8:
            raise ValueError(f"bus value out of bounds: {value}")

    def _check_slot(self, value: int) -> None:
        if not 0 <= value < 2**8:
            raise ValueError(f"slot value out of bounds: {value}")

    def _check_func(self, value: int) -> None:
        if not 0 <= value < 2**8:
            raise ValueError(f"func value out of bounds: {value}")

    @property
    def lspci(self) -> str:
        """lspci-compatible (Linux) representation."""
        return f"{self.domain:04x}:{self.bus:02x}:{self.slot:02x}.{self.func:x}"

    @property
    def lspci_short(self) -> str:
        """lspci-compatible (Linux) representation (bus slot function)."""
        return f"{self.bus:02x}:{self.slot:02x}.{self.func:x}"

    @property
    def sbdf(self) -> str:
        """sbdf-compatible (segment bus device function) representation."""
        return f"{self.domain:02}:{self.bus:03}:{self.slot:02}:{self.func:02}"

    @property
    def pciconf(self) -> str:
        """pciconf-compatible (FreeBSD) representation."""
        return f"pci{self.domain}:{self.bus}:{self.slot}:{self.func}"

    @property
    def nvmcheck_bdf(self) -> str:
        """nvmcheck-compatible (bus device function) representation."""
        return f"{self.bus:03}/{self.slot:02}/{self.func:02}"

    def __str__(self) -> str:
        return self.lspci


class PCIAddressMissingData(Exception):
    """Exception raised for wrong input data providing."""


class PCIDAddressIncomparableObject(Exception):
    """Exception raised for incorrect object passed for comparison."""
