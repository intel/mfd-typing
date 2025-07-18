> [!IMPORTANT]  
> This project is under development. All source code and features on the main branch are for the purpose of testing or evaluation and not production ready.
 
# Typing for MFD
Module containing common data structures and utilities shared between MFD modules.

## Supported structures
### OSType
Structure for supported types of OS (compatible with platform.system)
```python
class OSType(str, Enum):
    """Available OS types."""

    WINDOWS = "nt"
    POSIX = "posix"
    EFISHELL = "efishell"
```

### OSName
Structure for supported names of OS (compatible with os.name)
```python
class OSName(str, Enum):
    """Available os names."""

    WINDOWS = "Windows"
    LINUX = "Linux"
    FREEBSD = "FreeBSD"
    ESXI = "VMkernel"
    EFISHELL = "EFIShell"
```


### OSBitness
Structure for bitness of OS
```python
class OSBitness(str, Enum):
    """Available OS bitnesses."""

    OS_32BIT = "32bit"
    OS_64BIT = "64bit"
```


### WindowsFlavour
Structure for supported Windows OS Versions
```python
class WindowsFlavour(Enum):
    """Available Windows System Flavours."""
    WindowsServer2012R2 = "Microsoft Windows Server 2012 R2"
    WindowsServer2016 = "Microsoft Windows Server 2016"     # Windows-10.0.14393
    WindowsServer2019 = "Microsoft Windows Server 2019"     # Windows-10.0.17763
    WindowsServer2022 = "Microsoft Windows Server 2022"     # Windows-10.0.20348
    WindowsServer2022H2 = "Microsoft Windows Server 2022 H2"   # Windows-10.0.22621

```

### CPUBitness
Structure for available CPU bitnesses
```python
class CPUBitness(str, Enum):
    """Available CPU bitnesses."""

    CPU_32BIT = "32bit"
    CPU_64BIT = "64bit"
```

### CPUArchitecture
Structure for available CPU architectures
```python
class CPUArchitecture(str, Enum):
    """Available CPU architectures."""

    X86 = "x86"
    X86_64 = "x86-64"
    ARM = "ARM"
    ARM64 = "ARM64"
```

### SystemInfo
Generic Information about the System Under Test
```python
@dataclass
class SystemInfo:
    """Generic Information about the System Under Test."""

    host_name: str | None = None  # WINDOWS-2019
    os_name: str | None = None  # Microsoft Windows Server 2019 Standard
    os_version: str | None = None  # 10.0.17763 N/A Build 17763
    kernel_version: str | None = None  # 17763
    system_boot_time: str | None = None  # 4/4/2023, 2:40:55 PM
    system_manufacturer: str | None = None  # Intel Corporation
    system_model: str | None = None  # S2600BPB
    system_bitness: OSBitness | None = None  # x64-based PC -> OSBitness.OS_64BIT
    bios_version: str | None = None  # Intel Corporation SE5C620.86B.02.01.0012.070720200218, 7/7/2020
    total_memory: str | None = None  # 130,771 MB
    architecture_info: str | None = None  # x86_64
```


### MACAddress
Structure for representing mac address

