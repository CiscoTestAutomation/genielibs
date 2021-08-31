'''
    Interface classes for nxos OS.
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'VirtualInterface',
    'PseudoInterface',
    'LoopbackInterface',
    'EthernetInterface',
    'SubInterface',
    'VlanInterface',
    'PortchannelInterface',
    'NveInterface',
)

import re
import abc
from abc import ABC
from enum import Enum

from genie.conf.base.config import CliConfig
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.conf.base.exceptions import UnknownInterfaceTypeError
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, \
    AttributesHelper, UnsupportedAttributeWarning
from genie.conf.base.cli import CliConfigBuilder

from genie.libs.conf.base import \
    MAC, \
    IPv4Address, IPv4Interface, \
    IPv6Address, IPv6Interface

import genie.libs.conf.interface

from genie.libs.conf.interface import Layer, L2_type

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


class Option(Enum):

    def __str__(self):
        return str(self.value)


class Duplex(Option):
    # Create the same for Half, Full or Auto
    # This way it will remove the confusion of which name to use
    half = 'half'
    full = 'full'
    auto = 'auto'


class Interface(genie.libs.conf.interface.Interface):
    '''Base class for NX-OS interfaces.

        Args:
            name (str): Interface name.

        This is a factory class that instantiates proper subclasses chosen
        based on `name`.
    '''

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

    layer = Layer.L3

    priority_flow_control_mode = None
    switchport_mode = None
    sw_acc_vlan = None
    sw_trunk_encap = None
    sw_trunk_allowed_vlan = None
    sw_trunk_native_vlan = None
    sw_trunk_prun_vlan = None
    switchport_enable = None

    rip = None  # XXXJST TODO

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        """method to build the configuration of an interface object

        Api to build the configuration of an interface object. This
        configuration depends of the configurable attributes of this object.

        Args:
            None

        Return:
            `str`

        Examples:
            >>> from genie.libs.conf.interface.nxos import Interface

            Create a Interface obj

            >>> eth = Interface(name='ethernet3/1')

            assign configurable attributes to the interface obj

            >>> eth.description = 'ethernet3/1'
            >>> eth.shutdown = False

            Build configuration

            >>> configuration = eth.build_config()
        """
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        with self._build_config_create_interface_submode_context(\
            configurations):
            self._build_config_interface_submode(\
                    configurations=configurations, \
                    attributes=attributes, unconfig=unconfig)

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
        # -- ETHER, PC, VLAN, LO, MGMT
        # nxos: interface <intf> (config-if)
        # -- SUB
        # nxos: interface <intf> (config-subif)
        # -- NVE
        # nxos: interface <intf> (config-if-nve)
        return configurations.submode_context('interface {}'.format(self.name))

    def _build_config_interface_submode(self, configurations, \
        attributes, unconfig):

        # -- L3, SUB, PC, VLAN
        # nxos: interface <intf> / medium broadcast
        # nxos: interface <intf> / medium p2p

        configurations.append_line(
            attributes.format('medium {medium}'),
            unconfig_cmd='no medium')

        if attributes.value('cdp'):
            configurations.append_line(
                attributes.format('cdp enable'),
                unconfig_cmd='no cdp')

        # bandwidth
        configurations.append_line(
            attributes.format('bandwidth {bandwidth}'),
            unconfig_cmd='no bandwidth')

        configurations.append_line(
            attributes.format('delay {delay}'),
            unconfig_cmd='no delay')

        v = attributes.value('description')
        if v:
            if v is True:
                pass  # TODO Create a usefull default description
            configurations.append_line('description {}'.format(v),
                                       unconfig_cmd='no description')

        # mtu
        configurations.append_line(
            attributes.format('mtu {mtu}'),
            unconfig_cmd='no mtu')

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

        # link_up_down_trap_enable
        if attributes.value('link_up_down_trap_enable'):
            configurations.append_line('snmp trap link-status')

        # vrf
        configurations.append_line(
            attributes.format('vrf member {vrf.name}'))

        # link_status
        if attributes.value('link_status'):
            configurations.append_line('logging event port link-status')

        # ip address <ipv4> <prefix-length> [secondary] | [tag <route-tag>]
        # ip address dhcp
        # need to put 'if' with ipv4 address
        if attributes.value('dhcp'):
            configurations.append_line('ip address dhcp')

        # ip unnumbered <unnumbered_intf_ref>
        configurations.append_line(
            attributes.format(
                attributes.format('ip unnumbered {unnumbered_intf_ref}'),
                unconfig_cmd='no ip unnumbered'))

        # N/A : ipv6_unnumbered_intf_ref

        # N/A : ipv6_enabled

        # ipv6 address autoconfig [default]
        ipv6_autoconf = attributes.value('ipv6_autoconf')
        ipv6_autoconf_default = attributes.value('ipv6_autoconf_default')
        if ipv6_autoconf is not None:
            cmd = 'ipv6 address autoconfig'
            if ipv6_autoconf:
                if ipv6_autoconf_default:
                    cmd += ' default'
                configurations.append_line(cmd)

        # enable switchport configuration when attribute is True
        if not re.match('[V|v]lan', self.name):
            if attributes.value('switchport_enable'):
                configurations.append_line(
                    attributes.format('switchport'))

            if attributes.value('switchport_enable') == False:
                configurations.append_line(
                    attributes.format('no switchport'),
                    unconfig_cmd='switchport')


        # configure switchport realted configurations
        configurations.append_line(
            attributes.format('switchport mode {switchport_mode}'))

        if self.switchport_mode == L2_type.ACCESS:

            configurations.append_line(
                attributes.format('switchport access vlan {sw_acc_vlan}'))

        elif self.switchport_mode == L2_type.TRUNK:

            configurations.append_line(
                attributes.format('switchport trunk encapsulation {sw_trunk_encap}'))

            configurations.append_line(
                attributes.format('switchport trunk allowed vlan {sw_trunk_allowed_vlan}'))

            configurations.append_line(
                attributes.format('switchport trunk native vlan {sw_trunk_native_vlan}'))

            configurations.append_line(
                attributes.format('switchport trunk pruning vlan {sw_trunk_prun_vlan}'))

        # configure layer3 related configurations
        configurations.append_line(
            attributes.format('ip address {ipv4.ip} {ipv4.netmask}'),
            unconfig_cmd='no ip address')

        # XXXJST TODO move to Rip
        if self.ipv4:
            configurations.append_line(
                attributes.format('ip router rip {rip.instance_id}'))

        configurations.append_line(
            attributes.format('ipv6 address {ipv6.with_prefixlen}'),
            unconfig_cmd='no ipv6 address')

        # XXXJST TODO move to Rip
        if self.ipv6:
            configurations.append_line(
                attributes.format('ipv6 router rip {rip.instance_id}'))

        # load-interval
        configurations.append_line(
            attributes.format('load-interval {load_interval}'),
            unconfig_cmd='no load-interval')

        configurations.append_line(
            attributes.format('load-interval counter {load_interval_counter}'),
            unconfig_cmd='no load-interval counter')

        configurations.append_line(
            attributes.format('flowcontrol receive {flowcontrol_receive}'),
            unconfig_cmd='no flowcontrol receive')

        configurations.append_line(
            attributes.format('flowcontrol send {flowcontrol_send}'),
            unconfig_cmd='no flowcontrol send')

        configurations.append_line(
            attributes.format('priority-flow-control mode \
                {priority_flow_control_mode}'))

        # evpn_multisite_dci_tracking
        if attributes.value('evpn_multisite_dci_tracking'):
            configurations.append_line(
                attributes.format('evpn multisite dci-tracking'),
                unconfig_cmd='no evpn multisite dci-tracking')

        # evpn_multisite_fabric_tracking
        if attributes.value('evpn_multisite_fabric_tracking'):
            configurations.append_line(
                attributes.format('evpn multisite fabric-tracking'),
                unconfig_cmd='no evpn multisite fabric-tracking')

        # fabric_forwarding_mode
        mode = attributes.value('fabric_forwarding_mode')
        if mode:
            configurations.append_line(
                attributes.format('fabric forwarding mode {}'.format(mode)),
                unconfig_cmd='no fabric forwarding mode {}'.format(mode))

        # ip forward
        if attributes.value('ip_forward'):
            configurations.append_line(
                attributes.format('ip forward'),
                unconfig_cmd='no ip forward')

        # ipv6 forward
        if attributes.value('ipv6_forward'):
            configurations.append_line(
                attributes.format('ipv6 forward'),
                unconfig_cmd='no ipv6 forward')

        # ipv6 address use-link-local-only
        if attributes.value('ipv6_addr_use_link_local_only'):
            configurations.append_line(
                attributes.format('ipv6 address use-link-local-only'),
                unconfig_cmd='no ipv6 address use-link-local-only')

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

        # -- ETHER L2, L3, PC
        # nxos: interface <intf> / buffer-boost

    def restore_default(self, apply=True):
        """method to reset the interface configuration to defaults

        Api to reset the configutaion of an interface object.

        Args:
            None

        Return:
            `str`

        Examples:
            >>> from genie.libs.conf.interface.nxos import Interface

            Create a Interface obj

            >>> eth = Interface(name='ethernet3/1')

            Reset configuration

            >>> reset = eth.restore_default()
        """

        configurations = CliConfigBuilder()

        # name is a mandatory arguments
        configurations.append_line('default interface {}'.format(self.name))

        if apply:
            if configurations:
                self.device.configure(str(configurations))
        else:
            # Return configuration
            return str(configurations)

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        '''Abstract constructor.'''

        super().__init__(*args, **kwargs)


class PhysicalInterface(Interface, genie.libs.conf.interface.PhysicalInterface):
    """ Physical interface class, presenting physical type of `Interface`
    objects

    `PhysicalInterface` class inherits from the `Interface` class.
    It is the super class of and `EthernetInterface`

    Args:
        All the parameters/attributes inherits from its supper class
        'Interface'
    """

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):

        # physical interfaces unconfigured
        attributes_unconfig = AttributesHelper(self, attributes)
        if attributes_unconfig.iswildcard:
            configurations = CliConfigBuilder(unconfig=True)
            configurations.append_line('default interface {}'.format(self.name),
                                       raw=True)
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
        super()._build_config_interface_submode(configurations, attributes, unconfig)

class EthernetInterface(PhysicalInterface, genie.libs.conf.interface.EthernetInterface):
    """ EthernetInterface class, presenting ethernet type of `Interface`
    objects

    `EthernetInterface` class inherits from the `PhysicalInterface` class.

    Args:
        All the parameters/attributes inherits from its supper class
        'Interface'

    Class variables:
        type: interface type - ethernet

    Examples:
        >>> from genie.libs.conf.interface.nxos import Interface

        Create a Interface obj

        >>> eth = Interface(name='ethernet1/1')

        assign configurable attributes to the interface obj

        >>> eth.ipv4 = '10.1.1.1 255.255.255.0'

        Build configuration

        >>> configuration = eth.build_config()
    """

    _interface_name_types = (
        'ethernet',
        'Ethernet',
        'gigabitethernet',
        'GigabitEthernet',
    )

    class SwitchportAttributes(ConfigurableInterfaceNamespace):

        # nxos: interface <intf> / switchport
        enabled = False

        class Mode(Enum):
            access = 'access'
            dot1q_tunnel = 'dot1q-tunnel'
            fex_fabric = 'fex-fabric'
            trunk = 'trunk'

        _mode = None
        mode = managedattribute(name='mode', type=(None, Mode))

        access_vlan = None  # int

        trunk_allowed_vlan = None  # int
        trunk_native_vlan = None  # int

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            switchport_enabled = attributes.value('enabled')
            if switchport_enabled is True:
                configurations.append_block('switchport')
            elif switchport_enabled is False:
                if not unconfig:
                    configurations.append_block('no switchport')

            if self.enabled:
                # nxos: interface <intf> / switchport mode access
                # nxos: interface <intf> / switchport mode dot1q-tunnel
                # nxos: interface <intf> / switchport mode fex-fabric
                # nxos: interface <intf> / switchport mode trunk
                configurations.append_line('switchport mode {mode.value}')

                if self.mode is None:
                    pass
                elif self.mode == self.Mode.access:
                    # nxos: interface <intf> / switchport access vlan 1
                    configurations.append_line('switchport access vlan {access_vlan}')

                elif self.mode == self.Mode.dot1q_tunnel:
                    pass
                elif self.mode == self.Mode.fex_fabric:
                    pass
                elif self.mode == self.Mode.trunk:
                    # nxos: interface <intf> / switchport trunk allowed vlan 1
                    configurations.append_line('switchport trunk allowed vlan {trunk_allowed_vlan}')

                    # nxos: interface <intf> / switchport trunk allowed vlan add 1
                    # nxos: interface <intf> / switchport trunk allowed vlan all
                    # nxos: interface <intf> / switchport trunk allowed vlan except 1
                    # nxos: interface <intf> / switchport trunk allowed vlan none
                    # nxos: interface <intf> / switchport trunk allowed vlan remove 1

                    # nxos: interface <intf> / switchport trunk native vlan 1
                    configurations.append_line('switchport trunk native vlan {trunk_native_vlan}')

                # nxos: interface <intf> / switchport autostate exclude
                # nxos: interface <intf> / switchport autostate exclude vlan 1
                # nxos: interface <intf> / switchport autostate exclude vlan add 1
                # nxos: interface <intf> / switchport autostate exclude vlan all
                # nxos: interface <intf> / switchport autostate exclude vlan except 1
                # nxos: interface <intf> / switchport autostate exclude vlan remove 1
                # nxos: interface <intf> / switchport block multicast
                # nxos: interface <intf> / switchport block unicast
                # nxos: interface <intf> / switchport dot1q ethertype 0x8100
                # nxos: interface <intf> / switchport dot1q ethertype 0x88A8
                # nxos: interface <intf> / switchport dot1q ethertype 0x9100
                # nxos: interface <intf> / switchport dot1q ethertype 0x600
                # nxos: interface <intf> / switchport host
                # nxos: interface <intf> / switchport isolated
                # nxos: interface <intf> / switchport monitor
                # nxos: interface <intf> / switchport vlan mapping 1 1
                # nxos: interface <intf> / switchport vlan mapping 1 inner 1 1
                # nxos: interface <intf> / switchport vlan mapping enable

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    switchport = managedattribute(
        name='switchport',
        read_only=True,
        doc=SwitchportAttributes.__doc__)

    @switchport.initter
    def switchport(self):
        return EthernetInterface.SwitchportAttributes(interface=self)

    mac_aging = None
    auto_negotiate = None

    def _build_config_interface_submode(self, configurations, attributes, unconfig):
        """internal method to build the configuration of a ethernet interface object

        Please use build_config and build_unconfig.

        Api to build the configuration of a ethernet interface object. This
        configuration depends of the configurable attributes of this object.

        Args:
            None

        Return:
            `str`

        Examples:
            >>> from genie.libs.conf.interface.nxos import Interface

            Create a Interface obj

            >>> eth = Interface(name='ethernet3/1')

            assign configurable attributes to the interface obj

            >>> eth.description = 'ethernet3/1'
            >>> eth.shutdown = False
            >>> eth.vrf = <vrf object>
            >>> eth.rip = <rip object>
            >>> eth.speed = 100000
            >>> eth.duplex = 'auto'
            >>> eth.ipv4 = '10.0.0.1'

            Build configuration

            >>> configuration = eth.build_config()
        """

        super()._build_config_interface_submode(configurations=configurations,
                                                attributes=attributes,
                                                unconfig=unconfig)

        configurations.append_line(
            attributes.format('duplex {duplex}'),
            unconfig_cmd='no duplex')

        configurations.append_line(
            attributes.format('speed {speed}'),
            unconfig_cmd='no speed')

        configurations.append_line(
            attributes.format('mac-address {mac_address}'),
            unconfig_cmd='no mac-address')

        # TODO auto_negotiation

        # mac_address
        configurations.append_line(
            attributes.format('mac address-table aging-time {mac_aging}'),
            unconfig_cmd='no mac address-table aging')

        # speed <port_speed>
        configurations.append_line(
            attributes.format('speed {port_speed.value}'),
            unconfig_cmd='no speed')
        # access port
        if self.switchport_mode == L2_type.ACCESS.name.lower():
            # switchport access vlan <access_vlan>
            configurations.append_line(
                attributes.format('switchport access vlan {access_vlan}'),
                unconfig_cmd='no switchport access vlan')

        #dot1q port
        if self.switchport_mode == L2_type.DOT1Q_TUNNEL.value.lower():
            # switchport access vlan <dot1q_access_vlan>
            configurations.append_line(
                attributes.format('switchport access vlan {dot1q_access_vlan}'),
                unconfig_cmd='no switchport access vlan')

        # trunk port
        if self.switchport_mode == L2_type.TRUNK.name.lower():
            # switchport trunk allowed vlan <trunk_vlans>
            configurations.append_line(
                attributes.format('switchport trunk allowed vlan {trunk_vlans}'),
                unconfig_cmd='no switchport trunk allowed vlan')

            # switchport trunk allowed vlan add <trunk_add_vlans>
            cmd = 'switchport trunk allowed vlan add {trunk_add_vlans}'
            uncmd = 'switchport trunk allowed vlan remove {trunk_add_vlans}'
            configurations.append_line(
                attributes.format(cmd),
                unconfig_cmd=attributes.format(uncmd))

            # switchport trunk allowed vlan remove <trunk_remove_vlans>
            cmd = 'switchport trunk allowed vlan remove {trunk_remove_vlans}'
            uncmd = 'switchport trunk allowed vlan add {trunk_remove_vlans}'
            configurations.append_line(
                attributes.format(cmd),
                unconfig_cmd=attributes.format(uncmd))

            # switchport trunk native vlan <native_vlan>
            cmd = 'switchport trunk native vlan {native_vlan}'
            uncmd = 'no switchport trunk native vlan'
            configurations.append_line(
                attributes.format(cmd),
                unconfig_cmd=attributes.format(uncmd))

        # speed auto
        # duplex auto
        auto_negotiate = attributes.value('auto_negotiate')
        if auto_negotiate is not None:
            if auto_negotiate:
                configurations.append_line('speed auto')
                configurations.append_line('duplex auto')
            else:
                configurations.append_line('no speed', raw=True)
                configurations.append_line('no duplex', raw=True)
        else:
            # duplex_mode
            duplex_mode = attributes.value('duplex_mode')
            if duplex_mode:
                if duplex_mode.name == 'full':
                    configurations.append_line('duplex full',
                                               unconfig_cmd='no duplex')
                elif duplex_mode.name == 'half':
                    configurations.append_line('duplex half',
                                               unconfig_cmd='no duplex')

        # flow_control_receive
        flow_control_receive = attributes.value('flow_control_receive')
        if flow_control_receive is not None:
            if flow_control_receive:
                configurations.append_line('flowcontrol receive on')
            else:
                configurations.append_line('no flowcontrol receive')

        # flow_control_send
        flow_control_send = attributes.value('flow_control send')
        if flow_control_send is not None:
            if flow_control_send:
                configurations.append_line('flowcontrol send on')
            else:
                configurations.append_line('no flowcontrol send')

        # -- ETHER L2, L3
        # nxos: interface <intf> / beacon
        # nxos: interface <intf> / channel-group 1
        # nxos: interface <intf> / channel-group 1 force
        # nxos: interface <intf> / channel-group 1 force mode active
        # nxos: interface <intf> / channel-group 1 force mode on
        # nxos: interface <intf> / channel-group 1 force mode passive
        # nxos: interface <intf> / channel-group 1 mode active
        # nxos: interface <intf> / channel-group 1 mode on
        # nxos: interface <intf> / channel-group 1 mode passive
        # nxos: interface <intf> / errdisable port detect cause acl-exception
        # nxos: interface <intf> / fec cl74
        # nxos: interface <intf> / fec cl91
        # nxos: interface <intf> / fec off
        # nxos: interface <intf> / lacp port-priority 1
        # nxos: interface <intf> / lacp rate fast
        # nxos: interface <intf> / lacp rate normal
        # nxos: interface <intf> / mac packet-classify
        # nxos: interface <intf> / mdix auto
        # nxos: interface <intf> / power efficient-ethernet auto
        # nxos: interface <intf> / power efficient-ethernet sleep threshold aggressive
        # nxos: interface <intf> / speed-group 10000
        # nxos: interface <intf> / speed-group 40000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class VirtualInterface(EthernetInterface, genie.libs.conf.interface.VirtualInterface):
    """ VirtualInterface class, presenting logical/virtual type of `Interface`
    objects

    `VirtualInterface` class inherits from the `Interface` class. It is the
     super class of `LoopbackInterface`, 'PortchannelInterface`,
     `VlanInterface` and `SubInterface`

    Args:
        All the parameters/attributes inherits from its super class
        'Interface'
    """

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # Virtual interfaces can be fully unconfigured
        if unconfig and attributes.iswildcard:
            configurations.submode_unconfig()


        super()._build_config_interface_submode(configurations, attributes, unconfig)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply,
                                 attributes=attributes,
                                 unconfig=True, **kwargs)

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PseudoInterface(VirtualInterface, genie.libs.conf.interface.PseudoInterface):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LoopbackInterface(VirtualInterface, genie.libs.conf.interface.LoopbackInterface):
    """ LoopbackInterface class, presenting loopback type of `Interface`
    objects

    `LoopbackInterface` class inherits from the `VirtualInterface` class.

    Args:
        All the parameters/attrinutes inherits from its supper class
        'Interface'
    """

    _interface_name_types = (
        'loopback',
        'Loopback',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubInterface(VirtualInterface, genie.libs.conf.interface.SubInterface):
    """ SubInterface class, presenting subinterface type of `Interface`
    object

    `SubInterface` class inherits from the `VirtualInterface` class.
    class

    Args:
        All the parameters/attributes inherits from its super class
        `Interface`

    Class variables:
        type: interface type - subinterface
    """
    # -- SUB
    # nxos: interface <intf> / encapsulation dot1Q 1
    # nxos: interface <intf> / ip unnumbered loopback0

    first_dot1q = None

    def _build_config_interface_submode(self, configurations, attributes, unconfig):
        """internal method to build the configuration of a subinterface interface object

        Please use build_config and build_unconfig.

        Api to build the configuration of a subinterface interface object. This
        configuration depends of the configurable attributes of this object.

        Examples:
            >>> from genie.libs.conf.interface.nxos import SubInterface

            Create a Interface obj

            >>> subif = SubInterface(name='vlan11')

            assign configurable attributes to the interface obj

            >>> subif.mtu = '500'

            Build configuration

            >>> configuration = vlan.build_config()
        """

        super()._build_config_interface_submode(configurations, attributes, unconfig)

        # encapsulation <encapsulation> <first_dot1q>
        if attributes.value('encapsulation'):
            encapsulation = attributes.value('encapsulation').name
        else:
            encapsulation = None
        if attributes.value('first_dot1q'):
            first_dot1q = attributes.value('first_dot1q')
        else:
            first_dot1q = None

        if encapsulation and encapsulation == 'dot1q':
            if first_dot1q:
                cmd = 'encapsulation {} {}'.format(encapsulation, first_dot1q)
                uncmd = 'no encapsulation {}'.format(encapsulation)
                configurations.append_line(cmd, unconfig_cmd=uncmd)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MgmtInterface(EthernetInterface, genie.libs.conf.interface.ManagementInterface):
    # -- MGMT
    # nxos: interface <intf> / media-type auto
    # nxos: interface <intf> / media-type rj45
    # nxos: interface <intf> / media-type sfp

    _interface_name_types = (
        'mgmt',
        'Mgmt',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class VlanInterface(VirtualInterface, genie.libs.conf.interface.VlanInterface):
    """ VlanInterface class, presenting vlan type of `Interface`
    objects

    `VlanInterface` class inherits from the `VirtualInterface` class.

    Args:
        All the parameters/attrinutes inherits from its supper class
        'Interface'

    Class variables:
        type: interface type - vlan
    """

    _interface_name_types = (
        'vlan',
        'Vlan',
    )

    mac_aging = None

    def _build_config_interface_submode(self, configurations, attributes, unconfig):
        """internal method to build the configuration of a vlan interface object

        Please use build_config and build_unconfig.

        Api to build the configuration of a vlan interface object. This
        configuration depends of the configurable attributes of this object.

        Examples:
            >>> from genie.libs.conf.interface.nxos import Interface

            Create a Interface obj

            >>> port = Interface(name='vlan11')

            assign configurable attributes to the interface obj

            >>> vlan.mtu = '500'

            Build configuration

            >>> configuration = vlan.build_config()
        """

        super()._build_config_interface_submode(configurations, attributes, unconfig)

        configurations.append_line(
            attributes.format('mac address-table aging-time {mac_aging}'),
            unconfig_cmd='no mac address-table aging')

        # -- VLAN
        # nxos: interface <intf> / autostate
        # nxos: interface <intf> / carrier-delay <0-60>
        # nxos: interface <intf> / carrier-delay msec <0-1000>
        # nxos: interface <intf> / fabric forwarding mode anycast-gateway
        # nxos: interface <intf> / ip arp test 1.2.3.4 aaaa.bbbb.cccc 1
        # nxos: interface <intf> / ip drop-glean
        # nxos: interface <intf> / ipv6 forward
        # nxos: interface <intf> / management

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PortchannelInterface(VirtualInterface, genie.libs.conf.interface.AggregatedInterface):
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
        'Port-Channel',
    )

    members = managedattribute(
        name='members',
        finit=set,
        type=managedattribute.test_set_of(
            managedattribute.test_isinstance(Interface)),
        gettype=frozenset,
        doc='A `set` of Interface member objects')

    # XXXJST TODO align with iosxr and implement channel-group config within members, not port-channel interface
    def add_member(self, member):
        self.members |= {member}

    def remove_member(self, member):
        self.members -= {member}

    channel_group_mode = None

    # XXXJST TODO interface_number
    @property
    def channel_group(self):
        '''To extract the channel group number from the port-channel interface'''
        return int(re.search(r'\d+', self.name).group())

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        if attributes:
            try:
                for intf_member, attributes2 in attributes.sequence_values('members', sort=True):
                    attributes2.obj = self
                    with intf_member._build_config_create_interface_submode_context(configurations):

                        if attributes2.value('channel_group') is not None \
                                or attributes2.value('channel_group_mode') is not None:
                            cfg = attributes2.format('channel-group {channel_group}', force=True)
                            cfg += attributes2.format(' mode {channel_group_mode}', force=True)
                            configurations.append_line(cfg)

                        if not configurations:
                            configurations.submode_cancel()
            except:
                pass

        # -- PC
        # nxos: interface <intf> / l2protocol tunnel
        # nxos: interface <intf> / l2protocol tunnel cdp
        # nxos: interface <intf> / l2protocol tunnel dot1x
        # nxos: interface <intf> / l2protocol tunnel drop-threshold 1
        # nxos: interface <intf> / l2protocol tunnel drop-threshold cdp 1
        # nxos: interface <intf> / l2protocol tunnel drop-threshold dot1x 1
        # nxos: interface <intf> / l2protocol tunnel drop-threshold stp 1
        # nxos: interface <intf> / l2protocol tunnel drop-threshold vtp 1
        # nxos: interface <intf> / l2protocol tunnel shutdown-threshold 1
        # nxos: interface <intf> / l2protocol tunnel shutdown-threshold cdp 1
        # nxos: interface <intf> / l2protocol tunnel shutdown-threshold dot1x 1
        # nxos: interface <intf> / l2protocol tunnel shutdown-threshold stp 1
        # nxos: interface <intf> / l2protocol tunnel shutdown-threshold vtp 1
        # nxos: interface <intf> / l2protocol tunnel stp
        # nxos: interface <intf> / l2protocol tunnel vtp
        # nxos: interface <intf> / lacp graceful-convergence
        # nxos: interface <intf> / lacp max-bundle 1
        # nxos: interface <intf> / lacp min-links 1
        # nxos: interface <intf> / lacp mode delay
        # nxos: interface <intf> / lacp suspend-individual
        # nxos: interface <intf> / mode tap-aggregation
        # nxos: interface <intf> / port-channel port load-defer
        # nxos: interface <intf> / spanning-tree bpdufilter disable
        # nxos: interface <intf> / spanning-tree bpdufilter enable
        # nxos: interface <intf> / spanning-tree bpduguard disable
        # nxos: interface <intf> / spanning-tree bpduguard enable
        # nxos: interface <intf> / spanning-tree bridge-domain BD-LIST
        # nxos: interface <intf> / spanning-tree cost 1
        # nxos: interface <intf> / spanning-tree cost auto
        # nxos: interface <intf> / spanning-tree guard loop
        # nxos: interface <intf> / spanning-tree guard none
        # nxos: interface <intf> / spanning-tree guard root
        # nxos: interface <intf> / spanning-tree lc-issu auto
        # nxos: interface <intf> / spanning-tree lc-issu disruptive
        # nxos: interface <intf> / spanning-tree lc-issu non-disruptive
        # nxos: interface <intf> / spanning-tree link-type auto
        # nxos: interface <intf> / spanning-tree link-type point-to-point
        # nxos: interface <intf> / spanning-tree link-type shared
        # nxos: interface <intf> / spanning-tree mst <0-4094> cost 1
        # nxos: interface <intf> / spanning-tree mst <0-4094> cost auto
        # nxos: interface <intf> / spanning-tree mst <0-4094> port-priority <0-240>
        # nxos: interface <intf> / spanning-tree mst pre-standard
        # nxos: interface <intf> / spanning-tree mst simulate pvst
        # nxos: interface <intf> / spanning-tree mst simulate pvst disable
        # nxos: interface <intf> / spanning-tree port type edge
        # nxos: interface <intf> / spanning-tree port type edge trunk
        # nxos: interface <intf> / spanning-tree port type network
        # nxos: interface <intf> / spanning-tree port type normal
        # nxos: interface <intf> / spanning-tree port-priority <0-224>
        # nxos: interface <intf> / spanning-tree vlan 1 cost 1
        # nxos: interface <intf> / spanning-tree vlan 1 cost auto
        # nxos: interface <intf> / spanning-tree vlan 1 port-priority <0-224>

        configurations.append_block(super().build_config(apply=False, attributes=attributes, unconfig=unconfig, **kwargs))

        if apply:
            if configurations:
                self.device.configure(configurations, fail_invalid=True)
        else:
            return str(configurations)

    def __init__(self, *args, **kwargs):
        self.members  # init!
        super().__init__(*args, **kwargs)

class NveInterface(VirtualInterface, genie.libs.conf.interface.NveInterface):
    _interface_name_types = (
        'nve',
        'Nve',
    )

    vni_map = managedattribute(
        name='vni_map',
        finit=dict,
        doc='''Mapping of Vni.vni_id to Vni objects''')

    @property
    def vnis(self):
        return frozenset(self.vni_map.values())

    def add_vni(self, vni):
        if vni.vni_id in self.vni_map:
            raise ValueError(
                'Duplicate vni {} exists within {!r}'.\
                format(vni.vni_id, self))
        self.vni_map[vni.vni_id] = vni
        # TODO vni._on_added_from_nve_interface(self)

    def remove_vni(self, vni):
        try:
            vni_id = vni.vni_id
        except AttributeError:
            vni_id = vni
            vni = None

        try:
            old_vni = self.vni_map.pop(vni_id)
        except KeyError:
            raise ValueError(
                'Vni {!r} does not exist within {!r}'.\
                format(vni or vni_id, self))

        if vni is not None and old_vni is not vni:
            self.vni_map[vni_id] = old_vni
            raise ValueError(
                'Vni {!r} does not match existing {!r} within {!r}'.\
                format(vni, old_vni, self))

        # TODO vni._on_removed_from_nve_interface(self)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        super()._build_config_interface_submode(configurations, attributes, unconfig)
        if attributes.value('nve_host_reachability_protocol'):
            configurations.append_line(
                attributes.format('host-reachability protocol {nve_host_reachability_protocol.value}'))


        if attributes.value('nve_global_suppress_arp'):
            configurations.append_line(
                attributes.format('global suppress-arp'))


        if attributes.value('nve_global_ir_proto'):
            configurations.append_line(
                attributes.format('global ingress-replication protocol bgp'))


        if attributes.value('nve_global_mcast_group_l2'):
            configurations.append_line(
                attributes.format('global mcast-group {nve_global_mcast_group_l2} L2'),
                unconfig_cmd='no global mcast-group L2')

        if attributes.value('nve_global_mcast_group_l3'):
            configurations.append_line(
                attributes.format('global mcast-group {nve_global_mcast_group_l3} L3'),
                unconfig_cmd='no global mcast-group L3')

        if attributes.value('nve_adv_virtual_rmac'):
            configurations.append_line(
                attributes.format('advertise virtual-rmac'))


        if attributes.value('nve_src_intf_loopback'):
            configurations.append_line(
                attributes.format('source-interface {nve_src_intf_loopback}'),
                unconfig_cmd='no source-interface')

        if attributes.value('nve_src_intf_holddown'):
            configurations.append_line(
                attributes.format('source-interface hold-down-time {nve_src_intf_holddown}'))


        if attributes.value('nve_multisite_bgw_intf'):
            configurations.append_line(
                attributes.format('multisite border-gateway interface {nve_multisite_bgw_intf}'))

        # attributes for vnis
        if attributes.value('nve_vni'):
                if attributes.value('nve_vni_associate_vrf') == True:
                    cfg_line = 'member vni {nve_vni} associate-vrf'
                else:
                    cfg_line = 'member vni {nve_vni}'

                with configurations.submode_context(attributes.format(cfg_line, force=True)):
                    if unconfig and attributes.value('nve_vni') and \
                            len(getattr(attributes, 'attributes', {})) == 1:
                        configurations.submode_unconfig()

                    if attributes.value('nve_vni_suppress_arp'):
                        configurations.append_line('suppress-arp')

                    if attributes.value('nve_vni_multisite_ingress_replication'):
                        configurations.append_line('multisite ingress-replication')

                    if attributes.value('nve_vni_mcast_group'):
                        configurations.append_line(
                            attributes.format('mcast-group {nve_vni_mcast_group}'),
                            unconfig_cmd='no mcast-group')

                    if attributes.value('nve_vni_multisite_mcast_group'):
                        configurations.append_line(
                            attributes.format('multisite mcast-group {nve_vni_multisite_mcast_group}'),
                            unconfig_cmd='no multisite mcast-group')

        else:
            req_attr = getattr(attributes,'attributes', None)
            vni_attr = attributes.value('vni_map')
            if vni_attr or (req_attr and req_attr.get('vni_map')):
                vni_config_dict = attributes.value('vni_map')
                for key, value in vni_config_dict.items():
                   if vni_config_dict[key].get('nve_vni_associate_vrf', False) == True:
                       cfg_line = 'member vni {} associate-vrf'.format(key)
                   else:
                       cfg_line = 'member vni {}'.format(key)
                   with configurations.submode_context(attributes.format(cfg_line, force=True)):

                      if unconfig and vni_config_dict[key].get('nve_vni',0) and len(vni_config_dict[key].items()) == 1 :
                          configurations.submode_unconfig()

                      if vni_config_dict[key].get('nve_vni_suppress_arp', False):
                          configurations.append_line(
                            attributes.format('suppress-arp'))

                      if vni_config_dict[key].get('nve_vni_ir', False):
                          configurations.append_line(
                            attributes.format('ingress-replication protocol {}'.format(vni_config_dict[key].get('nve_vni_ir_proto',None))))

                      if vni_config_dict[key].get('nve_vni_multisite_ingress_replication', False):
                          configurations.append_line(
                            attributes.format('multisite ingress-replication'))

                      if vni_config_dict[key].get('nve_vni_multisite_ingress_replication_optimized', False):
                          configurations.append_line(
                            attributes.format('multisite ingress-replication optimized'))

                      if vni_config_dict[key].get('nve_vni_mcast_group'):
                          configurations.append_line(
                            attributes.format('mcast-group {}'.format(vni_config_dict[key].get('nve_vni_mcast_group',None))),
                            unconfig_cmd='no mcast-group')

                      if vni_config_dict[key].get('nve_vni_multisite_mcast_group'):
                          configurations.append_line(
                            attributes.format('multisite mcast-group {}'.format(vni_config_dict[key].get('nve_vni_multisite_mcast_group',None))),
                            unconfig_cmd='no multisite mcast-group')
        # -- NVE
        # nxos: interface <intf> / auto-remap-replication-servers
        # nxos: interface <intf> / host-reachability protocol
        # nxos: interface <intf> / host-reachability protocol bgp
        # nxos: interface <intf> / host-reachability protocol openflow
        # nxos: interface <intf> / host-reachability protocol openflow-ir
        # nxos: interface <intf> / member vni 4096 (config-if-nve-vni)
        # nxos: interface <intf> / member vni 4096 associate-vrf
        # nxos: interface <intf> / member vni 4096 / ingress-replication protocol bgp
        # nxos: interface <intf> / member vni 4096 / ingress-replication protocol static (config-if-nve-vni-ingr-rep)
        # nxos: interface <intf> / member vni 4096 / ingress-replication protocol static / peer-ip 1.2.3.4
        # nxos: interface <intf> / member vni 4096 / peer-vtep 1.2.3.4
        # nxos: interface <intf> / member vni 4096 / spine-anycast-gateway
        # nxos: interface <intf> / member vni 4096 / suppress-arp
        # nxos: interface <intf> / overlay-encapsulation vxlan
        # nxos: interface <intf> / overlay-encapsulation vxlan LACP
        # nxos: interface <intf> / overlay-encapsulation vxlan tunnel-control-frames
        # nxos: interface <intf> / overlay-encapsulation vxlan tunnel-control-frames LACP
        # nxos: interface <intf> / overlay-encapsulation vxlan-with-tag
        # nxos: interface <intf> / overlay-encapsulation vxlan-with-tag LACP
        # nxos: interface <intf> / overlay-encapsulation vxlan-with-tag tunnel-control-frames
        # nxos: interface <intf> / overlay-encapsulation vxlan-with-tag tunnel-control-frames LACP
        # nxos: interface <intf> / redundancy-group (config-if-nve-red-group)
        # nxos: interface <intf> / redundancy-group / ip 1.2.3.4
        # nxos: interface <intf> / source-interface hold-down-time 1
        # nxos: interface <intf> / source-interface loopback0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# -- ETHER L2, L3, SUB, PC, VLAN
# nxos: interface <intf> / bandwidth 1

# -- ETHER L2, L3, SUB, PC
# nxos: interface <intf> / bandwidth inherit
# nxos: interface <intf> / bandwidth inherit 1

# -- BFD?
# nxos: interface <intf> / bfd
# nxos: interface <intf> / bfd authentication Keyed-SHA1 key-id 1 hex-key someword
# nxos: interface <intf> / bfd authentication Keyed-SHA1 key-id 1 key someword
# nxos: interface <intf> / bfd echo
# nxos: interface <intf> / bfd echo-rx-interval 50
# nxos: interface <intf> / bfd interval 50 min_rx 50 multiplier 1
# nxos: interface <intf> / bfd ipv4
# nxos: interface <intf> / bfd ipv4 authentication Keyed-SHA1 key-id 1 hex-key someword
# nxos: interface <intf> / bfd ipv4 authentication Keyed-SHA1 key-id 1 key someword
# nxos: interface <intf> / bfd ipv4 echo
# nxos: interface <intf> / bfd ipv4 echo-rx-interval 50
# nxos: interface <intf> / bfd ipv4 interval 50 min_rx 50 multiplier 1
# nxos: interface <intf> / bfd ipv4 optimize subinterface
# nxos: interface <intf> / bfd ipv6
# nxos: interface <intf> / bfd ipv6 authentication Keyed-SHA1 key-id 1 hex-key someword
# nxos: interface <intf> / bfd ipv6 authentication Keyed-SHA1 key-id 1 key someword
# nxos: interface <intf> / bfd ipv6 echo
# nxos: interface <intf> / bfd ipv6 echo-rx-interval 50
# nxos: interface <intf> / bfd ipv6 interval 50 min_rx 50 multiplier 1
# nxos: interface <intf> / bfd neighbor src-ip 1.2.3.4 dest-ip 1.2.3.4
# nxos: interface <intf> / bfd neighbor src-ip 1:2::3 dest-ip 1:2::3
# nxos: interface <intf> / bfd optimize subinterface

# -- ETHER L2, L3, MGMT
# nxos: interface <intf> / cdp enable

# -- ETHER L2, L3, SUB, PC, VLAN
# nxos: interface <intf> / delay 1

# -- ETHER L2, L3, SUB, NVE, PC, VLAN, LO, MGMT
# nxos: interface <intf> / description some line data

# -- ETHER L2, L3, PC, MGMT
# nxos: interface <intf> / duplex auto
# nxos: interface <intf> / duplex full

# -- ETHER L2, L3, SUB, PC
# nxos: interface <intf> / fabric database inherit-profile-map 2

# -- ETHER L2, L3, PC
# nxos: interface <intf> / flowcontrol receive off
# nxos: interface <intf> / flowcontrol receive on
# nxos: interface <intf> / flowcontrol send off
# nxos: interface <intf> / flowcontrol send on

# -- ETHER L2, L3, SUB, PC, VLAN, LO
# nxos: interface <intf> / inherit port-profile someword

# -- ETHER L2, L3, SUB, PC, VLAN, MGMT
# nxos: interface <intf> / ip access-group someword in
# nxos: interface <intf> / ip access-group someword out

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / ip address 1.2.3.4 255.255.255.0
# nxos: interface <intf> / ip address 1.2.3.4 255.255.255.0 secondary
# nxos: interface <intf> / ip address 1.2.3.4 255.255.255.0 secondary tag <0-4294967295>
# nxos: interface <intf> / ip address 1.2.3.4 255.255.255.0 tag <0-4294967295>
# nxos: interface <intf> / ip address 1.2.3.0/24
# nxos: interface <intf> / ip address 1.2.3.0/24 secondary
# nxos: interface <intf> / ip address 1.2.3.0/24 secondary tag <0-4294967295>
# nxos: interface <intf> / ip address 1.2.3.0/24 tag <0-4294967295>

# -- L3, SUB, VLAN, MGMT
# nxos: interface <intf> / ip address dhcp

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / ip arp 1.2.3.4 aaaa.bbbb.cccc
# nxos: interface <intf> / ip arp gratuitous hsrp duplicate
# nxos: interface <intf> / ip arp gratuitous request
# nxos: interface <intf> / ip arp gratuitous update

# -- L3, SUB, VLAN, LO
# nxos: interface <intf> / ip arp timeout 60

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / ip directed-broadcast
# nxos: interface <intf> / ip directed-broadcast someword

# -- L3, SUB, VLAN, LO
# nxos: interface <intf> / ip forward
# nxos: interface <intf> / ip igmp access-group someword
# nxos: interface <intf> / ip igmp access-group prefix-list someword
# nxos: interface <intf> / ip igmp group-timeout 3
# nxos: interface <intf> / ip igmp immediate-leave
# nxos: interface <intf> / ip igmp join-group route-map rpl1
# nxos: interface <intf> / ip igmp last-member-query-count 1
# nxos: interface <intf> / ip igmp last-member-query-response-time 1
# nxos: interface <intf> / ip igmp querier-timeout 1
# nxos: interface <intf> / ip igmp query-interval 1
# nxos: interface <intf> / ip igmp query-max-response-time 1
# nxos: interface <intf> / ip igmp query-timeout 1
# nxos: interface <intf> / ip igmp report-link-local-groups
# nxos: interface <intf> / ip igmp report-policy someword
# nxos: interface <intf> / ip igmp report-policy prefix-list someword
# nxos: interface <intf> / ip igmp robustness-variable 1
# nxos: interface <intf> / ip igmp startup-query-count 1
# nxos: interface <intf> / ip igmp startup-query-interval 1
# nxos: interface <intf> / ip igmp state-limit 1
# nxos: interface <intf> / ip igmp state-limit 1 reserved someword 1
# nxos: interface <intf> / ip igmp static-oif route-map rpl1
# nxos: interface <intf> / ip igmp version 2
# nxos: interface <intf> / ip local-proxy-arp

# -- ETHER L2, L3, PC
# nxos: interface <intf> / ip port access-group someword in

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / ip port-unreachable

# -- L3, SUB, VLAN, LO
# nxos: interface <intf> / ip proxy-arp

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / ip redirects
# nxos: interface <intf> / ip unreachables
# nxos: interface <intf> / ipv6 address 1:2::3/128
# nxos: interface <intf> / ipv6 address 1:2::3/128 anycast
# nxos: interface <intf> / ipv6 address 1:2::3/128 eui64
# nxos: interface <intf> / ipv6 address 1:2::3/128 eui64 anycast
# nxos: interface <intf> / ipv6 address 1:2::3/128 eui64 route-preference <0-255>
# nxos: interface <intf> / ipv6 address 1:2::3/128 eui64 route-preference <0-255> anycast
# nxos: interface <intf> / ipv6 address 1:2::3/128 eui64 route-preference <0-255> tag <0-4294967295>
# nxos: interface <intf> / ipv6 address 1:2::3/128 eui64 route-preference <0-255> tag <0-4294967295> anycast
# nxos: interface <intf> / ipv6 address 1:2::3/128 eui64 tag <0-4294967295>
# nxos: interface <intf> / ipv6 address 1:2::3/128 eui64 tag <0-4294967295> anycast
# nxos: interface <intf> / ipv6 address 1:2::3/128 route-preference <0-255>
# nxos: interface <intf> / ipv6 address 1:2::3/128 route-preference <0-255> anycast
# nxos: interface <intf> / ipv6 address 1:2::3/128 route-preference <0-255> tag <0-4294967295>
# nxos: interface <intf> / ipv6 address 1:2::3/128 route-preference <0-255> tag <0-4294967295> anycast
# nxos: interface <intf> / ipv6 address 1:2::3/128 tag <0-4294967295>
# nxos: interface <intf> / ipv6 address 1:2::3/128 tag <0-4294967295> anycast

# -- L3, SUB, VLAN, MGMT
# nxos: interface <intf> / ipv6 address dhcp

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / ipv6 address use-link-local-only

# -- L3, SUB, VLAN, LO
# nxos: interface <intf> / ipv6 icmp unreachables

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / ipv6 link-local FE80::1

# -- L3, SUB, VLAN, LO
# nxos: interface <intf> / ipv6 nd dad attempts <0-15>
# nxos: interface <intf> / ipv6 nd hop-limit <0-255>
# nxos: interface <intf> / ipv6 nd mac-extract
# nxos: interface <intf> / ipv6 nd mac-extract exclude nud-phase
# nxos: interface <intf> / ipv6 nd managed-config-flag
# nxos: interface <intf> / ipv6 nd mtu 1280
# nxos: interface <intf> / ipv6 nd ns-interval 1000
# nxos: interface <intf> / ipv6 nd other-config-flag
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295>
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> no-autoconfig
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> no-autoconfig no-onlink
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> no-autoconfig no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> no-autoconfig off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> no-onlink
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> infinite
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> infinite no-autoconfig
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> infinite no-autoconfig no-onlink
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> infinite no-autoconfig no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> infinite no-autoconfig off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> infinite no-onlink
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> infinite no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 <0-4294967295> infinite off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 infinite infinite
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 infinite infinite no-autoconfig
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 infinite infinite no-autoconfig no-onlink
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 infinite infinite no-autoconfig no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 infinite infinite no-autoconfig off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 infinite infinite no-onlink
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 infinite infinite no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 infinite infinite off-link
# nxos: interface <intf> / ipv6 nd prefix 1:2::3/128 no-advertise
# nxos: interface <intf> / ipv6 nd prefix default
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> <0-4294967295>
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> <0-4294967295> no-autoconfig
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> <0-4294967295> no-autoconfig no-onlink
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> <0-4294967295> no-autoconfig no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> <0-4294967295> no-autoconfig off-link
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> <0-4294967295> no-onlink
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> <0-4294967295> no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> <0-4294967295> off-link
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> infinite
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> infinite no-autoconfig
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> infinite no-autoconfig no-onlink
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> infinite no-autoconfig no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> infinite no-autoconfig off-link
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> infinite no-onlink
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> infinite no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix default <0-4294967295> infinite off-link
# nxos: interface <intf> / ipv6 nd prefix default infinite infinite
# nxos: interface <intf> / ipv6 nd prefix default infinite infinite no-autoconfig
# nxos: interface <intf> / ipv6 nd prefix default infinite infinite no-autoconfig no-onlink
# nxos: interface <intf> / ipv6 nd prefix default infinite infinite no-autoconfig no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix default infinite infinite no-autoconfig off-link
# nxos: interface <intf> / ipv6 nd prefix default infinite infinite no-onlink
# nxos: interface <intf> / ipv6 nd prefix default infinite infinite no-onlink off-link
# nxos: interface <intf> / ipv6 nd prefix default infinite infinite off-link
# nxos: interface <intf> / ipv6 nd prefix default no-advertise
# nxos: interface <intf> / ipv6 nd ra dns search-list someword 4 sequence <0-4294967295>
# nxos: interface <intf> / ipv6 nd ra dns search-list someword infinite sequence <0-4294967295>
# nxos: interface <intf> / ipv6 nd ra dns search-list someword sequence <0-4294967295>
# nxos: interface <intf> / ipv6 nd ra dns search-list suppress
# nxos: interface <intf> / ipv6 nd ra dns server 1:2::3 4 sequence <0-4294967295>
# nxos: interface <intf> / ipv6 nd ra dns server 1:2::3 infinite sequence <0-4294967295>
# nxos: interface <intf> / ipv6 nd ra dns server 1:2::3 sequence <0-4294967295>
# nxos: interface <intf> / ipv6 nd ra dns server suppress
# nxos: interface <intf> / ipv6 nd ra route suppress
# nxos: interface <intf> / ipv6 nd ra-interval 4
# nxos: interface <intf> / ipv6 nd ra-interval 4 min <0-1800>
# nxos: interface <intf> / ipv6 nd ra-lifetime <0-9000>
# nxos: interface <intf> / ipv6 nd reachable-time <0-3600000>

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / ipv6 nd redirects

# -- L3, SUB, VLAN, LO
# nxos: interface <intf> / ipv6 nd retrans-timer <0-4294967295>
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference High <0-4294967295>
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference High <0-4294967295> verify-reachability
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference High infinite
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference High infinite verify-reachability
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference Low <0-4294967295>
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference Low <0-4294967295> verify-reachability
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference Low infinite
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference Low infinite verify-reachability
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference Medium <0-4294967295>
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference Medium <0-4294967295> verify-reachability
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference Medium infinite
# nxos: interface <intf> / ipv6 nd route 1:2::3/128 route-preference Medium infinite verify-reachability
# nxos: interface <intf> / ipv6 nd router-preference High
# nxos: interface <intf> / ipv6 nd router-preference Low
# nxos: interface <intf> / ipv6 nd router-preference Medium
# nxos: interface <intf> / ipv6 nd suppress-ra
# nxos: interface <intf> / ipv6 nd suppress-ra mtu

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / ipv6 neighbor 1:2::3 aaaa.bbbb.cccc

# -- ETHER L2, L3, PC
# nxos: interface <intf> / ipv6 port traffic-filter someword in

# -- L3, VLAN, LO, MGMT
# nxos: interface <intf> / ipv6 redirects

# -- ETHER L2, L3, SUB, PC, VLAN, MGMT
# nxos: interface <intf> / ipv6 traffic-filter someword in
# nxos: interface <intf> / ipv6 traffic-filter someword out

# -- ETHER L2, L3, SUB, PC, VLAN, LO
# nxos: interface <intf> / ipv6 unreachables

# -- ETHER L2, L3, SUB
# nxos: interface <intf> / link debounce
# nxos: interface <intf> / link debounce time <0-5000>

# -- ETHER L2, L3, PC, VLAN
# nxos: interface <intf> / load-interval 5
# nxos: interface <intf> / load-interval counter 1 5

# -- ETHER L2, L3, SUB, PC, LO
# nxos: interface <intf> / logging event port link-status
# nxos: interface <intf> / logging event port link-status default

# -- ETHER L2, L3, PC
# nxos: interface <intf> / logging event port trunk-status
# nxos: interface <intf> / logging event port trunk-status default
# nxos: interface <intf> / mac port access-group someword

# -- ETHER L2, L3, SUB, PC, VLAN
# nxos: interface <intf> / mac-address aaaa.bbbb.cccc

# -- ETHER L2, L3, SUB, PC
# nxos: interface <intf> / mac-address ipv6-extract

# -- ETHER L2, L3, SUB, PC, VLAN
# nxos: interface <intf> / mtu 1500

# -- ETHER L2, L3, PC
# nxos: interface <intf> / negotiate auto

# -- ETHER L2, L3, SUB, PC
# nxos: interface <intf> / priority-flow-control mode auto
# nxos: interface <intf> / priority-flow-control mode off
# nxos: interface <intf> / priority-flow-control mode on
# nxos: interface <intf> / priority-flow-control watch-dog-timer off
# nxos: interface <intf> / priority-flow-control watch-dog-timer on
# nxos: interface <intf> / service-policy input someword
# nxos: interface <intf> / service-policy input someword no-stats
# nxos: interface <intf> / service-policy output someword
# nxos: interface <intf> / service-policy output someword no-stats
# nxos: interface <intf> / service-policy type qos input someword
# nxos: interface <intf> / service-policy type qos input someword no-stats
# nxos: interface <intf> / service-policy type qos output someword
# nxos: interface <intf> / service-policy type qos output someword no-stats

# -- ETHER L2, L3, PC
# nxos: interface <intf> / service-policy type queuing input someword
# nxos: interface <intf> / service-policy type queuing input someword no-stats
# nxos: interface <intf> / service-policy type queuing input default-out-policy
# nxos: interface <intf> / service-policy type queuing input default-out-policy no-stats
# nxos: interface <intf> / service-policy type queuing output someword
# nxos: interface <intf> / service-policy type queuing output someword no-stats
# nxos: interface <intf> / service-policy type queuing output default-out-policy
# nxos: interface <intf> / service-policy type queuing output default-out-policy no-stats

# -- ETHER L2, L3, SUB, NVE, PC, VLAN, LO
# nxos: interface <intf> / shutdown

# -- ETHER L2, L3, SUB, NVE, PC, LO
# nxos: interface <intf> / shutdown force

# -- L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / site-of-origin 100:200000
# nxos: interface <intf> / site-of-origin 100000:200
# nxos: interface <intf> / site-of-origin 1.2.3.4:1

# -- ETHER L2, L3, SUB, PC, VLAN, MGMT
# nxos: interface <intf> / snmp trap link-status

# -- ETHER L2, L3, PC, MGMT
# nxos: interface <intf> / speed 100
# nxos: interface <intf> / speed 1000

# -- ETHER L2, L3, PC
# nxos: interface <intf> / speed 10000
# nxos: interface <intf> / speed 100000
# nxos: interface <intf> / speed 25000
# nxos: interface <intf> / speed 40000

# -- ETHER L2, L3, PC, MGMT
# nxos: interface <intf> / speed auto
# nxos: interface <intf> / speed auto 100
# nxos: interface <intf> / speed auto 100 1000

# -- ETHER L2, L3, PC
# nxos: interface <intf> / storm-control action shutdown
# nxos: interface <intf> / storm-control action trap

# -- ETHER L2, L3, SUB, VLAN, LO, MGMT
# nxos: interface <intf> / vrf member someword

# -- VTP?
# nxos: interface <intf> / vtp

Interface._build_name_to_class_map()
