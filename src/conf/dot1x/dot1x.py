
__all__ = (
    'Dot1x',
)
# import genie
from genie.decorator import managedattribute
from genie.conf.base.base import DeviceFeature
from genie.conf.base.attributes import DeviceSubAttributes,\
                                       SubAttributesDict,\
                                       AttributesHelper, \
                                       KeyedSubAttributes
# import genie.libs
from genie.conf.base.attributes import InterfaceSubAttributes


# Structure
# Dot1x
# +- DeviceAttributes
#     +- CredentialsAttributes
#     +- InterfaceAttributes


class Dot1x(DeviceFeature):

    # Device Attributes
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    system_auth_control = managedattribute(
        name='system_auth_control',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    supplicant_force_mcast = managedattribute(
        name='supplicant_force_mcast',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    # Credentials Attributes
    credential_profile = managedattribute(
        name='credential_profile',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    credential_username = managedattribute(
        name='credential_username',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    credential_pwd_type = managedattribute(
        name='credential_pwd_type',
        default=None,
        type=(None, managedattribute.test_in(['0','7'])))

    credential_secret = managedattribute(
        name='credential_secret',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    # Interfaces Attributes
    if_pae = managedattribute(
        name='if_pae',
        default=None,
        type=(None, managedattribute.test_in(['authenticator','supplicant','both'])))

    if_authen_eap_profile = managedattribute(
        name='if_authen_eap_profile',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    if_supplicant_eap_profile = managedattribute(
        name='if_supplicant_eap_profile',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    if_credentials = managedattribute(
        name='if_credentials',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    if_closed = managedattribute(
        name='if_closed',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    if_port_control = managedattribute(
        name='if_port_control',
        default=None,
        type=(None, managedattribute.test_in(['auto','force-authorized','force-unauthorized'])))

    if_host_mode = managedattribute(
        name='if_host_mode',
        default=None,
        type=(None, managedattribute.test_in(['multi-auth','multi-domain','multi-host','single-host'])))


    class DeviceAttributes(DeviceSubAttributes):
        
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

    
        class CredentialsAttributes(KeyedSubAttributes):

            def __init__(self, parent, key):
                self.credential_profile = key
                super().__init__(parent)            
           
        credentials_attr = managedattribute(
            name='credentials_attr',
            read_only=True,
            doc=CredentialsAttributes.__doc__)

        @credentials_attr.initter
        def credentials_attr(self):
            return SubAttributesDict(
                self.CredentialsAttributes, parent=self)

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
