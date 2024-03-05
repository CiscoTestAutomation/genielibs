
# Python
from enum import Enum

# Genie
from genie.decorator import managedattribute
from genie.libs.conf.base import MAC
from genie.libs.conf.base.feature import consolidate_feature_args
from genie.conf.base.base import DeviceFeature, InterfaceFeature, LinkFeature
from genie.conf.base.attributes import DeviceSubAttributes, SubAttributesDict,\
                                       AttributesHelper, KeyedSubAttributes,\
                                       InterfaceSubAttributes

__all__ = (
    'Macsec',
)

# Macsec
# +-- DeviceAttributes
#   +-- MacsecPolicyAttributes
#   +-- InterfaceAttributes

class CHIPHER_SUITE(Enum):
    gcm_aes_128 = 'GCM-AES-128' 
    gcm_aes_xpn_128 = 'GCM-AES-XPN-128' 
    gcm_aes_256 = 'GCM-AES-256'
    gcm_aes_xpn_256 = 'GCM-AES-XPN-256'
    
class CONF_OFFSET(Enum):
    conf_offset_0  = 'CONF-OFFSET-0'
    conf_offset_30 = 'CONF-OFFSET-30'
    conf_offset_50 = 'CONF-OFFSET-50'

class SECURITY_POLICY(Enum):
    should_secure = 'should-secure'
    must_secure = 'must-secure'    


class Macsec(DeviceFeature, LinkFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ==========================================================================
    #                           CONF CLASS STRUCTURE
    # ==========================================================================

    # +- DeviceAttributes
    class DeviceAttributes(DeviceSubAttributes):

        # +- DeviceAttributes
        #   +- MacsecPolicyAttributes
        class MacsecPolicyAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.macsec_policy_name=key
                super().__init__(parent)
            

        macsec_policy_attr = managedattribute(
            name='macsec_policy_attr',
                read_only=True,
                doc=MacsecPolicyAttributes.__doc__)

        @macsec_policy_attr.initter
        def macsec_policy_attr(self):
            return SubAttributesDict(self.MacsecPolicyAttributes, parent=self)

        # +- DeviceAttributes
        #   +- MacsecPolicyAttributes
        #   +- InterfaceAttributes
        class InterfaceAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.interface_name=key
                super().__init__(parent)

        interface_attr = managedattribute(
            name='interface_attr',
            read_only=True,
            doc=InterfaceAttributes.__doc__)

        @interface_attr.initter
        def interface_attr(self):
            return SubAttributesDict(self.InterfaceAttributes, parent=self)

    device_attr = managedattribute(
            name='device_attr',
            read_only=True,
            doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
            return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ===========================================# 
    #       managedattributes
    # ===========================================#
    # macsec feature enable attribute
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    #macsec policy attributes
    key_server_priority = managedattribute(name='key_server_priority',
                                            default=None,
                                            type=(None, managedattribute.test_istype(int)),
                                            doc='Configure key server priority')

    cipher_suite = managedattribute(name='cipher_suite',
                                    default=None,
                                    type=(None, CHIPHER_SUITE),
                                    doc='Set cipher suite algorithm')

    #can be single or multiple values possible, can't use Enum class as type. 
    enforce_cipher_suite = managedattribute(name='enforce',
                                default=False,
                                type=(None, managedattribute.test_istype(str)),
                                doc='Enable/disable enforce cipher-suite ')

    conf_offset = managedattribute(name='conf_offset',
                                default=None,
                                type=(None, CONF_OFFSET),
                                doc='Configure offset value')

    include_icv_indicator = managedattribute(name='include_icv_indicator',
                                            default=None,
                                            type=(None, managedattribute.test_istype(bool)),
                                            doc='Enable/disable ICV')

    security_policy = managedattribute(name='security_policy',
                                        default=None,
                                        type=(None, SECURITY_POLICY),
                                        doc='Configure security policy')
    
    window_size = managedattribute(name='window_size',
                                    default=None,
                                    type=(None, managedattribute.test_istype(int)),
                                    doc='Configure replay protection window size')

    sak_expiry_time = managedattribute(name='sak_expiry_time',
                                        default=None,
                                        type=(None, managedattribute.test_istype(int)),
                                        doc='Configure SAK expiry timer')
    
    include_sci = managedattribute(name='include_sci',
                                        default=None,
                                        type=(None, managedattribute.test_istype(bool)),
                                        doc='Enable/disable include-sci')
    
    ppk_profile_name = managedattribute(name='ppk_profile_name',
                                        default=None,
                                        type=(None, managedattribute.test_istype(str)),
                                        doc='Configure PPK crypto-qkd-profile')
    
    #macsec interface level attributes
    key_chain = managedattribute(name='key_chain',
                                default=None,
                                type=(None, managedattribute.test_istype(str)),
                                doc='Configure key chain name')
    
    fallback_key_chain = managedattribute(name='fallback_key_chain',
                                default=None,
                                type=(None, managedattribute.test_istype(str)),
                                doc='Configure fallback key chain name')
    
    macsec_policy_name = managedattribute(name='macsec_policy_name',
                                        default=None,
                                        type=(None, managedattribute.test_istype(str)),
                                        doc='Configure macsec policy name')
    
    eapol_mac_address = managedattribute(name='eapol_mac_address',
                                        default=None,
                                        type=(None, MAC),
                                        doc='Configure eapol mac address')
    eapol_broadcast_mac_address = managedattribute(name='eapol_broadcast_mac_address',
                                        default=False,
                                        type=(None, managedattribute.test_istype(bool)),
                                        doc='Configure eapol broadcast mac address')
    
    ether_type = managedattribute(name='ether_type',
                                        default=None,
                                        type=(None, managedattribute.test_istype(str)),
                                        doc='Configure ethernet type')

    interface_name = managedattribute(name='interface_name',
                                    default=None,
                                    type=(None, managedattribute.test_istype(str)),
                                    doc='Interface name to apply config')

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