For more information on this class please check out netaddr documentation:
[here](http://netaddr.readthedocs.io/en/latest/api.html#netaddr.EUI)

Represents mac address in standard IEEE mac_eui48 format by default, raises exception if input is not MAC 48b format

Usage Examples:

* mac = MACAddress("00-1B-77-49-54-FD")
* int(mac) -> 117965411581
* hex(mac) -> '0x1b774954fd'
* oct(mac) -> '01556722252375'
* mac.bits() -> '00000000-00011011-01110111-01001001-01010100-11111101'
* mac.bin -> '0b1101101110111010010010101010011111101'
* str(MACAddress(mac1)) -> '00:1b:77:49:54:fd'
* MACAddress(mac1) == MACAddress(mac2)
* MACAddress(mac1) > MACAddress(mac2)
* MACAddress(mac1) < MACAddress(mac2)


**Implemented methods**

`get_random_mac() -> MACAddress` : Generate a random MAC address.

`get_random_multicast_mac() -> MACAddress` : Generate multicast MAC starting from '01:00:5e:xx:xx:xx', with the last 3 octets randomize.

`get_random_unicast_mac() -> MACAddress` : Generate unicast MAC starting from 'fa:xx:xx:xx:xx:xx'

`get_random_mac_using_prefix(prefix: str = None) -> MACAddress`  :  Generate a random MAC address from the range prefix:xx:xx:xx - prefix:xx:xx:xx. If prefix is not passed the MAC address generated will be fa:11:11:xx:xx:xx.

`parse_mac(mac: MACAddress) -> str`: Parse mac in special way to get i.e. from `3c:fd:fe:bc:b7:68` -> `{0xffff,0xffff,0xffff}`. The function creates a list from string and chops it to 3x 2 byte, and reverses bytes order for each couple.

### InterfaceType 
Structure for network interface types. 

#### Available types: 
- `InterfaceType.GENERIC` : default
- `InterfaceType.ETH_CONTROLLER` : network controller listed on pci (default for network device without loaded driver)
- `InterfaceType.VIRTUAL_DEVICE` : interface located in path ../devices/virtual/net/ (bridge, macvlan, loopback)
- `InterfaceType.PF` : regular physical interface; located on PCI bus (../devices/pci0000/..) (eth)
- `InterfaceType.VF` : virtual inteface (SRIOV); described as 'Virtual Interface' in lspci detailed info
- `InterfaceType.VPORT` : IPU-specific interface which shares PCI Address with other interfaces (extra VSI Info stored in `VsiInfo`)
- `InterfaceType.VMNIC` : ESXi-specific interface, not used in Linux 
- `InterfceType.VMBUS`  : Hyper-V specific for Linux Guests (https://docs.kernel.org/virt/hyperv/vmbus.html)
- `InterfaceType.MANAGEMENT` : interface having IPv4 Address in range of management network (`from mfd_const.mfd_const import MANAGEMENT_NETWORK`)
- `InterfaceType.VLAN` : virtual device which is assigned to 802.1Q VLAN (extra VLAN details stored in `VlanInterfaceInfo`)
- `InterfaceType.CLUSTER_MANAGEMENT` : cluster management interface type
- `InterfaceType.CLUSTER_STORAGE` : storage / compute interfaces in cluster nodes, marked as `vSMB` in system
- `InterfaceType.BTS` : Linux: BTS shares PCI bus, device ID and index, we will mark it based on name starting with `nac`
- `InterfaceType.BOND` : Linux: Bonding interface, which is a virtual interface that combines multiple physical interfaces into a single logical interface
- `InterfaceType.BOND_SLAVE` : Linux: Bonding interface slave, which is a physical interface that is part of a bonding interface


### VlanInterfaceInfo
Structure for VSI Info

```python
@dataclass
class VlanInterfaceInfo:
    """Structure for vlan interface info."""
    vlan_id: int
    parent: Optional[str] = None
```

### VsiInfo
Structure for VSI Info

```python
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
```

### ClusterInfo
Structure for cluster Info

```python
@dataclass
class ClusterInfo:
    """Structure for cluster info."""

    node: Optional[str] = None
    network: Optional[str] = None
```

### InterfaceInfo
Structure for network interface info

```python
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
```

```python
@dataclass
class LinuxInterfaceInfo(InterfaceInfo):
    """
    Structure for Linux network interface info.

    All possible fields that can be helpful, while creating network interface.
    """

    namespace: Optional[str] = None
    vsi_info: Optional[VsiInfo] = None
```

```python
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
```

### DriverInfo
Structure for information about driver.

```python
@dataclass
class DriverInfo:
    """Structure for information about driver."""

    driver_name: str
    driver_version: str
```

For more information on this class please check out netaddr documentation:
[here](https://netaddr.readthedocs.io/en/latest/api.html#ip-addresses)

Raises exception if the input is not valid IPv4 or IPv6 address.

Usage examples

* ip = IPAddress('192.0.2.1')
* ip.version -> 4
* str(ip) -> '192.0.2.1'
* int(ip) -> 3221225985
* hex(ip) -> '0xc0000201'
* ip.bin -> '0b11000000000000000000001000000001'
* ip.bits() -> '11000000.00000000.00000010.00000001'
* ip.words() -> (192, 0, 2, 1)
* ip.is_multicast()
* ip.is_reserved()
* IPAddress(ip1) == IPAddress(ip2)


### IPNetwork
Structure for representing IPv4 and IPv6 network or subnet

For more information on this class please check out netaddr documentation:
[here](https://netaddr.readthedocs.io/en/latest/api.html#ip-networks-and-subnets)

Usage examples

* ip = IPNetwork('192.0.2.1/0')
* broadcast_ip = IPNetwork('192.0.2.0/24').broadcast
* IPNetwork('192.0.2.0/24').size
* ip = IPNetwork('fe80::dead:beef/64')
* netmask = IPNetwork('192.0.2.1/16').prefixlen


### PCIAddress
Structure  for representing pci address.


Structure contains `domain`, `bus`, `slot` and `func` as `int`'s, but can convert input parameters into `int`, such as `str, double`

Example:

```python
from mfd_typing.pci_address import PCIAddress
pci = PCIAddress('0', 0.0, '0', 0.0)
# PCIAddress(0,0,0,0)
print(pci.domain)
print(pci.bus)
print(pci.slot)
print(pci.func)
```

As an alternative, `string` with short `bdf` or `full lspci` can be provided as `PCIAddress` input parameter into `data` variable.

Example:

```python
from mfd_typing.pci_address import PCIAddress
pci = PCIAddress("0000:00:00.0")
# equivalent of PCIAddress(0,0,0,0)
pci = PCIAddress("00:00.0")
# equivalent of PCIAddress(0,0,0,0) because `domain` default will be se on `0`
```

Usage examples

* PCIAddress(0, 94, 0, 1).sbdf == "00:094:00:01"
* PCIAddress(0, 26, 10, 1).lspci == "0000:1a:0a.1"
* PCI Address from hex to decimal -> PCIAddress(0xFFFF, 0xFF, 0x1F, 0x7).sbdf == "65535:255:31:07"
* PCI Address from decimal to hex -> PCIAddress(0, 26, 10, 1).lspci == "0000:1a:0a.1"
* PCIAddress(0, 0xFF, 0x1F, 0x7).lspci_short == "ff:1f.7"


### PCIDevice
Structure for PCIDevice description:
`VendorID`, `DeviceID`, `SubVendorID`, `SubDeviceID`

Usage:

`PCIDevice(vendor_id: VendorID, device_id: DeviceID, sub_vendor_id: SubVendorID, sub_device_id: SubDeviceID)`
either:
`PCIDevice(data="vendor_id:device_id:sub_vendor_id:sub_device_id")` where `data` are in `string` format separated by colon.
or:
`PCIDevice(data="vendor_id:device_id")` where `data` are in `string` format and default `0000` `sub_vendor_id` and `sub_device_id` are set.

where `ID`s can handle `string` or `hexadecimal` value in constructor
`ID`s are hashable and comparable, the same as `PCIDevice`'s

### dataclass utils
Helper methods for dataclasses' typing:
* `get_field_type` - Get type hint of given field of given model.
* `convert_value_field_to_typehint_type` - Convert value of dataclass field to type expected in typehints for this field.

### utils
Generic API's supported in MFD-Typing

**Implemented methods**

`decimal_to_hex(decimal_value: Union[str, int]) -> str` : Convert decimal value to hexadecimal.

`decimal_to_bin(decimal_value: Union[str, int]) -> str` : Convert decimal value to binary number.

`get_number_based_on_string(input_string: str, range_of_results: int = 100) -> int` : Get calculated number based on provided string from specific range.

`compare_numbers_as_unsigned(number_1: int, number_2: int) -> bool` : Compare numbers as unsigned. This accounts for possible overflow on negative values.

`compare_non_conforming_versions(version_1: str, version_2: str) -> int` : Compare versions that cannot be compared using StrictVersion class.

`convert_port_dc_to_port_hex(port: Union[int, str])` : Convert Port number to comma separated hexadecimal port number.

`convert_ip_dc_to_ip_hex(ip: "IPAddress", pad_ipv6_len=False) -> str` : Convert IP address to comma separated hexadecimal IP address.

`get_windows_version_from_kernel(kernel_version: str) -> WindowsFlavour` : Map Kernel Version to Windows Flavour

`strtobool(param: Union[str, bool]) -> bool` : Convert strings to boolean True or False.
"true", "yes", "1", "y", "t", "on" are cast to True,
"false", "no", "0", "n", "f", "off" are cast to False, case insensitive

`convert_ip_dc_to_hex_value(ip: "IPv4Address | IPv6Address | IPv4Interface | IPv6Interface") -> str:` : Convert the IP value to its HEX value.

`convert_ip_to_brackets_colon_format(ip: "IPAddress") -> str` : Parse an IP address in a special way. The function creates a list from string and chops it to 2x 2 byte or 8x 2 byte,
and reverses bytes order for each couple. For example:
- `1.2.1.1` -> `{0x0201,0x0101}`
- `fe80::3efd:feff:febc:b4c9` -> `{0x80fe,0x0000,0x0000,0x0000,0xfd3e,0xfffe,0xbcfe,0xc9b4}`

`convert_mac_string_to_hex(mac: str) -> str:`: Convert the MAC string value to its HEX value.

`format_mac_string_to_canonical(mac: str) -> str:`: Format any mac format to canonical

`get_sed_inline(act_line: str, new_line: str, filename: "str | Path", line_idx: int | str = 0) -> str - Prepare sed command with all needed parameters.`

`prepare_sed_string(input_str: str, pattern: str) -> str - Prepare `str` to be parsed as a literal string by sed.`

### OSNames for Switches

`SWITCHES_OS_NAME_REGEXES` contains regexes for OS names for switches.
```python
SWITCHES_OS_NAME_REGEXES = {
    OSName.MELLANOX:
        [r"Onyx", r"SX_PPC_M460EX", r"MLNX-OS"]
}
```

## OS supported:
* LNX
* WINDOWS
* ESXI
* FREEBSD
* EFI Shell

## Issue reporting

If you encounter any bugs or have suggestions for improvements, you're welcome to contribute directly or open an issue [here](https://github.com/intel/mfd-typing/issues).
