
__all__ = (
    'Acl',
)
# import genie
from genie.decorator import managedattribute
from genie.conf.base import ConfigurableBase
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, InterfaceFeature
from genie.conf.base.attributes import DeviceSubAttributes,\
                                       SubAttributesDict,\
                                       AttributesHelper, \
                                       KeyedSubAttributes
# import genie.libs
from genie.conf.base.attributes import InterfaceSubAttributes


# Structure
# Acl
# +- DeviceAttributes
#     +- AclAttributes
#         +- AceAttributes
#         +- InterfaceAttributes


class Acl(DeviceFeature):

    # device attributes
    acl_type = managedattribute(
        name='acl_type',
        default=None,
        type=(None, managedattribute.test_in(['ipv4-acl-type','ipv6-acl-type','eth-acl-type'])))

    acl_name = managedattribute(
        name='acl_name',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    seq = managedattribute(
        name='seq',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    actions_forwarding = managedattribute(
        name='actions_forwarding',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    protocol = managedattribute(
        name='protocol',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    src = managedattribute(
        name='src',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    src_operator = managedattribute(
        name='src_operator',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    src_port = managedattribute(
        name='src_port',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    dst = managedattribute(
        name='dst',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    dst_operator = managedattribute(
        name='dst_operator',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    dst_port = managedattribute(
        name='dst_port',
        default=None,
        type=(None, managedattribute.test_istype(str),
                    managedattribute.test_istype(str)))

    option = managedattribute(
        name='option',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    precedence = managedattribute(
        name='precedence',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    dscp = managedattribute(
        name='dscp',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    established = managedattribute(
        name='established',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    actions_logging = managedattribute(
        name='actions_logging',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    ttl = managedattribute(
        name='ttl',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    ttl_operator = managedattribute(
        name='ttl_operator',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    ether_type = managedattribute(
        name='ether_type',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    interface_id = managedattribute(
        name='interface_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    if_in = managedattribute(
        name='if_in',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    if_out = managedattribute(
        name='if_out',
        default=None,
        type=(None, managedattribute.test_istype(bool)))


    class DeviceAttributes(DeviceSubAttributes):


        class AclAttributes(KeyedSubAttributes):

            def __init__(self, parent, key):
                self.acl_name = key
                super().__init__(parent)
        
            class InterfaceAttributes(InterfaceSubAttributes):

                def __init__(self, parent, key):
                    self.interface_id = key
                    super().__init__(parent, key)
                
               
            interface_attr = managedattribute(
                name='interface_attr',
                read_only=True,
                doc=InterfaceAttributes.__doc__)

            @interface_attr.initter
            def interface_attr(self):
                return SubAttributesDict(
                    self.InterfaceAttributes, parent=self)

        
            class AceAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.seq = key
                    super().__init__(parent)
                
               
            ace_attr = managedattribute(
                name='ace_attr',
                read_only=True,
                doc=AceAttributes.__doc__)

            @ace_attr.initter
            def ace_attr(self):
                return SubAttributesDict(
                    self.AceAttributes, parent=self)

        acl_attr = managedattribute(
            name='acl_attr',
            read_only=True,
            doc=AclAttributes.__doc__)

        @acl_attr.initter
        def acl_attr(self):
            return SubAttributesDict(
                self.AclAttributes, parent=self)

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
