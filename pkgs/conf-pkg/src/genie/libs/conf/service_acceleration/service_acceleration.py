__all__ = (
    'ServiceAcceleration',
)

# Python
from enum import Enum

# genie
from genie.utils.cisco_collections import typedset
from genie.decorator import managedattribute
from genie.conf.base.base import DeviceFeature

# genie.libs
from genie.conf.base.attributes import (
    DeviceSubAttributes,
    SubAttributesDict,
    AttributesHelper,
    KeyedSubAttributes
)

# multi-line config class
from .service_vrf import ServiceVrf

# service-acceleration Hierarchy
# --------------
# ServiceAcceleration
#     +- DeviceAttributes
#       +- ServiceAttributes

class ServiceAcceleration(DeviceFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ==========================================================================
    #                           CONF CLASS STRUCTURE
    # ==========================================================================

    # +- DeviceAttributes
    class DeviceAttributes(DeviceSubAttributes):
        class ServiceAttributes(KeyedSubAttributes):

            def __init__(self, parent, key):
                if key in parent.SERVICE_TYPE._member_names_:
                    self.service_type = key
                else:
                    raise ValueError(f'service_type: {key} is not supported. Supported types are: {parent.SERVICE_TYPE._member_names_}')
                super().__init__(parent)
            
            # service vrf configs
            servicevrf_keys = managedattribute(
                name='servicevrf_keys',
                finit=typedset(
                    managedattribute.test_isinstance(ServiceVrf)).copy,
                type=typedset(managedattribute.test_isinstance(
                    ServiceVrf))._from_iterable,
                doc='A `set` of ServiceVrf keys objects')

            def add_servicevrf_key(self, servicevrf_key):
                self.servicevrf_keys.add(servicevrf_key)

            def remove_servicevrf_key(self, servicevrf_key):
                servicevrf_key._device = None
                try:
                    self.servicevrf_keys.remove(servicevrf_key)
                except:
                    pass

        service_attr = managedattribute(
            name='service_attr',
            read_only=True,
            doc=ServiceAttributes.__doc__)

        @service_attr.initter
        def service_attr(self):
            return SubAttributesDict(self.ServiceAttributes, parent=self)

    device_attr = managedattribute(
        name="device_attr", read_only=True, doc=DeviceAttributes.__doc__
    )

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)
    
    # ==========================================================================
    #                           GLOBAL ENUM TYPES
    # ==========================================================================

    class SERVICE_VENDOR(Enum):
        hypershield = 'hypershield'

    class SERVICE_TYPE(Enum):
        firewall = 'firewall'

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================

    # enabled
    enabled = managedattribute(
        name="enabled", default=None, type=(None, managedattribute.test_istype(bool))
    )

    # service_vendor
    service_vendor = managedattribute(
        name='service_vendor',
        default=None,
        type=(None, SERVICE_VENDOR))

    # source_interface
    source_interface = managedattribute(
        name="source_interface", default=None, type=(None, managedattribute.test_istype(str))
    )

    # peer_ip
    peer_ip = managedattribute(
        name="peer_ip", default=None, type=(None, managedattribute.test_istype(str))
    )

    # peer_interface
    peer_interface = managedattribute(
        name="peer_interface", default=None, type=(None, managedattribute.test_istype(str))
    )

    # controller_token
    controller_token = managedattribute(
        name="controller_token", default=None, type=(None, managedattribute.test_istype(str))
    )

    # https_proxy_username
    https_proxy_username = managedattribute(
        name="https_proxy_username", default=None, type=(None, managedattribute.test_istype(str))
    )

    # https_proxy_password
    https_proxy_password = managedattribute(
        name="https_proxy_password", default=None, type=(None, managedattribute.test_istype(str))
    )

    # ==========================================================================
    # +- DeviceAttributes
    #   +- ServiceAttributes
    # ==========================================================================

    # in_service
    in_service = managedattribute(
        name="in_service", default=None, type=(None, managedattribute.test_istype(bool))
    )


    def __init__(self, service_vendor=None,*args, **kwargs):
        self.service_vendor = service_vendor
        super().__init__(*args, **kwargs)

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