import abc

from genie.decorator import managedattribute

from genie.libs.conf.interface.iosxe import Interface

from genie.libs.conf.interface import (
    Interface as BaseInterface,
    ParsedInterfaceName as BaseParsedInterfaceName,
    PhysicalInterface as BasePhysicalInterface,
    VirtualInterface as BaseVirtualInterface,
    LoopbackInterface as BaseLoopbackInterface,
    LagInterface as BaseLagInterface,
    EthernetInterface as BaseEthernetInterface,
    SubInterface as BaseSubInterface,
    TunnelInterface as BaseTunnelInterface,
    TunnelTeInterface as BaseTunnelTeInterface,
    VlanInterface as BaseVlanInterface,
    NveInterface as BaseNveInterface)

class PhysicalInterface(Interface, BasePhysicalInterface):

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

        if self.breakout is not None:
            # breakout must be configured at global config level
            breakout = attributes.value('breakout')
            if breakout is not None:
                d_parsed = self.parse_interface_name()
                self.device.custom_config_cli += '\nhw-module breakout {port}'.format(
                    port=d_parsed.port)

    breakout = managedattribute(
        name='breakout',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)