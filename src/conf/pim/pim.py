
__all__ = (
        'Pim',
        )
# import python
import ipaddress
from enum import Enum
from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface

# import genie
import genie.conf.base.attributes
from genie.utils.cisco_collections import typedset
from genie.conf.base import Base, Interface
from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature, InterfaceFeature, LinkFeature
from genie.conf.base.attributes import SubAttributes, \
                                       SubAttributesDict, \
                                       AttributesHelper

# import genie.libs
from .rp_address import RPAddressGroup
from genie.libs.conf.base import Routing
from genie.libs.conf.vrf import Vrf, VrfSubAttributes
from genie.conf.base.attributes import InterfaceSubAttributes
from genie.libs.conf.address_family import AddressFamily, \
                                           AddressFamilySubAttributes

from genie.abstract import Lookup

from genie.ops.base import Context
from genie.ops.base import Base as ops_Base

from genie.libs import parser


class Pim(Routing, DeviceFeature, InterfaceFeature):

    address_families = managedattribute(
        name='address_families',
        finit=typedset(AddressFamily, {AddressFamily.ipv4}).copy,
        type=typedset(AddressFamily)._from_iterable)

    sparse = managedattribute(
        name='sparse',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    rp_address = managedattribute(
        name='rp_address',
        default=None,
        type=(None, IPv4Address, IPv6Address))

    # ==================== NXOS specific ====================

    # feature pim
    # feature pim6
    enabled = managedattribute(
        name='enabled',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable or disable both feature pim and feature pim6')

    # feature pim
    enabled_pim = managedattribute(
        name='enabled_pim',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable or disable feature pim')

    # feature_pim6
    enabled_pim6 = managedattribute(
        name='enabled_pim6',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable or disable feature pim6')

    # ===========================================================

    # enable_bidir
    enabled_bidir = managedattribute(
        name='enabled_bidir',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable or disable feature bidir only for iosxe')

    # ==== PIM Auto-RP =======
    auto_rp = managedattribute(
        name='auto_rp',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Auto-RP protocol RP-distribution configuration")

    send_rp = managedattribute(
        name='send_rp',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configures router to send Auto-RP Announce messages")

    send_rp_announce_rp_group = managedattribute(
        name='send_rp_announce_rp_group',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="IP address of RP for group")

    send_rp_announce_intf = managedattribute(
        name='send_rp_announce_intf',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="auto-rp interface")

    send_rp_announce_group_list = managedattribute(
        name='send_rp_announce_group_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Group range list")

    send_rp_announce_route_map = managedattribute(
        name='send_rp_announce_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc=" Group range policy for Auto-RP Candidate RP")

    send_rp_announce_prefix_list = managedattribute(
        name='send_rp_announce_prefix_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Prefix List policy for Auto-RP Candidate RP")

    send_rp_announce_interval = managedattribute(
        name='send_rp_announce_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Auto-RP Announce message transmission interval")

    send_rp_announce_scope = managedattribute(
        name='send_rp_announce_scope',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure the scope of Auto-RP Announce messages")

    send_rp_announce_bidir = managedattribute(
        name='send_rp_announce_bidir',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Group range advertised in PIM bidirectional mode")

    auto_rp_discovery = managedattribute(
        name='auto_rp_discovery',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configures router as an Auto-RP RP-mapping agent")

    send_rp_discovery = managedattribute(
        name='send_rp_discovery',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configures router to send Auto-RP Discovery messages")

    send_rp_discovery_intf = managedattribute(
        name='send_rp_discovery_intf',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Auto-RP Discovery messages interface")

    send_rp_discovery_scope = managedattribute(
        name='send_rp_discovery_scope',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure the scope of Auto-RP Discovery messages")

    send_rp_discovery_interval = managedattribute(
        name='send_rp_discovery_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Auto-RP Discovery message transmission interval")

    autorp_listener = managedattribute(
        name='autorp_listener',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Listen to Auto-RP messages")

    # ==== PIM BSR =======
    # === bsr-candidate ===
    bsr_candidate_interface = managedattribute(
        name='bsr_candidate_interface',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure router as a Bootstrap Router candidate interface")

    bsr_candidate_hash_mask_length = managedattribute(
        name='bsr_candidate_hash_mask_length',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Hash mask length used in Bootstrap messages")

    bsr_candidate_priority = managedattribute(
        name='bsr_candidate_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="BSR priority used in Bootstrap messages")

    bsr_candidate_interval = managedattribute(
        name='bsr_candidate_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Bootstrap message transmission interval")

    bsr_candidate_accept_rp_acl = managedattribute(
        name='bsr_candidate_accept_rp_acl',
        default=None,
        type=(None, managedattribute.test_istype(str),
                    managedattribute.test_istype(int)),
        doc="bsr_candidate_accept_rp_acl")

    bsr_candidate_address = managedattribute(
        name='bsr_candidate_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="bsr_candidate_address")

    # === bsr rp-candidate ====
    bsr_rp_candidate_interface = managedattribute(
        name='bsr_rp_candidate_interface',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure router as a Rendezvous Point (RP) candidate interface")

    bsr_rp_candidate_group_list = managedattribute(
        name='bsr_rp_candidate_group_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Group range list")

    bsr_rp_candidate_route_map = managedattribute(
        name='bsr_rp_candidate_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Group range policy for Candidate RP")

    bsr_rp_candidate_prefix_list = managedattribute(
        name='bsr_rp_candidate_prefix_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Prefix List policy for Candidate RP")

    bsr_rp_candidate_priority = managedattribute(
        name='bsr_rp_candidate_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Group range policy for Candidate RP")

    bsr_rp_candidate_interval = managedattribute(
        name='bsr_rp_candidate_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Bootstrap message transmission interval")

    bsr_rp_candidate_bidir = managedattribute(
        name='bsr_rp_candidate_bidir',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Group range advertised in PIM bidirectional mode")

    bsr_rp_candidate_address = managedattribute(
        name='bsr_rp_candidate_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="bsr_rp_candidate_address")

    # # ==== PIM Other =======
    accept_register = managedattribute(
        name='accept_register',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="A route-map name")

    # only used for nxos ipv4
    accept_register_prefix_list = managedattribute(
        name='accept_register_prefix_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Prefix List policy for Registers")

    log_neighbor_changes = managedattribute(
        name='log_neighbor_changes',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Log up/down PIM neighbor transitions")

    register_source = managedattribute(
        name='accept_register_route_map',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure source address for Register messages")

    sg_expiry_timer = managedattribute(
        name='sg_expiry_timer',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Adjust expiry time for PIM ASM (S,G) routes")

    # NXOS only
    sg_expiry_timer_infinity = managedattribute(
        name='sg_expiry_timer_infinity',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="Never expire (S,G) route due to data inactivity")

    sg_expiry_timer_sg_list = managedattribute(
        name='sg_expiry_timer_sg_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Specifies route-map for (S,G)s to apply the expiry timer")

    sg_expiry_timer_prefix_list = managedattribute(
        name='sg_expiry_timer_prefix_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Specifies prefix-list for (S,G)s to apply the expiry timer")

    class SPT_SWITCH_INFINITY(Enum):
        active = 0
        passive = 'infinity'

    spt_switch_infinity = managedattribute(
        name='spt_switch_infinity',
        default=False,
        type=(None, SPT_SWITCH_INFINITY),
        doc="Source-tree switching threshold")

    spt_switch_policy = managedattribute(
        name='spt_switch_policy',
        default=None,
        type=(None, managedattribute.test_istype(str),
                    managedattribute.test_istype(int)),
        doc="Specify group ranges through policy")

    # ==== PIM AddressFamily Interface =======
    class MODE(Enum):
        mode1 = 'dense-mode'
        mode2 = 'sparse-mode'
        mode3 = 'sparse-dense-mode'

    mode = managedattribute(
        name='mode',
        default=None,
        type=(None, MODE),
        doc="pim mode - only 'sparse-mode' valid for NXOS")

    boundary = managedattribute(
        name='boundary',
        default=None,
        type=(None, managedattribute.test_istype(str),
                    managedattribute.test_istype(int)),
        doc="ip multicast boundary/jp_policy")

    boundary_filter_autorp = managedattribute(
        name='boundary_filter_autorp',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="boundary group")

    boundary_in = managedattribute(
        name='boundary_in',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="boundary direction in/jp_policy_in")

    boundary_out = managedattribute(
        name='boundary_out',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="boundary direction out/jp_policy_out")

    bsr_border = managedattribute(
        name='bsr_border',
        default=False,
        type=(None, managedattribute.test_istype(bool)),
        doc="bsr border - prevents both BSR and Auto-RP")

    hello_interval = managedattribute(
        name='hello_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="hello interval")

    hello_interval_msec = managedattribute(
        name='hello_interval_msec',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="hello interval msec")

    dr_priority = managedattribute(
        name='dr_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="pim dr-priority")

    neighbor_filter = managedattribute(
        name='neighbor_filter',
        default=None,
        type=(None, managedattribute.test_istype(str),
                    managedattribute.test_istype(int)),
        doc="pim neighbor filter")

    #  NXOS only
    neighbor_filter_prefix_list = managedattribute(
        name='neighbor_filter_prefix_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="pim neighbor filter prefix list")

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

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        address_families = managedattribute(
            name='address_families',
            type=typedset(AddressFamily)._from_iterable)

        @property
        def vrfs(self):
            return \
                self.force_vrfs | \
                {intf.vrf for intf in self.interfaces}

        @address_families.defaulter
        def address_families(self):
            return frozenset(self.parent.address_families)

        class VrfAttributes(VrfSubAttributes):

            address_families = managedattribute(
                name='address_families',
                type=typedset(AddressFamily)._from_iterable)

            @address_families.defaulter
            def address_families(self):
                return frozenset(self.parent.address_families)

            class AddressFamilyAttributes(AddressFamilySubAttributes):
                
                rp_addresses = managedattribute(
                    name='rp_addresses',
                    finit=typedset(managedattribute.test_isinstance(RPAddressGroup)).copy,
                    type=typedset(managedattribute.test_isinstance(RPAddressGroup))._from_iterable,
                    doc='A `set` of RPAddressGroup associated objects')

                def add_static_rp(self, rp_addresses):
                    self.rp_addresses.add(rp_addresses)

                def remove_static_rp(self, rp_addresses):
                    rp_addresses._device = None
                    try:
                        self.rp_addresses.remove(rp_addresses)
                    except:
                        pass

                class InterfaceAttributes(InterfaceSubAttributes):
                    pass

                interface_attr = managedattribute(
                    name='interface_attr',
                    read_only=True,
                    doc=InterfaceAttributes.__doc__)

                @interface_attr.initter
                def interface_attr(self):
                    return SubAttributesDict(self.InterfaceAttributes, parent=self)

            address_family_attr = managedattribute(
                name='address_family_attr',
                read_only=True,
                doc=AddressFamilyAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes, parent=self)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=True,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)

        def __init__(self, parent, key):
            super().__init__(parent, key)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_config(self, devices=None, apply=True, attributes=None,
                     **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True, attributes=None,
                       **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs


    @classmethod
    def learn_config(self, device, **kwargs):
        '''
            A method that learn the device configurational state and create
            a conf object with the same configuration.

            Args:
                self (`obj`): Conf object.
                device (`obj`): The device that will be used to parse the
                    command.
        '''
        if kwargs.get('attributes', None):
            kwargs['attributes'].extend(['v4_vrfs_list', 'v6_vrfs_list'])

        # Abstracting the show running bgp as per device os
        ret = Lookup.from_device(device)
        cmd = ret.parser.show_pim.ShowRunningConfigPim

        maker = ops_Base(device=device, **kwargs)

        maker.add_leaf(cmd=cmd,
                       src='[feature_pim]',
                       dest='pim[enabled_pim]',
                       address_family='ipv4',
                       pip_str='feature')

        maker.add_leaf(cmd=cmd,
                       src='[feature_pim6]',
                       dest='pim[enabled_pim6]',
                       address_family='ipv6',
                       pip_str='feature')

        # get vrfs for usage on attribtues of specific vrf
        maker.add_leaf(cmd=cmd,
                       src='[vrf]',
                       dest='v4_vrfs_list',
                       pip_str='vrf',
                       address_family='ipv4',
                       action=lambda x: list(x.keys()))

        maker.add_leaf(cmd=cmd,
                       src='[vrf]',
                       dest='v6_vrfs_list',
                       pip_str='vrf',
                       address_family='ipv6',
                       action=lambda x: list(x.keys()))

        # A workaround to pass the context as in maker it expects Context.cli
        # not just a string 'cli.
        maker.context_manager[cmd] = Context.cli
        maker.make()

        maker.v4_vrfs_list = getattr(maker, 'v4_vrfs_list', [])
        maker.v4_vrfs_list.append('default')
        maker.v4_vrfs_list = set(maker.v4_vrfs_list)

        maker.v6_vrfs_list = getattr(maker, 'v6_vrfs_list', [])
        maker.v6_vrfs_list.append('default')
        maker.v6_vrfs_list = set(maker.v6_vrfs_list)

        v4_map = map(lambda x: (x, 'ipv4'), maker.v4_vrfs_list)
        v6_map = map(lambda x: (x, 'ipv6'), maker.v6_vrfs_list)

        for vrf, af in list(v4_map) + list(v6_map):

            # only support on ipv4
            # auto-rp 
            if af == 'ipv4':
                atuo_an_src = '[vrf][{vrf}][address_family][ipv4][rp][autorp][send_rp_announce]'.format(vrf=vrf)
                atuo_an_dest = 'pim[vrf_attr][{vrf}][address_family_attr][ipv4]'.format(vrf=vrf)

                for src_key, dest_key in {'interface':'send_rp_announce_intf',
                                          'group':'send_rp_announce_rp_group',
                                          'group_list':'send_rp_announce_group_list',
                                          'route_map':'send_rp_announce_route_map',
                                          'prefix_list':'send_rp_announce_prefix_list',
                                          'interval':'send_rp_announce_interval',
                                          'scope':'send_rp_announce_scope',
                                          'bidir':'send_rp_announce_bidir',
                                          }.items():

                    maker.add_leaf(cmd=cmd,
                                   src=atuo_an_src + '[%s]' % src_key,
                                   dest=atuo_an_dest + '[%s]' % dest_key,
                                   pip_str='send-rp-announce',
                                   vrf=vrf,
                                   address_family='ipv4')


        maker.make()

        if kwargs.get('attributes', None):
            kwargs['attributes'].remove('v4_vrfs_list')
            kwargs['attributes'].remove('v6_vrfs_list')

        # Take a copy of the object dictionary
        if not hasattr(maker, 'pim'):
            maker.pim = {}
        new_pim = maker.pim

        # List of mapped conf objects
        conf_obj_list = []

        # Main structure attributes in the conf object
        structure_keys = ['vrf_attr',
                          'address_family_attr']

        # Instiantiate a PIM conf object
        conf_obj = self()

        # Pass the class method not the instnace.
        maker.dict_to_obj(conf=conf_obj,\
                          struct=structure_keys,\
                          struct_to_map=new_pim)

        conf_obj_list.append(conf_obj)

        # List of mapped conf objects
        return conf_obj_list


