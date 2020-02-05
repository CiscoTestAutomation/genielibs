
__all__ = (
    'Te',
    'Srlg',
)

from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature, LinkFeature, InterfaceFeature
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesHelper
from pyats.datastructures import WeakList
from genie.libs.conf.address_family import AddressFamily
from genie.libs.conf.vrf import VrfSubAttributes


class Te(DeviceFeature, LinkFeature):

    @property
    def interfaces(self):
        interfaces = set()
        interfaces.update(*[link.interfaces for link in self.links])
        return frozenset(interfaces)

    # Base-level (outside mpls te config) attributes
    ipv4_unnum_interfaces = managedattribute(
        name='ipv4_unnum_interfaces',
        default=None,
        type=(None, managedattribute.test_istype(set)))
    
    # Top level attributes
    auto_tun_backup_affinity_ignore = managedattribute(
        name='auto_tun_backup_affinity_ignore',
        default=False,
        type=(None, managedattribute.test_istype(bool)))
        
    auto_tun_backup_timers_rem_unused = managedattribute(
        name='auto_tun_backup_timers_rem_unused',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    backup_auto_tun_tunid_min = managedattribute(
        name='backup_auto_tun_tunid_min',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    backup_auto_tun_tunid_max = managedattribute(
        name='backup_auto_tun_tunid_max',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    mesh_auto_tun_tunid_min = managedattribute(
        name='mesh_auto_tun_tunid_min',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    mesh_auto_tun_tunid_max = managedattribute(
        name='mesh_auto_tun_tunid_max',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    p2mp_auto_tun_tunid_min = managedattribute(
        name='p2mp_auto_tun_tunid_min',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    p2mp_auto_tun_tunid_max = managedattribute(
        name='p2mp_auto_tun_tunid_max',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    p2p_auto_tun_tunid_min = managedattribute(
        name='p2p_auto_tun_tunid_min',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    p2p_auto_tun_tunid_max = managedattribute(
        name='p2p_auto_tun_tunid_max',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    pcc_auto_tun_tunid_min = managedattribute(
        name='pcc_auto_tun_tunid_min',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    pcc_auto_tun_tunid_max = managedattribute(
        name='pcc_auto_tun_tunid_max',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    
    log_events_all = managedattribute(
        name='log_events_all',
        default=False,
        type=(None, managedattribute.test_istype(bool)))
        
    log_events_issu = managedattribute(
        name='log_events_issu',
        default=False,
        type=(None, managedattribute.test_istype(bool)))
        
    log_events_nsr = managedattribute(
        name='log_events_nsr',
        default=False,
        type=(None, managedattribute.test_istype(bool)))
        
    log_events_preemption = managedattribute(
        name='log_events_preemption',
        default=False,
        type=(None, managedattribute.test_istype(bool)))
        
    log_events_role_head = managedattribute(
        name='log_events_role_head',
        default=False,
        type=(None, managedattribute.test_istype(bool)))
        
    log_events_role_mid = managedattribute(
        name='log_events_role_mid',
        default=False,
        type=(None, managedattribute.test_istype(bool)))
        
    log_events_role_tail = managedattribute(
        name='log_events_role_tail',
        default=False,
        type=(None, managedattribute.test_istype(bool)))
        
    log_events_frr_protection = managedattribute(
        name='log_events_frr_protection',
        default=None,
        type=(None, managedattribute.test_istype(bool)))
        
    log_events_frr_protection_type = managedattribute(
        name='log_events_frr_protection',
        default=None,
        type=(None, managedattribute.test_istype(str)))
        
    log_events_frr_protection_type = managedattribute(
        name='log_events_frr_protection_primary_lsp_type',
        default=None,
        type=(None, managedattribute.test_istype(str)))
        
    
    reoptimize_secs = managedattribute(
        name='reoptimize_secs',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    reoptimize_delay_install = managedattribute(
        name='reoptimize_delay_install',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    reoptimize_delay_cleanup = managedattribute(
        name='reoptimize_delay_cleanup',
        default=None,
        type=(None, managedattribute.test_istype(int)))
    
    frr_timers_hold_backup = managedattribute(
        name='frr_timers_hold_backup',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    frr_timers_promotion = managedattribute(
        name='frr_timers_promotion',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    
    flooding_threshold_up = managedattribute(
        name='flooding_threshold_up',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    flooding_threshold_down = managedattribute(
        name='flooding_threshold_down',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    
    srlg_admin_weight = managedattribute(
        name='srlg_admin_weight',
        default=None,
        type=(None, managedattribute.test_istype(int)))
        
    
    affinity_map_bitpos_dict = managedattribute(
        name='affinity_map_bitpos_dict',
        finit=dict)
        
    affinity_map_val_dict = managedattribute(
        name='affinity_map_val_dict',
        finit=dict)
    
    soft_preempt_timeout = managedattribute(
        name='soft_preempt_timeout',
        default=None,
        type=(None, managedattribute.test_istype(int)))
    
    soft_preempt_frr_rewrite = managedattribute(
        name='soft_preempt_frr_rewrite',
        default=False,
        type=(None, managedattribute.test_istype(bool)))

    advertise_expnull = managedattribute(
        name='advertise_expnull',
        default=False,
        type=(None, managedattribute.test_istype(bool)))
    
    # Per-interface attributes
    auto_tun_backup_attr_set = managedattribute(
        name='auto_tun_backup_attr_set',
        default=None,
        type=(None, managedattribute.test_istype(str)))
        
    auto_tun_backup_exclude_srlg = managedattribute(
        name='auto_tun_backup_exclude_srlg',
        default=None,
        type=(None, managedattribute.test_istype(bool)))
    
    auto_tun_backup_exclude_srlg_type = managedattribute(
        name='auto_tun_backup_exclude_srlg_type',
        default=None,
        type=(None, managedattribute.test_istype(str)))
    
    auto_tun_backup_nhop_only = managedattribute(
        name='auto_tun_backup_nhop_only',
        default=False,
        type=(None, managedattribute.test_istype(bool)))

    

    ### END ATTRIBUTES SECTION


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


class Srlg(DeviceFeature, InterfaceFeature):

    # Top level attributes
    name_value_dict = managedattribute(
        name='name_value_dict',
        finit=dict)
    
    # Per-interface attributes
    intf_name = managedattribute(
        name='intf_name',
        default=None,
        type=(None, str))

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

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

    def _on_added_from_device(self, device):
        super()._on_added_from_device(device)
        assert getattr(device, 'srlg', None) is None
        device.srlg = self

    def _on_removed_from_device(self, device):
        assert getattr(device, 'srlg', None) is self
        super()._on_removed_from_device(device)
        device.srlg = None

    def _on_added_from_interface(self, interface):
        super()._on_added_from_interface(interface)
        assert getattr(interface, 'srlg', None) is None
        interface.srlg = self

    def _on_removed_from_interface(self, interface):
        assert getattr(interface, 'srlg', None) is self
        super()._on_removed_from_interface(interface)
        interface.srlg = None

    def build_config(self, devices=None, interfaces=None, links=None,
                     apply=True, attributes=None, **kwargs):
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

    def build_unconfig(self, devices=None, interfaces=None, links=None,
                       apply=True, attributes=None, **kwargs):
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


