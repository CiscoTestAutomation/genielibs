
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
    'Crypto',
)

# Crypto
# +-- DeviceAttributes
#   +-- CryptoQkdAttributes


class TLS_AUTH_TYPE(Enum):
    psk = 'psk'
    trustpoint = 'trustpoint'

    
class Crypto(DeviceFeature, LinkFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ==========================================================================
    #                           CONF CLASS STRUCTURE
    # ==========================================================================

    # +- DeviceAttributes
    class DeviceAttributes(DeviceSubAttributes):

        # +- DeviceAttributes
        #   +- CryptoQkdAttributes
        class CryptoQkdAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.crypto_qkd_name=key
                super().__init__(parent)
            

        crypto_qkd_attr = managedattribute(
            name='crypto_qkd_attr',
            read_only=True,
            doc=CryptoQkdAttributes.__doc__)

        @crypto_qkd_attr.initter
        def crypto_qkd_attr(self):
            return SubAttributesDict(self.CryptoQkdAttributes, parent=self)

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
    # crytpopqc feature enable attribute
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)))
    
    qkd_profile_name = managedattribute(name='qkd_profile_name',
                                            default=None,
                                            type=(None, managedattribute.test_istype(str)),
                                            doc='Configure crypto qkd profile')

    kme_server_ip = managedattribute(name='kme_server_ip',
                                        default=None,
                                        type=(None, managedattribute.test_istype(str)),
                                        doc='Configure kme server ip')
    
    kme_server_http_port = managedattribute(name='kme_server_http_port',
                                        default=None,
                                        type=(None, managedattribute.test_istype(int)),
                                        doc='Configure kme server http port')
    
    http_proxy_server = managedattribute(name='http_proxy_server',
                                        default=None,
                                        type=(None, managedattribute.test_istype(str)),
                                        doc='Configure http proxy server')
    
    http_proxy_port = managedattribute(name='http_proxy_port',
                                        default=None,
                                        type=(None, managedattribute.test_istype(int)),
                                        doc='Configure http proxy port')
    
    
    tls_auth_type = managedattribute(name='tls_auth_type',
                                        default=None,
                                        type=(None, TLS_AUTH_TYPE),
                                        doc='Configure transport tls authentication type')
    
    tls_trustpoint_name =  managedattribute(name='tls_trustpoint_name',
                                        default=None,
                                        type=(None, managedattribute.test_istype(str)),
                                        doc='Configure transport tls trustpoint name ') 

    tls_trustpoint_ignore_certificate =  managedattribute(name='tls_trustpoint_ignore_certificate',
                                        default=None,
                                        type=(None, managedattribute.test_istype(bool)),
                                        doc='Configure transport tls trustpoint ignore certificate')
                                        
    tls_pks_key_id =  managedattribute(name='tls_pks_key_id',
                                        default=None,
                                        type=(None, managedattribute.test_istype(int)),
                                        doc='Configure transport tls pks key id') 

    tls_pks_key_string =  managedattribute(name='tls_pks_key_string',
                                        default=None,
                                        type=(None, managedattribute.test_istype(str)),
                                        doc='Configure transport tls pks key string')
    
    
    source_interface = managedattribute(name='source_interface',
                                            default=None,
                                            type=(None, managedattribute.test_istype(str)),
                                            doc='Configure crypto source interface')
    

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
