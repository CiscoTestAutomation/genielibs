
from enum import Enum

# Genie
from genie.decorator import managedattribute
from genie.conf.base import Base, \
                            DeviceFeature, \
                            LinkFeature, \
                            Interface
import genie.conf.base.attributes
from genie.libs.conf.base.feature import consolidate_feature_args
from genie.conf.base.attributes import SubAttributes, \
                                       SubAttributesDict, \
                                       AttributesHelper, \
                                       KeyedSubAttributes
from genie.conf.base.attributes import InterfaceSubAttributes
from genie.libs import parser
from genie.abstract import Lookup
from genie.ops.base import Base as ops_Base
from genie.ops.base import Context

__all__ = ('TunnelEncryption', )
# Structure Hierarchy:
# Keychains
#   +--DeviceAttributes
#     +-- KeyChainAttributes
#     | +-- KeyIdAttributes
#     +-- KeyChainMacSecAttributes
#     | +-- KeyIdAttributes
#     +-- KeyChainTunEncAttributes
#       +-- KeyIdAttributes


class TunnelEncryption(DeviceFeature):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ============ managedattributes ============#

    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable tunnelencryption feature.")

    policy_name = managedattribute(
        name='policy_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='create tunnel policy')

    class BIT_ENC(Enum):
        gcm_128_cmac = 'gcm-aes-xpn-128'
        gcm_256_cmac = 'gcm-aes-xpn-256'

    cipher_suite = managedattribute(
        name='cipher_suite',
        default=None,
        type=(None, BIT_ENC),
        doc='Set bit encryption algorithm')

    sak_rekey_time = managedattribute(
        name='sak_rekey_time',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Set rekey time')

    peer_ip = managedattribute(
        name='peer_ip',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="tunnel peer ip")

    keychain_name = managedattribute(
        name='keychain_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="set key chain name")

    tunnelpolicy_name = managedattribute(
        name='tunnelpolicy_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="tunnel policyname")

    tunnel_source_interface= managedattribute(
        name='tunnel_source_interface',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='tunnel source interface')

    enabled_must_secure_policy = managedattribute(
        name='enabled_must_secure_policy',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='tunnel-encryption must-secure-policy')

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        # tunnel encryption policy attributes
        class TunnelPolicyAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.policy_name = key
                super().__init__(parent)

        tunnelpolicy_attr = managedattribute(
            name='tunnelpolicy_attr',
            read_only=True,
            doc=TunnelPolicyAttributes.__doc__)

        @tunnelpolicy_attr.initter
        def tunnelpolicy_attr(self):
            return SubAttributesDict(
                self.TunnelPolicyAttributes, parent=self)

        class TunnelPeerIpAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.peer_ip = key
                super().__init__(parent)

        tunnelpeerip_attr = managedattribute(
            name='tunnelpeerip_attr',
            read_only=True,
            doc=TunnelPeerIpAttributes.__doc__)

        @tunnelpeerip_attr.initter
        def tunnelpeerip_attr(self):
            return SubAttributesDict(
                self.TunnelPeerIpAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # =========================================================
    #   build_config
    # =========================================================
    def build_config(self, devices=None, interfaces=None, links=None,
                     apply=True, attributes=None, **kwargs):
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        devices, interfaces, links = \
            consolidate_feature_args(self, devices, interfaces, links)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)
        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, interfaces=None, links=None,
                       apply=True, attributes=None, **kwargs):
        attributes = AttributesHelper(self, attributes)

        cfgs = {}

        devices, interfaces, links = \
            consolidate_feature_args(self, devices, interfaces, links)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs