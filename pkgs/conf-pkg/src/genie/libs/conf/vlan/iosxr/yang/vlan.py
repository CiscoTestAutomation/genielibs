
# Python
from abc import ABC

# Genie package
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base import Interface
from genie.conf.base.config import YangConfig
try:
    from ydk.models.ydkmodels import Cisco_IOS_XR_ifmgr_cfg as xr_ifmgr_cfg
    from ydk.providers._provider_plugin import _ClientSPPlugin
    from ydk.types import DELETE, Empty
    from ydk.services import CRUDService
    from ydk.services import CodecService
    from ydk.providers import CodecServiceProvider
    # patch a netconf provider
    from ydk.providers import NetconfServiceProvider as _NetconfServiceProvider


    class NetconfServiceProvider(_NetconfServiceProvider):
        def __init__(self, device):
            if 'yang' not in device.mapping:
                # Want it, but dont have a connection? 
                raise Exception("Missing connection of "
                                "type 'yang' in the device "
                                "mapping '{map}'".format(map=device.mapping))
            alias = device.mapping['yang']
            dev = device.connectionmgr.connections[alias]

            super().__init__(address=str(dev.connection_info.ip),
                             port=dev.connection_info.port,
                             username=dev.connection_info.username,
                             password=dev.connection_info.password,
                             protocol = 'ssh')

            self.sp_instance = _ClientSPPlugin(self.timeout,
                                               use_native_client=False)

            self.sp_instance._nc_manager = dev
        def _connect(self, *args, **kwargs): pass
except:
    pass


class Vlan(ABC):


    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, 
            **kwargs):
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            ydk_obj = xr_ifmgr_cfg.InterfaceConfigurations()

            vlan_config = []

            for sub, attributes2 in attributes.mapping_values(
                    'interface_attr', 
                    keys=self.interface_attr):
                vlan_config.extend(sub.build_config(apply=False, 
                                                    attributes=attributes2,
                                                    unconfig=unconfig, 
                                                    ydk_obj=ydk_obj, 
                                                    **kwargs))

            # instantiate crud service
            crud_service = CRUDService()

            if apply:

                # create netconf connection
                ncp = NetconfServiceProvider(self.device)

                if unconfig:
                    crud_service.delete(ncp,ydk_obj)
                else:
                    crud_service.create(ncp, ydk_obj)

                for cfg in vlan_config:
                  cfg.apply()
            else:
                ydks = []
                for cfg in vlan_config:
                  ydks.append(cfg)

                return ydks

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class AccessMapAttributes(ABC):

            def build_config(self, ydk_obj, apply=True, 
                             attributes=None, unconfig=False, **kwargs):
                assert not apply
                # instantiate crud service
                crud_service = CRUDService()
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, 
                                         unconfig=True, **kwargs)


        class VlanConfigurationAttributes(ABC):

            def build_config(self, ydk_obj, apply=True, attributes=None, 
                             unconfig=False, **kwargs):
                assert not apply
                # instantiate crud service
                crud_service = CRUDService()
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, 
                                         unconfig=True, **kwargs)


        class InterfaceAttributes(ABC):

            def build_config(self, ydk_obj, apply=True, 
                             attributes=None, unconfig=False, **kwargs):
                assert not apply
                # instantiate crud service
                crud_service = CRUDService()
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if attributes.value('eth_encap_type1'):
                    self.interface.eth_encap_type1 = \
                        attributes.value('eth_encap_type1')

                if attributes.value('eth_encap_val1'):
                    self.interface.eth_encap_val1 = \
                        attributes.value('eth_encap_val1')

                if attributes.value('eth_encap_type2'):
                    self.interface.eth_encap_type2 = \
                        attributes.value('eth_encap_type2')

                if attributes.value('eth_encap_val2'):
                    self.interface.eth_encap_val2 = \
                        attributes.value('eth_encap_val2')

                if unconfig:
                    if attributes.attributes != None:
                        vlan_config = self.interface.build_unconfig(apply=False, 
                                                                    attributes=\
                                                                    attributes.attributes)
                    else:
                        vlan_config = self.interface.build_unconfig(apply=False,
                                                                    attributes=\
                                                                    {'eth_encap_type1': None,
                                                                     'eth_encap_val1': None,
                                                                     'eth_encap_type2': None, 
                                                                     'eth_encap_val2': None})
                else:
                    vlan_config = self.interface.build_config(apply=False)

                return (vlan_config)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, 
                                         unconfig=True, **kwargs)

