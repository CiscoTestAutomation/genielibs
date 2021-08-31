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

__all__ = ('Keychains', )
# Structure Hierarchy:
# Keychains
#   +--DeviceAttributes
#     +-- KeyChainAttributes
#     | +-- KeyIdAttributes
#     +-- KeyChainMacSecAttributes
#     | +-- KeyIdAttributes
#     +-- KeyChainTunEncAttributes
#       +-- KeyIdAttributes


class Keychains(DeviceFeature):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        # KeyChainAttributes
        class KeyChainAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.key_chain = key
                super().__init__(parent)

            # KeyIdAttributes
            class KeyIdAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.key_id = key
                    super().__init__(parent)

            key_id_attr = managedattribute(name='key_id_attr',
                                           read_only=True,
                                           doc=KeyIdAttributes.__doc__)

            @key_id_attr.initter
            def key_id_attr(self):
                return SubAttributesDict(self.KeyIdAttributes, parent=self)

        keychain_attr = managedattribute(name='keychain_attr',
                                         read_only=True,
                                         doc=KeyChainAttributes.__doc__)

        @keychain_attr.initter
        def keychain_attr(self):
            return SubAttributesDict(self.KeyChainAttributes, parent=self)

        # KeyChainMacSecAttributes
        class KeyChainMacSecAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.ms_key_chain = key
                super().__init__(parent)

            # KeyIdAttributes
            class KeyIdAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.key_id = key
                    super().__init__(parent)

            key_id_attr = managedattribute(name='key_id_attr',
                                           read_only=True,
                                           doc=KeyIdAttributes.__doc__)

            @key_id_attr.initter
            def key_id_attr(self):
                return SubAttributesDict(self.KeyIdAttributes, parent=self)

        ms_keychain_attr = managedattribute(
            name='ms_keychain_attr',
            read_only=True,
            doc=KeyChainMacSecAttributes.__doc__)

        @ms_keychain_attr.initter
        def ms_keychain_attr(self):
            return SubAttributesDict(self.KeyChainMacSecAttributes,
                                     parent=self)

        # KeyChainTunEncAttributes
        class KeyChainTunEncAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.te_key_chain = key
                super().__init__(parent)

            # KeyIdAttributes
            class KeyIdAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.key_id = key
                    super().__init__(parent)

            key_id_attr = managedattribute(name='key_id_attr',
                                           read_only=True,
                                           doc=KeyIdAttributes.__doc__)

            @key_id_attr.initter
            def key_id_attr(self):
                return SubAttributesDict(self.KeyIdAttributes, parent=self)

        te_keychain_attr = managedattribute(
            name='te_keychain_attr',
            read_only=True,
            doc=KeyChainTunEncAttributes.__doc__)

        @te_keychain_attr.initter
        def te_keychain_attr(self):
            return SubAttributesDict(self.KeyChainTunEncAttributes,
                                     parent=self)

    device_attr = managedattribute(name='device_attr',
                                   read_only=True,
                                   doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ============ managedattributes ============#
    key_id = managedattribute(name='key_id',
                              default=None,
                              type=(None, managedattribute.test_istype(str)),
                              doc='Configure a key')

    key_enc_type = managedattribute(name='key_enc_type',
                                    default=None,
                                    type=managedattribute.test_istype(int),
                                    doc='Set key encode type')

    key_string = managedattribute(name='key_string',
                                  default=None,
                                  type=(None,
                                        managedattribute.test_istype(str)),
                                  doc='Set key string')

    class CRYPTO_ALGO(Enum):
        aes_128_cmac = 'aes-128-cmac'
        aes_256_cmac = 'aes-256-cmac'

    crypto_algo = managedattribute(
        name='crypto_algo',
        default=None,
        type=(None, CRYPTO_ALGO),
        doc='Set cryptographic authentication algorithm')

    lifetime_start = managedattribute(
        name='lifetime_start',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Set start time for sending lifetime of encryption key')

    lifetime_duration = managedattribute(
        name='lifetime_duration',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Set key lifetime duration')

    # =========================================================
    #   build_config
    # =========================================================
    def build_config(self,
                     devices=None,
                     interfaces=None,
                     links=None,
                     apply=True,
                     attributes=None,
                     **kwargs):
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        devices, interfaces, links = \
            consolidate_feature_args(self, devices, interfaces, links)

        for key, sub, attributes2 in attributes.mapping_items('device_attr',
                                                              keys=devices,
                                                              sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)
        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self,
                       devices=None,
                       interfaces=None,
                       links=None,
                       apply=True,
                       attributes=None,
                       **kwargs):
        attributes = AttributesHelper(self, attributes)
        cfgs = {}

        devices, interfaces, links = \
            consolidate_feature_args(self, devices, interfaces, links)
        for key, sub, attributes2 in attributes.mapping_items('device_attr',
                                                              keys=devices,
                                                              sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs
