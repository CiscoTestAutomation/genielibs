'''
    Interface classes for iosxr OS.
'''

__all__ = (
    'Interface',
    'PhysicalInterface',
    'VirtualInterface',
    'PseudoInterface',
    'LoopbackInterface',
    'EthernetInterface',
    'SubInterface',
    'MgmtEthernetInterface',
    'TunnelInterface',
    'NamedTunnelInterface',
    'TunnelTeInterface',
    'NamedTunnelTeInterface',
    'BundleEtherInterface',
    'BundlePosInterface',
    'BviInterface',
    'NveInterface',
)

import re
import contextlib
import abc
from enum import Enum

from genie.decorator import managedattribute, mixedmethod
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
from genie.libs.conf.l2vpn import IccpGroup

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
    """ base Interface class for IOS-XR devices
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

    @property
    def interface_location(self):
        '''The location part of the interface name (str).

        On IOS-XR, this is always the R/S/I/P.

        Examples:
            GigabitEthernet0/0/0/0 -> '0/0/0/0'
            GigabitEthernet0/0/0/0.2 -> '0/0/0/0'
            Bundle-Ether1.2 -> None
            tunnel-te1 -> None
            GCC0 -> None
            POS0/0/0/0/2 -> '0/0/0/0'
        '''

        # The Parent interface may know more about the location.
        parent_interface = self.parent_interface
        if parent_interface is not None:
            return parent_interface.interface_location

        d_parsed = self.parse_interface_name()
        return d_parsed.rsip

    @property
    def interface_cpu_slot(self):
        '''The CPU slot interface (str).

        Examples:
            GigabitEthernet0/1/2/0 -> '0/1/CPU0'
            GigabitEthernet0/1/2/0.2 -> '0/1/CPU0'
            Bundle-Ether1.2 -> None
            tunnel-te1 -> None
            GCC0 -> None
            POS0/1/2/0/2 -> '0/1/CPU0'
        '''

        # The Parent interface may know more about the CPU slot.
        parent_interface = self.parent_interface
        if parent_interface is not None:
            return parent_interface.interface_cpu_slot

        d_parsed = self.parse_interface_name()
        return d_parsed.cpu

    parent_controller = managedattribute(
        name='parent_controller',
        read_only=True,  # TODO Perhaps some derived classes can allow write
        doc='''The parent controller. Only meaningful for a few Interface subclasses.''')

    # TODO
    # ATM -> 'SONET' (no E3/T3 mode) or 'ATM'
    # Serial -> None (if flow_bw is POS) or 'SERIAL'
    # OTU1 - OTU1E - OTU1F - OTU2 - OTU2E - OTU2F - OTU3 - OTU3E1 - OTU3E2 - OTU4 -> 'Optics'
    # ODU0 - ODU1 - ODU1E - ODU1F - ODU2 - ODU2E - ODU2F - ODU3 - ODU3E1 - ODU3E2 - ODU4 - GCC0 - GCC1 -> return from parent

    @parent_controller.defaulter
    def parent_controller(self):
        parent_interface = self.parent_interface
        if parent_interface:
            return parent_interface.parent_controller
        # ODU* and GCC*, return parent_interface
        parent_controller_type = self.parent_controller_type
        if parent_controller_type is not None:
            location = self.interface_location
            if location is not None:
                parent_controller_name = parent_controller_type + location
                return self.device.interfaces[parent_controller_name]
        return None

    anycast_source_interface = managedattribute(
        name='anycast_source_interface',
        default=None,
        # Fixup once Interface is defined:
        # type=(None, managedattribute.test_isinstance(Interface)),
    )

    anycast_source_interface_sync_group = managedattribute(
        name='anycast_source_interface_sync_group',
        default=None,
        type=(None, IPv4Address))

    bundle = managedattribute(
        name='bundle',
        default=None)

    @bundle.setter
    def bundle(self, bundle):
        if bundle and not isinstance(bundle, BundleInterface):
            raise ValueError('%r is not a bundle interface' % (bundle,))
        if bundle and bundle.device is not self.device:
            raise ValueError('%r cannot be a member of %r' % (self, bundle))
        self._bundle = bundle

    class BundleMode(Enum):
        on = 'on'
        active = 'active'
        passive = 'passive'

    bundle_mode = managedattribute(
        name='bundle_mode',
        default=None,  # Default's to bundle.bundle_mode
        type=(None, BundleMode))

    bundle_port_priority = None

    bundle_port_priority = managedattribute(
        name='bundle_port_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ipv4_route_tag = managedattribute(
        name='ipv4_route_tag',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    secondary_ipv4 = managedattribute(
        name='secondary_ipv4',
        default=None,
        type=(None, IPv4Interface))

    secondary_ipv4_route_tag = managedattribute(
        name='secondary_ipv4_route_tag',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ipv6_eui64 = managedattribute(
        name='ipv6_eui64',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ipv6_route_tag = managedattribute(
        name='ipv6_route_tag',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ipv6_link_local = managedattribute(
        name='ipv6_link_local',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    rewrite_ingress_tag_pop_symmetric = managedattribute(
        name='rewrite_ingress_tag_pop_symmetric',
        default=None,
        type=(None, managedattribute.test_in((
            1,
            2,
        ))))

    rewrite_ingress_tag_translate_1_to_1_dot1q_symmetric = managedattribute(
        name='rewrite_ingress_tag_translate_1_to_1_dot1q_symmetric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    class L2transportAttributes(ConfigurableInterfaceNamespace):

        # iosxr: interface {name} / l2transport (config-if-l2)
        enabled = False

        # iosxr: interface {name} / l2transport / l2protocol cdp drop
        # iosxr: interface {name} / l2transport / l2protocol cdp forward
        # iosxr: interface {name} / l2transport / l2protocol cdp forward experimental <0-7>
        # iosxr: interface {name} / l2transport / l2protocol cdp tunnel
        # iosxr: interface {name} / l2transport / l2protocol cdp tunnel experimental <0-7>
        # iosxr: interface {name} / l2transport / l2protocol cpsv drop
        # iosxr: interface {name} / l2transport / l2protocol cpsv reverse-tunnel
        # iosxr: interface {name} / l2transport / l2protocol cpsv tunnel
        # iosxr: interface {name} / l2transport / l2protocol pvst drop
        # iosxr: interface {name} / l2transport / l2protocol pvst forward
        # iosxr: interface {name} / l2transport / l2protocol pvst forward experimental <0-7>
        # iosxr: interface {name} / l2transport / l2protocol pvst tunnel
        # iosxr: interface {name} / l2transport / l2protocol pvst tunnel experimental <0-7>
        # iosxr: interface {name} / l2transport / l2protocol stp drop
        # iosxr: interface {name} / l2transport / l2protocol stp forward
        # iosxr: interface {name} / l2transport / l2protocol stp forward experimental <0-7>
        # iosxr: interface {name} / l2transport / l2protocol stp tunnel
        # iosxr: interface {name} / l2transport / l2protocol stp tunnel experimental <0-7>
        # iosxr: interface {name} / l2transport / l2protocol vtp drop
        # iosxr: interface {name} / l2transport / l2protocol vtp forward
        # iosxr: interface {name} / l2transport / l2protocol vtp forward experimental <0-7>
        # iosxr: interface {name} / l2transport / l2protocol vtp tunnel
        # iosxr: interface {name} / l2transport / l2protocol vtp tunnel experimental <0-7>
        # iosxr: interface {name} / l2transport / propagate remote-status
        # iosxr: interface {name} / l2transport / service-policy input someword
        # iosxr: interface {name} / l2transport / service-policy output someword

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: interface {name} / l2transport (config-if-l2)
            if attributes.value('enabled', force=True):
                use_l2transport_submode = not isinstance(self.interface, SubInterface)
                with configurations.submode_context('l2transport' if use_l2transport_submode else None):
                    if use_l2transport_submode and unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: interface {name} / l2transport / l2protocol cdp drop
                    # iosxr: interface {name} / l2transport / l2protocol cdp forward
                    # iosxr: interface {name} / l2transport / l2protocol cdp forward experimental <0-7>
                    # iosxr: interface {name} / l2transport / l2protocol cdp tunnel
                    # iosxr: interface {name} / l2transport / l2protocol cdp tunnel experimental <0-7>
                    # iosxr: interface {name} / l2transport / l2protocol cpsv drop
                    # iosxr: interface {name} / l2transport / l2protocol cpsv reverse-tunnel
                    # iosxr: interface {name} / l2transport / l2protocol cpsv tunnel
                    # iosxr: interface {name} / l2transport / l2protocol pvst drop
                    # iosxr: interface {name} / l2transport / l2protocol pvst forward
                    # iosxr: interface {name} / l2transport / l2protocol pvst forward experimental <0-7>
                    # iosxr: interface {name} / l2transport / l2protocol pvst tunnel
                    # iosxr: interface {name} / l2transport / l2protocol pvst tunnel experimental <0-7>
                    # iosxr: interface {name} / l2transport / l2protocol stp drop
                    # iosxr: interface {name} / l2transport / l2protocol stp forward
                    # iosxr: interface {name} / l2transport / l2protocol stp forward experimental <0-7>
                    # iosxr: interface {name} / l2transport / l2protocol stp tunnel
                    # iosxr: interface {name} / l2transport / l2protocol stp tunnel experimental <0-7>
                    # iosxr: interface {name} / l2transport / l2protocol vtp drop
                    # iosxr: interface {name} / l2transport / l2protocol vtp forward
                    # iosxr: interface {name} / l2transport / l2protocol vtp forward experimental <0-7>
                    # iosxr: interface {name} / l2transport / l2protocol vtp tunnel
                    # iosxr: interface {name} / l2transport / l2protocol vtp tunnel experimental <0-7>
                    # iosxr: interface {name} / l2transport / propagate remote-status
                    # iosxr: interface {name} / l2transport / service-policy input someword
                    # iosxr: interface {name} / l2transport / service-policy output someword
                    pass

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    l2transport = managedattribute(
        name='l2transport',
        read_only=True,
        doc=L2transportAttributes.__doc__)

    @l2transport.initter
    def l2transport(self):
        return self.L2transportAttributes(interface=self)

    lacp_period = managedattribute(
        name='lacp_period',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    lacp_period_short = managedattribute(
        name='lacp_period_short',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    class MplsAttributes(ConfigurableInterfaceNamespace):

        # iosxr: interface {name} / mpls (config-if-mpls)
        enabled = managedattribute(
            name='enabled',
            default=False,
            type=managedattribute.test_istype(bool))

        # iosxr: interface {name} / mpls / label-security multi-label-packet drop
        # iosxr: interface {name} / mpls / label-security rpf
        # iosxr: interface {name} / mpls / mtu 68

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # iosxr: interface {name} / mpls (config-if-mpls)
            if attributes.value('enabled', force=True):
                with configurations.submode_context('mpls', cancel_empty=True):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: interface {name} / mpls / label-security multi-label-packet drop
                    # iosxr: interface {name} / mpls / label-security rpf
                    # iosxr: interface {name} / mpls / mtu 68

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    mpls = managedattribute(
        name='mpls',
        read_only=True,
        doc=MplsAttributes.__doc__)

    @mpls.initter
    def mpls(self):
        return self.MplsAttributes(interface=self)

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
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
        # iosxr: interface {name} (config-if)
        return configurations.submode_context('interface {}'.format(self.name))

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

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

        # iosxr: interface {name} / aaa radius attribute nas-identifier someword
        # iosxr: interface {name} / aaa radius attribute nas-port-type <0-44>
        # iosxr: interface {name} / aaa radius attribute nas-port-type ADSL-CAP
        # iosxr: interface {name} / aaa radius attribute nas-port-type ADSL-DMT
        # iosxr: interface {name} / aaa radius attribute nas-port-type Async
        # iosxr: interface {name} / aaa radius attribute nas-port-type CABLE
        # iosxr: interface {name} / aaa radius attribute nas-port-type Ethernet
        # iosxr: interface {name} / aaa radius attribute nas-port-type FDDI
        # iosxr: interface {name} / aaa radius attribute nas-port-type FTTP
        # iosxr: interface {name} / aaa radius attribute nas-port-type G3FAX
        # iosxr: interface {name} / aaa radius attribute nas-port-type HDLC-CLEAR-CHANNEL
        # iosxr: interface {name} / aaa radius attribute nas-port-type IAPP
        # iosxr: interface {name} / aaa radius attribute nas-port-type IDSL
        # iosxr: interface {name} / aaa radius attribute nas-port-type IPOEOE
        # iosxr: interface {name} / aaa radius attribute nas-port-type IPOEOQINQ
        # iosxr: interface {name} / aaa radius attribute nas-port-type IPOEOVLAN
        # iosxr: interface {name} / aaa radius attribute nas-port-type IPSEC
        # iosxr: interface {name} / aaa radius attribute nas-port-type ISDN
        # iosxr: interface {name} / aaa radius attribute nas-port-type ISDN-Async-PIAFS
        # iosxr: interface {name} / aaa radius attribute nas-port-type ISDN-Async-V110
        # iosxr: interface {name} / aaa radius attribute nas-port-type ISDN-Async-V120
        # iosxr: interface {name} / aaa radius attribute nas-port-type PPPoA
        # iosxr: interface {name} / aaa radius attribute nas-port-type PPPoEoA
        # iosxr: interface {name} / aaa radius attribute nas-port-type PPPoEoE
        # iosxr: interface {name} / aaa radius attribute nas-port-type PPPoEoQinQ
        # iosxr: interface {name} / aaa radius attribute nas-port-type PPPoEoVLAN
        # iosxr: interface {name} / aaa radius attribute nas-port-type SDSL-SYM-SL
        # iosxr: interface {name} / aaa radius attribute nas-port-type Sync
        # iosxr: interface {name} / aaa radius attribute nas-port-type TOKEN-RING
        # iosxr: interface {name} / aaa radius attribute nas-port-type VIRTUAL-IPOEOE
        # iosxr: interface {name} / aaa radius attribute nas-port-type VIRTUAL-IPOEOQINQ
        # iosxr: interface {name} / aaa radius attribute nas-port-type VIRTUAL-IPOEOVLAN
        # iosxr: interface {name} / aaa radius attribute nas-port-type Virtual
        # iosxr: interface {name} / aaa radius attribute nas-port-type Virtual-PPPoEoE
        # iosxr: interface {name} / aaa radius attribute nas-port-type Virtual-PPPoEoQinaQ
        # iosxr: interface {name} / aaa radius attribute nas-port-type Virtual-PPPoEoVLAN
        # iosxr: interface {name} / aaa radius attribute nas-port-type WIRELESS-1X-EV
        # iosxr: interface {name} / aaa radius attribute nas-port-type WIRELESS-CDMA
        # iosxr: interface {name} / aaa radius attribute nas-port-type WIRELESS-IEEE-802-11
        # iosxr: interface {name} / aaa radius attribute nas-port-type WIRELESS-IEEE-802-16
        # iosxr: interface {name} / aaa radius attribute nas-port-type WIRELESS-IEEE-802-20
        # iosxr: interface {name} / aaa radius attribute nas-port-type WIRELESS-IEEE-802-22
        # iosxr: interface {name} / aaa radius attribute nas-port-type WIRELESS-OTHER
        # iosxr: interface {name} / aaa radius attribute nas-port-type WIRELESS-UMTS
        # iosxr: interface {name} / aaa radius attribute nas-port-type X25
        # iosxr: interface {name} / aaa radius attribute nas-port-type X75
        # iosxr: interface {name} / aaa radius attribute nas-port-type XDSL

        # iosxr: interface {name} / address-family ipv4 multicast
        # iosxr: interface {name} / address-family ipv4 multicast topology someword
        # iosxr: interface {name} / address-family ipv6 multicast
        # iosxr: interface {name} / address-family ipv6 multicast topology someword

        # iosxr: interface {name} / anycast source-interface Loopback0
        cfg = attributes.format('anycast source-interface {anycast_source_interface}')
        if cfg:
            # iosxr: interface {name} / anycast source-interface Loopback0 sync-group 1.2.3.4
            cfg += attributes.format(' sync-group {anycast_source_interface_sync_group}', force=True)
            configurations.append_line(cfg)

        # iosxr: interface {name} / arp dagr (config-if-dagr)
        # iosxr: interface {name} / arp dagr / peer ipv4 1.2.3.4 (config-if-dagr-peer)
        # iosxr: interface {name} / arp dagr / peer ipv4 1.2.3.4 / priority-timeout 1
        # iosxr: interface {name} / arp dagr / peer ipv4 1.2.3.4 / route distance normal <0-256> priority <0-256>
        # iosxr: interface {name} / arp dagr / peer ipv4 1.2.3.4 / route metric normal <0-256> priority <0-256>
        # iosxr: interface {name} / arp dagr / peer ipv4 1.2.3.4 / timers query 1 standby 1
        # iosxr: interface {name} / arp gratuitous ignore
        # iosxr: interface {name} / arp learning disable
        # iosxr: interface {name} / arp learning local
        # iosxr: interface {name} / arp purge-delay 1
        # iosxr: interface {name} / arp timeout 30

        # iosxr: interface {name} / auto-ip-ring 1 ipv4-address 1.2.3.4

        # bandwidth : interface {name} / bandwidth <0-4294967295>
        configurations.append_line(attributes.format('bandwidth {bandwidth}'),\
            unconfig_cmd='no bandwidth')

        # link_status : N/A

        # iosxr: interface {name} / bundle id 1
        # iosxr: interface {name} / bundle id 1 mode active
        # iosxr: interface {name} / bundle id 1 mode on
        # iosxr: interface {name} / bundle id 1 mode passive
        cfg = attributes.format('bundle id {bundle.interface_number}')
        if cfg:
            bundle_mode = attributes.value('bundle_mode', force=True)
            if bundle_mode is None:
                bundle_mode = self.bundle.bundle_mode
            if bundle_mode is not None:
                cfg += ' mode {}'.format(bundle_mode.value)
            configurations.append_line(cfg)

        # iosxr: interface {name} / bundle port-priority 1
        configurations.append_line(attributes.format('bundle port-priority {bundle_port_priority}'))

        # iosxr: interface {name} / carrier-delay down <0-2147483647>
        # iosxr: interface {name} / carrier-delay down <0-2147483647> up <0-2147483647>
        # iosxr: interface {name} / carrier-delay up <0-2147483647>

        # iosxr: interface {name} / cdp
        if attributes.value('cdp'):
            configurations.append_line('cdp')

        # iosxr: interface {name} / cdp-mac-address ethernet-slow-protocols-mac

        # iosxr: interface {name} / dampening
        # iosxr: interface {name} / dampening 1
        # iosxr: interface {name} / dampening 1 1 1 1
        # iosxr: interface {name} / dampening 1 1 1 1 <0-20000>

        # iosxr: interface {name} / description some line data
        v = attributes.value('description')
        if v:
            if v is True:
                pass  # TODO Create a usefull default description
            configurations.append_line('description {}'.format(v),\
                unconfig_cmd='no description')

        # iosxr: interface {name} / dot1q native vlan 1
        # iosxr: interface {name} / dot1q tunneling ethertype 0x9100
        # iosxr: interface {name} / dot1q tunneling ethertype 0x9200
        if attributes.value ('eth_dot1q_type'):
            if attributes.value('eth_dot1q_value'):
                configurations.append_line(
                    attributes.format(
                        'dot1q {eth_dot1q_type} {eth_dot1q_value}'))

        # iosxr: interface {name}.1 / encapsulation ambiguous dot1ad 1 dot1q any ...
        # iosxr: interface {name}.1 / encapsulation ambiguous dot1ad any ...
        # iosxr: interface {name}.1 / encapsulation ambiguous dot1ad any dot1q any ...
        # iosxr: interface {name}.1 / encapsulation ambiguous dot1q 1 second-dot1q any ...
        # iosxr: interface {name}.1 / encapsulation ambiguous dot1q any ...
        # iosxr: interface {name}.1 / encapsulation ambiguous dot1q any second-dot1q any ...

        # iosxr: interface {name}.1 / encapsulation dot1ad 1
        # iosxr: interface {name}.1 / encapsulation dot1ad 1 dot1q 1
        # iosxr: interface {name}.1 / encapsulation dot1q 1
        # iosxr: interface {name}.1 / encapsulation dot1q 1 second-dot1q 1
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


        # encapsulation,first_dot1q,second_dot1q : encapsulation <encapsulation> <first_dot1q> [second-dot1q <second_dot1q>]
        if attributes.value('encapsulation'):
            encapsulation = attributes.value('encapsulation').name
            first_dot1q = attributes.value('first_dot1q')
            second_dot1q = attributes.value('second_dot1q')
            if (encapsulation == 'dot1q') and (isinstance(self, SubInterface)):
                if first_dot1q and second_dot1q:
                    cmd = 'encapsulation {} {} second-dot1q {}'\
                        .format(encapsulation, first_dot1q, second_dot1q)
                elif first_dot1q:
                    cmd = 'encapsulation {} {}'\
                        .format(encapsulation, first_dot1q)
                elif second_dot1q:
                    cmd = 'encapsulation {} {}'\
                        .format(encapsulation, first_dot1q)
                configurations.append_line(cmd)

        # dhcp : N/A

        # iosxr: interface {name}.1 / encapsulation default
        # iosxr: interface {name}.1 / encapsulation untagged
        # iosxr: interface {name}.1 / encapsulation untagged ingress source-mac aaaa.bbbb.cccc
        # iosxr: interface {name}.1 / encapsulation ... TODO

        # iosxr: interface {name} / ethernet cfm (config-if-cfm)
        # iosxr: interface {name} / ethernet cfm / ais transmission up
        # iosxr: interface {name} / ethernet cfm / ais transmission up cos <0-7>
        # iosxr: interface {name} / ethernet cfm / ais transmission up cos <0-7> interval 1s
        # iosxr: interface {name} / ethernet cfm / ais transmission up cos <0-7> interval 1m
        # iosxr: interface {name} / ethernet cfm / ais transmission up interval 1s
        # iosxr: interface {name} / ethernet cfm / ais transmission up interval 1m
        # iosxr: interface {name} / ethernet cfm / bandwidth-notifications (config-if-cfm-bw-ntfn)
        # iosxr: interface {name} / ethernet cfm / bandwidth-notifications / hold-off <0-600>
        # iosxr: interface {name} / ethernet cfm / bandwidth-notifications / log changes
        # iosxr: interface {name} / ethernet cfm / bandwidth-notifications / loss-threshold 2
        # iosxr: interface {name} / ethernet cfm / bandwidth-notifications / wait-to-restore <0-600>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 (config-if-cfm-mep)
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / cos <0-7>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters aggregate
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters priority <0-7>-...
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters priority <0-7>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters priority <0-7> <0-7>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters priority <0-7> <0-7> <0-7>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters priority <0-7> <0-7> <0-7> <0-7>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters priority <0-7> <0-7> <0-7> <0-7> <0-7>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters priority <0-7> <0-7> <0-7> <0-7> <0-7> <0-7>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters priority <0-7> <0-7> <0-7> <0-7> <0-7> <0-7> <0-7>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / loss-measurement counters priority <0-7> <0-7> <0-7> <0-7> <0-7> <0-7> <0-7> <0-7>
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / sla operation profile someword3 target mac-address aaaa.bbbb.cccc
        # iosxr: interface {name} / ethernet cfm / mep domain someword service someword2 mep-id 1 / sla operation profile someword3 target mep-id 1
        # iosxr: interface {name} / ethernet filtering dot1ad
        # iosxr: interface {name} / ethernet filtering dot1q
        # iosxr: interface {name} / ethernet filtering mac-relay
        # iosxr: interface {name} / ethernet lmi (config-if-elmi)
        # iosxr: interface {name} / ethernet lmi / extension remote-uni disable
        # iosxr: interface {name} / ethernet lmi / log errors disable
        # iosxr: interface {name} / ethernet lmi / log events disable
        # iosxr: interface {name} / ethernet lmi / polling-verification-timer 5
        # iosxr: interface {name} / ethernet lmi / polling-verification-timer disable
        # iosxr: interface {name} / ethernet lmi / status-counter 2
        # iosxr: interface {name} / ethernet loopback (config-if-ethlb)
        # iosxr: interface {name} / ethernet loopback / permit external
        # iosxr: interface {name} / ethernet loopback / permit internal
        # iosxr: interface {name} / ethernet oam (config-if-eoam)
        # iosxr: interface {name} / ethernet oam / action (config-if-eoam-action)
        # iosxr: interface {name} / ethernet oam / action / capabilities-conflict disable
        # iosxr: interface {name} / ethernet oam / action / capabilities-conflict efd
        # iosxr: interface {name} / ethernet oam / action / capabilities-conflict error-disable-interface
        # iosxr: interface {name} / ethernet oam / action / capabilities-conflict log
        # iosxr: interface {name} / ethernet oam / action / critical-event disable
        # iosxr: interface {name} / ethernet oam / action / critical-event error-disable-interface
        # iosxr: interface {name} / ethernet oam / action / critical-event log
        # iosxr: interface {name} / ethernet oam / action / discovery-timeout disable
        # iosxr: interface {name} / ethernet oam / action / discovery-timeout efd
        # iosxr: interface {name} / ethernet oam / action / discovery-timeout error-disable-interface
        # iosxr: interface {name} / ethernet oam / action / discovery-timeout log
        # iosxr: interface {name} / ethernet oam / action / dying-gasp disable
        # iosxr: interface {name} / ethernet oam / action / dying-gasp error-disable-interface
        # iosxr: interface {name} / ethernet oam / action / dying-gasp log
        # iosxr: interface {name} / ethernet oam / action / high-threshold disable
        # iosxr: interface {name} / ethernet oam / action / high-threshold error-disable-interface
        # iosxr: interface {name} / ethernet oam / action / high-threshold log
        # iosxr: interface {name} / ethernet oam / action / remote-loopback disable
        # iosxr: interface {name} / ethernet oam / action / remote-loopback log
        # iosxr: interface {name} / ethernet oam / action / session-down disable
        # iosxr: interface {name} / ethernet oam / action / session-down efd
        # iosxr: interface {name} / ethernet oam / action / session-down error-disable-interface
        # iosxr: interface {name} / ethernet oam / action / session-down log
        # iosxr: interface {name} / ethernet oam / action / session-up disable
        # iosxr: interface {name} / ethernet oam / action / session-up log
        # iosxr: interface {name} / ethernet oam / action / uni-directional link-fault disable
        # iosxr: interface {name} / ethernet oam / action / uni-directional link-fault efd
        # iosxr: interface {name} / ethernet oam / action / uni-directional link-fault error-disable-interface
        # iosxr: interface {name} / ethernet oam / action / uni-directional link-fault log
        # iosxr: interface {name} / ethernet oam / action / wiring-conflict disable
        # iosxr: interface {name} / ethernet oam / action / wiring-conflict efd
        # iosxr: interface {name} / ethernet oam / action / wiring-conflict error-disable-interface
        # iosxr: interface {name} / ethernet oam / action / wiring-conflict log
        # iosxr: interface {name} / ethernet oam / connection timeout 2
        # iosxr: interface {name} / ethernet oam / hello-interval 100ms
        # iosxr: interface {name} / ethernet oam / hello-interval 1s
        # iosxr: interface {name} / ethernet oam / link-monitor (config-if-eoam-lm)
        # iosxr: interface {name} / ethernet oam / link-monitor / frame threshold low 1
        # iosxr: interface {name} / ethernet oam / link-monitor / frame threshold low 1 high 1
        # iosxr: interface {name} / ethernet oam / link-monitor / frame threshold high 1
        # iosxr: interface {name} / ethernet oam / link-monitor / frame window 1000
        # iosxr: interface {name} / ethernet oam / link-monitor / frame-period threshold low 1
        # iosxr: interface {name} / ethernet oam / link-monitor / frame-period threshold low 1 high 1
        # iosxr: interface {name} / ethernet oam / link-monitor / frame-period threshold high 1
        # iosxr: interface {name} / ethernet oam / link-monitor / frame-period window 100
        # iosxr: interface {name} / ethernet oam / link-monitor / frame-seconds threshold low 1
        # iosxr: interface {name} / ethernet oam / link-monitor / frame-seconds threshold low 1 high 1
        # iosxr: interface {name} / ethernet oam / link-monitor / frame-seconds threshold high 1
        # iosxr: interface {name} / ethernet oam / link-monitor / frame-seconds window 10000
        # iosxr: interface {name} / ethernet oam / link-monitor / monitoring
        # iosxr: interface {name} / ethernet oam / link-monitor / monitoring disable
        # iosxr: interface {name} / ethernet oam / link-monitor / symbol-period threshold low 1
        # iosxr: interface {name} / ethernet oam / link-monitor / symbol-period threshold low 1 high 1
        # iosxr: interface {name} / ethernet oam / link-monitor / symbol-period threshold high 1
        # iosxr: interface {name} / ethernet oam / link-monitor / symbol-period window 1000
        # iosxr: interface {name} / ethernet oam / mib-retrieval
        # iosxr: interface {name} / ethernet oam / mib-retrieval disable
        # iosxr: interface {name} / ethernet oam / mode active
        # iosxr: interface {name} / ethernet oam / mode passive
        # iosxr: interface {name} / ethernet oam / profile someword
        # iosxr: interface {name} / ethernet oam / remote-loopback
        # iosxr: interface {name} / ethernet oam / remote-loopback disable
        # iosxr: interface {name} / ethernet oam / require-remote (config-if-eoam-require)
        # iosxr: interface {name} / ethernet oam / require-remote / link-monitoring
        # iosxr: interface {name} / ethernet oam / require-remote / link-monitoring disabled
        # iosxr: interface {name} / ethernet oam / require-remote / mib-retrieval
        # iosxr: interface {name} / ethernet oam / require-remote / mib-retrieval disabled
        # iosxr: interface {name} / ethernet oam / require-remote / mode active
        # iosxr: interface {name} / ethernet oam / require-remote / mode disabled
        # iosxr: interface {name} / ethernet oam / require-remote / mode passive
        # iosxr: interface {name} / ethernet oam / require-remote / remote-loopback
        # iosxr: interface {name} / ethernet oam / require-remote / remote-loopback disabled
        # iosxr: interface {name} / ethernet oam / uni-directional link-fault detection
        # iosxr: interface {name} / ethernet oam / uni-directional link-fault detection disable
        # iosxr: interface {name} / ethernet udld (config-if-udld)
        # iosxr: interface {name} / ethernet udld / destination mac-address aaaa.bbbb.cccc
        # iosxr: interface {name} / ethernet udld / destination mac-address cisco-l2cp
        # iosxr: interface {name} / ethernet udld / destination mac-address ieee-slow-protocols
        # iosxr: interface {name} / ethernet udld / logging disable
        # iosxr: interface {name} / ethernet udld / message-time 7
        # iosxr: interface {name} / ethernet udld / mode aggressive
        # iosxr: interface {name} / ethernet udld / mode normal

        # iosxr: interface {name} / ethernet uni id someword

        # iosxr: interface {name} / ethernet-services access-group someword egress
        # iosxr: interface {name} / ethernet-services access-group someword ingress

        # iosxr: interface {name} / flow ipv4 monitor someword egress
        # iosxr: interface {name} / flow ipv4 monitor someword ingress
        # iosxr: interface {name} / flow ipv4 monitor someword sampler someword2 egress
        # iosxr: interface {name} / flow ipv4 monitor someword sampler someword2 ingress
        # iosxr: interface {name} / flow ipv6 monitor someword egress
        # iosxr: interface {name} / flow ipv6 monitor someword ingress
        # iosxr: interface {name} / flow ipv6 monitor someword sampler someword2 egress
        # iosxr: interface {name} / flow ipv6 monitor someword sampler someword2 ingress
        # iosxr: interface {name} / flow mpls monitor someword egress
        # iosxr: interface {name} / flow mpls monitor someword ingress
        # iosxr: interface {name} / flow mpls monitor someword sampler someword2 egress
        # iosxr: interface {name} / flow mpls monitor someword sampler someword2 ingress

        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 common someword4 common someword5 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 common someword4 common someword5 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 common someword4 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 common someword4 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 common someword4 someword5 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 common someword4 someword5 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 common someword4 someword5 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 common someword4 someword5 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 someword4 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 someword4 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 someword4 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 someword4 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 someword4 someword5 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 someword4 someword5 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 someword4 someword5 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 common someword3 someword4 someword5 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 someword4 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 someword4 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 someword4 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 someword4 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 someword4 someword5 ingress
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 someword4 someword5 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 someword4 someword5 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword common someword2 someword3 someword4 someword5 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword ingress
        # iosxr: interface {name} / ipv4 access-group common someword ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword someword2 ingress
        # iosxr: interface {name} / ipv4 access-group common someword someword2 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword someword2 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword someword2 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword someword2 someword3 ingress
        # iosxr: interface {name} / ipv4 access-group common someword someword2 someword3 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword someword2 someword3 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword someword2 someword3 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword someword2 someword3 someword4 ingress
        # iosxr: interface {name} / ipv4 access-group common someword someword2 someword3 someword4 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group common someword someword2 someword3 someword4 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group common someword someword2 someword3 someword4 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword egress
        # iosxr: interface {name} / ipv4 access-group someword egress compress level <0-3>
        # iosxr: interface {name} / ipv4 access-group someword egress compress level <0-3> hardware-count
        # iosxr: interface {name} / ipv4 access-group someword egress compress level <0-3> hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword egress compress level <0-3> interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword egress hardware-count
        # iosxr: interface {name} / ipv4 access-group someword egress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword egress interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword ingress
        # iosxr: interface {name} / ipv4 access-group someword ingress compress level <0-3>
        # iosxr: interface {name} / ipv4 access-group someword ingress compress level <0-3> hardware-count
        # iosxr: interface {name} / ipv4 access-group someword ingress compress level <0-3> hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword ingress compress level <0-3> interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group someword ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword someword2 ingress
        # iosxr: interface {name} / ipv4 access-group someword someword2 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group someword someword2 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword someword2 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 ingress
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 someword4 ingress
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 someword4 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 someword4 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 someword4 ingress interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 someword4 someword5 ingress
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 someword4 someword5 ingress hardware-count
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 someword4 someword5 ingress hardware-count interface-statistics
        # iosxr: interface {name} / ipv4 access-group someword someword2 someword3 someword4 someword5 ingress interface-statistics

        # iosxr: interface {name} / ipv4 address 1.2.3.0/24
        # iosxr: interface {name} / ipv4 address 1.2.3.0/24 route-tag 1
        # vrf: interface {name} / vrf <vr>
        configurations.append_line(
            attributes.format('vrf {vrf.name}'))
        if self.l2transport.enabled and isinstance(self, SubInterface):
            pass  # not supported
        elif isinstance(self, (TunnelInterface,)):
            pass  # not supported
        else:
            cfg = attributes.format('ipv4 address {ipv4.with_prefixlen}', unconfig_cmd='no ipv4 address')
            if cfg:
                if not unconfig:
                    cfg += attributes.format(' route-tag {ipv4_route_tag}', force=True)
                if 'ipv4 address' not in str(configurations):
                    configurations.append_line(cfg)

        # iosxr: interface {name} / ipv4 address 1.2.3.0/24 secondary
        # iosxr: interface {name} / ipv4 address 1.2.3.0/24 secondary route-tag 1
        if self.l2transport.enabled and isinstance(self, SubInterface):
            pass  # not supported
        elif isinstance(self, (TunnelInterface,)):
            pass  # not supported
        else:
            cfg = attributes.format('ipv4 address {secondary_ipv4.with_prefixlen} secondary')
            if cfg:
                cfg += attributes.format(' route-tag {secondary_ipv4_route_tag}', force=True)
                configurations.append_line(cfg)

        # iosxr: interface {name} / ipv4 bgp policy accounting input destination-accounting
        # iosxr: interface {name} / ipv4 bgp policy accounting input destination-accounting source-accounting
        # iosxr: interface {name} / ipv4 bgp policy accounting input source-accounting
        # iosxr: interface {name} / ipv4 bgp policy accounting output destination-accounting
        # iosxr: interface {name} / ipv4 bgp policy accounting output destination-accounting source-accounting
        # iosxr: interface {name} / ipv4 bgp policy accounting output source-accounting
        # iosxr: interface {name} / ipv4 bgp policy propagation input flow-tag destination
        # iosxr: interface {name} / ipv4 bgp policy propagation input flow-tag source
        # iosxr: interface {name} / ipv4 bgp policy propagation input ip-precedence destination
        # iosxr: interface {name} / ipv4 bgp policy propagation input ip-precedence destination qos-group destination
        # iosxr: interface {name} / ipv4 bgp policy propagation input ip-precedence destination qos-group source
        # iosxr: interface {name} / ipv4 bgp policy propagation input ip-precedence source
        # iosxr: interface {name} / ipv4 bgp policy propagation input ip-precedence source qos-group source
        # iosxr: interface {name} / ipv4 bgp policy propagation input qos-group destination
        # iosxr: interface {name} / ipv4 bgp policy propagation input qos-group source

        # iosxr: interface {name} / ipv4 directed-broadcast
        # iosxr: interface {name} / ipv4 flowspec disable
        # iosxr: interface {name} / ipv4 helper-address 1.2.3.4
        # iosxr: interface {name} / ipv4 helper-address vrf someword 1.2.3.4
        # iosxr: interface {name} / ipv4 mask-reply
        # iosxr: interface {name} / ipv4 mtu 68
        # medium : interface {name} / ipv4 point-to-point
        medium = attributes.value('medium')
        if medium:
            if medium.name == 'p2p':
                configurations.append_line('ipv4 point-to-point', 
                    unconfig_cmd='no ipv4 point-to-point')
            elif medium.name == 'broadcast':
                configurations.append_line('no ipv4 point-to-point', 
                    unconfig_cmd='ipv4 point-to-point')

        # delay : N/A

        # iosxr: interface {name} / ipv4 redirects
        # iosxr: interface {name} / ipv4 tcp-mss-adjust enable
        # iosxr: interface {name} / ipv4 ttl-propagate disable

        # unnumbered_intf_ref : interface {name} / ipv4 unnumbered Bundle-Ether1
        configurations.append_line(
            attributes.format(
                attributes.format('ipv4 unnumbered {unnumbered_intf_ref}')))

        # ipv6_unnumbered_intf_ref : N/A

        # iosxr: interface {name} / ipv4 unreachables disable

        # iosxr: interface {name} / ipv4 verify unicast source reachable-via any
        # iosxr: interface {name} / ipv4 verify unicast source reachable-via any allow-default
        # iosxr: interface {name} / ipv4 verify unicast source reachable-via any allow-default allow-self-ping
        # iosxr: interface {name} / ipv4 verify unicast source reachable-via any allow-self-ping
        # iosxr: interface {name} / ipv4 verify unicast source reachable-via rx
        # iosxr: interface {name} / ipv4 verify unicast source reachable-via rx allow-default
        # iosxr: interface {name} / ipv4 verify unicast source reachable-via rx allow-default allow-self-ping
        # iosxr: interface {name} / ipv4 verify unicast source reachable-via rx allow-self-ping

        # iosxr: interface {name} / ipv6 access-group common someword common someword2 common someword3 common someword4 common someword5 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 common someword3 common someword4 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 common someword3 common someword4 someword5 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 common someword3 common someword4 someword5 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 common someword3 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 common someword3 someword4 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 common someword3 someword4 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 common someword3 someword4 someword5 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 common someword3 someword4 someword5 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 someword3 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 someword3 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 someword3 someword4 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 someword3 someword4 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 someword3 someword4 someword5 ingress
        # iosxr: interface {name} / ipv6 access-group common someword common someword2 someword3 someword4 someword5 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group common someword ingress
        # iosxr: interface {name} / ipv6 access-group common someword someword2 ingress
        # iosxr: interface {name} / ipv6 access-group common someword someword2 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group common someword someword2 someword3 ingress
        # iosxr: interface {name} / ipv6 access-group common someword someword2 someword3 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group common someword someword2 someword3 someword4 ingress
        # iosxr: interface {name} / ipv6 access-group common someword someword2 someword3 someword4 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group common someword someword2 someword3 someword4 someword5 ingress
        # iosxr: interface {name} / ipv6 access-group common someword someword2 someword3 someword4 someword5 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group someword egress
        # iosxr: interface {name} / ipv6 access-group someword egress compress level <0-3>
        # iosxr: interface {name} / ipv6 access-group someword egress compress level <0-3> interface-statistics
        # iosxr: interface {name} / ipv6 access-group someword egress interface-statistics
        # iosxr: interface {name} / ipv6 access-group someword ingress
        # iosxr: interface {name} / ipv6 access-group someword ingress compress level <0-3>
        # iosxr: interface {name} / ipv6 access-group someword ingress compress level <0-3> interface-statistics
        # iosxr: interface {name} / ipv6 access-group someword ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group someword someword2 ingress
        # iosxr: interface {name} / ipv6 access-group someword someword2 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group someword someword2 someword3 ingress
        # iosxr: interface {name} / ipv6 access-group someword someword2 someword3 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group someword someword2 someword3 someword4 ingress
        # iosxr: interface {name} / ipv6 access-group someword someword2 someword3 someword4 ingress interface-statistics
        # iosxr: interface {name} / ipv6 access-group someword someword2 someword3 someword4 someword5 ingress
        # iosxr: interface {name} / ipv6 access-group someword someword2 someword3 someword4 someword5 ingress interface-statistics

        # iosxr: interface {name} / ipv6 address 1:2::3%zone ...

        # iosxr: interface {name} / ipv6 address 1:2::3/128
        # iosxr: interface {name} / ipv6 address 1:2::3/128 eui-64
        # iosxr: interface {name} / ipv6 address 1:2::3/128 eui-64 route-tag 1
        # iosxr: interface {name} / ipv6 address 1:2::3/128 route-tag 1

        # ipv6_autoconf : ipv6 address autoconfig
        if attributes.value('ipv6_autoconf'):
            configurations.append_line('ipv6 address autoconfig')

        if self.l2transport.enabled and isinstance(self, SubInterface):
            pass  # not supported
        elif isinstance(self, (TunnelInterface,)):
            pass  # not supported
        else:
            cfg = attributes.format('ipv6 address {ipv6.with_prefixlen}', unconfig_cmd='no ipv6 address')
            if cfg:
                if not unconfig:
                    if attributes.value('ipv6_eui64', force=True):
                        cfg += ' eui-64'
                    cfg += attributes.format(' route-tag {ipv6_route_tag}', force=True)
                if 'ipv6 address' not in str(configurations):
                    configurations.append_line(cfg)

        # ipv6_enabled : interface {name} / ipv6 enable
        if attributes.value('ipv6_enabled'):
            configurations.append_line('ipv6 enable')
        else:
            if self.l2transport.enabled and isinstance(self, SubInterface):
                pass  # not supported
            elif isinstance(self, (TunnelInterface,)):
                pass  # not supported
            else:
                if attributes.value('ipv6_link_local'):
                    if 'ipv6 enable' not in str(configurations):
                        configurations.append_line('ipv6 enable')

        # switchport_mode : N/A

        # iosxr: interface {name} / ipv6 flowspec disable
        # iosxr: interface {name} / ipv6 mtu 1280

        # iosxr: interface {name} / ipv6 bgp policy accounting input destination-accounting
        # iosxr: interface {name} / ipv6 bgp policy accounting input destination-accounting source-accounting
        # iosxr: interface {name} / ipv6 bgp policy accounting input source-accounting
        # iosxr: interface {name} / ipv6 bgp policy accounting output destination-accounting
        # iosxr: interface {name} / ipv6 bgp policy accounting output destination-accounting source-accounting
        # iosxr: interface {name} / ipv6 bgp policy accounting output source-accounting
        # iosxr: interface {name} / ipv6 bgp policy propagation input flow-tag destination
        # iosxr: interface {name} / ipv6 bgp policy propagation input flow-tag source
        # iosxr: interface {name} / ipv6 bgp policy propagation input ip-precedence destination
        # iosxr: interface {name} / ipv6 bgp policy propagation input ip-precedence destination qos-group destination
        # iosxr: interface {name} / ipv6 bgp policy propagation input ip-precedence destination qos-group source
        # iosxr: interface {name} / ipv6 bgp policy propagation input ip-precedence source
        # iosxr: interface {name} / ipv6 bgp policy propagation input ip-precedence source qos-group source
        # iosxr: interface {name} / ipv6 bgp policy propagation input qos-group destination
        # iosxr: interface {name} / ipv6 bgp policy propagation input qos-group source

        # iosxr: interface {name} / ipv6 nd cache-limit <0-128000>
        # iosxr: interface {name} / ipv6 nd dad attempts <0-600>
        # iosxr: interface {name} / ipv6 nd managed-config-flag
        # iosxr: interface {name} / ipv6 nd ns-interval 1000
        # iosxr: interface {name} / ipv6 nd other-config-flag
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295>
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 <0-4294967295> <0-4294967295> off-link
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 at 1 January 2003 01:02 1 January 2003 01:02
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 at 1 January 2003 01:02 1 January 2003 01:02 no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 at 1 January 2003 01:02 1 January 2003 01:02 no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 at 1 January 2003 01:02 1 January 2003 01:02 off-link
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 infinite <0-4294967295>
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 infinite <0-4294967295> no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 infinite <0-4294967295> no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 infinite <0-4294967295> off-link
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 infinite infinite
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 infinite infinite no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 infinite infinite no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 infinite infinite off-link
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 no-adv
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix 1:2::3/128 off-link
        # iosxr: interface {name} / ipv6 nd prefix default <0-4294967295> <0-4294967295>
        # iosxr: interface {name} / ipv6 nd prefix default <0-4294967295> <0-4294967295> no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix default <0-4294967295> <0-4294967295> no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix default <0-4294967295> <0-4294967295> off-link
        # iosxr: interface {name} / ipv6 nd prefix default at 1 January 2003 01:02 1 January 2003 01:02
        # iosxr: interface {name} / ipv6 nd prefix default at 1 January 2003 01:02 1 January 2003 01:02 no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix default at 1 January 2003 01:02 1 January 2003 01:02 no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix default at 1 January 2003 01:02 1 January 2003 01:02 off-link
        # iosxr: interface {name} / ipv6 nd prefix default infinite <0-4294967295>
        # iosxr: interface {name} / ipv6 nd prefix default infinite <0-4294967295> no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix default infinite <0-4294967295> no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix default infinite <0-4294967295> off-link
        # iosxr: interface {name} / ipv6 nd prefix default infinite infinite
        # iosxr: interface {name} / ipv6 nd prefix default infinite infinite no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix default infinite infinite no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix default infinite infinite off-link
        # iosxr: interface {name} / ipv6 nd prefix default no-adv
        # iosxr: interface {name} / ipv6 nd prefix default no-autoconfig
        # iosxr: interface {name} / ipv6 nd prefix default no-autoconfig off-link
        # iosxr: interface {name} / ipv6 nd prefix default off-link
        # iosxr: interface {name} / ipv6 nd ra dns search list someword 4
        # iosxr: interface {name} / ipv6 nd ra dns search list someword infinite-lifetime
        # iosxr: interface {name} / ipv6 nd ra dns search list someword zero-lifetime
        # iosxr: interface {name} / ipv6 nd ra dns server 1:2::3 4
        # iosxr: interface {name} / ipv6 nd ra dns server 1:2::3 infinite-lifetime
        # iosxr: interface {name} / ipv6 nd ra dns server 1:2::3 zero-lifetime
        # iosxr: interface {name} / ipv6 nd ra hoplimit unspecified
        # iosxr: interface {name} / ipv6 nd ra mtu suppress
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime <0-4294967295>
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime <0-4294967295> preference high
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime <0-4294967295> preference medium
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime <0-4294967295> preference low
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime infinite-lifetime
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime infinite-lifetime preference high
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime infinite-lifetime preference medium
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime infinite-lifetime preference low
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime zero-lifetime
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime zero-lifetime preference high
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime zero-lifetime preference medium
        # iosxr: interface {name} / ipv6 nd ra specific route 1:2::3/128 Lifetime zero-lifetime preference low
        # iosxr: interface {name} / ipv6 nd ra-interval 4
        # iosxr: interface {name} / ipv6 nd ra-interval 4 3
        # iosxr: interface {name} / ipv6 nd ra-lifetime <0-9000>
        # iosxr: interface {name} / ipv6 nd reachable-time <0-3600000>
        # iosxr: interface {name} / ipv6 nd redirects
        # iosxr: interface {name} / ipv6 nd router-preference high
        # iosxr: interface {name} / ipv6 nd router-preference medium
        # iosxr: interface {name} / ipv6 nd router-preference low
        # iosxr: interface {name} / ipv6 nd suppress-ra

        # iosxr: interface {name} / ipv6 tcp-mss-adjust enable
        # iosxr: interface {name} / ipv6 ttl-propagate disable
        # iosxr: interface {name} / ipv6 unreachables disable
        # iosxr: interface {name} / ipv6 verify unicast source reachable-via any
        # iosxr: interface {name} / ipv6 verify unicast source reachable-via any allow-default
        # iosxr: interface {name} / ipv6 verify unicast source reachable-via any allow-default allow-self-ping
        # iosxr: interface {name} / ipv6 verify unicast source reachable-via any allow-self-ping
        # iosxr: interface {name} / ipv6 verify unicast source reachable-via rx
        # iosxr: interface {name} / ipv6 verify unicast source reachable-via rx allow-default
        # iosxr: interface {name} / ipv6 verify unicast source reachable-via rx allow-default allow-self-ping
        # iosxr: interface {name} / ipv6 verify unicast source reachable-via rx allow-self-ping

        # iosxr: interface {name} / l2transport (config-if-l2)
        ns, attributes2 = attributes.namespace('l2transport')
        if ns is not None:
            configurations.append_block(
                ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

        # iosxr: interface {name} / lacp default-threshold 1
        # iosxr: interface {name} / lacp expire-threshold 1

        # iosxr: interface {name} / lacp period 2
        configurations.append_line(attributes.format('lacp period {lacp_period}'))

        # iosxr: interface {name} / lacp period short
        if attributes.value('lacp_period_short'):
            configurations.append_line('lacp period short')

        # iosxr: interface {name} / lacp period short receive 2
        # iosxr: interface {name} / lacp period short transmit 2

        # iosxr: interface {name} / lldp (config-lldp)
        # iosxr: interface {name} / lldp / destination mac-address (config-dest-mac-address)
        # iosxr: interface {name} / lldp / destination mac-address / ieee-nearest-bridge
        # iosxr: interface {name} / lldp / destination mac-address / ieee-nearest-non-tmpr-bridge
        # iosxr: interface {name} / lldp / receive disable
        # iosxr: interface {name} / lldp / transmit disable

        # load_interval: interface {name} / load-interval <0-600>
        if attributes.value('load_interval'):
            configurations.append_line(
                attributes.format('load-interval {load_interval}'), \
                    unconfig_cmd='no load-interval')


        # iosxr: interface {name} / local-proxy-arp

        # iosxr: interface {name} / loopback external
        # iosxr: interface {name} / loopback internal
        # iosxr: interface {name} / loopback line

        # iosxr: interface {name} / mpls (config-if-mpls)
        ns, attributes2 = attributes.namespace('mpls')
        if ns is not None:
            configurations.append_block(
                ns.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

        # mtu: interface {name} / mtu 64
        configurations.append_line(
            attributes.format('mtu {mtu}'), unconfig_cmd='no mtu')

        # iosxr: interface {name} / nv (config-if-nV)
        # iosxr: interface {name} / nv / satellite-fabric-link network (config-sfl-network)
        # iosxr: interface {name} / nv / satellite-fabric-link network / ethernet cfm (config-cfm)
        # iosxr: interface {name} / nv / satellite-fabric-link network / ethernet cfm / continuity-check interval 3.3ms
        # iosxr: interface {name} / nv / satellite-fabric-link network / ethernet cfm / continuity-check interval 10ms
        # iosxr: interface {name} / nv / satellite-fabric-link network / ethernet cfm / continuity-check interval 100ms
        # iosxr: interface {name} / nv / satellite-fabric-link network / ethernet cfm / continuity-check interval 1s
        # iosxr: interface {name} / nv / satellite-fabric-link network / ethernet cfm / continuity-check interval 10s
        # iosxr: interface {name} / nv / satellite-fabric-link network / ethernet cfm / continuity-check interval 1m
        # iosxr: interface {name} / nv / satellite-fabric-link network / ethernet cfm / continuity-check interval 10m
        # iosxr: interface {name} / nv / satellite-fabric-link network / ethernet cfm / level <0-7>
        # iosxr: interface {name} / nv / satellite-fabric-link network / redundancy (config-nV-red)
        # iosxr: interface {name} / nv / satellite-fabric-link network / redundancy / iccp-group 1
        # iosxr: interface {name} / nv / satellite-fabric-link network / satellite 100 (config-sfl-network-sat)
        # iosxr: interface {name} / nv / satellite-fabric-link network / satellite 100 / remote-ports GigabitEthernet 0/0/1,3-8,9 ...
        # iosxr: interface {name} / nv / satellite-fabric-link network / satellite 100 / remote-ports TenGigE 0/0/1,3-8,9 ...
        # iosxr: interface {name} / nv / satellite-fabric-link network / satellite 100 / service-policy output someword
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 (config-satellite-fabric-link)
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / ethernet cfm (config-cfm)
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / ethernet cfm / continuity-check interval 3.3ms
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / ethernet cfm / continuity-check interval 10ms
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / ethernet cfm / continuity-check interval 100ms
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / ethernet cfm / continuity-check interval 1s
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / ethernet cfm / continuity-check interval 10s
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / ethernet cfm / continuity-check interval 1m
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / ethernet cfm / continuity-check interval 10m
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / ethernet cfm / level <0-7>
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / redundancy (config-nV-red)
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / redundancy / iccp-group 1
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / remote-ports GigabitEthernet 0/0/1,3-8,9 ...
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / remote-ports TenGigE 0/0/1,3-8,9 ...
        # iosxr: interface {name} / nv / satellite-fabric-link satellite 100 / service-policy output someword
        # iosxr: interface {name} / nv / service-policy input someword

        # iosxr: interface {name} / pm 15-min ether report fcs-err enable
        # iosxr: interface {name} / pm 15-min ether report ifIn-Octets enable
        # iosxr: interface {name} / pm 15-min ether report in-802-1Q-frames enable
        # iosxr: interface {name} / pm 15-min ether report in-Bcast enable
        # iosxr: interface {name} / pm 15-min ether report in-MIB-CRC enable
        # iosxr: interface {name} / pm 15-min ether report in-MIB-giant enable
        # iosxr: interface {name} / pm 15-min ether report in-MIB-jabber enable
        # iosxr: interface {name} / pm 15-min ether report in-Mcast enable
        # iosxr: interface {name} / pm 15-min ether report in-Ucast enable
        # iosxr: interface {name} / pm 15-min ether report in-drop-abort enable
        # iosxr: interface {name} / pm 15-min ether report in-drop-invalid-DMAC enable
        # iosxr: interface {name} / pm 15-min ether report in-drop-invalid-VLAN enable
        # iosxr: interface {name} / pm 15-min ether report in-drop-invalid-encap enable
        # iosxr: interface {name} / pm 15-min ether report in-drop-other enable
        # iosxr: interface {name} / pm 15-min ether report in-drop-overrun enable
        # iosxr: interface {name} / pm 15-min ether report in-error-collisions enable
        # iosxr: interface {name} / pm 15-min ether report in-error-fragments enable
        # iosxr: interface {name} / pm 15-min ether report in-error-giant enable
        # iosxr: interface {name} / pm 15-min ether report in-error-jabbers enable
        # iosxr: interface {name} / pm 15-min ether report in-error-other enable
        # iosxr: interface {name} / pm 15-min ether report in-error-runt enable
        # iosxr: interface {name} / pm 15-min ether report in-error-symbol enable
        # iosxr: interface {name} / pm 15-min ether report in-good-bytes enable
        # iosxr: interface {name} / pm 15-min ether report in-good-pkts enable
        # iosxr: interface {name} / pm 15-min ether report in-pause-frame enable
        # iosxr: interface {name} / pm 15-min ether report in-pkt-64-octet enable
        # iosxr: interface {name} / pm 15-min ether report in-pkts-1024-1518-octets enable
        # iosxr: interface {name} / pm 15-min ether report in-pkts-128-255-octets enable
        # iosxr: interface {name} / pm 15-min ether report in-pkts-1519-Max-octets enable
        # iosxr: interface {name} / pm 15-min ether report in-pkts-256-511-octets enable
        # iosxr: interface {name} / pm 15-min ether report in-pkts-512-1023-octets enable
        # iosxr: interface {name} / pm 15-min ether report in-pkts-65-127octets enable
        # iosxr: interface {name} / pm 15-min ether report out-802-1Q-frames enable
        # iosxr: interface {name} / pm 15-min ether report out-Bcast enable
        # iosxr: interface {name} / pm 15-min ether report out-Mcast enable
        # iosxr: interface {name} / pm 15-min ether report out-Ucast enable
        # iosxr: interface {name} / pm 15-min ether report out-drop-abort enable
        # iosxr: interface {name} / pm 15-min ether report out-drop-other enable
        # iosxr: interface {name} / pm 15-min ether report out-drop-underrun enable
        # iosxr: interface {name} / pm 15-min ether report out-error-other enable
        # iosxr: interface {name} / pm 15-min ether report out-good-bytes enable
        # iosxr: interface {name} / pm 15-min ether report out-good-pkts enable
        # iosxr: interface {name} / pm 15-min ether report out-octets enable
        # iosxr: interface {name} / pm 15-min ether report out-pause-frames enable
        # iosxr: interface {name} / pm 15-min ether report out-pkt-64-octet enable
        # iosxr: interface {name} / pm 15-min ether report out-pkts-1024-1518-octets enable
        # iosxr: interface {name} / pm 15-min ether report out-pkts-128-255-octets enable
        # iosxr: interface {name} / pm 15-min ether report out-pkts-1519-Max-octets enable
        # iosxr: interface {name} / pm 15-min ether report out-pkts-256-511-octets enable
        # iosxr: interface {name} / pm 15-min ether report out-pkts-512-1023-octets enable
        # iosxr: interface {name} / pm 15-min ether report out-pkts-65-127octets enable
        # iosxr: interface {name} / pm 15-min ether report rx-pkt enable
        # iosxr: interface {name} / pm 15-min ether report tx-pkt enable
        # iosxr: interface {name} / pm 15-min ether threshold fcs-err 1
        # iosxr: interface {name} / pm 15-min ether threshold ifIn-Octets 1
        # iosxr: interface {name} / pm 15-min ether threshold in-802-1Q-frames 1
        # iosxr: interface {name} / pm 15-min ether threshold in-Bcast 1
        # iosxr: interface {name} / pm 15-min ether threshold in-MIB-CRC 1
        # iosxr: interface {name} / pm 15-min ether threshold in-MIB-giant 1
        # iosxr: interface {name} / pm 15-min ether threshold in-MIB-jabber 1
        # iosxr: interface {name} / pm 15-min ether threshold in-Mcast 1
        # iosxr: interface {name} / pm 15-min ether threshold in-Ucast 1
        # iosxr: interface {name} / pm 15-min ether threshold in-drop-abort 1
        # iosxr: interface {name} / pm 15-min ether threshold in-drop-invalid-DMAC 1
        # iosxr: interface {name} / pm 15-min ether threshold in-drop-invalid-VLAN 1
        # iosxr: interface {name} / pm 15-min ether threshold in-drop-invalid-encap 1
        # iosxr: interface {name} / pm 15-min ether threshold in-drop-other 1
        # iosxr: interface {name} / pm 15-min ether threshold in-drop-overrun 1
        # iosxr: interface {name} / pm 15-min ether threshold in-error-collisions 1
        # iosxr: interface {name} / pm 15-min ether threshold in-error-fragments 1
        # iosxr: interface {name} / pm 15-min ether threshold in-error-giant 1
        # iosxr: interface {name} / pm 15-min ether threshold in-error-jabbers 1
        # iosxr: interface {name} / pm 15-min ether threshold in-error-other 1
        # iosxr: interface {name} / pm 15-min ether threshold in-error-runt 1
        # iosxr: interface {name} / pm 15-min ether threshold in-error-symbol 1
        # iosxr: interface {name} / pm 15-min ether threshold in-good-bytes 1
        # iosxr: interface {name} / pm 15-min ether threshold in-good-pkts 1
        # iosxr: interface {name} / pm 15-min ether threshold in-pause-frame 1
        # iosxr: interface {name} / pm 15-min ether threshold in-pkt-64-octet 1
        # iosxr: interface {name} / pm 15-min ether threshold in-pkts-1024-1518-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold in-pkts-128-255-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold in-pkts-1519-Max-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold in-pkts-256-511-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold in-pkts-512-1023-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold in-pkts-65-127octets 1
        # iosxr: interface {name} / pm 15-min ether threshold out-802-1Q-frames 1
        # iosxr: interface {name} / pm 15-min ether threshold out-Bcast 1
        # iosxr: interface {name} / pm 15-min ether threshold out-Mcast 1
        # iosxr: interface {name} / pm 15-min ether threshold out-Ucast 1
        # iosxr: interface {name} / pm 15-min ether threshold out-drop-abort 1
        # iosxr: interface {name} / pm 15-min ether threshold out-drop-other 1
        # iosxr: interface {name} / pm 15-min ether threshold out-drop-underrun 1
        # iosxr: interface {name} / pm 15-min ether threshold out-error-other 1
        # iosxr: interface {name} / pm 15-min ether threshold out-good-bytes 1
        # iosxr: interface {name} / pm 15-min ether threshold out-good-pkts 1
        # iosxr: interface {name} / pm 15-min ether threshold out-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold out-pause-frames 1
        # iosxr: interface {name} / pm 15-min ether threshold out-pkt-64-octet 1
        # iosxr: interface {name} / pm 15-min ether threshold out-pkts-1024-1518-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold out-pkts-128-255-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold out-pkts-1519-Max-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold out-pkts-256-511-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold out-pkts-512-1023-octets 1
        # iosxr: interface {name} / pm 15-min ether threshold out-pkts-65-127octets 1
        # iosxr: interface {name} / pm 15-min ether threshold rx-pkt 1
        # iosxr: interface {name} / pm 15-min ether threshold tx-pkt 1
        # iosxr: interface {name} / pm 24-hour ether report fcs-err enable
        # iosxr: interface {name} / pm 24-hour ether report ifIn-Octets enable
        # iosxr: interface {name} / pm 24-hour ether report in-802-1Q-frames enable
        # iosxr: interface {name} / pm 24-hour ether report in-Bcast enable
        # iosxr: interface {name} / pm 24-hour ether report in-MIB-CRC enable
        # iosxr: interface {name} / pm 24-hour ether report in-MIB-giant enable
        # iosxr: interface {name} / pm 24-hour ether report in-MIB-jabber enable
        # iosxr: interface {name} / pm 24-hour ether report in-Mcast enable
        # iosxr: interface {name} / pm 24-hour ether report in-Ucast enable
        # iosxr: interface {name} / pm 24-hour ether report in-drop-abort enable
        # iosxr: interface {name} / pm 24-hour ether report in-drop-invalid-DMAC enable
        # iosxr: interface {name} / pm 24-hour ether report in-drop-invalid-VLAN enable
        # iosxr: interface {name} / pm 24-hour ether report in-drop-invalid-encap enable
        # iosxr: interface {name} / pm 24-hour ether report in-drop-other enable
        # iosxr: interface {name} / pm 24-hour ether report in-drop-overrun enable
        # iosxr: interface {name} / pm 24-hour ether report in-error-collisions enable
        # iosxr: interface {name} / pm 24-hour ether report in-error-fragments enable
        # iosxr: interface {name} / pm 24-hour ether report in-error-giant enable
        # iosxr: interface {name} / pm 24-hour ether report in-error-jabbers enable
        # iosxr: interface {name} / pm 24-hour ether report in-error-other enable
        # iosxr: interface {name} / pm 24-hour ether report in-error-runt enable
        # iosxr: interface {name} / pm 24-hour ether report in-error-symbol enable
        # iosxr: interface {name} / pm 24-hour ether report in-good-bytes enable
        # iosxr: interface {name} / pm 24-hour ether report in-good-pkts enable
        # iosxr: interface {name} / pm 24-hour ether report in-pause-frame enable
        # iosxr: interface {name} / pm 24-hour ether report in-pkt-64-octet enable
        # iosxr: interface {name} / pm 24-hour ether report in-pkts-1024-1518-octets enable
        # iosxr: interface {name} / pm 24-hour ether report in-pkts-128-255-octets enable
        # iosxr: interface {name} / pm 24-hour ether report in-pkts-1519-Max-octets enable
        # iosxr: interface {name} / pm 24-hour ether report in-pkts-256-511-octets enable
        # iosxr: interface {name} / pm 24-hour ether report in-pkts-512-1023-octets enable
        # iosxr: interface {name} / pm 24-hour ether report in-pkts-65-127octets enable
        # iosxr: interface {name} / pm 24-hour ether report out-802-1Q-frames enable
        # iosxr: interface {name} / pm 24-hour ether report out-Bcast enable
        # iosxr: interface {name} / pm 24-hour ether report out-Mcast enable
        # iosxr: interface {name} / pm 24-hour ether report out-Ucast enable
        # iosxr: interface {name} / pm 24-hour ether report out-drop-abort enable
        # iosxr: interface {name} / pm 24-hour ether report out-drop-other enable
        # iosxr: interface {name} / pm 24-hour ether report out-drop-underrun enable
        # iosxr: interface {name} / pm 24-hour ether report out-error-other enable
        # iosxr: interface {name} / pm 24-hour ether report out-good-bytes enable
        # iosxr: interface {name} / pm 24-hour ether report out-good-pkts enable
        # iosxr: interface {name} / pm 24-hour ether report out-octets enable
        # iosxr: interface {name} / pm 24-hour ether report out-pause-frames enable
        # iosxr: interface {name} / pm 24-hour ether report out-pkt-64-octet enable
        # iosxr: interface {name} / pm 24-hour ether report out-pkts-1024-1518-octets enable
        # iosxr: interface {name} / pm 24-hour ether report out-pkts-128-255-octets enable
        # iosxr: interface {name} / pm 24-hour ether report out-pkts-1519-Max-octets enable
        # iosxr: interface {name} / pm 24-hour ether report out-pkts-256-511-octets enable
        # iosxr: interface {name} / pm 24-hour ether report out-pkts-512-1023-octets enable
        # iosxr: interface {name} / pm 24-hour ether report out-pkts-65-127octets enable
        # iosxr: interface {name} / pm 24-hour ether report rx-pkt enable
        # iosxr: interface {name} / pm 24-hour ether report tx-pkt enable
        # iosxr: interface {name} / pm 24-hour ether threshold fcs-err 1
        # iosxr: interface {name} / pm 24-hour ether threshold ifIn-Octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-802-1Q-frames 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-Bcast 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-MIB-CRC 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-MIB-giant 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-MIB-jabber 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-Mcast 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-Ucast 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-drop-abort 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-drop-invalid-DMAC 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-drop-invalid-VLAN 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-drop-invalid-encap 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-drop-other 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-drop-overrun 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-error-collisions 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-error-fragments 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-error-giant 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-error-jabbers 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-error-other 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-error-runt 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-error-symbol 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-good-bytes 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-good-pkts 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-pause-frame 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-pkt-64-octet 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-pkts-1024-1518-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-pkts-128-255-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-pkts-1519-Max-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-pkts-256-511-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-pkts-512-1023-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold in-pkts-65-127octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-802-1Q-frames 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-Bcast 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-Mcast 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-Ucast 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-drop-abort 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-drop-other 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-drop-underrun 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-error-other 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-good-bytes 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-good-pkts 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-pause-frames 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-pkt-64-octet 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-pkts-1024-1518-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-pkts-128-255-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-pkts-1519-Max-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-pkts-256-511-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-pkts-512-1023-octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold out-pkts-65-127octets 1
        # iosxr: interface {name} / pm 24-hour ether threshold rx-pkt 1
        # iosxr: interface {name} / pm 24-hour ether threshold tx-pkt 1

        # iosxr: interface {name} / pppoe enable
        # iosxr: interface {name} / pppoe enable bba-group someword

        # iosxr: interface {name} / proxy-arp

        # iosxr: interface {name} / ptp (config-if-ptp)
        # iosxr: interface {name} / ptp / announce frequency 1
        # iosxr: interface {name} / ptp / announce frequency 2
        # iosxr: interface {name} / ptp / announce frequency 4
        # iosxr: interface {name} / ptp / announce frequency 8
        # iosxr: interface {name} / ptp / announce frequency 16
        # iosxr: interface {name} / ptp / announce frequency 32
        # iosxr: interface {name} / ptp / announce frequency 64
        # iosxr: interface {name} / ptp / announce grant-duration 60
        # iosxr: interface {name} / ptp / announce interval 1
        # iosxr: interface {name} / ptp / announce interval 2
        # iosxr: interface {name} / ptp / announce interval 4
        # iosxr: interface {name} / ptp / announce interval 8
        # iosxr: interface {name} / ptp / announce interval 16
        # iosxr: interface {name} / ptp / announce timeout 2
        # iosxr: interface {name} / ptp / clock operation one-step
        # iosxr: interface {name} / ptp / clock operation two-step
        # iosxr: interface {name} / ptp / cos <0-7>
        # iosxr: interface {name} / ptp / cos event <0-7>
        # iosxr: interface {name} / ptp / cos general <0-7>
        # iosxr: interface {name} / ptp / delay-request frequency 1
        # iosxr: interface {name} / ptp / delay-request frequency 2
        # iosxr: interface {name} / ptp / delay-request frequency 4
        # iosxr: interface {name} / ptp / delay-request frequency 8
        # iosxr: interface {name} / ptp / delay-request frequency 16
        # iosxr: interface {name} / ptp / delay-request frequency 32
        # iosxr: interface {name} / ptp / delay-request frequency 64
        # iosxr: interface {name} / ptp / delay-request frequency 128
        # iosxr: interface {name} / ptp / delay-request interval 1
        # iosxr: interface {name} / ptp / delay-request interval 2
        # iosxr: interface {name} / ptp / delay-request interval 4
        # iosxr: interface {name} / ptp / delay-request interval 8
        # iosxr: interface {name} / ptp / delay-request interval 16
        # iosxr: interface {name} / ptp / delay-response grant-duration 60
        # iosxr: interface {name} / ptp / delay-response timeout 100
        # iosxr: interface {name} / ptp / dscp <0-63>
        # iosxr: interface {name} / ptp / dscp event <0-63>
        # iosxr: interface {name} / ptp / dscp general <0-63>
        # iosxr: interface {name} / ptp / local-priority 1
        # iosxr: interface {name} / ptp / master ethernet aaaa.bbbb.cccc (config-if-ptp-master)
        # iosxr: interface {name} / ptp / master ethernet aaaa.bbbb.cccc / clock-class <0-255>
        # iosxr: interface {name} / ptp / master ethernet aaaa.bbbb.cccc / multicast
        # iosxr: interface {name} / ptp / master ethernet aaaa.bbbb.cccc / multicast mixed
        # iosxr: interface {name} / ptp / master ethernet aaaa.bbbb.cccc / non-negotiated
        # iosxr: interface {name} / ptp / master ethernet aaaa.bbbb.cccc / priority <0-255>
        # iosxr: interface {name} / ptp / master ipv4 1.2.3.4 (config-if-ptp-master)
        # iosxr: interface {name} / ptp / master ipv4 1.2.3.4 / clock-class <0-255>
        # iosxr: interface {name} / ptp / master ipv4 1.2.3.4 / multicast
        # iosxr: interface {name} / ptp / master ipv4 1.2.3.4 / multicast mixed
        # iosxr: interface {name} / ptp / master ipv4 1.2.3.4 / non-negotiated
        # iosxr: interface {name} / ptp / master ipv4 1.2.3.4 / priority <0-255>
        # iosxr: interface {name} / ptp / multicast
        # iosxr: interface {name} / ptp / multicast disable
        # iosxr: interface {name} / ptp / multicast disable target-address ethernet 01-1B-19-00-00-00
        # iosxr: interface {name} / ptp / multicast disable target-address ethernet 01-80-C2-00-00-0E
        # iosxr: interface {name} / ptp / multicast mixed
        # iosxr: interface {name} / ptp / multicast mixed target-address ethernet 01-1B-19-00-00-00
        # iosxr: interface {name} / ptp / multicast mixed target-address ethernet 01-80-C2-00-00-0E
        # iosxr: interface {name} / ptp / multicast target-address ethernet 01-1B-19-00-00-00
        # iosxr: interface {name} / ptp / multicast target-address ethernet 01-80-C2-00-00-0E
        # iosxr: interface {name} / ptp / port state any
        # iosxr: interface {name} / ptp / port state master-only
        # iosxr: interface {name} / ptp / port state slave-only
        # iosxr: interface {name} / ptp / profile someword
        # iosxr: interface {name} / ptp / slave ethernet aaaa.bbbb.cccc non-negotiated
        # iosxr: interface {name} / ptp / slave ipv4 1.2.3.4 non-negotiated
        # iosxr: interface {name} / ptp / source ipv4 address 1.2.3.4
        # iosxr: interface {name} / ptp / source ipv4 address disable
        # iosxr: interface {name} / ptp / sync frequency 1
        # iosxr: interface {name} / ptp / sync frequency 2
        # iosxr: interface {name} / ptp / sync frequency 4
        # iosxr: interface {name} / ptp / sync frequency 8
        # iosxr: interface {name} / ptp / sync frequency 16
        # iosxr: interface {name} / ptp / sync frequency 32
        # iosxr: interface {name} / ptp / sync frequency 64
        # iosxr: interface {name} / ptp / sync frequency 128
        # iosxr: interface {name} / ptp / sync grant-duration 60
        # iosxr: interface {name} / ptp / sync interval 1
        # iosxr: interface {name} / ptp / sync interval 2
        # iosxr: interface {name} / ptp / sync interval 4
        # iosxr: interface {name} / ptp / sync interval 8
        # iosxr: interface {name} / ptp / sync interval 16
        # iosxr: interface {name} / ptp / sync timeout 100
        # iosxr: interface {name} / ptp / transport ethernet
        # iosxr: interface {name} / ptp / transport ipv4
        # iosxr: interface {name} / ptp / unicast-grant invalid-request deny
        # iosxr: interface {name} / ptp / unicast-grant invalid-request reduce

        # iosxr: interface {name} / rewrite ingress tag push ... TODO

        # iosxr: interface {name} / rewrite ingress tag translate ... TODO
        configurations.append_line(attributes.format('rewrite ingress tag translate 1-to-1 dot1q {rewrite_ingress_tag_translate_1_to_1_dot1q_symmetric} symmetric'))

        # iosxr: interface {name} / rewrite ingress tag pop 1|2 symmetric
        configurations.append_line(attributes.format('rewrite ingress tag pop {rewrite_ingress_tag_pop_symmetric} symmetric'))

        # iosxr: interface {name} / service-policy input someword
        # iosxr: interface {name} / service-policy input someword account layer1
        # iosxr: interface {name} / service-policy input someword account layer1 shared-policy-instance someword2
        # iosxr: interface {name} / service-policy input someword account layer1 subscriber-parent
        # iosxr: interface {name} / service-policy input someword account layer1 subscriber-parent resource-id <0-3>
        # iosxr: interface {name} / service-policy input someword account layer2
        # iosxr: interface {name} / service-policy input someword account layer2 shared-policy-instance someword2
        # iosxr: interface {name} / service-policy input someword account layer2 subscriber-parent
        # iosxr: interface {name} / service-policy input someword account layer2 subscriber-parent resource-id <0-3>
        # iosxr: interface {name} / service-policy input someword account nolayer2
        # iosxr: interface {name} / service-policy input someword account nolayer2 shared-policy-instance someword2
        # iosxr: interface {name} / service-policy input someword account nolayer2 subscriber-parent
        # iosxr: interface {name} / service-policy input someword account nolayer2 subscriber-parent resource-id <0-3>
        # iosxr: interface {name} / service-policy input someword shared-policy-instance someword2
        # iosxr: interface {name} / service-policy input someword subscriber-parent
        # iosxr: interface {name} / service-policy input someword subscriber-parent resource-id <0-3>
        # iosxr: interface {name} / service-policy output someword
        # iosxr: interface {name} / service-policy output someword account layer1
        # iosxr: interface {name} / service-policy output someword account layer1 shared-policy-instance someword2
        # iosxr: interface {name} / service-policy output someword account layer1 subscriber-parent
        # iosxr: interface {name} / service-policy output someword account layer1 subscriber-parent resource-id <0-3>
        # iosxr: interface {name} / service-policy output someword account layer2
        # iosxr: interface {name} / service-policy output someword account layer2 shared-policy-instance someword2
        # iosxr: interface {name} / service-policy output someword account layer2 subscriber-parent
        # iosxr: interface {name} / service-policy output someword account layer2 subscriber-parent resource-id <0-3>
        # iosxr: interface {name} / service-policy output someword account nolayer2
        # iosxr: interface {name} / service-policy output someword account nolayer2 shared-policy-instance someword2
        # iosxr: interface {name} / service-policy output someword account nolayer2 subscriber-parent
        # iosxr: interface {name} / service-policy output someword account nolayer2 subscriber-parent resource-id <0-3>
        # iosxr: interface {name} / service-policy output someword shared-policy-instance someword2
        # iosxr: interface {name} / service-policy output someword subscriber-parent
        # iosxr: interface {name} / service-policy output someword subscriber-parent resource-id <0-3>
        # iosxr: interface {name} / service-policy type control subscriber someword
        # iosxr: interface {name} / service-policy type pbr input someword

        # enabled : interface {name} / shutdown
        enabled = attributes.value('enabled')
        shutdown = attributes.value('shutdown')
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
        else:
            if shutdown is not None:
                if unconfig:
                    # Special case: unconfiguring always applies shutdown
                    configurations.append_line('shutdown', raw=True)
                elif shutdown:
                    configurations.append_line('shutdown', raw=True)
                else:
                    configurations.append_line('no shutdown', raw=True)

        # link_up_down_trap_enable : N/A


    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @mixedmethod
    def clean_interface_name(self, cls, interface_name=None):
        if interface_name is None:
            interface_name = self.name
        d_parsed = cls.parse_interface_name(interface_name)
        if d_parsed.number:
            d_parsed.number = d_parsed.number.replace('_', '/')
            # d_parsed.number = d_parsed.number.replace('\\.', '.')
            # d_parsed.number = d_parsed.number.replace('.*', '*')
        try:
            d_parsed.type = {
                # Special case for te that matches both FortyGigE (XR) and
                # FortyGigabitEthernet (IOS/NxOS(?)) and FortyGigECtrlr
                'fo': 'FortyGigE',
                # Special case for te that matches both HundredGigE (XR) and
                # HundredGigabitEthernet (IOS/NxOS(?)) and HundredGigECtrlr
                'hu': 'HundredGigE',
                # Special case for TenGigECtrlr... both TeEC and EC forms seen on XR
                'ec': 'TenGigECtrlr',
                'teec': 'TenGigECtrlr',
                # Special case for te that matches both TenGigE (XR) and
                # TenGigabitEthernet (IOS/NxOS(?)) and TenGigECtrlr
                'te': 'TenGigE',
                # Special case for tg that matches both tunnel-gre (now
                # tunnel-ip) and tunnel-gte
                'tg': 'tunnel-gte',
                # Special case for tt that matches both tunnel-te and tunnel-tp
                'tt': 'tunnel-te',
                # Special case for tp to differentiate from tunnel-te
                'tp': 'tunnel-tp',
                # Special case for ti that matches both tunnel-ip and
                # tunnel-ipsec
                'ti': 'tunnel-ip',
            }[d_parsed.type.lower()]
        except KeyError:
            pass
        return super(self or cls, Interface).clean_interface_name(d_parsed.reconstruct())

    @mixedmethod
    def short_interface_name(self, cls, interface_name=None):
        if interface_name is None:
            interface_name = self.name
        interface_name = (self or cls).clean_interface_name(interface_name)
        d_parsed = cls.parse_interface_name(interface_name)
        try:
            d_parsed.type = {
                'GCC0': 'g0',
                'GCC1': 'g1',
                'TenGigECtrlr': 'TeEC',
                'tunnel-tp': 'tp',
            }[d_parsed.type]
        except KeyError:
            pass
        else:
            return d_parsed.reconstruct()
        m = re.match(r'^OTU([01234](?:[EF][12]?)?)$', d_parsed.type)
        if m:
            d_parsed.type = 'O' + m.group(1).upper()
            return d_parsed.reconstruct()
        m = re.match(r'ODU([01234](?:[EF][12]?)?)$', d_parsed.type)
        if m:
            d_parsed.type = 'd' + m.group(1).upper()
            return d_parsed.reconstruct()
        return super(self or cls, Interface).short_interface_name(interface_name)

Interface.anycast_source_interface = Interface.anycast_source_interface.copy(
    type=(None, managedattribute.test_isinstance(Interface)))

Interface.bundle = Interface.bundle.copy(
    type=(None, managedattribute.test_isinstance(Interface)))


class Controller(Interface, genie.libs.conf.interface.Controller):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PhysicalInterface(Interface, genie.libs.conf.interface.PhysicalInterface):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    breakout = managedattribute(
        name='breakout',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    def build_config(self, apply=True, attributes=None, unconfig=False,
                     **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)


        if self.breakout is not None:
            # Non-Controller breakout must be configured at top-level and nothing else
            breakout = attributes.value('breakout')
            if breakout is not None:
                d_parsed = self.parse_interface_name()
                assert d_parsed.rack is not None \
                    and d_parsed.slot is not None \
                    and d_parsed.instance == '0' \
                    and d_parsed.cpu is not None \
                    and d_parsed.port \
                    and d_parsed.subport is None, d_parsed
                configurations.append_line(
                    'hw-module location {cpu} port {port} breakout {breakout}'.format(
                        cpu=d_parsed.cpu,
                        port=d_parsed.port,
                        breakout=breakout))

        else:
            configurations.append_block(super().build_config(
                apply=False, attributes=attributes, unconfig=unconfig,
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
            configurations.append_line('no interface {}'.format(self.name),
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


class VirtualInterface(Interface, genie.libs.conf.interface.VirtualInterface):

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # Virtual interfaces can be fully unconfigured
        if unconfig and attributes.iswildcard:
            configurations.submode_unconfig()

        super()._build_config_interface_submode(configurations, attributes, unconfig)

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PseudoInterface(VirtualInterface, genie.libs.conf.interface.PseudoInterface):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OpticsController(Controller, genie.libs.conf.interface.OpticsController):

    _interface_name_types = (
        'Optics',
    )

    breakout = managedattribute(
        name='breakout',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _build_config_create_interface_submode_context(self, configurations):
        # iosxr: controller {name} (config-Optics)
        return configurations.submode_context('controller {}'.format(self.name))

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # Controllers are too different from interfaces to configure defaults
        # super()._build_config_interface_submode(configurations, attributes, unconfig)

        # iosxr: controller {name} / breakout someword
        configurations.append_line(attributes.format('breakout {breakout}'))

        # iosxr: controller {name} / cd-high-threshold -70000
        # iosxr: controller {name} / cd-low-threshold -70000
        # iosxr: controller {name} / cd-max -70000
        # iosxr: controller {name} / cd-min -70000

        # iosxr: controller {name} / description some line data
        v = attributes.value('description')
        if v:
            if v is True:
                pass  # TODO Create a usefull default description
            configurations.append_line('description {}'.format(v))

        # iosxr: controller {name} / dgd-high-threshold <0-18000>
        # iosxr: controller {name} / dwdm-carrier 100MHz-grid frequency 1911500
        # iosxr: controller {name} / dwdm-carrier 50GHz-grid frequency 19115
        # iosxr: controller {name} / dwdm-carrier 50GHz-grid itu-ch 1
        # iosxr: controller {name} / dwdm-carrier 50GHz-grid wavelength 1528773
        # iosxr: controller {name} / ext-description some line data
        # iosxr: controller {name} / fec EnhancedHG15
        # iosxr: controller {name} / fec EnhancedHG25
        # iosxr: controller {name} / lbc-high-threshold <0-100>
        # iosxr: controller {name} / loopback internal
        # iosxr: controller {name} / loopback line
        # iosxr: controller {name} / network srlg (config-optics-srlg)
        # iosxr: controller {name} / network srlg / set 1 <0-4294967294> [<0-4294967294> [<0-4294967294> [<0-4294967294> [<0-4294967294> [<0-4294967294>]]]]]
        # iosxr: controller {name} / osnr-low-threshold <0-4000>
        # iosxr: controller {name} / perf-mon disable
        # iosxr: controller {name} / perf-mon enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour fec report ec-bits enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour fec report uc-words enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour fec threshold ec-bits someword
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour fec threshold uc-words someword
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report cd max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report cd min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report dgd max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report dgd min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report lbc max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report lbc min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report lbc-pc max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report lbc-pc min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report opr max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report opr min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report opt max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report opt min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report osnr max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report osnr min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report pcr max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report pcr min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report pdl max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report pdl min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report pn max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report pn min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report sopmd max-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics report sopmd min-tca enable
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold cd max -70000
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold cd min -70000
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold dgd max 4294967294
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold dgd min 1
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold lbc max 4294967294
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold lbc min 1
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold lbc-pc max 1000
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold lbc-pc min <0-1000>
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold opr max 4294967294
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold opr min 1
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold opt max 4294967294
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold opt min 1
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold osnr max 4294967294
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold osnr min 1
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold pcr max 4294967294
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold pcr min 1
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold pdl max 4294967294
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold pdl min 1
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold pn max 4294967290
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold pn min 1
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold sopmd max 4294967294
        # iosxr: controller {name} / pm 30-sec|15-min|24-hour optics threshold sopmd min 1
        # iosxr: controller {name} / port-mode speed 100G|150G|200G fec 15percent|25percent diff enable|disable
        # iosxr: controller {name} / rx-high-threshold -400
        # iosxr: controller {name} / rx-low-threshold -400
        # iosxr: controller {name} / sec-admin-state maintenance

        # iosxr: controller {name} / shutdown
        shutdown = attributes.value('shutdown')
        if shutdown:
            if unconfig:
                # Special case: unconfiguring always applies shutdown
                configurations.append_line('shutdown', raw=True)
            elif shutdown:
                configurations.append_line('shutdown', raw=True)
            else:
                configurations.append_line('no shutdown', raw=True)

        # iosxr: controller {name} / soak-time 10
        # iosxr: controller {name} / transmit-power -190
        # iosxr: controller {name} / transmit-shutdown
        # iosxr: controller {name} / tx-high-threshold -400
        # iosxr: controller {name} / tx-low-threshold -400


class OtuController(Controller):

    _interface_name_types = (
        'OTU1',
        'OTU1E',
        'OTU1F',
        'OTU2',
        'OTU2E',
        'OTU2F',
        'OTU3',
        'OTU3E1',
        'OTU3E2',
        'OTU4',
    )

    # TODO -- stay abstract meanwhile
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class OduController(Controller):

    _interface_name_types = (
        'ODU0',
        'ODU1',
        'ODU1E',
        'ODU1F',
        'ODU2',
        'ODU2E',
        'ODU2F',
        'ODU3',
        'ODU3E1',
        'ODU3E2',
        'ODU4',
    )

    # TODO -- stay abstract meanwhile
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class SonetController(Controller):

    _interface_name_types = (
        'SONET',
    )

    # TODO -- stay abstract meanwhile
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class MgmtMultilinkController(Controller):

    _interface_name_types = (
        'MgmtMultilink',
    )

    # TODO -- stay abstract meanwhile
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class LoopbackInterface(VirtualInterface, genie.libs.conf.interface.LoopbackInterface):

    _interface_name_types = (
        'Loopback',
        'loopback'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EthernetInterface(PhysicalInterface, genie.libs.conf.interface.EthernetInterface):

    _interface_name_types = (
        'FastEthernet',
        'FASTETHERNET',
        'GigabitEthernet',
        'TenGigE',
        'TwentyFiveGigE',
        'HundredGigE',
        'FortyGigE',
    )

    # Restrict to only IOS-XR strings
    duplex = genie.libs.conf.interface.EthernetInterface.duplex.copy(
        type=(None, managedattribute.test_in((
            'full',
            'half',
        ))))

    # Restrict to only IOS-XR values
    speed = genie.libs.conf.interface.EthernetInterface.speed.copy(
        type=(None, int))

    transceiver_permit_pid_all = managedattribute(
        name='transceiver_permit_pid_all',
        type=(None, managedattribute.test_istype(bool)))

    @transceiver_permit_pid_all.defaulter
    def transceiver_permit_pid_all(self):
        if re.match('asr9\d\d\d', self.device.platform or ''):
            return True
        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        super()._build_config_interface_submode(configurations=configurations,
                                                attributes=attributes,
                                                unconfig=unconfig)

        # iosxr: interface {name} / transceiver permit pid all
        if attributes.value('transceiver_permit_pid_all'):
            if unconfig:
                pass  # There is really no point in unconfiguring this
            else:
                configurations.append_line('transceiver permit pid all')

        # iosxr: interface {name} / duplex full
        # iosxr: interface {name} / duplex half
        configurations.append_line(attributes.format('duplex {duplex}'))

        # duplex_mode : duplex [full|half]
        configurations.append_line(attributes.format(\
            'duplex {duplex_mode.name}'))

        # iosxr: interface {name} / speed 10
        # iosxr: interface {name} / speed 100
        # iosxr: interface {name} / speed 1000
        configurations.append_line(attributes.format('speed {speed}'))

        # port_speed : interface {name} / speed <port_speed>
        configurations.append_line(attributes.format('speed {port_speed.value}'))

        # access_vlan : N/A

        # trunk_vlans : N/A

        # trunk_add_vlans : N/A

        # trunk_remote_vlans : N/A

        # native_vlan : N/A

        # iosxr: interface {name} / mac-accounting egress
        # iosxr: interface {name} / mac-accounting ingress

        # mac_address: interface {name} / mac-address aaaa.bbbb.cccc
        configurations.append_line(attributes.format(\
            'mac-address {mac_address}'), unconfig_cmd='no mac-address')

        # iosxr: interface {name} / negotiation auto
        if attributes.value('auto_negotiation'):
            configurations.append_line('negotiation auto')

        # auto_negotiate : negotiation auto
        if attributes.value('auto_negotiate'):
            configurations.append_line('negotiation auto')

        # flow_control_receive
        if attributes.value('flow_control_receive'):
            configurations.append_line('flow-control ingress')

        # flow_control_send
        if attributes.value('flow_control_send'):
            configurations.append_line('flow-control egress')


class PosInterface(PhysicalInterface, genie.libs.conf.interface.PosInterface):
    # TODO

    _interface_name_types = (
        'POS',
    )

    parent_controller_type = managedattribute(
        name='parent_controller_type',
        default='SONET',
        read_only=True,
        doc='''The associated controller type (SONET).''')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SrpInterface(PhysicalInterface,
                   # TODO genie.libs.conf.interface.SrpInterface
                   ):
    # TODO

    _interface_name_types = (
        'SRP',
    )

    parent_controller_type = managedattribute(
        name='parent_controller_type',
        default='SONET',
        read_only=True,
        doc='''The associated controller type (SONET).''')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MultilinkInterface(PhysicalInterface,
                   # TODO genie.libs.conf.interface.MultilinkInterface
                   ):
    # TODO

    _interface_name_types = (
        'Multilink',
    )

    parent_controller_type = managedattribute(
        name='parent_controller_type',
        default='MgmtMultilink',
        read_only=True,
        doc='''The associated controller type (MgmtMultilink).''')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class SubInterface(VirtualInterface, genie.libs.conf.interface.SubInterface):

    parent_controller_type = managedattribute(
        name='parent_controller_type',
        read_only=True,
        doc='''The associated controller type retrieved from the parent interface.''')

    @parent_controller_type.getter
    def parent_controller_type(self):
        parent_interface = self.parent_interface
        return parent_interface and parent_interface.parent_controller_type

    def _build_config_create_interface_submode_context(self, configurations):
        # sub-interfaces must provide their "l2transport" keyword on the interface line
        # iosxr: interface {name}.1 (config-subif)
        # iosxr: interface {name}.1 l2transport (config-subif)
        cfg = 'interface {}'.format(self.name)
        if self.l2transport.enabled:
            cfg += ' l2transport'
        return configurations.submode_context(cfg)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Gcc0Interface(VirtualInterface):

    _interface_name_types = (
        'GCC0',
    )

    # TODO -- stay abstract meanwhile
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class Gcc1Interface(VirtualInterface):

    _interface_name_types = (
        'GCC1',
    )

    # TODO -- stay abstract meanwhile
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class MgmtEthernetInterface(EthernetInterface, genie.libs.conf.interface.ManagementInterface):

    _interface_name_types = (
        'MgmtEth', 'MgmtEthernet',
    )

    transceiver_permit_pid_all = EthernetInterface.transceiver_permit_pid_all.copy(
        default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TunnelInterface(VirtualInterface, genie.libs.conf.interface.TunnelInterface):

    # TODO XXXJST This needs a big cleanup

    destination = managedattribute(
        name='destination',
        default=None,
        type=(None, IPv4Address))

    autoroute_announce = False
    autoroute_announce_metric = None
    autoroute_announce_include_ipv6 = False
    autoroute_announce_metric_absolute = None
    autoroute_announce_metric_relative = None
    autoroute_announce_destination = None
    autoroute_announce_ = None

    ipv4_unnumbered_interface = managedattribute(
        name='ipv4_unnumbered_interface',
        default=None,
        type=(None,
              managedattribute.test_isinstance(Interface)))

    affinity_exclude = None

    auto_bw = False
    auto_bw_adj_threshold_pct = None
    auto_bw_adj_threshold_min = None
    auto_bw_application_freq = None
    auto_bw_bwlimit_min = None
    auto_bw_bwlimit_max = None
    auto_bw_collect_bw_only = False
    auto_bw_overflow_thresh_pct = None
    auto_bw_overflow_thresh_min = None
    auto_bw_overflow_thresh_limit = None
    auto_bw_underflow_thresh_pct = None
    auto_bw_underflow_thresh_min = None
    auto_bw_underflow_thresh_limit = None

    priority_setup = None
    priority_hold = None

    frr = False
    frr_protect = None

    signalled_bandwidth = None
    signalled_bandwidth_class_type = None
    signalled_bandwidth_subpool = None
    signalled_name = None

    logging_lsp_state = False
    logging_lsp_reopt = False
    logging_lsp_record_route = False

    soft_preemption = False

    # TODO PathOption class, typedset and get rid of path_option_attr
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

        computation = managedattribute(
            name='computation',
            default=None,
            type=managedattribute.test_istype(str))

        preference = managedattribute(
            name='preference',
            default=None,
            type=managedattribute.test_istype(int))

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
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # path option is different for mpls named tunnels and interface tunnels
            if self.named_tunnel:

                # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-option someword (config-path-option-name)
                # iosxr: interface tunnel-te1 / path-option <1-1000>
                with configurations.submode_context(attributes.format('path-option {path_option}', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-option someword / computation dynamic
                    # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-option someword / computation explicit someword2
                    configurations.append_line(attributes.format('computation {computation}'))

                    # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-option someword / preference <0-4294967295>
                    configurations.append_line(attributes.format('preference {preference}'))

            else:
                # iosxr: interface tunnel-te1 / path-option 1 dynamic
                if attributes.value('dynamic'):
                    configurations.append_line(attributes.format('path-option {path_option} dynamic'))

                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword
                configurations.append_line(attributes.format('path-option {path_option} explicit name {explicit_name}'))

                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 level 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 level 1 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 level 1 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 level 1 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 level 1 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 level 1 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 level 1 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 level 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis lockdown
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword isis segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic attribute-set someword segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword level 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword level 1 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword level 1 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword level 1 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword level 1 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword level 1 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword level 1 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword level 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword lockdown
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis someword segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis lockdown
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic isis segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf someword segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf someword segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic pce
                # iosxr: interface tunnel-te1 / path-option 1 dynamic pce address ipv4 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 dynamic pce address ipv4 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic pce segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 dynamic protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 dynamic segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 level 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis someword2 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword isis verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area <0-4294967295> protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area <0-4294967295> protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area <0-4294967295> segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area <0-4294967295> verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area 1.2.3.4 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area 1.2.3.4 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area 1.2.3.4 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 area 1.2.3.4 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf someword2 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown ospf verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area <0-4294967295> protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area <0-4294967295> protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area <0-4294967295> segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area <0-4294967295> verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area 1.2.3.4 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area 1.2.3.4 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area 1.2.3.4 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 area 1.2.3.4 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf someword2 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword ospf verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 attribute-set someword verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword level 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis someword verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 isis verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area <0-4294967295> protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area <0-4294967295> protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area <0-4294967295> segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area <0-4294967295> verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area 1.2.3.4 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area 1.2.3.4 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area 1.2.3.4 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword area 1.2.3.4 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf someword verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown ospf verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area <0-4294967295> protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area <0-4294967295> protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area <0-4294967295> segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area <0-4294967295> verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area 1.2.3.4 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area 1.2.3.4 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area 1.2.3.4 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword area 1.2.3.4 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf someword verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 ospf verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit identifier 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 level 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis someword3 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 isis verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area <0-4294967295> segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area <0-4294967295> verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area 1.2.3.4 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area 1.2.3.4 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area 1.2.3.4 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 area 1.2.3.4 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf someword3 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown ospf verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area <0-4294967295> protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area <0-4294967295> protected-by 1 segment-routing verbatim lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area <0-4294967295> protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area <0-4294967295> segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area <0-4294967295> verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area 1.2.3.4 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area 1.2.3.4 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area 1.2.3.4 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 area 1.2.3.4 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf someword3 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 ospf verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword attribute-set someword2 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 level 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis someword2 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword isis verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area <0-4294967295> protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area <0-4294967295> protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area <0-4294967295> segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area <0-4294967295> verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area 1.2.3.4 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area 1.2.3.4 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area 1.2.3.4 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 area 1.2.3.4 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf someword2 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown ospf verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword lockdown verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area <0-4294967295> protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area <0-4294967295> protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area <0-4294967295> protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area <0-4294967295> segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area <0-4294967295> segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area <0-4294967295> verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area 1.2.3.4 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area 1.2.3.4 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area 1.2.3.4 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area 1.2.3.4 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area 1.2.3.4 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 area 1.2.3.4 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf someword2 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword ospf verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword protected-by 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword protected-by 1 segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword protected-by 1 verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword segment-routing verbatim
                # iosxr: interface tunnel-te1 / path-option 1 explicit name someword verbatim
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis someword2
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis someword2 level 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis someword2 level 1 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis someword2 level 1 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis someword2 level 1 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis someword2 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis someword2 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis lockdown
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword isis protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown ospf
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown ospf someword2
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown ospf someword2 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown ospf someword2 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown ospf someword2 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown ospf someword2 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown ospf someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword ospf
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword ospf someword2
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword ospf someword2 area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword ospf someword2 area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword ospf someword2 area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword ospf someword2 area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword ospf someword2 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing attribute-set someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis someword
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis someword level 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis someword level 1 lockdown
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis someword level 1 lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis someword level 1 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis someword lockdown
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis someword lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis lockdown
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing isis protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown ospf
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown ospf someword
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown ospf someword area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown ospf someword area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown ospf someword area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown ospf someword area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown ospf someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing lockdown protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing ospf
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing ospf someword
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing ospf someword area <0-4294967295>
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing ospf someword area <0-4294967295> protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing ospf someword area 1.2.3.4
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing ospf someword area 1.2.3.4 protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing ospf someword protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing ospf protected-by 1
                # iosxr: interface tunnel-te1 / path-option 1 segment-routing protected-by 1

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

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        self.path_options  # init!
        super().__init__(*args, **kwargs)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # ATTRIBUTES COMMON TO INTERFACE TUNNELS and MPLS NAMED TUNNELS

        # iosxr: interface tunnel-te1 / destination 1.2.3.4
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / destination 1.2.3.4
        configurations.append_line(attributes.format('destination {destination}'))

        # iosxr: interface tunnel-te1 / autoroute announce (config-if-tunte-aa)
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce (config-mpls-te-tunnel-name-aa)
        if attributes.value('autoroute_announce'):
            configurations.append_line('autoroute announce')

        # iosxr: interface tunnel-te1 / autoroute announce / metric 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce / metric 1
        configurations.append_line(attributes.format('autoroute announce metric {autoroute_announce_metric}'))

        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce / include-ipv6
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce / metric absolute 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute announce / metric relative -10
        # iosxr: interface tunnel-te1 / autoroute announce / include-ipv6
        # iosxr: interface tunnel-te1 / autoroute announce / metric absolute 1
        # iosxr: interface tunnel-te1 / autoroute announce / metric relative -10

        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute destination 1.2.3.4
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute metric 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / autoroute metric absolute 1
        # iosxr: interface tunnel-te1 / autoroute destination 1.2.3.4
        # iosxr: interface tunnel-te1 / autoroute metric 1
        # iosxr: interface tunnel-te1 / autoroute metric absolute 1

        # iosxr: interface tunnel-te1 / autoroute metric relative -10
        #TODO

        # iosxr: interface tunnel-te1 / affinity exclude someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
        v = attributes.value('affinity_exclude')
        if v is not None:
            configurations.append_line('affinity exclude {}'.format(' '.join(v)))

        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw (config-mpls-te-tun-autobw)
        # iosxr: interface tunnel-te1 / auto-bw (config-if-tunte-autobw)
        if attributes.value('auto_bw'):
            configurations.append_line('auto-bw')

        # iosxr: interface tunnel-te1 / auto-bw / adjustment-threshold 1
        # iosxr: interface tunnel-te1 / auto-bw / adjustment-threshold 1 min 10
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / adjustment-threshold 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / adjustment-threshold 1 min 10
        cfg = attributes.format('auto-bw adjustment-threshold {auto_bw_adj_threshold_pct}')
        if cfg:
            cfg += attributes.format(' min {auto_bw_adj_threshold_min}', force=True)
            configurations.append_line(cfg)

        # iosxr: interface tunnel-te1 / auto-bw / application 5
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / application 5
        configurations.append_line(attributes.format('auto-bw application {auto_bw_application_freq}'))

        # iosxr: interface tunnel-te1 / auto-bw / bw-limit min <0-4294967295> max 4294967295
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / bw-limit min <0-4294967295> max 4294967295
        configurations.append_line(attributes.format('auto-bw bw-limit min {auto_bw_bwlimit_min} max {auto_bw_bwlimit_min}'))

        # iosxr: interface tunnel-te1 / auto-bw / collect-bw-only
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / collect-bw-only
        if attributes.value('auto_bw_collect_bw_only'):
            configurations.append_line('auto-bw collect-bw-only')

        # iosxr: interface tunnel-te1 / auto-bw / overflow threshold 1 limit 1
        # iosxr: interface tunnel-te1 / auto-bw / overflow threshold 1 min 10 limit 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / overflow threshold 1 limit 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / overflow threshold 1 min 10 limit 1
        if attributes.value('auto_bw_overflow_thresh_pct') is not None \
                and attributes.value('auto_bw_overflow_thresh_limit') is not None:
            cfg = attributes.format('auto-bw overflow threshold {auto_bw_overflow_thresh_pct}')
            cfg += attributes.format(' min {auto_bw_overflow_thresh_min}', force=True)
            cfg += attributes.format(' limit {auto_bw_overflow_thresh_limit}')
            configurations.append_line(cfg)

        # iosxr: interface tunnel-te1 / auto-bw / underflow threshold 1 limit 1
        # iosxr: interface tunnel-te1 / auto-bw / underflow threshold 1 min 10 limit 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / underflow threshold 1 limit 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / auto-bw / underflow threshold 1 min 10 limit 1
        if attributes.value('auto_bw_underflow_thresh_pct') is not None \
                and attributes.value('auto_bw_underflow_thresh_limit') is not None:
            cfg = attributes.format('auto-bw underflow threshold {auto_bw_underflow_thresh_pct}')
            cfg += attributes.format(' min {auto_bw_underflow_thresh_min}', force=True)
            cfg += attributes.format(' limit {auto_bw_underflow_thresh_limit}')
            configurations.append_line(cfg)

        # iosxr: interface tunnel-te1 / auto-bw / disable (config-if-tunte-autobw)
        # iosxr: interface tunnel-te1 / auto-bw / disable / adjustment-threshold 1
        # iosxr: interface tunnel-te1 / auto-bw / disable / adjustment-threshold 1 min 10
        # iosxr: interface tunnel-te1 / auto-bw / disable / application 5
        # iosxr: interface tunnel-te1 / auto-bw / disable / bw-limit min <0-4294967295> max 4294967295
        # iosxr: interface tunnel-te1 / auto-bw / disable / collect-bw-only
        # iosxr: interface tunnel-te1 / auto-bw / disable / overflow threshold 1 limit 1
        # iosxr: interface tunnel-te1 / auto-bw / disable / overflow threshold 1 min 10 limit 1
        # iosxr: interface tunnel-te1 / auto-bw / disable / underflow threshold 1 limit 1
        # iosxr: interface tunnel-te1 / auto-bw / disable / underflow threshold 1 min 10 limit 1
        # auto-bw disable is NOT supported?

        # iosxr: interface tunnel-te1 / priority <0-7> <0-7>
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / priority <0-7> <0-7>
        configurations.append_line(attributes.format('priority {priority_setup} {priority_hold}'))

        # iosxr: interface tunnel-te1 / fast-reroute
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / fast-reroute
        if attributes.value('frr'):
            configurations.append_line('fast-reroute')

        # iosxr: interface tunnel-te1 / fast-reroute protect bandwidth
        # iosxr: interface tunnel-te1 / fast-reroute protect bandwidth node
        # iosxr: interface tunnel-te1 / fast-reroute protect node
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / fast-reroute protect bandwidth
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / fast-reroute protect bandwidth node
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / fast-reroute protect node
        configurations.append_line(attributes.format('fast-reroute protect {frr_protect}'))

        # iosxr: interface tunnel-te1 / signalled-bandwidth <0-4294967295>
        # iosxr: interface tunnel-te1 / signalled-bandwidth <0-4294967295> class-type <0-1>
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / signalled-bandwidth <0-4294967295>
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / signalled-bandwidth <0-4294967295> class-type <0-1>
        cfg = attributes.format('signalled-bandwidth {signalled_bandwidth}')
        if cfg:
            cfg += attributes.format(' class-type {signalled_bandwidth_class_type}', force=True)
            configurations.append_line(cfg)

        # iosxr: interface tunnel-te1 / signalled-bandwidth sub-pool 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / signalled-bandwidth sub-pool 1
        configurations.append_line(attributes.format('signalled-bandwidth sub-pool {signalled_bandwidth_subpool}'))

        # iosxr: interface tunnel-te1 / logging events lsp-status state
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status state
        # iosxr: interface tunnel-te1 / logging events lsp-status reoptimize
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status reoptimize
        # iosxr: interface tunnel-te1 / logging events lsp-status record-route
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status record-route
        if attributes.value('logging_lsp_state'):
            configurations.append_line('logging events lsp-status state')
        if attributes.value('logging_lsp_reopt'):
            configurations.append_line('logging events lsp-status reoptimize')
        if attributes.value('logging_lsp_record_route'):
            configurations.append_line('logging events lsp-status record-route')

        # iosxr: interface tunnel-te1 / soft-preemption
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / soft-preemption
        if attributes.value('soft_preemption'):
            configurations.append_line('soft-preemption')

        # TODO - more attributes
        # iosxr: interface tunnel-te1 / affinity 0x0 mask 0x0
        # iosxr: interface tunnel-te1 / affinity exclude-all
        # iosxr: interface tunnel-te1 / affinity ignore
        # iosxr: interface tunnel-te1 / affinity include someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
        # iosxr: interface tunnel-te1 / affinity include-strict someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity 0x0 mask 0x0
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity exclude-all
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity ignore
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / affinity include-strict someword someword2 someword3 someword4 someword5 someword6 someword7 someword8 someword9 someword10

        # iosxr: interface tunnel-te1 / forward-class 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / forward-class 1

        # iosxr: interface tunnel-te1 / load-interval <0-600>
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / load-interval <0-600>

        # iosxr: interface tunnel-te1 / load-share 1
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / load-share 1

        # iosxr: interface tunnel-te1 / logging events all
        # iosxr: interface tunnel-te1 / logging events bfd-status
        # iosxr: interface tunnel-te1 / logging events link-status
        # iosxr: interface tunnel-te1 / logging events lsp-status bw-change
        # iosxr: interface tunnel-te1 / logging events lsp-status insufficient-bandwidth
        # iosxr: interface tunnel-te1 / logging events lsp-status reoptimize-attempts
        # iosxr: interface tunnel-te1 / logging events lsp-status reroute
        # iosxr: interface tunnel-te1 / logging events lsp-status switchover
        # iosxr: interface tunnel-te1 / logging events pcalc-failure
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events all
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status bw-change
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status insufficient-bandwidth
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status reoptimize-attempts
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status reroute
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events lsp-status switchover
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / logging events pcalc-failure

        # iosxr: interface tunnel-te1 / path-selection (config-if-tunte-path-sel)
        # iosxr: interface tunnel-te1 / path-selection / cost-limit 1
        # iosxr: interface tunnel-te1 / path-selection / hop-limit 1
        # iosxr: interface tunnel-te1 / path-selection / invalidation <0-60000>
        # iosxr: interface tunnel-te1 / path-selection / invalidation <0-60000> drop
        # iosxr: interface tunnel-te1 / path-selection / invalidation <0-60000> tear
        # iosxr: interface tunnel-te1 / path-selection / invalidation drop
        # iosxr: interface tunnel-te1 / path-selection / invalidation tear
        # iosxr: interface tunnel-te1 / path-selection / metric igp
        # iosxr: interface tunnel-te1 / path-selection / metric te
        # iosxr: interface tunnel-te1 / path-selection / segment-routing adjacency protected
        # iosxr: interface tunnel-te1 / path-selection / segment-routing adjacency unprotected
        # iosxr: interface tunnel-te1 / path-selection / tiebreaker max-fill
        # iosxr: interface tunnel-te1 / path-selection / tiebreaker min-fill
        # iosxr: interface tunnel-te1 / path-selection / tiebreaker random
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / metric igp
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / metric te
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / tiebreaker max-fill
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / tiebreaker min-fill
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / path-selection / tiebreaker random

        # iosxr: interface tunnel-te1 / record-route
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / record-route

        # iosxr: interface tunnel-te1 / shutdown
        # iosxr: mpls traffic-eng / named-tunnels / tunnel-te tunnel-te1 / shutdown

        # END ATTRIBUTES COMMON TO INTERFACE TUNNELS and MPLS NAMED TUNNELS

        # ATTRIBUTES for INTERFACE TUNNELS only
        if not self.named_tunnel:
            # iosxr: interface tunnel-te1 / ipv4 unnumbered Loopback0
            configurations.append_line(attributes.format('ipv4 unnumbered {ipv4_unnumbered_interface.name}'))

            # iosxr: interface tunnel-te1 / signalled-name someword
            configurations.append_line(attributes.format('signalled-name {signalled_name}'))

            # iosxr: interface tunnel-te1 / address-family ipv4 multicast
            # iosxr: interface tunnel-te1 / address-family ipv4 multicast topology someword
            # iosxr: interface tunnel-te1 / address-family ipv6 multicast
            # iosxr: interface tunnel-te1 / address-family ipv6 multicast topology someword

            # iosxr: interface tunnel-te1 / anycast source-interface Loopback0
            # iosxr: interface tunnel-te1 / anycast source-interface Loopback0 sync-group 1.2.3.4

            # iosxr: interface tunnel-te1 / backup-bw 1
            # iosxr: interface tunnel-te1 / backup-bw 1 any-class-type
            # iosxr: interface tunnel-te1 / backup-bw 1 class-type <0-1>
            # iosxr: interface tunnel-te1 / backup-bw global-pool 1
            # iosxr: interface tunnel-te1 / backup-bw global-pool unlimited
            # iosxr: interface tunnel-te1 / backup-bw sub-pool 1
            # iosxr: interface tunnel-te1 / backup-bw sub-pool unlimited
            # iosxr: interface tunnel-te1 / backup-bw unlimited any-class-type
            # iosxr: interface tunnel-te1 / backup-bw unlimited class-type <0-1>
            # iosxr: interface tunnel-te1 / bandwidth <0-4294967295>
            # iosxr: interface tunnel-te1 / bfd (config-if-tunte-bfd)
            # iosxr: interface tunnel-te1 / bfd / bringup-timeout 60
            # iosxr: interface tunnel-te1 / bfd / dampening initial-wait 1
            # iosxr: interface tunnel-te1 / bfd / dampening maximum-wait 1
            # iosxr: interface tunnel-te1 / bfd / dampening secondary-wait 1
            # iosxr: interface tunnel-te1 / bfd / encap-mode gal
            # iosxr: interface tunnel-te1 / bfd / fast-detect
            # iosxr: interface tunnel-te1 / bfd / lsp-ping disable
            # iosxr: interface tunnel-te1 / bfd / lsp-ping interval 60
            # iosxr: interface tunnel-te1 / bfd / minimum-interval 3
            # iosxr: interface tunnel-te1 / bfd / multiplier 3
            # iosxr: interface tunnel-te1 / bidirectional (config-if-bidir)
            # iosxr: interface tunnel-te1 / bidirectional / association id <0-65535> source-address 1.2.3.4
            # iosxr: interface tunnel-te1 / bidirectional / association id <0-65535> source-address 1.2.3.4 global-id <0-4294967295>
            # iosxr: interface tunnel-te1 / bidirectional / association type co-routed (config-if-bidir-co-routed)
            # iosxr: interface tunnel-te1 / bidirectional / association type co-routed / fault-oam
            # iosxr: interface tunnel-te1 / bidirectional / association type co-routed / wrap-protection
            # iosxr: interface tunnel-te1 / binding-sid mpls
            # iosxr: interface tunnel-te1 / binding-sid mpls label 16
            # iosxr: interface tunnel-te1 / description some line data
            v = attributes.value('description')
            if v:
                if v is True:
                    pass  # TODO Create a usefull default description
                configurations.append_line('description {}'.format(v))

            # iosxr: interface tunnel-te1 / forwarding-adjacency (config-if-tunte-fwdadj)
            # iosxr: interface tunnel-te1 / forwarding-adjacency / holdtime <0-20000>
            # iosxr: interface tunnel-te1 / forwarding-adjacency / include-ipv6
            # iosxr: interface tunnel-te1 / ipv4 address 1.2.3.0/24
            # iosxr: interface tunnel-te1 / ipv4 address 1.2.3.0/24 route-tag 1
            # iosxr: interface tunnel-te1 / ipv4 address 1.2.3.0/24 secondary
            # iosxr: interface tunnel-te1 / ipv4 address 1.2.3.0/24 secondary route-tag 1
            # iosxr: interface tunnel-te1 / ipv4 directed-broadcast
            # iosxr: interface tunnel-te1 / ipv4 flowspec disable
            # iosxr: interface tunnel-te1 / ipv4 helper-address 1.2.3.4
            # iosxr: interface tunnel-te1 / ipv4 helper-address vrf someword 1.2.3.4
            # iosxr: interface tunnel-te1 / ipv4 mask-reply
            # iosxr: interface tunnel-te1 / ipv4 mtu 68
            # iosxr: interface tunnel-te1 / ipv4 redirects
            # iosxr: interface tunnel-te1 / ipv4 tcp-mss-adjust enable
            # iosxr: interface tunnel-te1 / ipv4 ttl-propagate disable
            # iosxr: interface tunnel-te1 / ipv4 unreachables disable
            # iosxr: interface tunnel-te1 / ipv6 enable
            # iosxr: interface tunnel-te1 / ipv6 flowspec disable
            # iosxr: interface tunnel-te1 / ipv6 tcp-mss-adjust enable
            # iosxr: interface tunnel-te1 / ipv6 ttl-propagate disable

            # iosxr: interface tunnel-te1 / mpls (config-if-mpls)
            # iosxr: interface tunnel-te1 / mpls / label-security multi-label-packet drop
            # iosxr: interface tunnel-te1 / mpls / label-security rpf
            # iosxr: interface tunnel-te1 / mpls / mtu 68

            # iosxr: interface tunnel-te1 / path-protection

            # iosxr: interface tunnel-te1 / pce (config-if-pce)
            # iosxr: interface tunnel-te1 / pce / delegation
            # iosxr: interface tunnel-te1 / pm 15-min ether report fcs-err enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report ifIn-Octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-802-1Q-frames enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-Bcast enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-MIB-CRC enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-MIB-giant enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-MIB-jabber enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-Mcast enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-Ucast enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-drop-abort enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-drop-invalid-DMAC enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-drop-invalid-VLAN enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-drop-invalid-encap enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-drop-other enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-drop-overrun enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-error-collisions enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-error-fragments enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-error-giant enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-error-jabbers enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-error-other enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-error-runt enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-error-symbol enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-good-bytes enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-good-pkts enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-pause-frame enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-pkt-64-octet enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-pkts-1024-1518-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-pkts-128-255-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-pkts-1519-Max-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-pkts-256-511-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-pkts-512-1023-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report in-pkts-65-127octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-802-1Q-frames enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-Bcast enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-Mcast enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-Ucast enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-drop-abort enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-drop-other enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-drop-underrun enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-error-other enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-good-bytes enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-good-pkts enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-pause-frames enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-pkt-64-octet enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-pkts-1024-1518-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-pkts-128-255-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-pkts-1519-Max-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-pkts-256-511-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-pkts-512-1023-octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report out-pkts-65-127octets enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report rx-pkt enable
            # iosxr: interface tunnel-te1 / pm 15-min ether report tx-pkt enable
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold fcs-err 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold ifIn-Octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-802-1Q-frames 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-Bcast 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-MIB-CRC 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-MIB-giant 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-MIB-jabber 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-Mcast 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-Ucast 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-drop-abort 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-drop-invalid-DMAC 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-drop-invalid-VLAN 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-drop-invalid-encap 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-drop-other 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-drop-overrun 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-error-collisions 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-error-fragments 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-error-giant 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-error-jabbers 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-error-other 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-error-runt 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-error-symbol 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-good-bytes 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-good-pkts 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-pause-frame 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-pkt-64-octet 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-pkts-1024-1518-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-pkts-128-255-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-pkts-1519-Max-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-pkts-256-511-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-pkts-512-1023-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold in-pkts-65-127octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-802-1Q-frames 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-Bcast 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-Mcast 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-Ucast 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-drop-abort 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-drop-other 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-drop-underrun 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-error-other 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-good-bytes 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-good-pkts 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-pause-frames 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-pkt-64-octet 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-pkts-1024-1518-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-pkts-128-255-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-pkts-1519-Max-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-pkts-256-511-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-pkts-512-1023-octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold out-pkts-65-127octets 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold rx-pkt 1
            # iosxr: interface tunnel-te1 / pm 15-min ether threshold tx-pkt 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether report fcs-err enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report ifIn-Octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-802-1Q-frames enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-Bcast enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-MIB-CRC enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-MIB-giant enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-MIB-jabber enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-Mcast enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-Ucast enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-drop-abort enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-drop-invalid-DMAC enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-drop-invalid-VLAN enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-drop-invalid-encap enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-drop-other enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-drop-overrun enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-error-collisions enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-error-fragments enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-error-giant enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-error-jabbers enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-error-other enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-error-runt enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-error-symbol enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-good-bytes enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-good-pkts enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-pause-frame enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-pkt-64-octet enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-pkts-1024-1518-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-pkts-128-255-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-pkts-1519-Max-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-pkts-256-511-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-pkts-512-1023-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report in-pkts-65-127octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-802-1Q-frames enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-Bcast enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-Mcast enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-Ucast enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-drop-abort enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-drop-other enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-drop-underrun enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-error-other enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-good-bytes enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-good-pkts enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-pause-frames enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-pkt-64-octet enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-pkts-1024-1518-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-pkts-128-255-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-pkts-1519-Max-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-pkts-256-511-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-pkts-512-1023-octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report out-pkts-65-127octets enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report rx-pkt enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether report tx-pkt enable
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold fcs-err 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold ifIn-Octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-802-1Q-frames 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-Bcast 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-MIB-CRC 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-MIB-giant 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-MIB-jabber 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-Mcast 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-Ucast 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-drop-abort 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-drop-invalid-DMAC 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-drop-invalid-VLAN 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-drop-invalid-encap 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-drop-other 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-drop-overrun 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-error-collisions 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-error-fragments 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-error-giant 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-error-jabbers 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-error-other 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-error-runt 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-error-symbol 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-good-bytes 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-good-pkts 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-pause-frame 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-pkt-64-octet 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-pkts-1024-1518-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-pkts-128-255-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-pkts-1519-Max-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-pkts-256-511-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-pkts-512-1023-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold in-pkts-65-127octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-802-1Q-frames 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-Bcast 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-Mcast 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-Ucast 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-drop-abort 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-drop-other 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-drop-underrun 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-error-other 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-good-bytes 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-good-pkts 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-pause-frames 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-pkt-64-octet 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-pkts-1024-1518-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-pkts-128-255-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-pkts-1519-Max-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-pkts-256-511-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-pkts-512-1023-octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold out-pkts-65-127octets 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold rx-pkt 1
            # iosxr: interface tunnel-te1 / pm 24-hour ether threshold tx-pkt 1
            # iosxr: interface tunnel-te1 / policy-class 1
            # iosxr: interface tunnel-te1 / policy-class 1 1
            # iosxr: interface tunnel-te1 / policy-class 1 1 1
            # iosxr: interface tunnel-te1 / policy-class 1 1 1 1
            # iosxr: interface tunnel-te1 / policy-class 1 1 1 1 1
            # iosxr: interface tunnel-te1 / policy-class 1 1 1 1 1 1
            # iosxr: interface tunnel-te1 / policy-class 1 1 1 1 1 1 1
            # iosxr: interface tunnel-te1 / policy-class default

            # END ATTRIBUTES for INTERFACE TUNNELS only

        # ADD PATH OPTIONS

        # iosxr: l2vpn / xconnect group someword / mp2mp someword2 / autodiscovery bgp / signaling-protocol bgp / ce-id 1 (config-l2vpn)
        for ns, attributes2 in attributes.mapping_values('path_option_attr', keys=self.path_options, sort=True):
            configurations.append_block(ns.build_config(apply=False, unconfig=unconfig, attributes=attributes2))


class NamedTunnelInterface(genie.libs.conf.interface.NamedTunnelInterface, TunnelInterface, PseudoInterface):

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TunnelTeInterface(TunnelInterface):

    _interface_name_types = (
        'tunnel-te',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TunnelTpInterface(TunnelInterface):

    _interface_name_types = (
        'tunnel-tp',
    )

    # TODO -- stay abstract meanwhile
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class NamedTunnelTeInterface(NamedTunnelInterface, TunnelTeInterface, genie.libs.conf.interface.NamedTunnelTeInterface):

    def _build_config_create_interface_submode_context(self, configurations):
        @contextlib.contextmanager
        def multiple_submode_context():
            # iosxr: mpls traffic-eng (config-mpls-te)
            with configurations.submode_context('mpls traffic-eng', cancel_empty=True):
                # iosxr: mpls traffic-eng / named-tunnels (config-mpls-te-named-tunnels)
                with configurations.submode_context('named-tunnels', cancel_empty=True):
                    # iosxr: mpls traffic-eng / named-tunnels / tunnel-te {signalled_name} (config-mpls-te-tunnel-name)
                    with configurations.submode_context('tunnel-te {}'.format(self.signalled_name)):
                        yield

        return multiple_submode_context()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BundleInterface(VirtualInterface, genie.libs.conf.interface.AggregatedInterface,
    genie.libs.conf.interface.LagInterface):

    _interface_name_number_range = range(1, 65535 + 1)

    mlacp_iccp_group = managedattribute(
        name='mlacp_iccp_group',
        default=None,
        type=(None, managedattribute.test_isinstance(IccpGroup)))

    mlacp_port_priority = managedattribute(
        name='mlacp_port_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    @property    
    def members(self):
        '''Member interfaces of this bundle'''
        return frozenset(
            interface
            for interface in self.device.interfaces
            if getattr(interface, 'bundle', None) is self)

    @members.setter
    def members(self, interfaces):
        interfaces = set(interfaces)
        for interface in interfaces:
            if not isinstance(interface, Interface):
                raise ValueError(interface)
            if interface.device is not self.device:
                raise ValueError('%r cannot be a member of %r' % (interface, self))
        old_members = self.members
        for interface in old_members - interfaces:
            interface.bundle = None
        for interface in interfaces - old_members:
            interface.bundle = self

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        super()._build_config_interface_submode(configurations=configurations,
                                                attributes=attributes,
                                                unconfig=unconfig)

        # iosxr: interface {name} / mlacp iccp-group 1
        configurations.append_line(attributes.format('mlacp iccp-group {mlacp_iccp_group.group_id}'))

        # iosxr: interface {name} / mlacp port-priority 1
        configurations.append_line(attributes.format('mlacp port-priority {mlacp_port_priority}'))

        # iosxr: interface {name} / bfd address-family ipv4 destination 5.0.0.97
        configurations.append_line(attributes.format('bfd address-family ipv4 destination {lag_bfd_v4_destination}'))

        # iosxr: interface {name} / bfd address-family ipv4 fast-detect
        if attributes.value('lag_bfd_v4_fast_detect'):
            configurations.append_line(attributes.format('bfd address-family ipv4 fast-detect'))

        # iosxr: interface {name} / bfd address-family ipv4 minimum-interval 100
        configurations.append_line(attributes.format('bfd address-family ipv4 minimum-interval {lag_bfd_v4_min_interval}'))

        # iosxr: interface {name} / bfd address-family ipv6 destination 5.0.0.97
        configurations.append_line(attributes.format('bfd address-family ipv6 destination {lag_bfd_v6_destination}'))

        # iosxr: interface {name} / bfd address-family ipv6 fast-detect
        if attributes.value('lag_bfd_v6_fast_detect'):
            configurations.append_line(attributes.format('bfd address-family ipv6 fast-detect'))

        # iosxr: interface {name} / bfd address-family ipv6 minimum-interval 100
        configurations.append_line(attributes.format('bfd address-family ipv6 minimum-interval {lag_bfd_v6_min_interval}'))

        # iosxr: interface {name} / mlacp switchover ... TODO

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BundleEtherInterface(BundleInterface):

    _interface_name_types = (
        'Bundle-Ether',
    )

    eth_encap_type1 = EthernetInterface.eth_encap_type1.copy()
    eth_encap_val1 = EthernetInterface.eth_encap_val1.copy()
    eth_encap_type2 = EthernetInterface.eth_encap_type2.copy()
    eth_encap_val2 = EthernetInterface.eth_encap_val2.copy()
    eth_dot1q_type = EthernetInterface.eth_dot1q_type.copy()
    eth_dot1q_value = EthernetInterface.eth_dot1q_value.copy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BundlePosInterface(BundleInterface):

    _interface_name_types = (
        'Bundle-POS',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BviInterface(VirtualInterface, genie.libs.conf.interface.BviInterface):

    _interface_name_types = (
        'BVI',
    )

    _interface_name_number_range = range(1, 65535 + 1)

    host_routing = managedattribute(
        name='host_routing',
        default=None,
        type=managedattribute.test_istype(bool))

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        super()._build_config_interface_submode(configurations=configurations,
                                                attributes=attributes,
                                                unconfig=unconfig)

        if attributes.value('host_routing'):
            configurations.append_line('host-routing')

        # iosxr: interface {name} / mac-address aaaa.bbbb.cccc
        configurations.append_line(attributes.format('mac-address {mac_address}'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NveInterface(VirtualInterface, genie.libs.conf.interface.NveInterface):

    _interface_name_types = (
        'nve',
    )

    overlay_encapsulation = managedattribute(
        name='overlay_encapsulation',
        default=None,
        type=(None, managedattribute.test_istype(str)))  # TODO

    source_interface = managedattribute(
        name='source_interface',
        default=None,
        type=(None, managedattribute.test_isinstance(Interface)))

    vxlan_udp_port = managedattribute(
        name='vxlan_udp_port',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    class RedundancyNamespace(ConfigurableInterfaceNamespace):

        enabled = managedattribute(
            name='enabled',
            default=False,
            type=managedattribute.test_istype(bool))

        class BackboneMplsNamespace(ConfigurableInterfaceNamespace):

            enabled = managedattribute(
                name='enabled',
                default=False,
                type=managedattribute.test_istype(bool))

            iccp_group = managedattribute(
                name='iccp_group',
                default=None,
                type=(None, managedattribute.test_isinstance(IccpGroup)))

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if attributes.value('enabled'):
                    # iosxr: interface nve1 / redundancy / backbone mpls (config-nve-red-backbone-mpls)
                    with configurations.submode_context('backbone mpls'):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: interface nve1 / redundancy / backbone mpls / iccp group 1
                        configurations.append_line(attributes.format('iccp group {iccp_group.group_id}'))

                return configurations

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        backbone_mpls = managedattribute(
            name='backbone_mpls',
            read_only=True,
            doc=BackboneMplsNamespace.__doc__)

        @backbone_mpls.initter
        def backbone_mpls(self):
            return self.BackboneMplsNamespace(interface=self.interface)

        class BackboneVxlanNamespace(ConfigurableInterfaceNamespace):

            enabled = managedattribute(
                name='enabled',
                default=False,
                type=managedattribute.test_istype(bool))

            iccp_group = managedattribute(
                name='iccp_group',
                default=None,
                type=(None, managedattribute.test_isinstance(IccpGroup)))

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not apply
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if attributes.value('enabled'):
                    # iosxr: interface nve1 / redundancy / backbone vxlan (config-nve-red-backbone-vxlan)
                    with configurations.submode_context('backbone vxlan'):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        # iosxr: interface nve1 / redundancy / backbone vxlan / iccp group 1
                        configurations.append_line(attributes.format('iccp group {iccp_group.group_id}'))

                return configurations

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        backbone_vxlan = managedattribute(
            name='backbone_vxlan',
            read_only=True,
            doc=BackboneVxlanNamespace.__doc__)

        @backbone_vxlan.initter
        def backbone_vxlan(self):
            return self.BackboneVxlanNamespace(interface=self.interface)

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not apply
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            if attributes.value('enabled'):
                # iosxr: interface nve1 / redundancy (config-nve-red)
                with configurations.submode_context('redundancy'):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # iosxr: interface nve1 / redundancy / backbone mpls (config-nve-red-backbone-mpls)
                    sub, attributes2 = attributes.namespace('backbone_mpls')
                    if sub:
                        configurations.append_block(
                            sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

                    # iosxr: interface nve1 / redundancy / backbone vxlan (config-nve-red-backbone-vxlan)
                    sub, attributes2 = attributes.namespace('backbone_vxlan')
                    if sub:
                        configurations.append_block(
                            sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

            return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

    redundancy = managedattribute(
        name='redundancy',
        read_only=True,
        doc=RedundancyNamespace.__doc__)

    @redundancy.initter
    def redundancy(self):
        return self.RedundancyNamespace(interface=self)

    vnis_map = managedattribute(
        name='vnis_map',
        finit=dict,
        doc='''Mapping of Vni.vni_id to Vni objects''')

    @property
    def vnis(self):
        return frozenset(self.vnis_map.values())

    def add_vni(self, vni):
        if vni.vni_id in self.vnis_map:
            raise ValueError(
                'Duplicate vni {} exists within {!r}'.\
                format(vni.vni_id, self))
        self.vnis_map[vni.vni_id] = vni
        vni._on_added_from_nve_interface(self)

    def remove_vni(self, vni):
        try:
            vni_id = vni.vni_id
        except AttributeError:
            vni_id = vni
            vni = None

        try:
            old_vni = self.vnis_map.pop(vni_id)
        except KeyError:
            raise ValueError(
                'Vni {!r} does not exist within {!r}'.\
                format(vni or vni_id, self))

        if vni is not None and old_vni is not vni:
            self.vnis_map[vni_id] = old_vni
            raise ValueError(
                'Vni {!r} does not match existing {!r} within {!r}'.\
                format(vni, old_vni, self))

        vni._on_removed_from_nve_interface(self)

    def _build_config_interface_submode(self, configurations, attributes, unconfig):

        # iosxr: interface nve1 (config-if)

        super()._build_config_interface_submode(configurations=configurations,
                                                attributes=attributes,
                                                unconfig=unconfig)

        # iosxr: interface nve1 / logging events link-status

        # iosxr: interface nve1 / member vni 1 (config-nve-vni)
        def cmp_vni_key(vni, key):
            return vni.vni_id == int(key)

        for vni, attributes2 in attributes.sequence_values('vnis', sort=True,
                                                           cmp=cmp_vni_key):
            configurations.append_block(
                vni.build_config(apply=False, attributes=attributes2, unconfig=unconfig,
                                 contained=True))

        # iosxr: interface nve1 / overlay-encapsulation soft-gre
        # iosxr: interface nve1 / overlay-encapsulation vxlan
        configurations.append_line(attributes.format('overlay-encapsulation {overlay_encapsulation}'))

        # iosxr: interface nve1 / redundancy (config-nve-red)
        sub, attributes2 = attributes.namespace('redundancy')
        if sub:
            configurations.append_block(
                sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig))

        # iosxr: interface nve1 / source-interface Loopback0
        configurations.append_line(attributes.format('source-interface {source_interface.name}'))

        # iosxr: interface nve1 / vxlan-udp-port 4789
        configurations.append_line(attributes.format('vxlan-udp-port {vxlan_udp_port}'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

Interface._build_name_to_class_map()

