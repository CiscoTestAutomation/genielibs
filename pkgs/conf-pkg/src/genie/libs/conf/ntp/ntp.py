__all__ = (
        'Ntp',
        )
# ptyhon
from enum import Enum

# genie
from genie.utils.cisco_collections import typedset
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, InterfaceFeature

# genie.libs
from genie.libs.conf.vrf import VrfSubAttributes
from genie.conf.base.attributes import DeviceSubAttributes, \
                                       SubAttributesDict,\
                                       InterfaceSubAttributes, \
                                       AttributesHelper, \
                                       KeyedSubAttributes

# Structure Hierarchy:
# Ntp
# +-- DeviceAttribute
#     +-- VrfAttributes
#     |   +-- ServerAttributes
#     |   +-- PeerAttributes
#     +-- AuthKeyAttribute
#     +-- InterfaceAttribute


class Ntp(DeviceFeature):
    
    # enabled
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable NTP feature.")

    # master_stratum
    master_stratum = managedattribute(
        name='master_stratum',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure NTP master clock stratum number.")

    # auth_enabled
    auth_enabled = managedattribute(
        name='auth_enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable/Disable authentication.")

    # source_interface
    source_interface = managedattribute(
        name='source_interface',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure Source interface sending NTP packets.")

    # vrf
    vrf = managedattribute(
        name='vrf',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure per-VRF information.")

    # server_address
    server_address = managedattribute(
        name='server_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure Hostname/IP address of the NTP Server.")

    # server_key_id
    server_key_id = managedattribute(
        name='server_key_id',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure Keyid to be used while communicating to this server.")

    # server_minpoll
    server_minpoll = managedattribute(
        name='server_minpoll',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure Minimum interval to poll a server.")

    # server_maxpoll
    server_maxpoll = managedattribute(
        name='server_maxpoll',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure Maximum interval to poll a server.")

    # server_prefer
    server_prefer = managedattribute(
        name='server_prefer',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configure Preferred Server.")

    # server_version
    server_version = managedattribute(
        name='server_version',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure server_version.")

    # peer_address
    peer_address = managedattribute(
        name='peer_address',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure Hostname/IP address of the NTP Peer.")

    # peer_key_id
    peer_key_id = managedattribute(
        name='peer_key_id',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure Keyid to be used while communicating to this peer.")

    # peer_minpoll
    peer_minpoll = managedattribute(
        name='peer_minpoll',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure Minimum interval to poll a peer.")

    # peer_maxpoll
    peer_maxpoll = managedattribute(
        name='peer_maxpoll',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure Maximum interval to poll a peer.")

    # peer_prefer
    peer_prefer = managedattribute(
        name='peer_prefer',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configure Preferred peer.")

    # peer_version
    peer_version = managedattribute(
        name='peer_version',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure peer version.")

    # auth_key_id
    auth_key_id = managedattribute(
        name='auth_key_id',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Configure NTP authentication key number.")

    # auth_algorithm
    class AUTH_ALGORITHM(Enum):
        md5 = 'md5'

    auth_algorithm = managedattribute(
        name='auth_algorithm',
        default=None,
        type=(None, AUTH_ALGORITHM),
        doc="Use md5 authentication scheme.")
    
    # auth_key
    auth_key = managedattribute(
        name='auth_key',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="Configure MD5 string.")

    # auth_trusted_key
    auth_trusted_key = managedattribute(
        name='auth_trusted_key',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Configure NTP trusted-key.")

    # if_disabled
    if_disabled = managedattribute(
        name='if_disabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable/Disable NTP.")


    class DeviceAttributes(DeviceSubAttributes):

        class VrfAttributes(VrfSubAttributes):
            
            class ServerAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.server_address = key
                    super().__init__(parent)

            server_attr = managedattribute(
                name='server_attr',
                read_only=True,
                doc=ServerAttributes.__doc__)

            @server_attr.initter
            def server_attr(self):
                return SubAttributesDict(
                    self.ServerAttributes, parent=self)

            
            class PeerAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.peer_address = key
                    super().__init__(parent)

            peer_attr = managedattribute(
                name='peer_attr',
                read_only=True,
                doc=ServerAttributes.__doc__)

            @peer_attr.initter
            def peer_attr(self):
                return SubAttributesDict(
                    self.PeerAttributes, parent=self)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=True,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)

        class AuthKeyAttribute(KeyedSubAttributes):

            def __init__(self, parent, key):
                self.auth_key_id = key
                super().__init__(parent)

        auth_key_attr = managedattribute(
            name='auth_key_attr',
            read_only=True,
            doc=AuthKeyAttribute.__doc__)

        @auth_key_attr.initter
        def auth_key_attr(self):
            return SubAttributesDict(self.AuthKeyAttribute, parent=self)

        class InterfaceAttribute(InterfaceSubAttributes):
            pass

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttribute.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttribute, parent=self)

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
