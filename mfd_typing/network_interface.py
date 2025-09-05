# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Network interface structures."""

from dataclasses import dataclass
from enum import Enum, auto
from uuid import UUID

from mfd_typing import PCIAddress, PCIDevice, MACAddress


class InterfaceType(Enum):
    """Structure for network interface types."""

    GENERIC = auto()  # default # noqa BLK100
    ETH_CONTROLLER = auto()  # network controller listed on pci (default for network device without loaded driver)
    VIRTUAL_DEVICE = auto()  # interface located in path ../devices/virtual/net/ (bridge, macvlan, loopback)
    PF = auto()  # regular physical interface; located on PCI bus (../devices/pci0000/..) (eth)
    VF = auto()  # virtual inteface (SRIOV); described as 'Virtual Interface' in lspci detailed info
    VPORT = auto()  # IPU-specific interface with shared PCIAddress (extra VSI Info stored in `VsiInfo`)
    VMNIC = auto()  # ESXi-specific interface or Windows Hyper-V interface (VNIC associated with SR-IOV interface)
    VMBUS = auto()  # Hyper-V specific for Linux Guests (https://docs.kernel.org/virt/hyperv/vmbus.html)
    MANAGEMENT = auto()  # interface that have management IPv4 address assigned
    VLAN = auto()  # virtual device which is assigned to 802.1Q VLAN (details in`VlanInterfaceInfo`)
    CLUSTER_MANAGEMENT = auto()  # cluster management interface type
    CLUSTER_STORAGE = auto()  # storage / compute interfaces in cluster nodes, marked as vSMB in system
    BTS = auto()  # Linux: BTS shares PCI bus, device ID and index, we will mark it based on name starting with "nac"
    BOND = auto()  # Linux: Bonding interface, which is a virtual interface that aggregates multiple physical interfaces
    BOND_SLAVE = auto()  # Slave interface of a bonding interface


@dataclass
class VlanInterfaceInfo:
    """Structure for vlan interface info."""

    vlan_id: int
    parent: str | None = None


@dataclass
class VsiInfo:
    """Structure for VSI Info."""

    fn_id: int
    host_id: int
    is_vf: bool
    vsi_id: int
    vport_id: int
    is_created: bool
    is_enabled: bool


@dataclass
class ClusterInfo:
    """Structure for cluster info."""

    node: str | None = None
    network: str | None = None


@dataclass
class InterfaceInfo:
    """
    Structure for network interface info.

    All possible fields that can be helpful, while creating network interface.
    """

    pci_address: PCIAddress | None = None
    pci_device: PCIDevice | None = None
    name: str | None = None
    interface_type: InterfaceType = InterfaceType.GENERIC
    mac_address: MACAddress | None = None
    installed: bool | None = None
    branding_string: str | None = None
    vlan_info: VlanInterfaceInfo | None = None


@dataclass
class LinuxInterfaceInfo(InterfaceInfo):
    """
    Structure for Linux network interface info.

    All possible fields that can be helpful, while creating network interface.
    """

    namespace: str | None = None
    vsi_info: VsiInfo | None = None
    uuid: UUID | None = None


@dataclass
class WindowsInterfaceInfo(InterfaceInfo):
    """
    Structure for Windows network interface info.

    All possible fields that can be helpful, while creating network interface.
    """

    description: str | None = None
    index: str | None = None
    manufacturer: str | None = None
    net_connection_status: str | None = None
    pnp_device_id: str | None = None
    product_name: str | None = None
    service_name: str | None = None
    guid: str | None = None
    speed: str | None = None
    cluster_info: ClusterInfo | None = None


# WindowsInterfaceInfo field matched with PowerShell name of property
win_interface_properties = {
    "description": "Description",
    "index": "Index",
    "installed": "Installed",
    "mac_address": "MACAddress",
    "manufacturer": "Manufacturer",
    "branding_string": "Name",
    "name": "NetConnectionID",
    "net_connection_status": "NetConnectionStatus",
    "pnp_device_id": "PNPDeviceID",
    "product_name": "ProductName",
    "service_name": "ServiceName",
    "guid": "GUID",
    "speed": "Speed",
}
