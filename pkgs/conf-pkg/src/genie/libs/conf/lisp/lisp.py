__all__ = ('Lisp', 'Encapsulation', 'ServiceType')
from genie.conf.base import (Device,
                             Interface)

from genie.conf.base.attributes import (DeviceSubAttributes,
                                        SubAttributes,
                                        KeyedSubAttributes,
                                        SubAttributesDict,
                                        AttributesHelper)
from genie.conf.base.base import DeviceFeature
from genie.decorator import managedattribute
from genie.libs.conf.base import Routing
from genie.libs.conf.base.feature import consolidate_feature_args
from enum import Enum
from ipaddress import IPv4Address, IPv6Address, IPv6Network, IPv4Network
from genie.libs.conf.vrf import Vrf, VrfSubAttributes

class ServiceType(Enum):
    ethernet = 'ethernet'
    ipv4 = 'ipv4'
    ipv6 = 'ipv6'
    iwan = 'iwan'

class Encapsulation(Enum):
    vxlan = 'vxlan'
    lisp = 'lisp'

class Lisp(Routing, DeviceFeature):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    router_lisp_id = managedattribute(
        name="router_lisp_id",
        default="",
        type=(None,
              managedattribute.test_istype(str)))

    site_id = managedattribute(
        name="site_id",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    security = managedattribute(
        name="security",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    auto_discover_rlocs = managedattribute(
        name="auto_discover_rlocs",
        default=None, type=(None, managedattribute.test_istype(bool)))

    encapsulation = managedattribute(
        name="encapsulation",
        default=None,
        type=(None, managedattribute.test_istype(Encapsulation)))

    service = managedattribute(
        name="service",
        default=None,
        type=(None, managedattribute.test_istype(ServiceType)))

    dynamic_eid_name = managedattribute(
        name="dynamic_eid_name",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    eid_records = managedattribute(
        name="eid_records",
        default=None,
        type=(None,
              managedattribute.test_istype(list),))

    eid_table = managedattribute(
        name="eid_table",
        default=None,
        type=(None,
              managedattribute.test_istype(str)))

    itr_enabled = managedattribute(
        name="itr_enabled",
        default=None,
        type=(None,
              managedattribute.test_istype(bool)))

    # TODO: make itr_values a namedtuple type
    itr_values = managedattribute(
        name="itr_values",
        default=None,
        type=(None,
              managedattribute.test_istype(list)))

    etr_enabled = managedattribute(
        name="etr_enabled",
        default=None,
        type=(None,
              managedattribute.test_istype(bool)))

    # TODO: make etr_values a namedtuple type
    etr_values = managedattribute(
        name="etr_values",
        default=None,
        type=(None,
              managedattribute.test_istype(list)))

    eth_db_mapping = managedattribute(
        name="eth_db_map",
        default=None,
        type=(None,
              managedattribute.test_istype(list)))

    ipv4_db_map = managedattribute(
        name="ipv4_db_map",
        default=None,
        type=(None,
              managedattribute.test_istype(list)))

    ipv6_db_map = managedattribute(
        name="ipv6_db_map",
        default=None,
        type=(None,
              managedattribute.test_istype(list)))

    rloc_value = managedattribute(
        name = "rloc_value",
        default = None,
        type= (None,
               managedattribute.test_istype(str)))

    map_request_source = managedattribute(
        name = "map_request_source",
        default = None,
        type= (None,
               managedattribute.test_istype(str)))

    use_petr = managedattribute(
        name = "use_petr",
        default = None,
        type= (None,
               managedattribute.test_istype(str)))

    map_cache_persistence_interval = managedattribute(
        name = "map_cache_persistence_interval",
        default = 0,
        type=(None,
              managedattribute.test_istype(int)))

    site_registrations = managedattribute(
        name = "site_registrations",
        default = None,
        type=(None,
              managedattribute.test_istype(int)))

    authentication_key = managedattribute(
        name="authentication_key",
        default=None,
        type=(None,
              managedattribute.test_istype(str)))

    test_attrib = managedattribute(
        name="test_attrib",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    map_resolver_enabled = managedattribute(
        name="map_resolver_enabled",
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    map_cache_limit = managedattribute(
        name="map_cache_limit",
        default=None,
        type=(None,
              managedattribute.test_istype(int)))

    map_server_enabled = managedattribute(
        name="map_server_enabled",
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    map_resolver = managedattribute(
        name="map_resolver",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    map_server = managedattribute(
        name="map_server",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    locator_table = managedattribute(
        name="locator_table",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    control_packet = managedattribute(
        name="control_packet",
        default=None,
        type=(None, managedattribute.test_istype(int)))

    ddt = managedattribute(
        name="ddt",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    decapsulation = managedattribute(
        name="decapsulation",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    default = managedattribute(
        name="default",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    disable_ttl_propagate = managedattribute(
        name="disable_ttl_progagate",
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    loc_reach_algorithm = managedattribute(
        name="loc_reach_algorithm",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    locator = managedattribute(
        name="locator",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    locator_down = managedattribute(
        name="locator_down",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    rloc_prefix = managedattribute(
        name="rloc_prefix",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    rtr_locator_set = managedattribute(
        name="rtr_locater_set",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    map_request = managedattribute(
        name="map_request",
        default=None,
        type=(None, managedattribute.test_istype(str)))

    class DeviceAttributes(DeviceSubAttributes):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        class VrfAttributes(VrfSubAttributes):

            def __init__(self, **kwargs):
                super().__init__(**kwargs)

            class ServiceAttributes(KeyedSubAttributes):
                """Block for service attributes"""
                def __init__(self, parent, key):
                    self.service_name = key
                    super().__init__(parent=parent)

            service_attr = managedattribute(
                name="service_attr",
                read_only=False,
                doc=ServiceAttributes.__doc__)

            @service_attr.initter
            def service_attr(self):
               return SubAttributesDict(self.ServiceAttributes, parent=self)

            class LocatorScopeAttributes(KeyedSubAttributes):
                """Block for locator-scopy attributes"""
                def __init__(self, parent, key):
                    self.locator_scope_name = key
                    super().__init__(parent=parent)

            locator_scope_attr = managedattribute(
                name="locator_scope_attr",
                read_only=False,
                doc=LocatorScopeAttributes.__doc__)

            @locator_scope_attr.initter
            def locator_scope_attr(self):
                return SubAttributesDict(self.LocatorScopeAttributes, parent=self)

            class DynamicEIDAttributes(KeyedSubAttributes):
                """Block for Dynamic EID attributes"""
                def __init__(self, parent, key):
                    self.dynamic_eid_name = key
                    super().__init__(parent=parent)

            dynamic_eid_attr = managedattribute(
                name="dynamic_eid_attr",
                read_only=False)

            @dynamic_eid_attr.initter
            def dynamic_eid_attr(self):
                return SubAttributesDict(self.DynamicEIDAttributes, parent=self)

            class SiteAttributes(KeyedSubAttributes):
                """Block for site attrs"""
                def __init__(self, parent, key):
                    self.site_name = key
                    super().__init__(parent=parent)

            site_attr = managedattribute(
                name="site_attr",
                read_only=False,
                doc=SiteAttributes.__doc__)

            @site_attr.initter
            def site_attr(self):
                return SubAttributesDict(self.SiteAttributes, parent=self)

            class LocatorSetAttributes(KeyedSubAttributes):
                """Block for locator-set"""
                def __init__(self, parent, key):
                    self.locator_set_name = key
                    super().__init__(parent=parent)

            locatorset_attr = managedattribute(
                name='locatorset_attr',
                read_only=False,
                doc=LocatorSetAttributes.__doc__)

            @locatorset_attr.initter
            def locatorset_attr(self):
                return SubAttributesDict(self.LocatorSetAttributes, parent=self)

            class InstanceAttributes(KeyedSubAttributes):
                """Block for instance attrs"""
                def __init__(self, parent, key):
                    self.instance_id = key
                    super().__init__(parent=parent)

                service_attr = managedattribute(name="service_attr",
                                                read_only=False)

                @service_attr.initter
                def service_attr(self):
                   return SubAttributesDict(self.parent.ServiceAttributes, parent=self)

                dynamic_eid_attr = managedattribute(
                    name="dynamic_eid_attr",
                    read_only=False)

                @dynamic_eid_attr.initter
                def dynamic_eid_attr(self):
                    return SubAttributesDict(self.DynamicEIDAttributes, parent=self)

            instance_attr = managedattribute(
                name="instance_attr",
                read_only=False,
                doc=InstanceAttributes.__doc__)

            @instance_attr.initter
            def instance_attr(self):
                return SubAttributesDict(self.InstanceAttributes, parent=self)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=False,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=False,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def build_config(self, devices=None, apply=True, attributes=None):
        #TODO add interfaces
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True, attributes=None):
        #TODO add interfaces
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        # devices = consolidate_feature_args(self, devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs
