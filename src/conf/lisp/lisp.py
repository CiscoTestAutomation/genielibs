
__all__ = (
    'Lisp',
)

# Python
from enum import Enum

# Genie
from genie.utils.cisco_collections import typedset
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, InterfaceFeature, LinkFeature

from genie.libs.conf.base import Routing
from genie.libs.conf.vrf import Vrf, VrfSubAttributes
from genie.conf.base.attributes import DeviceSubAttributes, SubAttributesDict,\
                                       AttributesHelper, KeyedSubAttributes,\
                                       InterfaceSubAttributes


# LISP Hierarchy
# --------------
# Lisp
#  +- DeviceAttributes
#      +- InterfaceAttributes
#      |   +- MobilityDynamicEidAttributes
#      +- RouterInstanceAttributes
#          +- LocatorSetAttributes
#          |   +- InterfaceAttributes
#          |       +- InterfacdTypeAttributes
#          +- ServiceAttributes
#          |   +- ItrMrAttributes
#          |   +- EtrMsAttributes
#          |   +- ProxyItrAttributes
#          +- InstanceAttributes
#          |   +- DynamicEidAttributes
#          |       +- DbMappingAttributes
#          |   +- ServiceAttributes
#          |       +- DbMappingAttributes
#          |       +- UsePetrAttributes
#          |       +- MapCacheAttributes
#          +- SiteAttributes
#          |   +- InstanceIdAttributes
#          |       +- EidRecordAttributes
#          +- ExtranetAttributes
#              +- InstanceIdAttributes
#                  +- EidRecordProviderAttributes
#                  +- EidRecordSubscriberAttributes


# ==========================================================================
#                           GLOBAL ENUM TYPES
# ==========================================================================

class ENCAP(Enum):
    lisp = 'lisp'
    vxlan = 'vxlan'

class ETR_AUTH_KEY_TYPE(Enum):
    none = None
    sha1 = 'hmac-sha-1-96'
    sha2 = 'hmac-sha-256-128'


class Lisp(Routing, DeviceFeature):

    # ==========================================================================
    #                           CONF CLASS STRUCTURE
    # ==========================================================================

    # +- DeviceAttributes
    class DeviceAttributes(DeviceSubAttributes):

        # +- DeviceAttributes
        #   +- InterfaceAttributes
        class InterfaceAttributes(InterfaceSubAttributes):

            # +- DeviceAttributes
            #   +- InterfaceAttributes
            #       +- MobilityDynamicEidAttributes
            class MobilityDynamicEidAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.if_mobility_dynamic_eid_name = key
                    super().__init__(parent)

            mobility_dynamic_eid_attr = managedattribute(
                name='mobility_dynamic_eid_attr',
            	read_only=True,
            	doc=MobilityDynamicEidAttributes.__doc__)

            @mobility_dynamic_eid_attr.initter
            def mobility_dynamic_eid_attr(self):
               return SubAttributesDict(self.MobilityDynamicEidAttributes, parent=self)

        intf_attr = managedattribute(
            name='intf_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @intf_attr.initter
        def intf_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

        # +- DeviceAttributes
        #   +- RouterInstanceAttributes
        class RouterInstanceAttributes(KeyedSubAttributes):

            def __init__(self, parent, key):
                self.lisp_router_instance_id = key
                super().__init__(parent)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #	  +- LocatorSetAttributes
            class LocatorSetAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.locator_set_name = key
                    super().__init__(parent)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- LocatorSetAttributes
                #       +- InterfaceAttributes
                class InterfaceAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.ls_interface = key
                        super().__init__(parent)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- LocatorSetAttributes
                    #       +- InterfaceAttributes
                    #         +- InterfaceTypeAttributes
                    class InterfaceTypeAttributes(KeyedSubAttributes):

                        def __init__(self, parent, key):
                            assert key in ['ipv4', 'ipv6', 'ethernet'],\
                                "'{key}' is not supported for locator_set_intf_type_attr, only 'ipv4' and 'ipv6' are supported".format(key=key)
                            self.ls_interface_type = key
                            super().__init__(parent)

                    locator_set_intf_type_attr = managedattribute(
                        name='locator_set_intf_type_attr',
                        read_only=True,
                        doc=InterfaceTypeAttributes.__doc__)

                    @locator_set_intf_type_attr.initter
                    def locator_set_intf_type_attr(self):
                        return SubAttributesDict(self.InterfaceTypeAttributes, parent=self)

                locator_set_intf_attr = managedattribute(
                    name='InterfaceAttributes',
                    read_only=True,
                    doc=InterfaceAttributes.__doc__)

                @locator_set_intf_attr.initter
                def locator_set_intf_attr(self):
                    return SubAttributesDict(self.InterfaceAttributes, parent=self)

            locator_set_attr = managedattribute(
                name='locator_set_attr',
                read_only=True,
                doc=LocatorSetAttributes.__doc__)

            @locator_set_attr.initter
            def locator_set_attr(self):
                return SubAttributesDict(self.LocatorSetAttributes, parent=self)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- ServiceAttributes
            class ServiceAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    assert key in ['ipv4', 'ipv6', 'ethernet'],\
                        "'{key}' is not supported for service_attr, only 'ipv4', 'ipv6' and 'ethernet' are supported".format(key=key)
                    self.service = key
                    super().__init__(parent)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- ServiceAttributes
                #       +- ItrMrAttributes
                class ItrMrAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.itr_map_resolver = key
                        super().__init__(parent)

                itr_mr_attr = managedattribute(
                    name='itr_mr_attr',
                    read_only=True,
                    doc=ItrMrAttributes.__doc__)

                @itr_mr_attr.initter
                def itr_mr_attr(self):
                    return SubAttributesDict(self.ItrMrAttributes, parent=self)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- ServiceAttributes
                #       +- EtrMsAttributes
                class EtrMsAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.etr_map_server = key
                        super().__init__(parent)

                etr_ms_attr = managedattribute(
                    name='etr_ms_attr',
                    read_only=True,
                    doc=EtrMsAttributes.__doc__)

                @etr_ms_attr.initter
                def etr_ms_attr(self):
                    return SubAttributesDict(self.EtrMsAttributes, parent=self)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- ServiceAttributes
                #       +- ProxyItrAttributes
                class ProxyItrAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.proxy_itr = key
                        super().__init__(parent)

                proxy_attr = managedattribute(
                    name='proxy_attr',
                    read_only=True,
                    doc=ProxyItrAttributes.__doc__)

                @proxy_attr.initter
                def proxy_attr(self):
                    return SubAttributesDict(self.ProxyItrAttributes, parent=self)

            service_attr = managedattribute(
                name='service_attr',
                read_only=True,
                doc=ServiceAttributes.__doc__)

            @service_attr.initter
            def service_attr(self):
                return SubAttributesDict(self.ServiceAttributes, parent=self)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- InstanceAttributes
            class InstanceAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.instance_id = key
                    super().__init__(parent)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- InstanceAttributes
                #       +- DynamicEidAttributes
                class DynamicEidAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.inst_dyn_eid = key
                        super().__init__(parent)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- InstanceAttributes
                    #       +- DynamicEidAttributes
                    #         +- DbMappingAttributes
                    class DbMappingAttributes(KeyedSubAttributes):

                        def __init__(self, parent, key):
                            self.etr_dyn_eid_id = key
                            super().__init__(parent)

                    db_mapping_attr = managedattribute(
                        name='db_mapping_attr',
                        read_only=True,
                        doc=DbMappingAttributes.__doc__)

                    @db_mapping_attr.initter
                    def db_mapping_attr(self):
                        return SubAttributesDict(self.DbMappingAttributes, parent=self)

                dynamic_eid_attr = managedattribute(
                    name='dynamic_eid_attr',
                    read_only=True,
                    doc=DynamicEidAttributes.__doc__)

                @dynamic_eid_attr.initter
                def dynamic_eid_attr(self):
                    return SubAttributesDict(self.DynamicEidAttributes, parent=self)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- InstanceAttributes
                #       +- ServiceAttributes
                class ServiceAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.inst_service = key
                        super().__init__(parent)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- InstanceAttributes
                    #       +- ServiceAttributes
                    #         +- DbMappingAttributes
                    class DbMappingAttributes(KeyedSubAttributes):

                        def __init__(self, parent, key):
                            self.etr_eid_id = key
                            super().__init__(parent)

                    service_db_mapping_attr = managedattribute(
                        name='service_db_mapping_attr',
                        read_only=True,
                        doc=DbMappingAttributes.__doc__)

                    @service_db_mapping_attr.initter
                    def service_db_mapping_attr(self):
                        return SubAttributesDict(self.DbMappingAttributes, parent=self)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- InstanceAttributes
                    #       +- ServiceAttributes
                    #         +- UsePetrAttributes
                    class UsePetrAttributes(KeyedSubAttributes):

                        def __init__(self, parent, key):
                            self.etr_use_petr = key
                            super().__init__(parent)

                    use_petr_attr = managedattribute(
                        name='use_petr_attr',
                        read_only=True,
                        doc=UsePetrAttributes.__doc__)

                    @use_petr_attr.initter
                    def use_petr_attr(self):
                        return SubAttributesDict(self.UsePetrAttributes, parent=self)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- InstanceAttributes
                    #       +- ServiceAttributes
                    #         +- MapCacheAttributes
                    class MapCacheAttributes(KeyedSubAttributes):

                        def __init__(self, parent, key):
                            self.itr_mc_id = key
                            super().__init__(parent)

                    map_cache_attr = managedattribute(
                        name='map_cache_attr',
                        read_only=True,
                        doc=MapCacheAttributes.__doc__)

                    @map_cache_attr.initter
                    def map_cache_attr(self):
                        return SubAttributesDict(self.MapCacheAttributes, parent=self)

                inst_service_attr = managedattribute(
                    name='inst_service_attr',
                    read_only=True,
                    doc=ServiceAttributes.__doc__)

                @inst_service_attr.initter
                def inst_service_attr(self):
                    return SubAttributesDict(self.ServiceAttributes, parent=self)

            instance_id_attr = managedattribute(
                name='instance_id_attr',
                read_only=True,
                doc=InstanceAttributes.__doc__)

            @instance_id_attr.initter
            def instance_id_attr(self):
                return SubAttributesDict(self.InstanceAttributes, parent=self)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- SiteAttributes
            class SiteAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.ms_site_id = key
                    super().__init__(parent)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- SiteAttributes
                #       +- InstanceIdAttributes
                class InstanceIdAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.site_inst_id = key
                        super().__init__(parent)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- SiteAttributes
                    #       +- InstanceIdAttributes
                    #         +- EidRecordAttributes
                    class EidRecordAttributes(KeyedSubAttributes):

                        def __init__(self, parent, key):
                            self.ms_eid_id = key
                            super().__init__(parent)

                    eid_record_attr = managedattribute(
                        name='eid_record_attr',
                        read_only=True,
                        doc=EidRecordAttributes.__doc__)

                    @eid_record_attr.initter
                    def eid_record_attr(self):
                        return SubAttributesDict(self.EidRecordAttributes, parent=self)

                site_inst_id_attr = managedattribute(
                    name='site_inst_id_attr',
                    read_only=True,
                    doc=InstanceIdAttributes.__doc__)

                @site_inst_id_attr.initter
                def site_inst_id_attr(self):
                    return SubAttributesDict(self.InstanceIdAttributes, parent=self)

            site_attr = managedattribute(
                name='site_attr',
                read_only=True,
                doc=SiteAttributes.__doc__)

            @site_attr.initter
            def site_attr(self):
                return SubAttributesDict(self.SiteAttributes, parent=self)

            # +- DeviceAttributes
            #   +- RouterInstanceAttributes
            #     +- ExtranetAttributes
            class ExtranetAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.ms_extranet = key
                    super().__init__(parent)

                # +- DeviceAttributes
                #   +- RouterInstanceAttributes
                #     +- ExtranetAttributes
                #       +- InstanceIdAttributes
                class InstanceIdAttributes(KeyedSubAttributes):

                    def __init__(self, parent, key):
                        self.extranet_inst_id = key
                        super().__init__(parent)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- ExtranetAttributes
                    #       +- InstanceIdAttributes
                    #         +- EidRecordProviderAttributes
                    class EidRecordProviderAttributes(KeyedSubAttributes):

                        def __init__(self, parent, key):
                            self.ms_extranet_provider_eid = key
                            super().__init__(parent)

                    eid_record_provider_attr = managedattribute(
                        name='eid_record_provider_attr',
                        read_only=True,
                        doc=EidRecordProviderAttributes.__doc__)

                    @eid_record_provider_attr.initter
                    def eid_record_provider_attr(self):
                        return SubAttributesDict(self.EidRecordProviderAttributes, parent=self)

                    # +- DeviceAttributes
                    #   +- RouterInstanceAttributes
                    #     +- ExtranetAttributes
                    #       +- InstanceIdAttributes
                    #         +- EidRecordSubscriberAttributes
                    class EidRecordSubscriberAttributes(KeyedSubAttributes):

                        def __init__(self, parent, key):
                            self.ms_extranet_subscriber_eid = key
                            super().__init__(parent)

                    eid_record_subscriber_attr = managedattribute(
                        name='eid_record_subscriber_attr',
                        read_only=True,
                        doc=EidRecordSubscriberAttributes.__doc__)

                    @eid_record_subscriber_attr.initter
                    def eid_record_subscriber_attr(self):
                        return SubAttributesDict(self.EidRecordSubscriberAttributes, parent=self)

                extranet_inst_id_attr = managedattribute(
                    name='extranet_inst_id_attr',
                    read_only=True,
                    doc=InstanceIdAttributes.__doc__)

                @extranet_inst_id_attr.initter
                def extranet_inst_id_attr(self):
                    return SubAttributesDict(self.InstanceIdAttributes, parent=self)

            extranet_attr = managedattribute(
                name='extranet_attr',
                read_only=True,
                doc=ExtranetAttributes.__doc__)

            @extranet_attr.initter
            def extranet_attr(self):
                return SubAttributesDict(self.ExtranetAttributes, parent=self)

        router_instance_attr = managedattribute(
            name='router_instance_attr',
            read_only=True,
            doc=RouterInstanceAttributes.__doc__)

        @router_instance_attr.initter
        def router_instance_attr(self):
            return SubAttributesDict(self.RouterInstanceAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)


    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # enabled
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- InterfaceAttributes
    # ==========================================================================

    # if_mobility_liveness_test_disabled
    if_mobility_liveness_test_disabled = managedattribute(
        name='if_mobility_liveness_test_disabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- LocatorSetAttributes
    #       +- InterfaceAttributes
    #         +- InterfaceTypeAttributes
    # ==========================================================================

    # ls_priority
    ls_priority = managedattribute(
        name='ls_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ls_weight
    ls_weight = managedattribute(
        name='ls_weight',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- ServiceAttributes
    # ==========================================================================

    # itr_enabled
    itr_enabled = managedattribute(
        name='itr_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # etr_enabled
    etr_enabled = managedattribute(
        name='etr_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ms_enabled
    ms_enabled = managedattribute(
        name='ms_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # mr_enabled
    mr_enabled = managedattribute(
        name='mr_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # proxy_etr_enabled
    proxy_etr_enabled = managedattribute(
        name='proxy_etr_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # locator_vrf
    locator_vrf = managedattribute(
        name='locator_vrf',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # encapsulation
    encapsulation = managedattribute(
        name='encapsulation',
        default=ENCAP.lisp,
        type=(None, ENCAP))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- ServiceAttributes
    #       +- EtrMsAttributes
    # ==========================================================================

    # etr_auth_key
    etr_auth_key = managedattribute(
        name='etr_auth_key',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # etr_auth_key_type
    etr_auth_key_type = managedattribute(
        name='etr_auth_key_type',
        default=ETR_AUTH_KEY_TYPE.none,
        type=(None, ETR_AUTH_KEY_TYPE))

    # etr_proxy_reply
    etr_proxy_reply = managedattribute(
        name='etr_proxy_reply',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- InstanceAttributes
    #       +- DynamicEidAttributes
    #         +- DbMappingAttributes
    # ==========================================================================

    # etr_dyn_eid_rlocs
    etr_dyn_eid_rlocs = managedattribute(
        name='etr_dyn_eid_rlocs',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # etr_dyn_eid_loopback_address
    etr_dyn_eid_loopback_address = managedattribute(
        name='etr_dyn_eid_loopback_address',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # etr_dyn_eid_priority
    etr_dyn_eid_priority = managedattribute(
        name='etr_dyn_eid_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # etr_dyn_eid_weight
    etr_dyn_eid_weight = managedattribute(
        name='etr_dyn_eid_weight',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- InstanceAttributes
    #       +- ServiceAttributes
    # ==========================================================================

    # etr_eid_vrf
    etr_eid_vrf = managedattribute(
        name='etr_eid_vrf',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- InstanceAttributes
    #       +- ServiceAttributes
    #         +- DbMappingAttributes
    # ==========================================================================

    # etr_eid_rlocs
    etr_eid_rlocs = managedattribute(
        name='etr_eid_rlocs',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # etr_eid_loopback_address
    etr_eid_loopback_address = managedattribute(
        name='etr_eid_loopback_address',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # etr_eid_priority
    etr_eid_priority = managedattribute(
        name='etr_eid_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # etr_eid_weight
    etr_eid_weight = managedattribute(
        name='etr_eid_weight',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- InstanceAttributes
    #       +- ServiceAttributes
    #         +- UsePetrAttributes
    # ==========================================================================

    # etr_use_petr_priority
    etr_use_petr_priority = managedattribute(
        name='etr_use_petr_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # etr_use_petr_weight
    etr_use_petr_weight = managedattribute(
        name='etr_use_petr_weight',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- InstanceAttributes
    #       +- ServiceAttributes
    #         +- MapCacheAttributes
    # ==========================================================================

    # itr_mc_map_request
    itr_mc_map_request = managedattribute(
        name='itr_mc_map_request',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- SiteAttributes
    # ==========================================================================

    # ms_site_auth_key
    ms_site_auth_key = managedattribute(
        name='ms_site_auth_key',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # ==========================================================================
    # +- DeviceAttributes
    #   +- RouterInstanceAttributes
    #     +- SiteAttributes
    #       +- InstanceIdAttributes
    #         +- EidRecordAttributes
    # ==========================================================================

    # ms_eid_accept_more_specifics
    ms_eid_accept_more_specifics = managedattribute(
        name='ms_eid_accept_more_specifics',
        default=None,
        type=(None, managedattribute.test_istype(bool)))


    # ==========================================================================
    #                       BUILD_CONFIG & BUILD_UNCONFIG
    # ==========================================================================

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
