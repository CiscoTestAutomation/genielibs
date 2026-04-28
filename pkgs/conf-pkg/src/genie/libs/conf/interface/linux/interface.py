'''
    Interface classes for Linux OS.

    Supports basic interface configuration using iproute2 commands:
    - IPv4/IPv6 address assignment
    - Interface enable/disable (link up/down)
    - MTU configuration
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'EthernetInterface',
    'WlanInterface',
    'WwanInterface',
    'VirtualInterface',
    'LoopbackInterface',
    'BridgeInterface',
    'BondInterface',
    'VlanInterface',
    'TunnelInterface',
    'SubInterface',
    'AliasInterface',
    'ParsedInterfaceName',
)

import re
import abc
import logging
import types

from genie.decorator import managedattribute
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder

from genie.libs.conf.base import \
    IPv4Address, IPv4Interface, \
    IPv6Address, IPv6Interface

from genie.libs.conf.interface import (
    Interface as BaseInterface,
    ParsedInterfaceName as BaseParsedInterfaceName,
    PhysicalInterface as BasePhysicalInterface,
    VirtualInterface as BaseVirtualInterface,
    LoopbackInterface as BaseLoopbackInterface,
    EthernetInterface as BaseEthernetInterface,
    SubInterface as BaseSubInterface,
)


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Predictable network interface name tables
# (https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/
#  networking_guide/sec-understanding_the_predictable_network_interface_device_names)
# ---------------------------------------------------------------------------

# 2-char type prefix → human-readable type
_PREDICTABLE_TYPE_MAP = {
    'en': 'ethernet',
    'ib': 'infiniband',
    'sl': 'slip',
    'wl': 'wlan',
    'ww': 'wwan',
}

# Sub-type character → human-readable sub-type
_PREDICTABLE_SUBTYPE_MAP = {
    'b': 'bcma',
    'c': 'ccw',
    'd': 'devicetree',   # DeviceTree / ACPI onboard (end0, end1 …)
    'o': 'onboard',
    'p': 'pci',
    's': 'pcie',
    'x': 'mac',
}


class ParsedInterfaceName(BaseParsedInterfaceName):
    '''Linux interface name parser.

    Decomposes a Linux interface name into structured attributes.  Suffixes are
    stripped right-to-left before the base name is classified:

    1. **IP alias** suffix ``:N`` → ``alias_sep=':', alias='N'``
    2. **Sub-interface** suffix ``.N`` → ``subintf_sep='.', subintf='N'``
    3. **Base name** → classified as *predictable* or *simple/classical*

    ---

    **Simple / classical names** — ``eth0``, ``bond0``, ``lo``, ``wlan0``, …

    +-----------------+------------------------------------------+
    | Attribute       | Value                                    |
    +=================+==========================================+
    | ``type``        | leading alpha stem: ``'eth'``, ``'lo'``  |
    +-----------------+------------------------------------------+
    | ``number``      | trailing digit string: ``'0'``           |
    +-----------------+------------------------------------------+
    | ``type_prefix`` | ``None``                                 |
    +-----------------+------------------------------------------+
    | ``sub_type``    | ``None``                                 |
    +-----------------+------------------------------------------+

    ---

    **Predictable names** [1] — ``eno1``, ``ens34``, ``enp0s3``, ``wlp2s0``, …

    The name begins with a recognised 2-char type prefix:

    +----------------+---------------+
    | Prefix         | ``type``      |
    +================+===============+
    | ``en``         | ``ethernet``  |
    +----------------+---------------+
    | ``wl``         | ``wlan``      |
    +----------------+---------------+
    | ``ww``         | ``wwan``      |
    +----------------+---------------+
    | ``ib``         | ``infiniband``|
    +----------------+---------------+
    | ``sl``         | ``slip``      |
    +----------------+---------------+

    After the optional ``[P<domain>]`` domain prefix, the next character
    selects the ``sub_type`` and the remaining positional attributes:

    +---------+-------------+------------------------------------------------------------------+
    | Char    | sub_type    | Populated attributes / pattern                                   |
    +=========+=============+==================================================================+
    | ``o``   | onboard     | ``number``                                                       |
    |         |             | opt: ``dev_port`` (``d<N>``), ``port_name`` (``n<name>``)        |
    |         |             | Pattern: ``o<index>[d<dev_port>][n<port_name>]``                 |
    +---------+-------------+------------------------------------------------------------------+
    | ``p``   | pci         | ``bus``, ``slot``,                                               |
    |         |             | opt: ``function``, ``dev_id``, ``port``,                         |
    |         |             | ``config``, ``interface_id``                                     |
    |         |             | Pattern: ``[P<domain>]p<bus>s<slot>[f<func>][d<dev_id>]``        |
    |         |             |          ``[u<port>][c<config>][i<interface_id>]``               |
    +---------+-------------+------------------------------------------------------------------+
    | ``s``   | pcie        | ``slot``                                                         |
    |         |             | opt: ``function``, ``dev_port`` (``d<N>``),                      |
    |         |             | ``port_name`` (``n<name>``)                                      |
    |         |             | Pattern: ``s<slot>[f<function>][d<dev_port>][n<port_name>]``     |
    +---------+-------------+------------------------------------------------------------------+
    | ``b``   | bcma        | ``number``                                                       |
    +---------+-------------+------------------------------------------------------------------+
    | ``d``   | devicetree  | ``number`` (DeviceTree / ACPI alias index, e.g. ``end0``)        |
    +---------+-------------+------------------------------------------------------------------+
    | ``x``   | mac         | ``number`` (MAC hex digits)                                      |
    +---------+-------------+------------------------------------------------------------------+
    | ``c``   | ccw         | ``number`` (CCW bus-ID string)                                   |
    +---------+-------------+------------------------------------------------------------------+

    ``type_prefix`` always holds the raw 2-char prefix (``'en'``, ``'wl'``, …).
    ``domain`` is set only when an uppercase ``P<N>`` domain token is present
    (e.g. ``enP1p0s3`` → ``domain=1``).

    ---

    **Sub-interfaces** — dot suffix on any base name

    ``eth0.100``, ``enp0s3.200``, ``bond0.10`` → ``subintf_sep='.'``,
    ``subintf='100'`` (string).  The sub-interface number is available as an
    int via ``Interface.sub_interface_number``.

    ---

    **IP aliases** — colon suffix (legacy ``ifconfig``-style virtual addresses)

    ``eth0:1``, ``ens34:0``, ``eth0.100:1`` → ``alias_sep=':'``,
    ``alias='1'`` (string).  The alias index is available as an int via
    ``AliasInterface.alias_number``.  An alias suffix always takes priority
    over a sub-interface suffix in the factory dispatch, so ``eth0.100:1``
    resolves to an ``AliasInterface`` whose parent is ``eth0.100``.

    ---

    Attribute reference
    ~~~~~~~~~~~~~~~~~~~

    +------------------+--------+----------------------------------------------+
    | Attribute        | Type   | Description                                  |
    +==================+========+==============================================+
    | ``type``         | str    | Human-readable interface type                |
    +------------------+--------+----------------------------------------------+
    | ``type_prefix``  | str    | Raw 2-char predictable prefix or ``None``    |
    +------------------+--------+----------------------------------------------+
    | ``sub_type``     | str    | Predictable sub-type or ``None``             |
    +------------------+--------+----------------------------------------------+
    | ``number``       | str    | Numeric suffix for simple/onboard names      |
    +------------------+--------+----------------------------------------------+
    | ``subintf_sep``  | str    | ``'.'`` when a sub-interface suffix present  |
    +------------------+--------+----------------------------------------------+
    | ``subintf``      | str    | Sub-interface index (digits) or ``None``     |
    +------------------+--------+----------------------------------------------+
    | ``alias_sep``    | str    | ``':'`` when an IP alias suffix is present   |
    +------------------+--------+----------------------------------------------+
    | ``alias``        | str    | Alias index (digits) or ``None``             |
    +------------------+--------+----------------------------------------------+
    | ``domain``       | int    | PCI domain from ``P<N>`` token               |
    +------------------+--------+----------------------------------------------+
    | ``bus``          | int    | PCI bus number                               |
    +------------------+--------+----------------------------------------------+
    | ``slot``         | int    | PCI/PCIe slot number                         |
    +------------------+--------+----------------------------------------------+
    | ``function``     | int    | PCI function number                          |
    +------------------+--------+----------------------------------------------+
    | ``dev_id``       | int    | PCI device ID (``d<N>``)                     |
    +------------------+--------+----------------------------------------------+
    | ``port``         | int    | USB port number (``u<N>``)                   |
    +------------------+--------+----------------------------------------------+
    | ``config``       | int    | USB config (``c<N>``)                        |
    +------------------+--------+----------------------------------------------+
    | ``interface_id`` | int    | USB interface (``i<N>``)                     |
    +------------------+--------+----------------------------------------------+
    | ``dev_port``     | int    | Device port index (``d<N>`` in onboard/slot) |
    +------------------+--------+----------------------------------------------+
    | ``port_name``    | str    | Firmware port name (``n<name>`` in           |
    |                  |        | onboard/slot names)                          |
    +------------------+--------+----------------------------------------------+

    [1] https://www.freedesktop.org/software/systemd/man/systemd.net-naming-scheme.html
        https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/
        networking_guide/sec-understanding_the_predictable_network_interface_device_names
    '''

    def __init__(self, name, device=None, **kwargs):
        if device is None and isinstance(name, ParsedInterfaceName):
            return super().__init__(vars(name))
        assert type(name) is str

        d = dict(
            type=None,
            type_prefix=None,    # raw 2-char predictable prefix, e.g. 'en'
            sub_type=None,       # 'onboard', 'pci', 'pcie', 'bcma', 'ccw', 'mac'
            number=None,         # index for simple/onboard/bcma/mac names
            subintf_sep=None,    # '.' for dot sub-interfaces (eth0.100)
            subintf=None,        # sub-interface index string, e.g. '100' for eth0.100
            alias_sep=None,      # ':' for IP aliases (eth0:1)
            alias=None,          # alias index string, e.g. '1' for eth0:1
            # PCI / PCIe / USB positional attributes
            domain=None,         # from P<domain>
            bus=None,            # from p<bus>
            slot=None,           # from s<slot>  or PCIe hotplug slot
            function=None,       # from f<function>
            dev_id=None,         # from d<dev_id>
            port=None,           # from u<port>  (USB port)
            config=None,         # from c<config>
            interface_id=None,   # from i<interface>
            dev_port=None,       # from d<N> in onboard / pcie slot names
            port_name=None,      # from n<name> in onboard / pcie slot names
        )

        # --- Step 1: strip optional suffixes (alias :N then sub-interface .N) ---
        # Alias colon-suffix is stripped first so that eth0.100:1 decomposes
        # correctly into base=eth0, subintf=100, alias=1.
        name_stripped = name.strip()

        m_alias = re.match(r'^(.+?):([0-9]+)\s*$', name_stripped)
        if m_alias:
            name_stripped = m_alias.group(1)
            d['alias_sep'] = ':'
            d['alias'] = m_alias.group(2)

        # Linux dot sub-interface separator is always followed by only digits.
        m_sub = re.match(r'^(.+?)(?:\.([0-9]+))?\s*$', name_stripped)
        base_name = m_sub.group(1)
        if m_sub.group(2) is not None:
            d['subintf_sep'] = '.'
            d['subintf'] = m_sub.group(2)

        # --- Step 2: try predictable interface name parsing ---
        # Predictable names begin with a known 2-char type prefix.
        m_prefix = re.match(
            r'^(?P<type_prefix>en|ib|sl|wl|ww)(?P<body>\S+)$',
            base_name, re.IGNORECASE
        )

        parsed_predictable = False
        if m_prefix:
            type_prefix = m_prefix.group('type_prefix').lower()
            body = m_prefix.group('body')

            # Optional domain prefix [P<domain>] — uppercase P only; lowercase p
            # is the PCI sub-type character and must not be confused with domain.
            domain = None
            m_domain = re.match(r'^P(\d+)(.+)$', body)
            if m_domain:
                domain = int(m_domain.group(1))
                body = m_domain.group(2)

            # Sub-type character and remainder
            sub_type_char = body[0].lower() if body else ''
            rest = body[1:]  # everything after the sub-type char

            sub_type = _PREDICTABLE_SUBTYPE_MAP.get(sub_type_char)

            if sub_type is not None:
                if sub_type == 'onboard':
                    # o<index>[d<dev_port>][n<port_name>]
                    m = re.match(
                        r'^(\d+)'
                        r'(?:d(\d+))?'
                        r'(?:n([A-Za-z0-9]+))?$',
                        rest
                    )
                    if m:
                        parsed_predictable = True
                        d['number'] = m.group(1)
                        if m.group(2) is not None:
                            d['dev_port'] = int(m.group(2))
                        if m.group(3) is not None:
                            d['port_name'] = m.group(3)

                elif sub_type == 'pci':
                    # p<bus>s<slot>[f<func>][d<dev_id>][u<port>][c<config>][i<iface>]
                    m = re.match(
                        r'^(\d+)s(\d+)'
                        r'(?:f(\d+))?'
                        r'(?:d(\d+))?'
                        r'(?:u(\d+))?'
                        r'(?:c(\d+))?'
                        r'(?:i(\d+))?$',
                        rest
                    )
                    if m:
                        parsed_predictable = True
                        d['bus'] = int(m.group(1))
                        d['slot'] = int(m.group(2))
                        if m.group(3) is not None:
                            d['function'] = int(m.group(3))
                        if m.group(4) is not None:
                            d['dev_id'] = int(m.group(4))
                        if m.group(5) is not None:
                            d['port'] = int(m.group(5))
                        if m.group(6) is not None:
                            d['config'] = int(m.group(6))
                        if m.group(7) is not None:
                            d['interface_id'] = int(m.group(7))

                elif sub_type == 'pcie':
                    # s<slot>[f<function>][d<dev_port>][n<port_name>]
                    m = re.match(
                        r'^(\d+)'
                        r'(?:f(\d+))?'
                        r'(?:d(\d+))?'
                        r'(?:n([A-Za-z0-9]+))?$',
                        rest
                    )
                    if m:
                        parsed_predictable = True
                        d['slot'] = int(m.group(1))
                        if m.group(2) is not None:
                            d['function'] = int(m.group(2))
                        if m.group(3) is not None:
                            d['dev_port'] = int(m.group(3))
                        if m.group(4) is not None:
                            d['port_name'] = m.group(4)

                elif sub_type == 'devicetree':
                    # d<number>  — DeviceTree / ACPI alias index (end0, end1 …)
                    m = re.match(r'^(\d+)$', rest)
                    if m:
                        parsed_predictable = True
                        d['number'] = m.group(1)

                elif sub_type in ('bcma', 'ccw', 'mac'):
                    if rest:  # any non-empty remainder is valid
                        parsed_predictable = True
                        d['number'] = rest

                if parsed_predictable:
                    d['type'] = _PREDICTABLE_TYPE_MAP[type_prefix]
                    d['type_prefix'] = type_prefix
                    d['sub_type'] = sub_type
                    if domain is not None:
                        d['domain'] = domain

        # --- Step 3: simple name parsing (eth0, bond0, lo, wlan0) ---
        if not parsed_predictable:
            m = re.match(
                r'^(?P<type>[A-Za-z][A-Za-z_-]*?)(?P<number>\d+)?$',
                base_name, re.IGNORECASE
            )
            if m and (m.group('type') or m.group('number')):
                d.update({k: v for k, v in m.groupdict().items()
                          if v is not None})
            else:
                d['type'] = base_name

        super().__init__(name=None, **d)

    def reconstruct(self):
        '''Rebuild the interface name string from parsed attributes.'''
        if self.type_prefix is not None:
            # --- predictable name ---
            s = self.type_prefix
            if self.domain is not None:
                s += 'P{}'.format(self.domain)
            sub_type = self.sub_type
            if sub_type == 'onboard':
                s += 'o{}'.format(self.number or '')
                if self.dev_port is not None:
                    s += 'd{}'.format(self.dev_port)
                if self.port_name is not None:
                    s += 'n{}'.format(self.port_name)
            elif sub_type == 'pci':
                s += 'p{}'.format(self.bus)
                s += 's{}'.format(self.slot)
                if self.function is not None:
                    s += 'f{}'.format(self.function)
                if self.dev_id is not None:
                    s += 'd{}'.format(self.dev_id)
                if self.port is not None:
                    s += 'u{}'.format(self.port)
                if self.config is not None:
                    s += 'c{}'.format(self.config)
                if self.interface_id is not None:
                    s += 'i{}'.format(self.interface_id)
            elif sub_type == 'pcie':
                s += 's{}'.format(self.slot)
                if self.function is not None:
                    s += 'f{}'.format(self.function)
                if self.dev_port is not None:
                    s += 'd{}'.format(self.dev_port)
                if self.port_name is not None:
                    s += 'n{}'.format(self.port_name)
            elif sub_type == 'devicetree':
                s += 'd{}'.format(self.number or '')
            elif sub_type == 'bcma':
                s += 'b{}'.format(self.number or '')
            elif sub_type == 'mac':
                s += 'x{}'.format(self.number or '')
            elif sub_type == 'ccw':
                s += 'c{}'.format(self.number or '')
            if self.subintf is not None:
                s += '{}{}'.format(self.subintf_sep or '.', self.subintf)
            if self.alias is not None:
                s += '{}{}'.format(self.alias_sep or ':', self.alias)
            return s
        else:
            # --- simple name ---
            return '{type}{number}{subintf_sep}{subintf}{alias_sep}{alias}'.format(
                type=self.type or '',
                number=self.number if self.number is not None else '',
                subintf_sep=(
                    (self.subintf_sep or '.')
                    if self.subintf is not None else ''
                ),
                subintf=self.subintf if self.subintf is not None else '',
                alias_sep=(
                    (self.alias_sep or ':')
                    if self.alias is not None else ''
                ),
                alias=self.alias if self.alias is not None else '',
            )


class Interface(BaseInterface):
    '''Base Interface class for Linux devices.

    Generates iproute2 (ip) commands for interface configuration.
    '''

    # Resolve parent interface automatically from the dot-subinterface suffix
    # (e.g. eth0.100 -> eth0, enp0s3.100 -> enp0s3).  The base class
    # defaulter only consults the 'parent' YAML attribute; Linux sub-interfaces
    # are always dot-separated so we can derive it from the name.
    parent_interface = managedattribute(
        name='parent_interface',
        read_only=True,
        doc='The parent interface (derived from sub-interface name suffix).')

    @parent_interface.getter
    def parent_interface(self):
        d_parsed = self.parse_interface_name()
        # Alias parent: eth0:1 → eth0, eth0.100:1 → eth0.100
        if d_parsed.alias is not None:
            d_parsed.alias = None
            d_parsed.alias_sep = None
            parent_name = d_parsed.reconstruct()
            return self.device.interfaces.get(parent_name, None)
        # Sub-interface parent: eth0.100 → eth0
        if d_parsed.subintf is not None:
            d_parsed.subintf = None
            d_parsed.subintf_sep = None
            parent_name = d_parsed.reconstruct()
            return self.device.interfaces.get(parent_name, None)
        # Fall back to the YAML 'parent' attribute if present
        parent_name = getattr(self, 'parent', None)
        if parent_name:
            return self.device.interfaces.get(parent_name, None)
        return None

    def __new__(cls, *args, **kwargs):
        factory_cls = cls
        if cls is Interface:
            try:
                name = kwargs['name']
            except KeyError:
                raise TypeError("'name' argument missing")

            d_parsed = ParsedInterfaceName(
                name, kwargs.get('device', None))

            # Alias interfaces (colon-notation: eth0:1, eth0.100:1) take
            # priority — an alias of a sub-interface is still an alias.
            if d_parsed.alias is not None:
                factory_cls = AliasInterface
            # Sub-interfaces (dot-notation: eth0.100, enp0s3.100) next.
            elif d_parsed.subintf is not None:
                factory_cls = SubInterface
            else:
                iface_type = (d_parsed.type or '').lower()
                # Look up by human-readable type first, then type_prefix for
                # predictable names whose factory key is the 2-char prefix
                # (e.g. wlp2s0 → type_prefix='wl' → WlanInterface).
                factory_cls = (
                    cls._name_to_class_map.get(iface_type)
                    or cls._name_to_class_map.get(
                        (d_parsed.type_prefix or '').lower())
                    or EthernetInterface
                )

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        self._build_config_linux(configurations=configurations,
                                 attributes=attributes,
                                 unconfig=unconfig)

        if apply:
            if configurations:
                self.device.execute(str(configurations))
        else:
            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply,
                                 attributes=attributes,
                                 unconfig=True, **kwargs)

    def _build_config_linux(self, configurations, attributes, unconfig):
        '''Build Linux interface configuration using iproute2 commands.'''

        name = self.name

        # --- enabled (ip link set <name> up/down) ---
        enabled = attributes.value('enabled')
        if enabled is not None:
            if unconfig:
                # Unconfig: bring the interface down
                configurations.append_line(
                    'ip link set {name} down'.format(name=name),
                    raw=True)
            elif enabled:
                configurations.append_line(
                    'ip link set {name} up'.format(name=name),
                    raw=True)
            else:
                configurations.append_line(
                    'ip link set {name} down'.format(name=name),
                    raw=True)

        # --- MTU (ip link set <name> mtu <value>) ---
        mtu = attributes.value('mtu')
        if mtu is not None:
            if unconfig:
                # Reset MTU to default (1500)
                configurations.append_line(
                    'ip link set {name} mtu 1500'.format(name=name),
                    raw=True)
            else:
                configurations.append_line(
                    'ip link set {name} mtu {mtu}'.format(
                        name=name, mtu=mtu),
                    raw=True)

        # --- IPv4 address (ip addr add <ip>/<prefix> dev <name>) ---
        ipv4 = attributes.value('ipv4')
        if ipv4 is not None:
            if unconfig:
                configurations.append_line(
                    'ip addr del {ipv4} dev {name}'.format(
                        ipv4=ipv4, name=name),
                    raw=True)
            else:
                configurations.append_line(
                    'ip addr add {ipv4} dev {name}'.format(
                        ipv4=ipv4, name=name),
                    raw=True)

        # --- IPv6 address (ip -6 addr add <ipv6>/<prefix> dev <name>) ---
        ipv6 = attributes.value('ipv6')
        if ipv6 is not None:
            if unconfig:
                configurations.append_line(
                    'ip -6 addr del {ipv6} dev {name}'.format(
                        ipv6=ipv6, name=name),
                    raw=True)
            else:
                configurations.append_line(
                    'ip -6 addr add {ipv6} dev {name}'.format(
                        ipv6=ipv6, name=name),
                    raw=True)

        # --- IPv4Addr objects ---
        for ipv4addr, attributes2 in attributes.sequence_values(
                'ipv4addr', sort=True):
            if unconfig:
                configurations.append_block(ipv4addr.build_unconfig(
                    apply=False, attributes=attributes2))
            else:
                configurations.append_block(ipv4addr.build_config(
                    apply=False, attributes=attributes2))

        # --- IPv6Addr objects ---
        for ipv6addr, attributes2 in attributes.sequence_values(
                'ipv6addr', sort=True):
            if unconfig:
                configurations.append_block(ipv6addr.build_unconfig(
                    apply=False, attributes=attributes2))
            else:
                configurations.append_block(ipv6addr.build_config(
                    apply=False, attributes=attributes2))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhysicalInterface(Interface, BasePhysicalInterface):
    '''Generic physical interface on a Linux device.

    Concrete subclasses (``EthernetInterface``, ``WlanInterface``, …) are
    selected automatically by the factory in ``Interface.__new__``.  Use this
    class directly only when the type is genuinely unknown.
    '''

    _interface_name_types = ()   # no direct name mappings — subclasses own them

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EthernetInterface(PhysicalInterface, BaseEthernetInterface):
    '''Wired Ethernet interface.

    Matches classical names (``eth<N>``) and all predictable names whose
    parsed ``type`` is ``'ethernet'`` (``eno<N>``, ``ens<N>``, ``enp…``,
    ``en…``).
    '''

    _interface_name_types = (
        'eth',       # classical: eth0, eth1 …
        'ethernet',  # predictable: eno1, ens34, enp0s3, enP1p0s3 …
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WlanInterface(PhysicalInterface):
    '''Wireless LAN interface (``wlan<N>``, predictable ``wl…``).'''

    _interface_name_types = (
        'wlan',  # classical: wlan0
        'wl',    # predictable prefix (wlp2s0 → type_prefix='wl', type='wlan')
                 # NOTE: we match on type_prefix here because the factory key
                 # for predictable wl* names is the type_prefix, not 'wlan';
                 # 'wlan' (classical) is already covered above.
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WwanInterface(PhysicalInterface):
    '''Wireless WAN / mobile broadband interface (predictable ``ww…``).'''

    _interface_name_types = (
        'wwan',  # human-readable type for predictable ww* names
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VirtualInterface(Interface, BaseVirtualInterface):
    '''Generic virtual interface — base for all software-only interfaces.

    Concrete subclasses are ``LoopbackInterface``, ``BridgeInterface``,
    ``BondInterface``, ``VlanInterface``, ``TunnelInterface``, and
    ``SubInterface``.
    '''

    _interface_name_types = ()   # no direct name mappings — subclasses own them

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoopbackInterface(VirtualInterface, BaseLoopbackInterface):
    '''Loopback interface (``lo``, ``loopback<N>``).'''

    _interface_name_types = (
        'lo',
        'loopback',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BridgeInterface(VirtualInterface):
    '''Software Ethernet bridge (``br<N>``, ``virbr<N>``, ``docker<N>``).'''

    _interface_name_types = (
        'br',
        'virbr',
        'docker',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BondInterface(VirtualInterface):
    '''Bonding / link-aggregation interface (``bond<N>``).'''

    _interface_name_types = (
        'bond',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VlanInterface(VirtualInterface):
    '''802.1Q VLAN sub-interface or VLAN device (``vlan<N>``).'''

    _interface_name_types = (
        'vlan',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TunnelInterface(VirtualInterface):
    '''Software tunnel interface (``tun<N>``, ``tap<N>``, ``dummy<N>``,
    ``veth<N>``).
    '''

    _interface_name_types = (
        'tun',
        'tap',
        'dummy',
        'veth',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubInterface(VirtualInterface, BaseSubInterface):
    '''Dot-notation sub-interface (e.g. ``eth0.100``, ``enp0s3.100``).

    Created automatically by the factory whenever the parsed name contains
    a ``subintf`` component.
    '''

    _interface_name_types = ()   # matched by factory logic, not a name prefix

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AliasInterface(VirtualInterface):
    '''Linux virtual IP alias (e.g. ``eth0:1``, ``ens34:0``, ``eth0.100:1``).

    IP aliases are the legacy Linux mechanism for assigning multiple addresses
    to a single interface using a colon-separated index suffix.  With iproute2
    they map to ``ip addr add ... dev <parent> label <alias>`` so that
    ``ip addr show`` displays the label alongside the address.

    - ``alias_number`` — the integer alias index (1 for ``eth0:1``).
    - ``parent_interface`` — the base interface (``eth0`` for ``eth0:1``,
      ``eth0.100`` for ``eth0.100:1``).
    - ``enabled`` and ``mtu`` are **not** configurable on an alias; they are
      properties of the parent.  Only IPv4/IPv6 address assignment is
      generated.

    Created automatically by the factory whenever the parsed name contains an
    ``alias`` component.
    '''

    _interface_name_types = ()   # matched by factory logic, not a name prefix

    @property
    def alias_number(self):
        '''The numeric alias index (int), e.g. ``1`` for ``eth0:1``.'''
        d_parsed = self.parse_interface_name()
        if d_parsed.alias is not None:
            return int(d_parsed.alias)
        return None

    def _build_config_linux(self, configurations, attributes, unconfig):
        '''Build iproute2 commands for a virtual IP alias.

        Uses ``ip addr add/del ... dev <parent> label <alias>`` so the kernel
        associates the address with the alias name visible via ``ip addr show``.
        ``enabled`` and ``mtu`` are silently ignored (set on the parent).
        '''
        name = self.name

        # Derive parent device name by stripping the alias suffix.
        d_parent = self.parse_interface_name()
        d_parent.alias = None
        d_parent.alias_sep = None
        parent_name = d_parent.reconstruct()

        # IPv4 address
        ipv4 = attributes.value('ipv4')
        if ipv4 is not None:
            if unconfig:
                configurations.append_line(
                    'ip addr del {ipv4} dev {parent} label {name}'.format(
                        ipv4=ipv4, parent=parent_name, name=name),
                    raw=True)
            else:
                configurations.append_line(
                    'ip addr add {ipv4} dev {parent} label {name}'.format(
                        ipv4=ipv4, parent=parent_name, name=name),
                    raw=True)

        # IPv6 address
        ipv6 = attributes.value('ipv6')
        if ipv6 is not None:
            if unconfig:
                configurations.append_line(
                    'ip -6 addr del {ipv6} dev {parent} label {name}'.format(
                        ipv6=ipv6, parent=parent_name, name=name),
                    raw=True)
            else:
                configurations.append_line(
                    'ip -6 addr add {ipv6} dev {parent} label {name}'.format(
                        ipv6=ipv6, parent=parent_name, name=name),
                    raw=True)

        # IPv4Addr / IPv6Addr managed objects
        for ipv4addr, attributes2 in attributes.sequence_values(
                'ipv4addr', sort=True):
            if unconfig:
                configurations.append_block(ipv4addr.build_unconfig(
                    apply=False, attributes=attributes2))
            else:
                configurations.append_block(ipv4addr.build_config(
                    apply=False, attributes=attributes2))

        for ipv6addr, attributes2 in attributes.sequence_values(
                'ipv6addr', sort=True):
            if unconfig:
                configurations.append_block(ipv6addr.build_unconfig(
                    apply=False, attributes=attributes2))
            else:
                configurations.append_block(ipv6addr.build_config(
                    apply=False, attributes=attributes2))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ---------------------------------------------------------------------------
# Factory name→class map
# ---------------------------------------------------------------------------
# Includes all concrete subclasses that declare _interface_name_types.
# SubInterface is handled separately in Interface.__new__ (subintf check).

_CONCRETE_CLASSES = (
    EthernetInterface,
    WlanInterface,
    WwanInterface,
    LoopbackInterface,
    BridgeInterface,
    BondInterface,
    VlanInterface,
    TunnelInterface,
)

Interface._name_to_class_map = {
    prefix: cls
    for cls in _CONCRETE_CLASSES
    for prefix in cls._interface_name_types
}
