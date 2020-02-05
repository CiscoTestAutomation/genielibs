
__all__ = (
    'Rsvp',
)

from enum import Enum

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature, LinkFeature
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesHelper
from pyats.datastructures import WeakList
from genie.libs.conf.base import IPv4Neighbor, IPv4Address
from genie.libs.conf.base.neighbor import IPv4NeighborSubAttributes
from genie.libs.conf.address_family import AddressFamily
from genie.libs.conf.vrf import Vrf, VrfSubAttributes
from genie.libs.conf.access_list import AccessList


class Rsvp(DeviceFeature, LinkFeature):

    @property
    def interfaces(self):
        interfaces = set()
        interfaces.update(*[link.interfaces for link in self.links])
        return frozenset(interfaces)

    @property
    def controllers(self):
        controllers = set()
        # TODO
        return frozenset(controllers)

    # Top level attributes

    auth_keysrc_keychain = managedattribute(
        name='auth_keysrc_keychain',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    auth_lifetime = managedattribute(
        name='auth_lifetime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    auth_window_size = managedattribute(
        name='auth_window_size',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    auth_retransmit = managedattribute(
        name='auth_retransmit',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    log_events_issu = managedattribute(
        name='log_events_issu',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    log_events_nsr = managedattribute(
        name='log_events_nsr',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    sig_checksum = managedattribute(
        name='sig_checksum',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    sig_event_per_pulse = managedattribute(
        name='sig_event_per_pulse',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_gr = managedattribute(
        name='sig_gr',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    sig_gr_mode = managedattribute(
        name='sig_gr_mode',
        default='full',
        type=(None, managedattribute.test_istype(str)))

    sig_gr_recov_time = managedattribute(
        name='sig_gr_recov_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_gr_restart_time = managedattribute(
        name='sig_gr_restart_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_hello_gr_refresh_interval = managedattribute(
        name='sig_hello_gr_refresh_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_hello_gr_refresh_misses = managedattribute(
        name='sig_hello_gr_refresh_misses',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_message_bundle = managedattribute(
        name='sig_message_bundle',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    sig_outofband_vrf = managedattribute(
        name='sig_outofband_vrf',
        default=None,
        type=(None, managedattribute.test_isinstance(Vrf)))

    sig_patherr_state_removal = managedattribute(
        name='sig_patherr_state_removal',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    sig_prefixfilt_acl = managedattribute(
        name='sig_prefixfilt_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    class PrefixFilteringAction(Enum):
        drop = 'drop'

    sig_prefixfilt_defdenyaction = managedattribute(
        name='sig_prefixfilt_defdenyaction',
        default=None,
        type=(None, PrefixFilteringAction))

    # Per-interface attributes

    sig_refresh_outofband_interval = managedattribute(
        name='sig_refresh_outofband_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_refresh_outofband_missed = managedattribute(
        name='sig_refresh_outofband_missed',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_dscp = managedattribute(
        name='sig_dscp',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_hello_gr_intfbased = managedattribute(
        name='sig_hello_gr_intfbased',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    sig_rate_limit = managedattribute(
        name='sig_rate_limit',
        default=None,
        type=(None, managedattribute.test_istype((bool, int))))

    sig_rate_limit_interval = managedattribute(
        name='sig_rate_limit_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_refresh_interval = managedattribute(
        name='sig_refresh_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_refresh_missed = managedattribute(
        name='sig_refresh_missed',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_refresh_reduction_bundle_maxsize = managedattribute(
        name='sig_refresh_reduction_bundle_maxsize',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_refresh_reduction = managedattribute(
        name='sig_refresh_reduction',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    sig_refresh_reduction_reliable_ack_holdtime = managedattribute(
        name='sig_refresh_reduction_reliable_ack_holdtime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_refresh_reduction_reliable_ack_maxsize = managedattribute(
        name='sig_refresh_reduction_reliable_ack_maxsize',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_refresh_reduction_reliable_retransmit_time = managedattribute(
        name='sig_refresh_reduction_reliable_retransmit_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    sig_refresh_reduction_reliable_summary_refresh = managedattribute(
        name='sig_refresh_reduction_reliable_summary_refresh',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    sig_refresh_reduction_summary_maxsize = managedattribute(
        name='sig_refresh_reduction_summary_maxsize',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    class BwUnit(Enum):
        kbps = 'kbps'
        mbps = 'mbps'
        gbps = 'gbps'

    enable_default_bw = managedattribute(
        name='enable_default_bw',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    class RdmBwCliStyle(Enum):
        unnamed_subpool = 'unnamed_subpool'
        bc0_bc1 = 'bc0_bc1'
        global_subpool = 'global_subpool'

    rdm_bw_cli_rdm_kw = managedattribute(
        name='rdm_bw_cli_rdm_kw',
        default=True,
        type=managedattribute.test_istype(bool))

    rdm_bw_cli_style = managedattribute(
        name='rdm_bw_cli_style',
        default=RdmBwCliStyle.unnamed_subpool,
        type=RdmBwCliStyle)

    rdm_bw_percentage = managedattribute(
        name='rdm_bw_percentage',
        default=False,
        type=managedattribute.test_istype(bool))

    rdm_bw_total = managedattribute(
        name='rdm_bw_total',
        default=20000,
        type=(None, managedattribute.test_istype(int)))

    rdm_bw_total_unit = managedattribute(
        name='rdm_bw_total_unit',
        default=None,
        type=(None, BwUnit))

    rdm_bw_largest = managedattribute(
        name='rdm_bw_largest',
        default=20000,
        type=(None, managedattribute.test_istype(int)))

    rdm_bw_largest_unit = managedattribute(
        name='rdm_bw_largest_unit',
        default=None,
        type=(None, BwUnit))

    rdm_bw_subpool = managedattribute(
        name='rdm_bw_subpool',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    rdm_bw_subpool_unit = managedattribute(
        name='rdm_bw_subpool_unit',
        default=None,
        type=(None, BwUnit))

    mam_bw_percentage = managedattribute(
        name='mam_bw_percentage',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    mam_bw_max_reservable = managedattribute(
        name='mam_bw_max_reservable',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    mam_bw_total = managedattribute(
        name='mam_bw_total',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    mam_bw_total_unit = managedattribute(
        name='mam_bw_total_unit',
        default=None,
        type=(None, BwUnit))

    mam_bw_largest = managedattribute(
        name='mam_bw_largest',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    mam_bw_largest_unit = managedattribute(
        name='mam_bw_largest_unit',
        default=None,
        type=(None, BwUnit))

    mam_bw_bc0 = managedattribute(
        name='mam_bw_bc0',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    mam_bw_bc0_unit = managedattribute(
        name='mam_bw_bc0_unit',
        default=None,
        type=(None, BwUnit))

    mam_bw_bc1 = managedattribute(
        name='mam_bw_bc1',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    mam_bw_bc1_unit = managedattribute(
        name='mam_bw_bc1_unit',
        default=None,
        type=(None, BwUnit))

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        enabled_feature = managedattribute(
            name='enabled_feature',
            default=False,
            type=managedattribute.test_istype(bool),
            doc='''Argument to control 'mpls traffic-engineering' CLI''')

        @property
        def interfaces(self):
            device = self.device
            interfaces = set(self.parent.interfaces)
            #interfaces.update(*[link.interfaces for link in self.parent.links])
            interfaces = {intf for intf in interfaces if intf.device is device}
            return frozenset(interfaces)

        @property
        def controllers(self):
            # TODO
            device = self.device
            controllers = set(self.parent.controllers)
            #controllers.update(*[link.interfaces for link in self.parent.links])
            controllers = {intf for intf in controllers if intf.device is device}
            return frozenset(controllers)

        neighbors = managedattribute(
            name='neighbors',
            finit=typedset(IPv4NeighborSubAttributes).copy,
            type=typedset(IPv4NeighborSubAttributes)._from_iterable)

        def add_neighbor(self, neighbor):  # TODO DEPRECATE
            self.neighbors.add(neighbor)

        def remove_neighbor(self, neighbor):  # TODO DEPRECATE
            self.neighbors.remove(neighbor)

        class InterfaceAttributes(genie.conf.base.attributes.InterfaceSubAttributes):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

        class NeighborAttributes(IPv4NeighborSubAttributes):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        neighbor_attr = managedattribute(
            name='neighbor_attr',
            read_only=True,
            doc=NeighborAttributes.__doc__)

        @neighbor_attr.initter
        def neighbor_attr(self):
            return SubAttributesDict(self.NeighborAttributes, parent=self)

        class ControllerAttributes(genie.conf.base.attributes.InterfaceSubAttributes):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        controller_attr = managedattribute(
            name='controller_attr',
            read_only=True,
            doc=ControllerAttributes.__doc__)

        @controller_attr.initter
        def controller_attr(self):
            return SubAttributesDict(self.ControllerAttributes, parent=self)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, pid=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_config(self, links=None, apply=True, attributes=None, **kwargs):
        '''Rsvp top build config'''
        attributes = AttributesHelper(self, attributes)

        cfgs = {}

        if links is None:
            devices = self.devices
        else:
            devices = set().union(*[link.devices for link in links])

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, links=None, apply=True, attributes=None, **kwargs):
        '''Rsvp top build unconfig'''
        attributes = AttributesHelper(self, attributes)

        cfgs = {}

        if links is None:
            devices = self.devices
        else:
            devices = set().union(*[link.devices for link in links])

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

