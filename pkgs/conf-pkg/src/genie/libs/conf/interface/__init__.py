'''
    Common base Interface classes for all OSes.
'''

import importlib
import warnings
import logging
import abc
import types
import re
from enum import Enum

from genie.utils.cisco_collections import typedset
from genie.decorator import managedattribute, mixedmethod
from genie.conf.base import Base, Interface as Intf, ConfigurableBase, Device
from genie.conf.base.interface import BaseInterface,\
                                PhysicalInterface as BasePhysicalInterface,\
                                VirtualInterface as BaseVirtualInterface,\
                                LoopbackInterface as BaseLoopbackInterface,\
                                PseudoInterface as BasePseudoInterface

from .ipv4addr import IPv4Addr
from .ipv6addr import IPv6Addr
from genie.libs import conf
from genie.libs.conf.base import IPv4Address, IPv6Address, IPv4Interface, IPv6Interface, MAC
from genie.libs.conf.vrf import Vrf

from pyats.topology.schema import ipv6_or_list_of_ipv6


log = logging.getLogger(__name__)


class Option(Enum):

    def __str__(self):
        return str(self.value)


class Layer(Option):

    # Creating static variable name for layer 2 and layer 3.
    # This way it will remove the confusion of which name to use
    L3 = 'L3'
    L2 = 'L2'


class L2_type(Option):
    # Create the same for Trunk and Access
    # This way it will remove the confusion of which name to use
    TRUNK = 'trunk'
    ACCESS = 'access'
    DOT1Q_TUNNEL = 'dot1q-tunnel'
    FEX_FABRIC = 'fex-fabric'
    PRIVATE_VLAN = 'private-vlan'

class Medium(Option):
    # Create the same for p2p or broadcast
    # This way it will remove the confusion of which name to use
    p2p = 'p2p'
    broadcast = 'broadcast'

def _get_descendent_subclass(cls, subcls):
    '''Find the descendent class of cls that is a subclass of subcls.'''
    found_subclasses = set()
    subclasses_walked = set()
    subclasses_to_walk = [cls]
    while subclasses_to_walk:
        cls = subclasses_to_walk.pop(0)
        if cls in subclasses_walked:
            continue
        else:
            subclasses_walked.add(cls)
        if issubclass(cls, subcls):
            found_subclasses.add(cls)
        else:
            subclasses_to_walk.extend(cls.__subclasses__())
    if not found_subclasses:
        raise TypeError('No %r specific subclass of %r found.' % (
            subcls.__qualname__, cls.__qualname__))
    if len(found_subclasses) > 1:
        raise TypeError('Too many %r specific subclass of %r found: %r' % (
            subcls.__qualname__, cls.__qualname__, found_subclasses))
    cls = found_subclasses.pop()
    return cls




class UnsupportedInterfaceOsWarning(UserWarning):
    pass


class UnknownInterfaceName(UserWarning):
    pass


class ParsedInterfaceName(types.SimpleNamespace):

    def __init__(self, name, device=None):
        if device is None and isinstance(name, ParsedInterfaceName):
            # copy constructor
            return super().__init__(vars(name))
        assert type(name) is str

        d = dict(
            # main parts
            type=None,
            number=None,
            subintf_sep=None,
            subintf=None,
            # sub-parts
            net_module=None,
            module=None,
            rack=None,
            slot=None,
            instance=None,
            port=None,
            subport=None,
            cpu=None,
            rsip=None,
        )

        m = re.match(r'''
            ^
            # ignore leading spaces
            \s*
            # not an empty string
            (?=\S)
            # optional <type>
            (?P<type>
                [JTE][13]|                                      # J1, T1, E1, ...
                (?:ODU|d|OTU|O)(?:[01234]|[12][EF]|3E[12])|     # ODU2, OTU3E2, ...
                (?:GCC|g)[01]|                                  # GCC0, GCC1
                [A-Za-z]+(?:-[A-Za-z]+)*                        # generic: POS, tunnel-te, odu...
            )?
            # optional spaces
            \s*
            # rest is optional too
            (?:
                # <number>
                (?P<number>\d+(?:[/_](?:RP|RSP|CPU)?\d+)*)
                # optional <subintf>
                (?:(?P<subintf_sep>[.:])(?P<subintf>\d+))?
            )?
            # ignore trailing spaces
            \s*
            $
        ''', name, re.VERBOSE | re.IGNORECASE)
        if not m:
            raise ValueError('Unrecognized interface name %r' % (name,))
        d.update(m.groupdict())

        if d['number']:
            m = re.match(r'^(?P<cpu>(?P<rack>\d+)[/_](?P<slot>(?:RP|RSP)?\d+)[/_](?:CPU\d+|\*))$', d['number'])
            if m:
                # IOS-XR
                d.update(m.groupdict())

            else:
                # 0/RP0/CPU0/0
                # 0/RSP0/CPU0/0
                # 0/0/0/0
                m = re.match(r'^(?P<rsip>(?P<rack>\d+)[/_](?P<slot>(?:RP|RSP)?\d+)[/_](?P<instance>\d+)[/_](?P<port>\d+))(?:[/_](?P<subport>\d+))?', d['number'])
                if m:
                    # IOS-XR
                    d.update(m.groupdict())
                    d['cpu'] = '{rack}/{slot}/CPU0'.format_map(d)

                else:
                    m = re.match(r'^(?P<module>(?:(?P<net_module>\d+)[/_])?\d+)[/_](?P<port>\d+)$', d['number'])
                    if m:
                        # IOS/NX-OS
                        d.update(m.groupdict())

        super().__init__(**d)

    def reconstruct(self):
        return '{type}{number}{subintf_sep}{subintf}'.format(
            type=self.type or '',
            number=self.number if self.number is not None else '',
            subintf_sep=(self.subintf_sep or '.') if self.subintf is not None else '',
            subintf=self.subintf if self.subintf is not None else '',
        )


