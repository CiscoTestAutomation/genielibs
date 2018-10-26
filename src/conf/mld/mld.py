__all__ = (
        'Mld',
        )

# Genie
from genie.utils.cisco_collections import typedset
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, InterfaceFeature

# genie.libs
from .ssm import Ssm
from .mld_group import MldGroup
from genie.libs.conf.base import Routing
from genie.libs.conf.vrf import VrfSubAttributes
from genie.conf.base.attributes import DeviceSubAttributes, \
                                       SubAttributesDict,\
                                       InterfaceSubAttributes, \
                                       AttributesHelper

# Structure Hierarchy:
# Mld
# +-- DeviceAtributes
#       +-- VrfAttributes
#             +-- InterfaceAttributes


class Mld(Routing, DeviceFeature, InterfaceFeature):
    
    # global_max_groups
    global_max_groups = managedattribute(
        name='global_max_groups',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure global_max_groups under vrf attribute.")

    # enable
    enable = managedattribute(
        name='enable',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configure 'ipv6 mld router' under interface.")

    # group_policy
    group_policy = managedattribute(
        name='group_policy',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure group_policy under interface.")

    # immediate_leave
    immediate_leave = managedattribute(
        name='immediate_leave',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configure immediate_leave under interface.")

    # max_groups
    max_groups = managedattribute(
        name='max_groups',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure max_groups under interface.")

    # query_interval
    query_interval = managedattribute(
        name='query_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure query_interval under interface.")

    # query_max_response_time
    query_max_response_time = managedattribute(
        name='query_max_response_time',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure query_max_response_time under interface.")

    # robustness_variable
    robustness_variable = managedattribute(
        name='robustness_variable',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure robustness_variable.")

    # version
    version = managedattribute(
        name='version',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure version under interface.")


    class DeviceAttributes(DeviceSubAttributes):

        class VrfAttributes(VrfSubAttributes):

            def __init__(self, parent, key):
                self.vrf_id = key
                super().__init__(parent, key)

            ssm = managedattribute(
                name='ssm',
                finit=typedset(managedattribute.test_isinstance(Ssm)).copy,
                type=typedset(managedattribute.test_isinstance(Ssm))._from_iterable,
                doc='A `set` of ssm associated objects')

            def add_ssm(self, ssm):
                self.ssm.add(ssm)

            def remove_ssm(self, ssm):
                ssm._device = None
                try:
                    self.ssm.remove(ssm)
                except:
                    pass

            
            class InterfaceAttributes(InterfaceSubAttributes):

                def __init__(self, parent, key):
                    self.intf = key
                    super().__init__(parent, key)
                
                groups = managedattribute(
                    name='groups',
                    finit=typedset(managedattribute.test_isinstance(MldGroup)).copy,
                    type=typedset(managedattribute.test_isinstance(MldGroup))._from_iterable,
                    doc='A `set` of MldGroup associated objects')

                def add_groups(self, groups):
                    self.groups.add(groups)

                def remove_groups(self, groups):
                    groups._device = None
                    try:
                        self.groups.remove(groups)
                    except:
                        pass

            interface_attr = managedattribute(
                name='interface_attr',
                read_only=True,
                doc=InterfaceAttributes.__doc__)

            @interface_attr.initter
            def interface_attr(self):
                return SubAttributesDict(
                    self.InterfaceAttributes, parent=self)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=True,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ===========================================================

    def build_config(self, devices=None, apply=True, attributes=None,
                     unconfig=False):
        cfgs = {}
        attributes = AttributesHelper(self, attributes)
        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr', sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)
        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True, attributes=None):
        cfgs = {}
        attributes = AttributesHelper(self, attributes)
        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr', sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs
