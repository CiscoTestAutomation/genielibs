
__all__ = (
    'Ldp',
)

import re

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature, LinkFeature, Interface
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesHelper

from genie.libs.conf.base import IPv4Address, IPv6Address
from genie.libs.conf.base.neighbor import IPv4LsrNeighbor, IPv6Neighbor, IPLsrNeighborSubAttributes
from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes
from genie.libs.conf.vrf import Vrf, VrfSubAttributes
from genie.libs.conf.base import PasswordType
from genie.libs.conf.access_list import AccessList
from genie.libs.conf.route_policy import RoutePolicy

def _ldp_neighbor(value):
    try:
        return IPv4LsrNeighbor(value)
    except (TypeError, ValueError):
        pass
    try:
        return IPv6Neighbor(value)
    except (TypeError, ValueError):
        pass
    raise ValueError(value)


class Ldp(DeviceFeature, LinkFeature):

    @property
    def interfaces(self):
        interfaces = set()
        interfaces.update(*[link.interfaces for link in self.links])
        return frozenset(interfaces)

    @property
    def vrfs(self):
        return \
            self.force_vrfs | \
            {intf.vrf for intf in self.interfaces}

    force_vrfs = managedattribute(
        name='force_vrfs',
        read_only=True,
        finit=set,
        gettype=frozenset)
    # XXXJST TODO force_vrfs needs to also be accessible per-device. Being read_only, that can't happen

    def add_force_vrf(self, vrf):
        assert vrf is None or isinstance(vrf, Vrf)
        self.force_vrfs  # init!
        self._force_vrfs.add(vrf)

    def remove_force_vrf(self, vrf):
        assert vrf is None or isinstance(vrf, Vrf)
        self.force_vrfs  # init!
        self._force_vrfs.remove(vrf)

    address_families = managedattribute(
        name='address_families',
        finit=typedset(AddressFamily, {AddressFamily.ipv4}).copy,
        type=typedset(AddressFamily)._from_iterable)

    # Top level configs

    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    default_route = managedattribute(
        name='default_route',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    capabilities_cisco_iosxr = managedattribute(
        name='capabilities_cisco_iosxr',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    default_vrf_impl_ipv4 = managedattribute(
        name='default_vrf_impl_ipv4',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ds_tlv = managedattribute(
        name='ds_tlv',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    hello_holdtime = managedattribute(
        name='hello_holdtime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    targetted_hello_holdtime = managedattribute(
        name='targetted_hello_holdtime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    hello_interval = managedattribute(
        name='hello_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    targetted_hello_interval = managedattribute(
        name='targetted_hello_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    instance_tlv = managedattribute(
        name='instance_tlv',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    quickstart = managedattribute(
        name='quickstart',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    targeted_hello_holdtime = managedattribute(
        name='targeted_hello_holdtime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    targeted_hello_interval = managedattribute(
        name='targeted_hello_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    entropy_label = managedattribute(
        name='entropy_label',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    gr = managedattribute(
        name='gr',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    gr_fwdstate_holdtime = managedattribute(
        name='gr_fwdstate_holdtime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    gr_max_recovery = managedattribute(
        name='gr_max_recovery',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    gr_neighbor_liveness = managedattribute(
        name='gr_neighbor_liveness',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    gr_reconnect_timeout = managedattribute(
        name='gr_reconnect_timeout',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    igp_sync = managedattribute(
        name='igp_sync',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    igp_sync_delay_time = managedattribute(
        name='igp_sync_delay_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    igp_sync_delay_on_proc_restart = managedattribute(
        name='igp_sync_delay_on_proc_restart',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    igp_sync_delay_on_session_up = managedattribute(
        name='igp_sync_delay_on_session_up',
        default=None,
        type=(None,
              managedattribute.test_istype(int),
              managedattribute.test_in((
                  False,
              ))))

    log_gr = managedattribute(
        name='log_gr',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    log_hello_adj = managedattribute(
        name='log_hello_adj',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    log_neighbor = managedattribute(
        name='log_neighbor',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    log_nsr = managedattribute(
        name='log_nsr',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    log_sess_prot = managedattribute(
        name='log_sess_prot',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    ltrace_buffer_multiplier = managedattribute(
        name='ltrace_buffer_multiplier',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    dualstack_tlv_compliance = managedattribute(
        name='dualstack_tlv_compliance',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    dualstack_transport_max_wait = managedattribute(
        name='dualstack_transport_max_wait',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    dualstack_transport_prefer_ipv4 = managedattribute(
        name='dualstack_transport_prefer_ipv4',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    password_type = managedattribute(
        name='password_type',
        default=None,
        type=(None, PasswordType))

    password = managedattribute(
        name='password',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    password_for_acl = managedattribute(
        name='password_for_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    disable_password = managedattribute(
        name='disable_password',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    nsr = managedattribute(
        name='nsr',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    session_backoff_init = managedattribute(
        name='session_backoff_init',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    session_backoff_max = managedattribute(
        name='session_backoff_max',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    session_holdtime = managedattribute(
        name='session_holdtime',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    session_protection = managedattribute(
        name='session_protection',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    session_protection_for_acl = managedattribute(
        name='session_protection_for_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    session_protection_dur = managedattribute(
        name='session_protection_dur',
        default=None,
        type=(None,
              managedattribute.test_istype(int),
              managedattribute.test_in((
                  float('inf'),
              ))))

    signalling_dscp = managedattribute(
        name='signalling_dscp',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    session_dod_with_acl = managedattribute(
        name='session_dod_with_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    gr_maintain_acl = managedattribute(
        name='gr_maintain_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    disc_hello_dualstack_tlv = managedattribute(
        name='disc_hello_dualstack_tlv',
        default=None,
        type=(None, managedattribute.test_in((
            AddressFamily.ipv4,
            AddressFamily.ipv6,
        ))))

    igp_autoconfig = managedattribute(
        name='igp_autoconfig',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    transport_address = managedattribute(
        name='transport_address',
        default=None,
        type=(None,
              managedattribute.test_in((
                  'interface',
              )),
              IPv4Address,
              IPv6Address))

    targeted = managedattribute(
        name='targeted',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    advertise = managedattribute(
        name='advertise',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    advertise_expnull = managedattribute(
        name='advertise_expnull',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    advertise_expnull_for_acl = managedattribute(
        name='advertise_expnull_for_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    advertise_expnull_to_acl = managedattribute(
        name='advertise_expnull_to_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    advertise_interfaces = managedattribute(
        name='advertise_interfaces',
        finit=typedset(managedattribute.test_isinstance(Interface)).copy,
        type=typedset(managedattribute.test_isinstance(Interface))._from_iterable)

    allocate_for_acl = managedattribute(
        name='allocate_for_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    allocate_for_host_routes = managedattribute(
        name='allocate_for_host_routes',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    default_route = managedattribute(
        name='default_route',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    impnull_override_for_acl = managedattribute(
        name='impnull_override_for_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    targeted_hello_accept = managedattribute(
        name='targeted_hello_accept',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    targeted_hello_accept_from_acl = managedattribute(
        name='targeted_hello_accept_from_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    redist_bgp = managedattribute(
        name='redist_bgp',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    redist_bgp_advto_acl = managedattribute(
        name='redist_bgp_advto_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    redist_bgp_as = managedattribute(
        name='redist_bgp_as',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    te_autotunnel_mesh_group_id = managedattribute(
        name='te_autotunnel_mesh_group_id',
        default=None,
        type=(None,
              managedattribute.test_in((
                  'all',
              )),
              managedattribute.test_istype(int)))

    advertise_for_acl = managedattribute(
        name='advertise_for_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    advertise_to_acl = managedattribute(
        name='advertise_to_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    accept_for_acl = managedattribute(
        name='accept_for_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    session_dod_acl = managedattribute(
        name='session_dod_acl',
        default=None,
        type=(None, managedattribute.test_isinstance(AccessList)))

    class MldpAttributes(object):

        enabled = managedattribute(
            name='enabled',
            default=False,
            type=managedattribute.test_istype(bool))

        csc = managedattribute(
            name='csc',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        forwarding_recursive = managedattribute(
            name='forwarding_recursive',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        forwarding_recursive_route_policy = managedattribute(
            name='forwarding_recursive_route_policy',
            default=None,
            type=(None, managedattribute.test_isinstance(RoutePolicy)))

        make_before_break = managedattribute(
            name='make_before_break',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        make_before_break_delay = managedattribute(
            name='make_before_break_delay',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        make_before_break_delete_delay = managedattribute(
            name='make_before_break_delete_delay',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        make_before_break_route_policy = managedattribute(
            name='make_before_break_route_policy',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        mofrr = managedattribute(
            name='mofrr',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        mofrr_route_policy = managedattribute(
            name='mofrr_route_policy',
            default=None,
            type=(None, managedattribute.test_isinstance(RoutePolicy)))

        route_policy_in = managedattribute(
            name='route_policy_in',
            default=None,
            type=(None, managedattribute.test_isinstance(RoutePolicy)))

        recursive_fec = managedattribute(
            name='recursive_fec',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        recorsive_fec_route_policy = managedattribute(
            name='recorsive_fec_route_policy',
            default=None,
            type=(None, managedattribute.test_isinstance(RoutePolicy)))

        rib_unicast_always = managedattribute(
            name='rib_unicast_always',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        # TODO need support for multiple root_ip/num_lsps
        mp2mp_static_root_ip = managedattribute(
            name='mp2mp_static_root_ip',
            default=None,
            type=(None, IPv4Address))

        mp2mp_static_num_lsps = managedattribute(
            name='mp2mp_static_num_lsps',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        p2mp_static_root_ip = managedattribute(
            name='p2mp_static_root_ip',
            default=None,
            type=(None, IPv4Address))

        p2mp_static_num_lsps = managedattribute(
            name='p2mp_static_num_lsps',
            default=None,
            type=(None, managedattribute.test_istype(int)))

        log_internal = managedattribute(
            name='log_internal',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

        log_notifications = managedattribute(
            name='log_notifications',
            default=None,
            type=(None, managedattribute.test_istype(bool)))

    mldp = managedattribute(
        name='mldp',
        read_only=True,
        finit=MldpAttributes,
        doc=MldpAttributes.__doc__)

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        enabled_feature = managedattribute(
            name='enabled_feature',
            default=False,
            type=managedattribute.test_istype(bool),
            doc='''Argument to control 'feature ldp' CLI''')

        address_families = managedattribute(
            name='address_families',
            type=typedset(AddressFamily)._from_iterable)

        @address_families.defaulter
        def address_families(self):
            return frozenset(self.parent.address_families)

        advertise_interfaces = managedattribute(
            name='advertise_interfaces',
            type=typedset(managedattribute.test_isinstance(Interface))._from_iterable)

        @advertise_interfaces.defaulter
        def advertise_interfaces(self):
            device = self.device
            return frozenset(interface
                             for interface in self.parent.advertise_interfaces
                             if interface.device is device)

        @property
        def vrfs(self):
            return \
                self.force_vrfs | \
                {intf.vrf for intf in self.interfaces}

        @property
        def interfaces(self):
            device = self.device
            interfaces = set(self.parent.interfaces)
            #interfaces.update(*[link.interfaces for link in self.parent.links])
            interfaces = {intf for intf in interfaces if intf.device is device}
            return frozenset(interfaces)

        class MldpAttributes(SubAttributes):

            def __init__(self, _device_attr):
                self._device_attr = _device_attr
                super().__init__(
                        # Ldp.mldp
                        parent=_device_attr.parent.mldp)

            @property
            def testbed(self):
                return self._device_attr.testbed

            @property
            def device_name(self):
                return self._device_attr.device_name

            @property
            def device(self):
                return self._device_attr.device

        mldp = managedattribute(
            name='mldp',
            read_only=True,
            doc=MldpAttributes.__doc__)

        @mldp.initter
        def mldp(self):
            return self.MldpAttributes(_device_attr=self)

        class VrfAttributes(VrfSubAttributes):

            address_families = managedattribute(
                name='address_families',
                type=typedset(AddressFamily)._from_iterable)

            @address_families.defaulter
            def address_families(self):
                return frozenset(self.parent.address_families)

            advertise_interfaces = managedattribute(
                name='advertise_interfaces',
                type=typedset(managedattribute.test_isinstance(Interface))._from_iterable)

            @advertise_interfaces.defaulter
            def advertise_interfaces(self):
                return frozenset(self.parent.advertise_interfaces)

            # implicit: interface_attr = parent.interface_attr
            # implicit: interfaces = parent.interfaces

            router_id = managedattribute(
                name='router_id',
                default=None,
                type=(None, IPv4Address,\
                      managedattribute.test_isinstance(Interface)))

            class NeighborAttributes(IPLsrNeighborSubAttributes):

                def __init__(self, **kwargs):
                    super().__init__(**kwargs)

            neighbor_attr = managedattribute(
                name='neighbor_attr',
                read_only=True,
                doc=NeighborAttributes.__doc__)

            @neighbor_attr.initter
            def neighbor_attr(self):
                return SubAttributesDict(self.NeighborAttributes, parent=self)

            neighbors = managedattribute(
                name='neighbors',
                finit=typedset(_ldp_neighbor).copy,
                type=typedset(_ldp_neighbor)._from_iterable)

            class AddressFamilyAttributes(AddressFamilySubAttributes):

                allowed_keys = (AddressFamily.ipv4, AddressFamily.ipv6)

                advertise_interfaces = managedattribute(
                    name='advertise_interfaces',
                    type=typedset(managedattribute.test_isinstance(Interface))._from_iterable)

                @advertise_interfaces.defaulter
                def advertise_interfaces(self):
                    return frozenset(self.parent.advertise_interfaces)

                class NeighborAttributes(IPLsrNeighborSubAttributes):

                    def __init__(self, **kwargs):
                        super().__init__(**kwargs)

                neighbor_attr = managedattribute(
                    name='neighbor_attr',
                    read_only=True,
                    doc=NeighborAttributes.__doc__)

                @neighbor_attr.initter
                def neighbor_attr(self):
                    return SubAttributesDict(self.NeighborAttributes, parent=self)

                def __init__(self, **kwargs):
                    super().__init__(**kwargs)

            address_family_attr = managedattribute(
                name='address_family_attr',
                read_only=True,
                doc=AddressFamilyAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes, parent=self)

            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=True,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)

        @property
        def router_id(self):
            return self.vrf_attr[None].router_id

        @router_id.setter
        def router_id(self, value):
            self.vrf_attr[None].router_id = value

        @property
        def neighbor_attr(self):
            return self.vrf_attr[None].neighbor_attr

        @property
        def address_family_attr(self):
            return self.vrf_attr[None].address_family_attr

        class InterfaceAttributes(genie.conf.base.attributes.InterfaceSubAttributes):

            address_families = managedattribute(
                name='address_families',
                type=typedset(AddressFamily)._from_iterable)

            @address_families.defaulter
            def address_families(self):
                return frozenset(self.parent.address_families)

            class AddressFamilyAttributes(AddressFamilySubAttributes):

                allowed_keys = (AddressFamily.ipv4, AddressFamily.ipv6)

                def __init__(self, **kwargs):
                    super().__init__(**kwargs)

            address_family_attr = managedattribute(
                name='address_family_attr',
                read_only=True,
                doc=AddressFamilyAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes, parent=self)

            def __init__(self, **kwargs):
                super().__init__(**kwargs)

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build_config(self, links=None, apply=True, attributes=None, **kwargs):
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