class Interface(BaseInterface):

    ipv4addr = managedattribute(
        name='ipv4addr',
        finit=typedset(managedattribute.test_isinstance(IPv4Addr)).copy,
        type=typedset(managedattribute.test_isinstance(IPv4Addr))._from_iterable,
        doc='A `set` of IPv4Addr associated objects')

    def add_ipv4addr(self, ipv4addr=None, ipv4=None, prefix_length=None):
        if not ipv4addr and not (ipv4 and prefix_length):
            raise KeyError('At least ipv4addr or <ipv4(str), prefix_length(str)> is defined')
        if ipv4addr:
            self.ipv4addr.add(ipv4addr)
        else:
            ipv4_obj = IPv4Addr(self.device)
            ipv4_obj.ipv4 = ipv4
            ipv4_obj.prefix_length = prefix_length
            self.ipv4addr.add(ipv4_obj)

    def remove_ipv4addr(self, ipv4addr):
        ipv4addr._device = None
        try:
            self.ipv4addr.remove(ipv4addr)
        except:
            pass

    ipv6addr = managedattribute(
        name='ipv6addr',
        finit=typedset(managedattribute.test_isinstance(IPv6Addr)).copy,
        type=typedset(managedattribute.test_isinstance(IPv6Addr))._from_iterable,
        doc='A `set` of IPv6Addr associated objects')

    def add_ipv6addr(self, ipv6addr):
        self.ipv6addr.add(ipv6addr)

    def remove_ipv6addr(self, ipv6addr):
        ipv6addr._device = None
        try:
            self.ipv6addr.remove(ipv6addr)
        except:
            pass

    ipv4 = managedattribute(
        name='ipv4',
        default=None,
        type=(None, IPv4Interface))

    ipv6 = managedattribute(
        name='ipv6',
        default=None,
        type=(None, ipv6_or_list_of_ipv6))

    vrf = managedattribute(
        name='vrf',
        default=None,
        type=(None,
              managedattribute.test_isinstance(Vrf)))

    # enabled
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable the selected interfac')

    # link_up_down_trap_enable
    link_up_down_trap_enable = managedattribute(
        name='link_up_down_trap_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Allow SNMP LINKUP and LINKDOWN traps')

    # link-status
    link_status = managedattribute(
        name='link_status',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='UPDOWN and CHANGE messages')

    # encapsulation
    class Encapsulation(Enum):
        dot1q = 'dot1q'
        isl = 'isl'
        priority_tagged = 'priority-tagged'

    encapsulation = managedattribute(
        name='encapsulation',
        default=None,
        type=(None, Encapsulation),
        doc='Set encapsulation type for an interface')

    # first_dot1q
    first_dot1q = managedattribute(
        name='first_dot1q',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='IEEE 802.1Q VLAN ID')

    # sedond_dot1q
    sedond_dot1q = managedattribute(
        name='second_dot1q',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Second (inner) VLAN IDs')

    # native_vlan_dot1q
    native_vlan_dot1q = managedattribute(
        name='native_vlan_dot1q',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Make this as native vlan')

    # dhcp
    dhcp = managedattribute(
        name='dhcp',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='IP Address negotiated via DHCP')

    # dhcp_client_id
    dhcp_client_id = managedattribute(
        name='dhcp_client_id',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Specify client-id to use')

    # dhcp_hostname
    dhcp_hostname = managedattribute(
        name='dhcp_hostname',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Specify value for hostname option')

    # unnumbered_intf_ref
    unnumbered_intf_ref = managedattribute(
        name='unnumbered_intf_ref',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Enable IP processing without an explicit address')

    # ipv6_unnumbered_intf_ref
    ipv6_unnumbered_intf_ref = managedattribute(
        name='ipv6_unnumbered_intf_ref',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Preferred interface for source address selection')

    # ipv6_enabled
    ipv6_enabled = managedattribute(
        name='ipv6_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable IPv6 on interface')

    # ipv6_autoconf
    ipv6_autoconf = managedattribute(
        name='ipv6_autoconf',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Obtain address using autoconfiguration')

    # ipv6_autoconf_default
    ipv6_autoconf_default = managedattribute(
        name='ipv6_autoconf_default',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Insert default route')

    # medium
    medium = managedattribute(
        name='medium',
        default=None,
        type=(None, Medium),
        doc='Configure Interface medium mode')

    # delay
    delay = managedattribute(
        name='delay',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Specify interface throughput delay')

    # load_interval
    load_interval = managedattribute(
        name='load_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Specify interval for load calculation for an interface')

    # load_interval_counter
    load_interval_counter = managedattribute(
        name='load_interval_counter',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Specify counter for the load interval')

    # flowcontrol_receive
    flowcontrol_receive = managedattribute(
        name='flowcontrol_receive',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Receive pause frames')

    # flowcontrol_send
    flowcontrol_send = managedattribute(
        name='flowcontrol_send',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Send pause frames')

    # bandwidth
    bandwidth = managedattribute(
        name='bandwidth',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Set bandwidth informational parameter')

    # cdp
    cdp = managedattribute(
        name='cdp',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure CDP interface parameters')

    # description
    description = managedattribute(
        name='description',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Enter description')

    # mtu
    mtu = managedattribute(
        name='mtu',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Configure mtu for the port')

    # shutdown
    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable/disable an interface')

    switchport_enable = managedattribute(
        name='switchport_enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure switchport')

    class SWITCHPORTMODE(Enum):
        access = 'access'
        dot1q_tunnel = 'dot1q-tunnel'
        fex_fabric = 'fex-fabric'
        private_vlan = 'private-vlan'
        trunk = 'trunk'

    switchport_mode = managedattribute(
        name='switchport_mode',
        default=None,
        type=(None, SWITCHPORTMODE),
        doc= 'Interface switchport mode')

    evpn_multisite_fabric_tracking = managedattribute(
        name='evpn_multisite_fabric_tracking',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure evpn multisites fabric links')

    evpn_multisite_dci_tracking = managedattribute(
        name='evpn_multisite_dci_tracking',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure evpn multisites dci links')

    fabric_forwarding_mode = managedattribute(
        name='fabric_forwarding_mode',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Configure fabric forwarding mode')

    ip_forward = managedattribute(
        name='ip_forward',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure ip forward')

    ipv6_forward = managedattribute(
        name='ipv6_forward',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure ipv6 forward')


    @abc.abstractmethod
    def build_config(self, *args, **kwargs):
        '''Derived OS-specific classes must provide build_config and
        build_unconfig methods.

        Example:

            Scenario #1: OS-specific interface module with inline configuration
            support::

                # <os>/interface.py
                class Interface(genie.libs.conf.interface.Interface):
                    def build_config(self, ...):
                        ...
                        return configurations

            Scenario #2: OS-specific interface module with context-specific
            configuration modules::

                # <os>/interface.py
                class Interface(genie.libs.conf.interface.Interface):
                    @abstract.lookup('context')
                    def build_config(self, ...):
                        \'\'\'Context-specific interface module provides configuration support.\'\'\'
                        raise NotImplementedError

                # <os>/<context>/interface.py
                class Interface(abstract.AbstractImplementationBase):
                    def build_config(self, ...):
                        ...
                        return configurations

        '''
        raise NotImplementedError

    @abc.abstractmethod
    def build_unconfig(self, *args, **kwargs):
        '''Derived OS-specific classes must provide build_config and
        build_unconfig methods.

        See build_config documentation.
        '''

    @classmethod
    def _build_name_to_class_map(cls):
        cls._name_to_class_map = {}
        for subcls in cls.__subclasses__():
            subcls._build_name_to_class_map()
            cls._name_to_class_map.update(subcls._name_to_class_map)
        for k in cls.__dict__.get('_interface_name_types', ()):
            cls._name_to_class_map[k] = cls

    def generate_sub_interface(self, range=None, **kwargs):
        name = SubInterface._generate_unused_sub_interface_name(
            parent_interface=self,
            range=range)
        return Interface(device=self.device, name=name, **kwargs)

    @classmethod
    def _get_os_specific_Interface_class(cls, os):
        assert type(os) is str
        if False:
            # XXXJST TODO The abstract module needs to be enhanced.
            # Use it's API to perform a fast(cached) os-specific only lookup
            # without instantiating a Lookup instance everytime and be able to
            # work on classes / class methods.
            from genie.abstract import Lookup
            lib = Lookup(os)
            osInterface = lib.conf.interface.Interface
            if osInterface is Interface:
                raise ImportError(
                    'No Interface class found specific to OS {os!r}' \
                    .format(os=os))

        else:
            mod = 'genie.libs.conf.interface.{os}'.\
                format(os=os)
            OsInterfaceModule = importlib.import_module(mod)
            osInterface = OsInterfaceModule.Interface
        return osInterface

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if factory_cls is Interface:
            # need to load the correct interface for the right os.
            if 'device' in kwargs:
                device = kwargs['device']
                if not device.os and 'os' in kwargs['device'].__dict__:
                    device.os = kwargs['device'].__dict__['os']
                if device.os is None:
                    log.debug("Cannot convert interfaces for "
                              "device '{dev}' as mandatory field "
                              "'os' was not given in the "
                              "yaml file".format(dev=device.name))
                    device.os = 'generic'

                try:
                    factory_cls = cls._get_os_specific_Interface_class(device.os)
                except (ImportError, AttributeError):
                    # it does not exist, then just use the default one,
                    # but configuration is not possible
                    pass

            elif not cls.device:
                raise TypeError('\'device\' argument missing')

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    def __init__(self, *args, **kwargs):
        '''Base initialization for all Interface subclasses.

        This is not an abstract class since it may be used to instantiate
        generic interfaces for unsupported devices.

        All direct subclasses of Interface are abstract classes.
        '''

        super().__init__(*args, **kwargs)

        if 'ipv4' not in kwargs:
            if self.ipv4:
                self.testbed.ipv4_cache.reserve(self.ipv4)
        if 'ipv6' not in kwargs:
            if self.ipv6:
                self.testbed.ipv6_cache.reserve(self.ipv6)

    parent_interface = managedattribute(
        name='parent_interface',
        read_only=True,
        doc='''The parent interface. Only meaningful for a few Interface subclasses.''')

    @parent_interface.defaulter
    def parent_interface(self):
        # If the 'parent' attribute is set in the pyATS YAML file, look it up
        parent_interface_name = getattr(self, 'parent', None)
        if parent_interface_name:
            return self.device.interfaces.get(parent_interface_name, None)
        return None

    parent_controller_type = managedattribute(
        name='parent_controller_type',
        default=None,
        read_only=True,
        doc='''The associated controller type. Only meaningful for a few Interface subclasses.''')

    @mixedmethod
    def parse_interface_name(inst, cls, *args, **kwargs):
        if inst:
            if args or kwargs:
                raise TypeError('Unexpected arguments: %r %r' % (args, kwargs))
            return ParsedInterfaceName(
                name=inst.name,
                device=inst.device)
        else:
            return ParsedInterfaceName(*args, **kwargs)

    @property
    def interface_type(self):
        '''The type part of the interface name (str).

        Examples:
            GigabitEthernet0/0/0/0 -> 'GigabitEthernet'
            GigabitEthernet0/0/0/0.2 -> 'GigabitEthernet'
            Bundle-Ether1.2 -> 'Bundle-Ether'
            tunnel-te1 -> 'tunnel-te'
            GCC0 -> 'GCC0'
        '''

        d_parsed = self.parse_interface_name()
        return d_parsed.type

    @property
    def interface_number(self):
        '''The number part of the interface name (int).

        Only valid for virtual interfaces constructed as "<type><number>"

        Examples:
            GigabitEthernet0/0/0/0 -> None
            GigabitEthernet0/0/0/0.2 -> None
            Bundle-Ether1.2 -> None
            tunnel-te1 -> 1
            GCC0 -> None
        '''

        d_parsed = self.parse_interface_name()
        if d_parsed.subintf:
            return None
        try:
            # Return only simple integers
            return int(d_parsed.number)
        except (TypeError, ValueError):
            # None or not a simple integer, it is a location
            return None

    @property
    def sub_interface_number(self):
        '''The sub-interface number part of the interface name (int).
        '''
        d_parsed = self.parse_interface_name()
        if d_parsed.subintf_sep == '.':
            return int(d_parsed.subintf)
        return None

    @property
    def interface_location(self):
        '''The location part of the interface name (str).

        Examples:
            GigabitEthernet0/0/0/0 -> '0/0/0/0'
            GigabitEthernet0/0/0/0.2 -> '0/0/0/0'
            Bundle-Ether1.2 -> None
            tunnel-te1 -> None
            GCC0 -> None
        '''

        # The Parent interface may know more about the location.
        parent_interface = self.parent_interface
        if parent_interface is not None:
            return parent_interface.interface_location

        d_parsed = self.parse_interface_name()
        try:
            # If it is a simple integer then it is not a location
            int(d_parsed.number)
            return None
        except (TypeError, ValueError):
            # None or not a simple integer, it is a location
            return d_parsed.number

    @mixedmethod
    def clean_interface_name(self, cls, interface_name=None):
        if interface_name is None:
            interface_name = self.name
        name_to_class_map = getattr(cls, '_name_to_class_map', {})
        d_parsed = cls.parse_interface_name(interface_name)
        # check for exact match
        if d_parsed.type in name_to_class_map:
            return d_parsed.reconstruct()
        # Apply generic short->long mappings
        try:
            d_parsed.type = {
                'g0': 'GCC0',
                'g1': 'GCC1',
                'dt': 'Odu-Group-Te',  # what about Odu-Group-Mp?
                # Special case for at that matches both ATM and Auto-Template
                'at': 'ATM',
                # Special case for gi that matches both GigabitEthernet and
                'gi': 'GigabitEthernet',
                # Special case for TenGigECtrlr... both TeEC and EC forms seen on XR
                'ec': 'TenGigECtrlr',
                'teec': 'TenGigECtrlr',
                'il': 'InterflexLeft',
                'ir': 'InterflexRight',
                # TODO move to nxos
                # Special case for pw (NXOS pseudowire) that matches several
                'pw': 'pseudowire',
                # Special case for se that matches both Serial and Service*
                # names
                'se': 'Serial',
                'sa': 'ServiceApp',
                'si': 'ServiceInfra',
                # TODO
                #'tu' {
                #    if { $name eq "Tu" } {
                #        set name_lower "tunnel"
                #    } else {
                #        switch -exact -- $caas_os {
                #            "IOS" -
                #            "IOSXE" -
                #            "NXOS" {
                #                set name_lower "tunnel"
                #            }
                #            default {
                #                set name_lower "tunnel-uti"
                #            }
                #        }
                #    }
                #}
                # 'vl' {
                #     # Special case for vl/Vl/VL that matches vlan on ACSW (but
                #     # doesn't support short names), Vlan on IOS and VASILeft
                #     # (hardcoded short name)
                #     if { $name eq "VL" } {
                #         set name_lower "vasileft"
                #     } else {
                #         set name_lower "vlan"
                #     }
                # }
                'vl': 'vlan',
                'vr': 'VASIRight',
                # Special case for lo that matches both Loopback and
                # LongReachEthernet on Nexus (but doesn't support short names)
                'lo': 'Loopback',
            }[d_parsed.type.lower()]
        except KeyError:
            for once in [1]:
                m = re.match(r'^o([01234](?:[EF][12]?)?)$', d_parsed.type, re.IGNORECASE)
                if m:
                    d_parsed.type = 'OTU' + m.group(1).upper()
                    break
                m = re.match(r'^d([01234](?:[EF][12]?)?)$', d_parsed.type, re.IGNORECASE)
                if m:
                    d_parsed.type = 'ODU' + m.group(1).upper()
                    break
            # There are still disambiguation issues for:
            #   Port-channel
            #   Service-Engine
            #   ServiceApp
            #   ServiceInfra
            #   tunnel-ipsec
            #   Virtual-Template
            #   Virtual-TokenRing
            #   MgmtIMA
            #   MgmtMultilink
        # re-check for exact match
        if d_parsed.type in name_to_class_map:
            return d_parsed.reconstruct()
        matches = []
        # check for different capitalization
        pat = d_parsed.type.lower()
        matches += [name for name in name_to_class_map
                    if name.lower() == pat]
        if not matches:
            # check for start of name
            re_pat = r'^' + re.escape(d_parsed.type) + r'[^-]+$'
            matches += [name for name in name_to_class_map
                        if re.match(re_pat, name, re.IGNORECASE)]
            # check for 2 letter abreviation of composite interface name
            if len(d_parsed.type) == 2:
                re_pat = r'^{}.*-{}.*$'.format(re.escape(d_parsed.type[0]), re.escape(d_parsed.type[1]))
                matches += [name for name in name_to_class_map
                            if re.match(re_pat, name, re.IGNORECASE)]
        if len(matches) == 0:
            warnings.warn(
                'Unknown interface type/name {!r}'.format(
                    d_parsed.reconstruct()),
                UnknownInterfaceName)
            pass
        elif len(matches) == 1:
            d_parsed.type = matches[0]
        else:
            raise ValueError('Ambiguous interface type/name {!r} matches: {}'.format(
                d_parsed.reconstruct(),
                ', '.join(matches)))
        return d_parsed.reconstruct()

    @mixedmethod
    def short_interface_name(self, cls, interface_name=None):
        if interface_name is None:
            interface_name = self.name
        interface_name = (self or cls).clean_interface_name(interface_name)
        d_parsed = cls.parse_interface_name(interface_name)
        # When a dash is present, take the first letter of each word.
        # Otherwise, take the first 2 letters
        m = re.match('^([a-z])[a-z]*-([a-z])[a-z]*$', d_parsed.type, re.IGNORECASE) \
            or re.match('^([a-z])([a-z])[a-z]*$', d_parsed.type, re.IGNORECASE)
        if m:
            d_parsed.type = m.group(1) + m.group(2)
            return d_parsed.reconstruct()
        return d_parsed.reconstruct()

    @property
    def sub_interfaces(self):
        return {
            interface
            for interface in self.device.interfaces
            if isinstance(interface, SubInterface) \
            and interface.parent_interface is self}


class Controller(Interface):
    # XXXJST TODO Perhaps Interface should not be used as a base class

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OpticsController(Controller):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhysicalInterface(Interface,
                        BasePhysicalInterface):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VirtualInterface(Interface,
                       BaseVirtualInterface):
    '''Base class for all sorts of virtual interfaces.

    Example:
        lo_intf = LoopbackInterface.generate_interface(device=dev)
    '''
    _interface_name_number_range = range(0, 2147483647 + 1)

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def generate_interface(cls, device, range=None, **kwargs):
        name = cls._generate_unused_interface_name(
            device=device, range=range)
        return Interface(device=device, name=name, **kwargs)

    @classmethod
    def _generate_unused_interface_name(cls, device, range=None):
        assert isinstance(device, Device)
        # Find the os-specific version of this class
        cls = _get_descendent_subclass(
            cls._get_os_specific_Interface_class(device.os),
            cls)

        # Determine the interface name type
        interface_name_types = set(cls.__dict__.get('_interface_name_types', ()))
        if not interface_name_types:
            raise TypeError('No interface name types supported by %r' % (
                cls.__qualname__))
        if len(interface_name_types) > 2:
            raise TypeError('Too many interface name types supported by %r: %r' % (
                cls.__qualname__, set(interface_name_types)))
        interface_name_type = interface_name_types.pop()

        if range is None:
            range = cls._interface_name_number_range
        if type(range) is int:
            range = [range]
        for n in range:
            interface_name = '{}{}'.format(
                interface_name_type, n)
            if interface_name not in device.interfaces:
                break
        else:
            raise TypeError('No more %r interface numbers available on %r' % (
                interface_name_type, device))
        return interface_name


class PseudoInterface(VirtualInterface,
                      BasePseudoInterface):
    pass


class EmulatedInterface(Interface):

    @classmethod
    def _get_os_specific_EmulatedInterface_class(cls, os):
        assert type(os) is str
        mod = 'genie.libs.conf.interface.{os}'.\
            format(os=os)
        OsInterfaceModule = importlib.import_module(mod)
        return OsInterfaceModule.EmulatedInterface

    @property
    def tgen_interface(self):
        return self.device.tgen_interface

    @property
    def tgen_device(self):
        return self.device.tgen_device

    def build_config(self, *args, **kwargs):
        return ''

    def build_unconfig(self, *args, **kwargs):
        return ''

class LagInterface(VirtualInterface):

    enabled_lacp = managedattribute(
        name='enabled_lacp',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc= 'enabled_lacp')

    lag_lacp_system_priority = managedattribute(
        name='lag_lacp_system_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc= 'lag_lacp_system_priority')

    lag_lacp_max_bundle = managedattribute(
        name='lag_lacp_max_bundle',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc= 'lag_lacp_max_bundle')

    lag_lacp_min_bundle = managedattribute(
        name='lag_lacp_min_bundle',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc= 'lag_lacp_min_bundle')

    lag_bfd_v4_destination = managedattribute(
        name='lag_bfd_v4_destination',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc= 'lag_bfd_v4_destination')

    lag_bfd_v4_fast_detect = managedattribute(
        name='lag_bfd_v4_fast_detect',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc= 'lag_bfd_v4_fast_detect')

    lag_bfd_v4_min_interval = managedattribute(
        name='lag_bfd_v4_min_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc= 'lag_bfd_v4_min_interval')

    lag_bfd_v6_destination = managedattribute(
        name='lag_bfd_v6_destination',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc= 'lag_bfd_v6_destination')

    lag_bfd_v6_fast_detect = managedattribute(
        name='lag_bfd_v6_fast_detect',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc= 'lag_bfd_v6_fast_detect')

    lag_bfd_v6_min_interval = managedattribute(
        name='lag_bfd_v6_min_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc= 'lag_bfd_v6_min_interval')

class LoopbackInterface(VirtualInterface,
                        BaseLoopbackInterface):
    pass


class ManagementInterface(PhysicalInterface):
    pass


class EthernetInterface(PhysicalInterface):

    # mac_address
    mac_address = managedattribute(
        name='mac_address',
        default=None,
        type=(None, MAC))

    burnin_mac_address = managedattribute(
        name='burnin_mac_address',
        default=None,
        type=(None, MAC))

    @property
    def effective_mac_address(self):
        return self.mac_address or self.burnin_mac_address

    auto_negotiation = managedattribute(
        name='auto_negotiation',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    speed = managedattribute(
        name='speed',
        default=None,
        type=(None, int, managedattribute.test_istype(str)))

    duplex = managedattribute(
        name='duplex',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    eth_encap_type1 = managedattribute(
        name='eth_encap_type1',
        type=(None, managedattribute.test_istype(str)))

    @eth_encap_type1.defaulter
    def eth_encap_type1(self):
        if self.eth_encap_val1 is not None:
            return "dot1q"
        return None

    eth_encap_val1 = managedattribute(
        name='eth_encap_val1',
        default=None,
        type=(None,
              managedattribute.test_istype((int, range))))

    eth_encap_type2 = managedattribute(
        name='eth_encap_type2',
        type=(None, managedattribute.test_istype(str)))

    @eth_encap_type2.defaulter
    def eth_encap_type2(self):
        if self.eth_encap_val2 is not None:
            if self.eth_encap_type1 == 'dot1q':
                return 'second-dot1q'
            if self.eth_encap_type1 == 'dot1ad':
                return 'dot1q'
        return None

    eth_encap_val2 = managedattribute(
        name='eth_encap_val2',
        default=None,
        type=(None, managedattribute.test_istype((int, range))))

    eth_dot1q_type = managedattribute(
        name='eth_dot1q_type',
        type=(None, managedattribute.test_istype(str)))

    @eth_dot1q_type.defaulter
    def eth_dot1q_type(self):
        if self.eth_dot1q_value is not None:
            return "native"
        return None

    eth_dot1q_value = managedattribute(
        name='eth_dot1q_value',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # port_speed
    class PORTSPEED(Enum):
        sp1 = '10'
        sp2 = '100'
        sp3 = '1000'
        sp4 = '10000'
        sp5 = '100000'
        sp6 = '40000'
        auto = 'auto'

    port_speed = managedattribute(
        name='port_speed',
        default=None,
        type=(None, PORTSPEED),
        doc= 'port_speed')

    # access_vlan
    access_vlan = managedattribute(
        name='access_vlan',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Set access mode characteristics of the interface')

    # trunk_vlan
    trunk_vlan = managedattribute(
        name='trunk_vlans',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Configure trunking parameters on an interface')

    # trunk_add_vlans
    trunk_add_vlans = managedattribute(
        name='trunk_add_vlans',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Add VLANs to the current list')

    # trunk_remove_vlans
    trunk_remove_vlans = managedattribute(
        name='trunk_remove_vlans',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Remove VLANs from the current list')

    # native_vlan
    native_vlan = managedattribute(
        name='native_vlan',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Set trunking native characteristics when interface is in trunking mode')

    # dot1_access_vlan
    dot1q_access_vlan = managedattribute(
        name='dot1q_access_vlan',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Set access mode characteristics of the dot1q tunnel interface')

    # auto_negotiate
    auto_negotiate = managedattribute(
        name='auto_negotiate',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Auto negotiate speed for speed and duplex')

    # duplex_mode
    class Duplex_Mode(Enum):
        full = 'full'
        half = 'half'

    duplex_mode = managedattribute(
        name='duplex_mode',
        default=None,
        type=(None, Duplex_Mode),
        doc='the port duplex mode')

    # flow_control_receive
    flow_control_receive = managedattribute(
        name='flow_control_receive',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Receive pause frames')

    # flow_control_send
    flow_control_send = managedattribute(
        name='flow_control_send',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Send pause frames')

    lag_bundle_id = managedattribute(
        name='lag_bundle_id',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc= 'lag_bundle_id')

    lag_activity = managedattribute(
        name='lag_activity',
        default=None,
        type=(None, managedattribute.test_in(['active','passive','on','auto','desirable'])),
        doc= 'lag_activity')

    lag_non_silent = managedattribute(
        name='lag_non_silent',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc= 'lag_non_silent')

    lag_force = managedattribute(
        name='lag_force',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc= 'lag_force')

    lag_lacp_port_priority = managedattribute(
        name='lag_lacp_port_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc= 'lag_lacp_port_priority')

    lag_pagp_port_priority = managedattribute(
        name='lag_pagp_port_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc= 'lag_pagp_port_priority')

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'mac_address' not in kwargs:
            try:
                self.mac_address
            except AttributeError:
                pass
            else:
                if self.mac_address:
                    self.testbed.mac_cache.reserve(self.mac_address)
        if 'auto_negotiation' not in kwargs:
            try:
                self.auto_negotiation
            except AttributeError:
                pass
        if 'speed' not in kwargs:
            try:
                self.speed
            except AttributeError:
                pass
        if 'duplex' not in kwargs:
            try:
                self.duplex
            except AttributeError:
                pass


class PosInterface(PhysicalInterface):
    pass


class AtmInterface(PhysicalInterface):
    pass


class SubInterface(VirtualInterface):
    '''Base class for sub-interfaces.

    Example:
        sub_intf = intf.generate_sub_interface(eth_encap_val1=1)
        assert sub_intf.parent_interface is intf
        assert sub_intf in intf.sub_interfaces
        number_after_dot = sub_intf.sub_interface_number
    '''

    _interface_name_subintf_range = range(0, 2147483647 + 1)

    @property
    def mac_address(self):
        '''Not accessible.'''
        raise AttributeError('mac_address not accessible on SubInterface objects')

    @property
    def burnin_mac_address(self):
        '''Not accessible.'''
        raise AttributeError('burnin_mac_address not accessible on SubInterface objects')

    @property
    def effective_mac_address(self):
        return self.parent_interface.effective_mac_address

    eth_encap_type1 = EthernetInterface.eth_encap_type1.copy()
    eth_encap_val1 = EthernetInterface.eth_encap_val1.copy()
    eth_encap_type2 = EthernetInterface.eth_encap_type2.copy()
    eth_encap_val2 = EthernetInterface.eth_encap_val2.copy()

    parent_interface = managedattribute(
        name='parent_interface',
        read_only=True,
        doc='''The parent interface.''')

    @parent_interface.getter
    def parent_interface(self):
        d_parsed = self.parse_interface_name()
        if d_parsed.subintf is not None:
            d_parsed.subintf = None
            parent_interface_name = d_parsed.reconstruct()
        else:
            return None
        return self.device.interfaces.get(parent_interface_name, None)

    @classmethod
    def _generate_unused_sub_interface_name(cls, parent_interface, range=None):
        assert isinstance(parent_interface, BaseInterface)
        device = parent_interface.device
        # Find the os-specific version of this class
        cls = _get_descendent_subclass(
            cls._get_os_specific_Interface_class(device.os),
            cls)

        parent_interface_name = parent_interface.name
        if range is None:
            range = cls._interface_name_subintf_range
        if type(range) is int:
            range = [range]
        for n in range:
            interface_name = '{}.{}'.format(
                parent_interface_name, n)
            if interface_name not in device.interfaces:
                break
        else:
            raise TypeError('No more %r subinterface numbers available on %r' % (
                parent_interface_name, device))
        return interface_name


class VlanInterface(VirtualInterface):
    pass


class AggregatedInterface(VirtualInterface):
    '''Base class for all aggregated/bundle interfaces.

    Example:
        bundle_intf = BundleEtherInterface.generate_interface(device=dev)
        bundle_intf.members = [intf1, intf2]
        bundle_id = bundle_intf.interface_number
        assert intf1.bundle is bundle_intf
        assert intf2.bundle is bundle_intf
        intf3.bundle = bundle_intf
        assert set(bundle_intf.members) == set([intf1, intf2, intf3])
        intf2.bundle = None
        assert set(bundle_intf.members) == set([intf1, intf3])
    '''

    @property
    @abc.abstractmethod
    def members(self):
        '''Derived classes must provide the members property'''
        pass


class TunnelInterface(VirtualInterface):

    named_tunnel = managedattribute(
        name='named_tunnel',
        default=False,
        read_only=True)


class NamedTunnelInterface(TunnelInterface, PseudoInterface):

    named_tunnel = managedattribute(
        name='named_tunnel',
        default=True,
        read_only=True)

    signalled_name = managedattribute(
        name='signalled_name',
        read_only=True)

    @signalled_name.getter
    def signalled_name(self):
        return self.name


class TunnelTeInterface(TunnelInterface):

    _interface_name_number_range = range(0, 65535 + 1)

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if factory_cls is TunnelTeInterface:
            # need to load the correct interface for the right os.
            if 'device' not in kwargs:
                raise TypeError('\'device\' argument missing')
            device = kwargs['device']
            if device.os is None:
                log.debug("Cannot convert interfaces for "
                          "device '{dev}' as mandatory field "
                          "'os' was not given in the "
                          "yaml file".format(dev=device.name))
                device.os = 'generic'
            try:
                factory_cls = _get_descendent_subclass(
                    factory_cls._get_os_specific_Interface_class(device.os),
                    factory_cls)
            except (ImportError, AttributeError, TypeError) as e:
                # it does not exist, then just use the default one,
                # but configuration is not possible
                warnings.warn(
                    'TunnelTeInterfaces for {dev} OS {os!r} are not'
                    ' supported; Configuration will not be available:'
                    ' {e}'.format(
                        dev=device.name, os=device.os, e=e),
                    UnsupportedInterfaceOsWarning)

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self


class NamedTunnelTeInterface(NamedTunnelInterface, TunnelTeInterface):

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if factory_cls is NamedTunnelTeInterface:
            # need to load the correct interface for the right os.
            if 'device' not in kwargs:
                raise TypeError('\'device\' argument missing')
            device = kwargs['device']
            if device.os is None:
                log.debug("Cannot convert interfaces for "
                          "device '{dev}' as mandatory field "
                          "'os' was not given in the "
                          "yaml file".format(dev=device.name))
                device.os = 'generic'
            try:
                factory_cls = _get_descendent_subclass(
                    factory_cls._get_os_specific_Interface_class(device.os),
                    factory_cls)
            except (ImportError, AttributeError, TypeError) as e:
                # it does not exist, then just use the default one,
                # but configuration is not possible
                warnings.warn(
                    'NamedTunnelTeInterfaces for {dev} OS {os!r} are not'
                    ' supported; Configuration will not be available:'
                    ' {e}'.format(
                        dev=device.name, os=device.os, e=e),
                    UnsupportedInterfaceOsWarning)

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self


class BviInterface(VirtualInterface):

    mac_address = EthernetInterface.mac_address.copy()
    burnin_mac_address = EthernetInterface.burnin_mac_address.copy()
    effective_mac_address = EthernetInterface.effective_mac_address
    eth_encap_type1 = EthernetInterface.eth_encap_type1.copy()
    eth_encap_val1 = EthernetInterface.eth_encap_val1.copy()
    eth_encap_type2 = EthernetInterface.eth_encap_type2.copy()
    eth_encap_val2 = EthernetInterface.eth_encap_val2.copy()


class NveInterface(VirtualInterface):

    name = managedattribute(
        name='name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Nve name')

    class HOST_REACHABILTY_PROTOCOL(Enum):
        bgp = 'bgp'

    nve_host_reachability_protocol = managedattribute(
        name='nve_host_reachability_protocol',
        default=None,
        type=(None, HOST_REACHABILTY_PROTOCOL),
        doc='Nve host reachability protocol')

    nve_adv_virtual_rmac = managedattribute(
        name='nve_adv_virtual_rmac',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Nve virtual rmac')

    nve_global_suppress_arp = managedattribute(
        name='nve_global_suppress_arp',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Nve global suppress ARP')

    nve_global_ir_proto = managedattribute(
        name='nve_global_ir_proto',
        default=None,
        type=(None, HOST_REACHABILTY_PROTOCOL),
        doc='Nve Global IR protocol')

    nve_global_mcast_group_l2 = managedattribute(
        name='nve_mcast_global_group_l2',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Nve Global L2 mcast group')

    nve_global_mcast_group_l3 = managedattribute(
        name='nve_mcast_global_group_l3',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Nve Global L3 mcast group')

    nve_src_intf_loopback = managedattribute(
        name='nve_src_intf_loopback',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Nve source interface')

    nve_src_intf_holddown = managedattribute(
        name='nve_src_intf_holddown',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Nve source interface Holddown Timer')

    nve_multisite_bgw_intf = managedattribute(
        name='nve_multisite_bgw_intf',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Nve Multisite bgw interface')

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VniInterface(NveInterface):

    nve_vni = managedattribute(
        name='nve_vni',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Nve vni')

    vni_map = managedattribute(
        name='vni_map',
        default=None,
        type=(None, managedattribute.test_istype(dict)),
        doc='Nve vni MAP DICTIONARY')

    nve_vni_associate_vrf = managedattribute(
        name='nve_vni_associate_vrf',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Nve vni associate vrf')

    nve_vni_suppress_arp = managedattribute(
        name='nve_vni_suppress_arp',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Nve vni suppress arp')

    nve_vni_multisite_ingress_replication_optimized = managedattribute(
        name='nve_vni_multisite_ingress_replication_optimized',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable TRM for Multisite')

    nve_vni_ir = managedattribute(
        name='nve_vni_ir',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable  IR on VNI')

    nve_vni_ir_proto = managedattribute(
        name='nve_vni_ir_proto',
        default=None,
        type=(None, NveInterface.HOST_REACHABILTY_PROTOCOL),
        doc='Enable  BGP or Static as IR protocol')

    nve_vni_multisite_ingress_replication = managedattribute(
        name='nve_vni_multisite_ingress_replication',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable Multsite IR on VNI')


    nve_vni_mcast_group = managedattribute(
        name='nve_vni_mcast_group',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Nve vni mcast group')

    nve_vni_multisite_mcast_group = managedattribute(
        name='nve_vni_multisite_mcast_group',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Enable Mcast group for DCI underlay')

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


