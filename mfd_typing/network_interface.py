# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Network interface structures."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

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
    parent: Optional[str] = None


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

    node: Optional[str] = None
    network: Optional[str] = None


@dataclass
class InterfaceInfo:
    """
    Structure for network interface info.

    All possible fields that can be helpful, while creating network interface.
    """

    pci_address: Optional[PCIAddress] = None
    pci_device: Optional[PCIDevice] = None
    name: Optional[str] = None
    interface_type: InterfaceType = InterfaceType.GENERIC
    mac_address: Optional[MACAddress] = None
    installed: Optional[bool] = None
    branding_string: Optional[str] = None
    vlan_info: Optional[VlanInterfaceInfo] = None


@dataclass
class LinuxInterfaceInfo(InterfaceInfo):
    """
    Structure for Linux network interface info.

    All possible fields that can be helpful, while creating network interface.
    """

    namespace: Optional[str] = None
    vsi_info: Optional[VsiInfo] = None


@dataclass
class WindowsInterfaceInfo(InterfaceInfo):
    """
    Structure for Windows network interface info.

    All possible fields that can be helpful, while creating network interface.
    """

    description: Optional[str] = None
    index: Optional[str] = None
    manufacturer: Optional[str] = None
    net_connection_status: Optional[str] = None
    pnp_device_id: Optional[str] = None
    product_name: Optional[str] = None
    service_name: Optional[str] = None
    guid: Optional[str] = None
    speed: Optional[str] = None
    cluster_info: Optional[ClusterInfo] = None


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
