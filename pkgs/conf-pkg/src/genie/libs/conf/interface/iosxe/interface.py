'''
    Interface classes for iosxe OS.
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'VirtualInterface',
    'LoopbackInterface',
    'EthernetInterface',
    'SubInterface',
    'VlanInterface',
    'EFPInterface',
    'PseudowireInterface',
    'TunnelInterface',
    'TunnelTeInterface',
    'PortchannelInterface',
    'NveInterface',
)

import re
import contextlib
import abc
import weakref
from enum import Enum

from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.conf.base.exceptions import UnknownInterfaceTypeError
from genie.conf.base.attributes import SubAttributes, KeyedSubAttributes, SubAttributesDict,\
    AttributesHelper
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder

from genie.libs.conf.base import \
    MAC, \
    IPv4Address, IPv4Interface, \
    IPv6Address, IPv6Interface

from genie.libs.conf.l2vpn import PseudowireNeighbor
from genie.libs.conf.l2vpn.pseudowire import EncapsulationType

import genie.libs.conf.interface

class ConfigurableInterfaceNamespace(ConfigurableBase):

    def __init__(self, interface=None):
        assert interface
        self._interface = interface

    _interface = None

    @property
    def interface(self):
        return self._interface

    @property
    def testbed(self):
        return self.interface.testbed

    @property
    def device(self):
        return self.interface.device


class Interface(genie.libs.conf.interface.Interface):
    """ base Interface class for IOS-XE devices
    """

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is Interface:
            try:
                name = kwargs['name']
            except KeyError:
                raise TypeError('\'name\' argument missing')
            d_parsed = genie.libs.conf.interface.ParsedInterfaceName(
                name, kwargs.get('device', None))
            if d_parsed.subintf:
                factory_cls = SubInterface
            else:
                try:
                    factory_cls = cls._name_to_class_map[d_parsed.type]
                except KeyError:
                    pass

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self



    switchport = managedattribute(
        name='switchport',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure switchport')

    sw_trunk_allowed_vlan = managedattribute(
        name='sw_trunk_allowed_vlan',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc= 'Allowed Vlan on the trunk')

    sw_access_allowed_vlan = managedattribute(
        name='sw_access_allowed_vlan',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc= 'Access VLAN assigned to the interfaces')

    sw_trunk_native_vlan = managedattribute(
        name='sw_trunk_native_vlan',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc= 'Set the native VLAN id for untagged frames arriving on\
                 a trunk interface')

    vrf_downstream  = managedattribute(
        name='vrf_downstream ',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc= 'vrf_downstream ')

    dhcp_snooping = managedattribute(
        name='dhcp_snooping',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc= 'Enabling IP DHCP Snooping trust on the interface')


    class ENCAPSULATION(Enum):
        dot1q = 'dot1q'

    encapsulation  = managedattribute(
        name='encapsulation ',
        default=None,
        type=(None, ENCAPSULATION),
        doc= 'encapsulation ')

    ipv6_autoconf_default = managedattribute(
        name='ipv6_autoconf_default',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc= 'ipv6_autoconf_default')

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        with self._build_config_create_interface_submode_context(configurations):
            self._build_config_interface_submode(configurations=configurations, attributes=attributes, unconfig=unconfig)

        if apply:
            if configurations:
                self.device.configure(configurations, fail_invalid=True)
        else:
            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply,
                                 attributes=attributes,
                                 unconfig=True, **kwargs)

    def _build_config_create_interface_submode_context(self, configurations):
        return configurations.submode_context('interface {}'.format(self.name))

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # encapsulation <encapsulation> <first_dot1q>
        # encapsulation <encapsulation> <first_dot1q> native
        # encapsulation <encapsulation> <first_dot1q> second-dot1q <second_dot1q>
        if attributes.value('encapsulation') and \
           attributes.value('first_dot1q'):
            if attributes.value('second_dot1q'):
                configurations.append_line(
                    attributes.format('encapsulation {encapsulation.value} {first_dot1q}'
                                      ' second-dot1q {second_dot1q}'),
                    unconfig_cmd='no encapsulation {}'
                                 .format(attributes.value('encapsulation').value))
            elif attributes.value('native_vlan_dot1q'):
                configurations.append_line(
                    attributes.format('encapsulation {encapsulation.value} {first_dot1q}'
                                      ' native'),
                    unconfig_cmd='no encapsulation {}'
                                 .format(attributes.value('encapsulation').value))
            else:
                configurations.append_line(
                    attributes.format('encapsulation {encapsulation.value} {first_dot1q}'),
                    unconfig_cmd='no encapsulation {}'
                                 .format(attributes.value('encapsulation').value))

        # iosxe: interface {name} / vrf forwarding someword
        if attributes.value('vrf_downstream'):
            configurations.append_line(
                attributes.format('vrf forwarding {vrf.name}'
                                  ' downstream {vrf_downstream}'))
        else:
            configurations.append_line(
                attributes.format('vrf forwarding {vrf.name}'))

        # iosxe: interface {name} / description some line data
        v = attributes.value('description')
        if v:
            if v is True:
                pass  # TODO Create a usefull default description
            configurations.append_line('description {}'.format(v))

        # iosxe: interface {name} / bandwidth <0-4294967295>
        configurations.append_line(attributes.format('bandwidth {bandwidth}'))

        # iosxe: interface {name} / ip address 1.1.1.1 255.255.255.255
        configurations.append_line(
            attributes.format('ip address {ipv4.ip} {ipv4.netmask}'))

        # iosxe: interface {name} / ipv6 address 2001::1/128
        configurations.append_line(
            attributes.format('ipv6 address {ipv6.with_prefixlen}'))

        # iosxe: interface {name} / mtu 64
        configurations.append_line(
            attributes.format('mtu {mtu}'))

        # iosxe: interface {name} / shutdown
        # enabled
        enabled = attributes.value('enabled')
        if enabled is not None:
            if enabled:
                config_cmd = 'no shutdown'
                unconfig_cmd = 'shutdown'
            else:
                config_cmd = 'shutdown'
                unconfig_cmd = 'no shutdown'
            configurations.append_line(
                attributes.format(config_cmd),
                unconfig_cmd=unconfig_cmd)

        # Compatibility
        else:
            shutdown = attributes.value('shutdown')
            if shutdown is not None:
                if unconfig:
                    # Special case: unconfiguring always applies shutdown
                    configurations.append_line('shutdown', raw=True)
                elif shutdown:
                    configurations.append_line('shutdown', raw=True)
                else:
                    configurations.append_line('no shutdown', raw=True)

        # snmp trap link-status
        if attributes.value('link_up_down_trap_enable'):
            configurations.append_line(
                'snmp trap link-status')

        # logging event link-status
        if attributes.value('link_status'):
            configurations.append_line(
                'logging event link-status')

        # load-interval <load_interval>
        if attributes.value('load_interval'):
            configurations.append_line(
                attributes.format('load-interval {load_interval}'))

        # ipv6 enable
        if attributes.value('ipv6_enabled'):
            configurations.append_line('ipv6 enable')

        # ipv6 address autoconfig [default]
        if attributes.value('ipv6_autoconf'):
            if attributes.value('ipv6_autoconf_default'):
                configurations.append_line('ipv6 address autoconfig default')
            else:
                configurations.append_line('ipv6 address autoconfig')

        # ip unnumbered <unnumbered_intf_ref>
        configurations.append_line(
            attributes.format('ip unnumbered {unnumbered_intf_ref}'),
                unconfig_cmd='no ip unnumbered')

        # ipv6 unnumbered <ipv6_unnumbered_intf_ref>
        configurations.append_line(
            attributes.format('ipv6 unnumbered {ipv6_unnumbered_intf_ref}'),
                unconfig_cmd='no ipv6 unnumbered')

        # speed <port_speed>
        if attributes.value('port_speed'):
            configurations.append_line(
                attributes.format('speed {port_speed.value}'))

        # negotiation auto
        if attributes.value('auto_negotiate'):
            configurations.append_line('negotiation auto')

        # duplex <duplex_mode>
        if attributes.value('duplex_mode'):
            configurations.append_line(
                attributes.format('duplex {duplex_mode.value}'))

        # flowcontrol receive on|off
        if attributes.value('flow_control_receive'):
            configurations.append_line('flowcontrol receive on')
        elif attributes.value('flow_control_receive') == False:
            configurations.append_line('flowcontrol receive off')

        # flowcontrol send on|off
        if attributes.value('flow_control_send'):
            configurations.append_line('flowcontrol send on')
        elif attributes.value('flow_control_send') == False:
            configurations.append_line('flowcontrol send off')

        # ip address dhcp
        # ip address dhcp client-id <dhcp_client_id>
        # ip address dhcp client-id <dhcp_client_id> hostname <dhcp_hostname>
        if attributes.value('dhcp'):

            cfg_str = 'ip address dhcp'
            if attributes.value('dhcp_client_id'):
                cfg_str += ' client-id {dhcp_client_id}'
            if attributes.value('dhcp_hostname'):
                cfg_str += ' hostname {dhcp_hostname}'
            configurations.append_line(
                attributes.format(cfg_str))

        # ip dhcp snooping trust
        if attributes.value('dhcp_snooping'):
            cfg_str = 'ip dhcp snooping trust'
            configurations.append_line(
                attributes.format(cfg_str))


        # medium  <medium >
        if attributes.value('medium'):
            configurations.append_line(
                attributes.format('medium {medium.value}'))

        # delay  <delay >
        if attributes.value('delay'):
            configurations.append_line(
                attributes.format('delay {delay}'))


        # ----- switchport configure ---------#


        # iosxe: interface {name} / switchport
        # Switchport mode configuration can't be applied
        #  on loopback and Vlan interfaces attribute definition
        if not re.match('[V|v]lan', self.name) and \
           not re.match('[L|l]oopback', self.name):

            switchport = attributes.value('switchport')
            switchport_enable = attributes.value('switchport_enable')
            if switchport != None or switchport_enable != None:
                if switchport or switchport_enable:
                    configurations.append_line(
                        attributes.format('switchport'))
                else:
                    configurations.append_line(
                        attributes.format('no switchport'),
                        unconfig_cmd='switchport')

            #  location might be reconsidered
            # iosxe: interface {name} / switchport mode trunk
            switchport = attributes.value('switchport_mode')
            # if 'trunk' in str(switchport):
            configurations.append_line(
                attributes.format('switchport mode {switchport_mode.value}'))

            # iosxe: interface {name} / switchport trunk allowed vlan 100-110
            configurations.append_line(
                attributes.format(
                    'switchport trunk allowed vlan {sw_trunk_allowed_vlan}'))
            configurations.append_line(
                attributes.format(
                    'switchport trunk allowed vlan {trunk_vlans}'))

            # iosxe: interface {name} / switchport trunk native vlan 100
            configurations.append_line(
                attributes.format(
                    'switchport trunk native vlan {sw_trunk_native_vlan}'))
            configurations.append_line(
                attributes.format(
                    'switchport trunk native vlan {native_vlan}'))

            # iosxe: interface {name} / switchport access vlan 100
            if 'access' in str(switchport):
                configurations.append_line(
                    attributes.format('switchport access vlan {sw_access_allowed_vlan}'))
                configurations.append_line(
                    attributes.format('switchport access vlan {access_vlan}'))

            # switchport trunk allowed vlan add <trunk_add_vlans>
            configurations.append_line(
                attributes.format('switchport trunk allowed vlan add {trunk_add_vlans}'))

            # switchport trunk allowed vlan remove <trunk_remove_vlans>
            configurations.append_line(
                attributes.format('switchport trunk allowed vlan remove {trunk_remove_vlans}'))

        # iosxr: interface {name} / vlan <vlan-id>
        ns, attributes2 = attributes.namespace('vlan')
        if ns is not None:
            configurations.append_block(
                ns.build_config(apply=False, attributes=attributes2,
                     unconfig=unconfig))

        # IPv4Addr attributes
        for ipv4addr, attributes2 in attributes.sequence_values(
            'ipv4addr', sort=True):
            if unconfig:
                configurations.append_block(ipv4addr.build_unconfig(
                    apply=False, attributes=attributes2))
            else:
                configurations.append_block(ipv4addr.build_config(
                    apply=False, attributes=attributes2))

        # IPv6Addr attributes
        for ipv6addr, attributes2 in attributes.sequence_values(
            'ipv6addr', sort=True):
            if unconfig:
                configurations.append_block(ipv6addr.build_unconfig(
                    apply=False, attributes=attributes2))
            else:
                configurations.append_block(ipv6addr.build_config(
                    apply=False, attributes=attributes2))

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PhysicalInterface(Interface, genie.libs.conf.interface.PhysicalInterface):

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # Virtual interfaces can be fully unconfigured
        if unconfig and attributes.iswildcard:
            configurations.submode_unconfig()

        super()._build_config_interface_submode(configurations, attributes, unconfig)

        # ----- LagMemberInterface configure ---------#

        # channel-group <lag_bundle_id> mode auto [non-silent]
        # channel-group <lag_bundle_id> mode desirable [non-slilent]
        # channel-group <lag_bundle_id> mode on
        # channel-group <lag_bundle_id> mode active
        # channel-group <lag_bundle_id> mode passive
        if attributes.value('lag_bundle_id'):
            if attributes.value('lag_activity') and \
               ('active' in attributes.value('lag_activity') or \
                'passive' in attributes.value('lag_activity') or \
                'on' in attributes.value('lag_activity')):
                configurations.append_line(
                    attributes.format(
                        'channel-group {lag_bundle_id} mode {lag_activity}'))
            elif attributes.value('lag_activity') and \
               ('auto' in attributes.value('lag_activity') or \
                'desirable' in attributes.value('lag_activity')):
                cmd = 'channel-group {lag_bundle_id} mode {lag_activity}'
                if attributes.value('lag_non_silent'):
                    cmd += ' non-silent'
                configurations.append_line(
                    attributes.format(cmd))

        # lacp port-priority <lag_lacp_port_priority>
        configurations.append_line(
            attributes.format('lacp port-priority {lag_lacp_port_priority}'))

        # pagp port-priority <lag_pagp_port_priority>
        configurations.append_line(
            attributes.format('pagp port-priority {lag_pagp_port_priority}'))



    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VirtualInterface(Interface, genie.libs.conf.interface.VirtualInterface):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # lacp system-priority <lag_lacp_system_priority>
        configurations.append_line(
            attributes.format('lacp system-priority {lag_lacp_system_priority}'))

        with self._build_config_create_interface_submode_context(configurations):
            self._build_config_interface_submode(configurations=configurations, attributes=attributes, unconfig=unconfig)

        if apply:
            if configurations:
                self.device.configure(configurations, fail_invalid=True)
        else:
            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # Virtual interfaces can be fully unconfigured
        if unconfig and attributes.iswildcard:
            configurations.submode_unconfig()

        super()._build_config_interface_submode(configurations, attributes, unconfig)

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoopbackInterface(VirtualInterface, genie.libs.conf.interface.LoopbackInterface):

    _interface_name_types = (
        'loopback',
        'Loopback',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PortchannelInterface(VirtualInterface, genie.libs.conf.interface.LagInterface):
    """ PortchannelInterface class, presenting port-channel type of `Interface`
    objects

    `PortchannelInterface` class inherits from the `VirtualInterface` class.

    Args:
        All the parameters/attrinutes inherits from its supper class
        'Interface'

    Class variables:
        type: interface type - portchannel
    """

    _interface_name_types = (
        'port-channel',
        'Port-channel',
    )

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # Virtual interfaces can be fully unconfigured
        if unconfig and attributes.iswildcard:
            configurations.submode_unconfig()

        super()._build_config_interface_submode(configurations, attributes, unconfig)

        # lacp max-bundle <lag_lacp_max_bundle>
        configurations.append_line(
            attributes.format('lacp max-bundle {lag_lacp_max_bundle}'))

        # lacp min-bundle <lag_lacp_min_bundle>
        configurations.append_line(
            attributes.format('lacp min-bundle {lag_lacp_min_bundle}'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EthernetInterface(PhysicalInterface, genie.libs.conf.interface.EthernetInterface):

    _interface_name_types = (
        'ethernet',
        'Ethernet',
        'fastethernet',
        'FastEthernet',
        'gigabitethernet',
        'GigabitEthernet',
        'tengige',
        'TenGigE',
        'tengigabitethernet',
        'TenGigabitEthernet',
        'twentyfivegige',
        'TwentyFiveGigE',
        'twentyfivegigabitethernet',
        'TwentyFiveGigabitEthernet',
        'fiftygige',
        'FiftyGigE',
        'fiftygigabitethernet',
        'FiftyGigabitEthernet',
        'hundredgige',
        'HundredGigE',
        'hundredgigabitethernet',
        'HundredGigabitEthernet',
        'fortygige',
        'FortyGigE',
        'fortygigabitethernet',
        'FortyGigabitEthernet',
        'fourhundredgige',
        'FourHundredGigE',
        'fourhundredgigabitethernet',
        'FourHundredGigabitEthernet'
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)


        configurations.append_block(super().build_config(apply=False,
                                                         attributes=attributes,
                                                         unconfig=unconfig,
                                                         **kwargs))

        if apply:
            if configurations:
                self.device.configure(configurations, fail_invalid=True)
        else:
            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):

        # physical interfaces unconfigured
        attributes_unconfig = AttributesHelper(self, attributes)
        if attributes_unconfig.iswildcard:
            configurations = CliConfigBuilder(unconfig=True)
            configurations.append_line('default interface {}'.format(self.name),raw=True)
            configurations.append_line('interface {}'.format(self.name), raw=True)
            configurations.append_line('shutdown', raw=True)
            if apply:
                if configurations:
                    self.device.configure(str(configurations))
            else:
                # Return configuration
                return configurations
        else:
            return self.build_config(apply=apply,
                                     attributes=attributes,
                                     unconfig=True, **kwargs)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        super()._build_config_interface_submode(configurations=configurations,
                                                attributes=attributes,
                                                unconfig=unconfig)

        # iosxe: interface {name} / mac-address aaaa.bbbb.cccc
        configurations.append_line(attributes.format('mac-address {mac_address}'))

        # iosxe: interface {name} / negotiation auto
        v = attributes.value('auto_negotiation')
        if v is not None:
            if v:
                configurations.append_line('negotiation auto',unconfig_cmd = 'default negotiation auto')
            else:
                configurations.append_line('no negotiation auto',unconfig_cmd = 'default negotiation auto')


class SubInterface(VirtualInterface, genie.libs.conf.interface.SubInterface):

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is SubInterface:
            if 'service_instance' in kwargs:
                factory_cls = EFPInterface

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # Encapsulation needs to be declared before IP address configs
        if attributes.value('eth_encap_type1') is not None:
            cfg = attributes.format('encapsulation {eth_encap_type1}', force=True)
            v = attributes.value('eth_encap_val1', force=True)
            if v is not None:
                if type(v) is range:
                    cfg += ' {}-{}'.format(v.start, v[-1])
                else:
                    cfg += ' {}'.format(v)

                if attributes.value('eth_encap_val2', force=True) is not None:
                    cfg += attributes.format(' {eth_encap_type2}', force=True)
                    v = attributes.value('eth_encap_val2', force=True)
                    if v is not None:
                        if type(v) is range:
                            cfg += ' {}-{}'.format(v.start, v[-1])
                        else:
                            cfg += ' {}'.format(v)

            configurations.append_line(cfg)

        super()._build_config_interface_submode(configurations, attributes, unconfig)


class EFPInterface(SubInterface):

    service_instance = managedattribute(
        name='service_instance',
        read_only=True)  # mandatory

    rewrite_ingress = managedattribute(
        name='rewrite_ingress',
        type=str)

    rewrite_egress = managedattribute(
        name='rewrite_egress',
        type=str)

    def _build_config_create_interface_submode_context(self, configurations):
        @contextlib.contextmanager
        def multiple_submode_context():
            with configurations.submode_context('interface {}'.format(self.parent_interface.name), cancel_empty=True):
                with configurations.submode_context('service instance {} ethernet'.format(self.service_instance)):
                    yield

        return multiple_submode_context()

    def __init__(self, *args, service_instance, **kwargs):
        self._service_instance = int(service_instance)
        super().__init__(*args, **kwargs)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        super()._build_config_interface_submode(configurations, attributes, unconfig)

        configurations.append_line(attributes.format('rewrite ingress tag {rewrite_ingress}'))
        configurations.append_line(attributes.format('rewrite egress tag {rewrite_egress}'))


class PseudowireInterface(VirtualInterface):

    _interface_name_types = (
        'pseudowire',
        'Pseudowire',
    )

    pseudowire_neighbor = managedattribute(
        name='pseudowire_neighbor',
        type=(None, managedattribute.test_isinstance(PseudowireNeighbor)))

    encapsulation = managedattribute(
        name='encapsulation',
        default=EncapsulationType.mpls,
        type=(None, EncapsulationType))

    preferred_path = managedattribute(
        name='preferred_path',
        default=None,
        type=(None, managedattribute.test_isinstance(Interface), IPv4Address))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pseudowire_neighbor.pseudowire_interface = self

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        #super()._build_config_interface_submode(configurations=configurations,
        #                                        attributes=attributes,
        #                                        unconfig=unconfig)

        # Virtual interfaces can be fully unconfigured
        if unconfig and attributes.iswildcard:
            configurations.submode_unconfig()

        # iosxe: interface {name} / shutdown
        shutdown = attributes.value('shutdown')
        if shutdown is not None:
            if shutdown:
                configurations.append_line('shutdown', raw=True)
            else:
                configurations.append_line('no shutdown', raw=True)

        configurations.append_line(attributes.format('encapsulation {encapsulation}', transform={
            EncapsulationType.mpls: 'mpls',
            EncapsulationType.l2tpv3: 'l2tpv3',
        }))

        if attributes.value('pseudowire_neighbor') is not None:
            configurations.append_line(attributes.format('neighbor {pseudowire_neighbor.ip} {pseudowire_neighbor.pw_id}'))

        v = attributes.value('preferred_path')
        if v is not None:
            if isinstance(v,Interface):
                configurations.append_line(attributes.format('preferred-path interface {preferred_path.name}'))
            elif isinstance(v,IPv4Address):
                configurations.append_line(attributes.format('preferred-path peer {preferred_path}'))

class TunnelInterface(VirtualInterface, genie.libs.conf.interface.TunnelInterface):

    _interface_name_types = (
        'tunnel',
        'Tunnel',
    )

    tunnel_mode = managedattribute(
        name='tunnel_mode',
        type=str)

    def __new__(cls, *args, **kwargs):

        factory_cls = cls
        if cls is TunnelInterface:
            try:
                tunnel_mode = kwargs['tunnel_mode']
            except KeyError:
                raise TypeError('\'tunnel_mode\' argument missing')
            if tunnel_mode == 'mpls traffic-eng':
                factory_cls = TunnelTeInterface
            else:
                raise UnknownInterfaceTypeError  # ('Unsupported tunnel_mode %r' % (tunnel_mode,))

        if factory_cls is not cls:
            self = factory_cls.__new__(factory_cls, *args, **kwargs)
        elif super().__new__ is object.__new__:
            self = super().__new__(factory_cls)
        else:
            self = super().__new__(factory_cls, *args, **kwargs)
        return self


class TunnelTeInterface(TunnelInterface, genie.libs.conf.interface.TunnelTeInterface):

    tunnel_mode = managedattribute(
        name='tunnel_mode',
        default='mpls traffic-eng',
        type=managedattribute.test_in((
            'mpls traffic-eng',
        )))

    destination = managedattribute(
        name='destination',
        default=None,
        type=(None, IPv4Address))

    autoroute_announce = managedattribute(
        name='autoroute_announce',
        default=None,
        type=(None, bool))

    forwarding_adjacency = managedattribute(
        name='forwarding_adjacency',
        default=None,
        type=(None,bool))

    record_route = managedattribute(
        name='record_route',
        default=None,
        type=(None,bool))

    frr = managedattribute(
        name='frr',
        default=None,
        type=(None,bool))

    ipv4_unnumbered_interface = managedattribute(
        name='ipv4_unnumbered_interface',
        default=None,
        type=(None,
              managedattribute.test_isinstance(Interface)))

    priority_setup = managedattribute(
        name='priority_setup',
        default=None,
        type=(None,int))

    priority_hold = managedattribute(
        name='priority_hold',
        default=None,
        type=(None,int))

    affinity = managedattribute(
        name='affinity',
        default=None,
        type=(None,str))

    te_bw =  managedattribute(
        name='te_bw',
        default=None,
        type=(None,int,str))

    te_backup_bw =  managedattribute(
        name='te_backup_bw',
        default=None,
        type=(None,int,str))

    path_options = managedattribute(
        name='path_options',
        finit=set,
        type=managedattribute.test_set_of(
            # TODO managedattribute.test_isinstance(PathOption)),
            managedattribute.test_istype(str)),
        gettype=frozenset,
        doc='A `set` of PathOption associated objects')

    def add_path_option(self, path_option):
        self._path_options.add(path_option)

    def remove_path_option(self, path_option):
        self._path_options.remove(path_option)

    class PathOptionAttributes(KeyedSubAttributes):

        @classmethod
        def _sanitize_key(cls, key):
            return str(key)

        path_option = managedattribute(
            name='path_option',
            read_only=True,  # key
            doc='The path-option name (read-only key)')

        dynamic = managedattribute(
            name='dynamic',
            default=None,
            type=managedattribute.test_istype(bool))

        explicit_name = managedattribute(
            name='explicit_name',
            default=None,
            type=managedattribute.test_istype(str))

        def __init__(self, parent, key, **kwargs):
            self._path_option = key
            super().__init__(parent=parent, **kwargs)

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxe: interface tunnel1 / tunnel mpls traffic-eng path-option 1 dynamic
            if attributes.value('dynamic'):
                configurations.append_line(attributes.format('tunnel mpls traffic-eng path-option {path_option} dynamic'))

            # iosxe: interface tunnel1 / tunnel mpls traffic-eng path-option 1 explicit name someword
            configurations.append_line(attributes.format\
                    ('tunnel mpls traffic-eng path-option {path_option} explicit name {explicit_name}'))

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    path_option_attr = managedattribute(
        name='path_option_attr',
        read_only=True,
        doc=PathOptionAttributes.__doc__)

    @path_option_attr.initter
    def path_option_attr(self):
        return SubAttributesDict(self.PathOptionAttributes, parent=self)

    def __init__(self, *args, **kwargs):
        self.path_options  # init!
        super().__init__(*args, **kwargs)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        #super()._build_config_interface_submode(configurations=configurations,
        #                                        attributes=attributes,
        #                                        unconfig=unconfig)

        # Virtual interfaces can be fully unconfigured
        if unconfig and attributes.iswildcard:
            configurations.submode_unconfig()

        # iosxe: interface {name} / shutdown
        shutdown = attributes.value('shutdown')
        if shutdown is not None:
            if shutdown:
                configurations.append_line('shutdown', raw=True)
            else:
                configurations.append_line('no shutdown', raw=True)

        # iosxe: interface tunnel1 / tunnel mode mpls traffic-eng
        configurations.append_line(attributes.format('tunnel mode {tunnel_mode}'))

        # iosxe: interface tunnel1 / ip unnumbered Loopback0
        configurations.append_line(attributes.format('ip unnumbered {ipv4_unnumbered_interface.name}'))

        # iosxe: interface tunnel1 / tunnel destination 1.2.3.4
        configurations.append_line(attributes.format('tunnel destination {destination}'))

        # iosxe: interface tunnel1 / tunnel mpls traffic-eng autoroute announce
        if attributes.value('autoroute_announce'):
            configurations.append_line('tunnel mpls traffic-eng autoroute announce')

        # iosxe: interface tunnel1 / tunnel mpls traffic-eng forwarding adjacency
        if attributes.value('forwarding_adjacency'):
            configurations.append_line('tunnel mpls traffic-eng forwarding-adjacency')

        # iosxe: interface tunnel1 / tunnel mpls traffic-eng record-route
        if attributes.value('record_route'):
            configurations.append_line('tunnel mpls traffic-eng record_route')

        # iosxe: interface tunnel1 / tunnel mpls traffic-eng priority <0-7> <0-7>
        configurations.append_line(attributes.format('tunnel mpls traffic-eng priority {priority_setup} {priority_hold}'))

        # iosxe: interface tunnel1 / tunnel mpls traffic-eng affinity 0xFFFF
        configurations.append_line(attributes.format('tunnel mpls traffic-eng affinity {affinity}'))

        # iosxe: interface tunnel1 / tunnel mpls traffic-eng bandwidth 1000
        configurations.append_line(attributes.format('tunnel mpls traffic-eng affinity {te_bw}'))

        # iosxe: interface tunnel1 / tunnel mpls traffic-eng backup-bw 1000
        configurations.append_line(attributes.format('tunnel mpls traffic-eng affinity {te_backup_bw}'))

        # iosxe: interface tunnel1 / tunnel mpls trafic-eng fast-reroute
        if attributes.value('frr'):
            configurations.append_line('tunnel mpls traffic-eng fast-reroute')

        # iosxe: interface tunnel-te1 / description some line data
        v = attributes.value('description')
        if v:
            if v is True:
                pass  # TODO Create a usefull default description
            else:
                configurations.append_line('description {}'.format(v))

        # iosxe: interface tunnel-te1 / ipv4 address 1.2.3.0/24

        # ADD PATH OPTIONS
        for ns, attributes2 in attributes.mapping_values('path_option_attr', keys=self.path_options, sort=True):
            configurations.append_block(ns.build_config(apply=False, unconfig=unconfig, attributes=attributes2))

class VlanInterface(
    VirtualInterface, genie.libs.conf.interface.VlanInterface):
    """ VlanInterface class, presenting vlan type of `Interface`
    objects

    `VlanInterface` class inherits from the `VirtualInterface` class.

    Args:
        All the parameters/attributes inherits from its supper class
        'Interface'

    Class variables:
        type: interface type - vlan
    """

    _interface_name_types = (
        'vlan',
        'Vlan',
    )

    def _build_config_interface_submode(self, configurations, attributes,
         unconfig):
        """internal method to build the configuration of a vlan interface object

        Please use build_config and build_unconfig.

        Api to build the configuration of a vlan interface object. This
        configuration depends of the configurable attributes of this object.

        Examples:
            >>> from genie.libs.conf.interface.iosxe import Interface

            Create a Interface obj

            >>> port = Interface(name='vlan11')

            assign configurable attributes to the interface obj

            >>> vlan.mtu = '500'

            Build configuration

            >>> configuration = vlan.build_config()
        """

        super()._build_config_interface_submode(configurations, attributes,
             unconfig)

        # # -- VLAN
        # configuration alreday covered in main interface build section
        # iosxe: interface <intf> / ipv6 address 2001:2::14:1/112
        # configurations.append_line(
        #         attributes.format('ipv6 address {ipv6.with_prefixlen}'),
        #         unconfig_cmd='no ipv6 address')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class NveInterface(VirtualInterface, genie.libs.conf.interface.NveInterface):
    _interface_name_types = (
        'nve',
        'Nve',
    )

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        super()._build_config_interface_submode(configurations, attributes, unconfig)
        if attributes.value('nve_bgp_host_reachability'):
            configurations.append_line(
                attributes.format('host-reachability protocol bgp'))

        if attributes.value('nve_src_intf_loopback'):
            configurations.append_line(
                attributes.format('source-interface {nve_src_intf_loopback}'))


        # attributes for vnis
        if attributes.value('nve_vni'):
            cfg = 'member vni {nve_vni}'

            if attributes.value('nve_vni_vrf'):
                cfg += ' vrf {nve_vni_vrf}'
                configurations.append_line(attributes.format(cfg))
                return

            with configurations.submode_context(attributes.format(cfg)):
                if unconfig:
                    configurations.submode_unconfig()

                if attributes.value('nve_vni_mcast_group'):
                    sub_cfg = 'mcast-group {nve_vni_mcast_group}'

                if attributes.value('nve_vni_ingress_replication'):
                    sub_cfg = 'ingress-replication'

                if attributes.value('nve_vni_local_routing'):
                    sub_cfg += ' local-routing'

                configurations.append_line(attributes.format(sub_cfg))

        # -- NVE
        # iosxe: interface <intf> / host-reachability protocol bgp
        # iosxe: interface <intf> / member vni <nve_vni> vrf <nve_vni_vrf>
        # iosxe: interface <intf> / member vni <nve_vni> / ingress-replication
        # iosxe: interface <intf> / member vni <nve_vni> / ingress-replication local-routing
        # iosxe: interface <intf> / member vni <nve_vni> / mcast-group <nve_vni_mcast_group>
        # iosxe: interface <intf> / member vni <nve_vni> / mcast-group <nve_vni_mcast_group> local-routing
        # iosxe: interface <intf> / source-interface Loopback0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

Interface._build_name_to_class_map()

