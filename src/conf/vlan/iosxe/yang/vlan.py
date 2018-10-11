
# Python
from abc import ABC

# xBU_shared genie package
from genie.libs.conf.vrf import VrfSubAttributes

# Genie package
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base import Interface
from genie.conf.base.config import YangConfig
try:
    # from ydk.models.ned import ned
    from ydk.models.xe_recent_edison import Cisco_IOS_XE_native as ned
    from ydk.types import DELETE, Empty
    from ydk.services import CRUDService

    # patch a netconf provider
    from ydk.providers import NetconfServiceProvider as _NetconfServiceProvider
    from ydk.providers._provider_plugin import _ClientSPPlugin
    from ydk.services import CodecService
    from ydk.providers import CodecServiceProvider

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
            ydk_obj = ned.Native.Vlan()

            vlan_config = []
            for sub, attributes2 in attributes.mapping_values(
                    'access_map_attr', 
                    keys=self.access_map_attr.keys()):
                vlan_config.extend(sub.build_config(apply=False, 
                                                    attributes=attributes2,
                                                    unconfig=unconfig, 
                                                    ydk_obj=ydk_obj,
                                                    **kwargs))

            for sub, attributes2 in attributes.mapping_values(
                    'vlan_configuration_attr', 
                    keys=self.vlan_configuration_attr.keys()):
                vlan_config.extend(sub.build_config(apply=False, 
                                                    attributes=attributes2,
                                                    unconfig=unconfig, 
                                                    ydk_obj=ydk_obj, 
                                                    **kwargs))

            for sub, attributes2 in attributes.mapping_values(
                    'interface_attr', 
                    keys=self.interface_attr.keys()):
                vlan_config.extend(sub.build_config(apply=False, 
                                                    attributes=attributes2,
                                                    unconfig=unconfig, 
                                                    ydk_obj=ydk_obj, 
                                                    **kwargs))

            # iosxe: vlan 1000 (config-vlan)
            id = attributes.value('vlan_id', force = True)

            if id:
                vlan = ydk_obj.VlanList()
                vlan.id = int(id)
                ydk_obj.vlan_list.append(vlan)

            # instantiate crud service
            crud_service = CRUDService()

            if apply:

                # create netconf connection
                ncp = NetconfServiceProvider(self.device)

                if unconfig:
                    crud_service.delete(ncp,ydk_obj)
                else:
                    crud_service.create(ncp, ydk_obj)
            else:
                ydks = []

                if unconfig:
                    ydks.append(YangConfig(device=self.device,
                                           ydk_obj=ydk_obj,
                                           ncp=NetconfServiceProvider,
                                           crud_service=crud_service.delete))
                else:
                    ydks.append(YangConfig(device=self.device,
                                           ydk_obj=ydk_obj,
                                           ncp=NetconfServiceProvider,
                                           crud_service=crud_service.create))

                return ydks

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class AccessMapAttributes(ABC):

            def build_config(self, ydk_obj, apply=True, attributes=None, 
                             unconfig=False, **kwargs):
                assert not apply
                # instantiate crud service
                crud_service = CRUDService()
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if unconfig:
                    return YangConfig(device=self.device,
                                      ydk_obj=ydk_obj,
                                      ncp=NetconfServiceProvider,
                                      crud_service=crud_service.delete)
                else:
                    return YangConfig(device=self.device,
                                      ydk_obj=ydk_obj,
                                      ncp=NetconfServiceProvider,
                                      crud_service=crud_service.create)

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

                if unconfig:
                    return YangConfig(device=self.device,
                                      ydk_obj=ydk_obj,
                                      ncp=NetconfServiceProvider,
                                      crud_service=crud_service.delete)
                else:
                    return YangConfig(device=self.device,
                                      ydk_obj=ydk_obj,
                                      ncp=NetconfServiceProvider,
                                      crud_service=crud_service.create)

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

                if unconfig:
                    return YangConfig(device=self.device,
                                      ydk_obj=ydk_obj,
                                      ncp=NetconfServiceProvider,
                                      crud_service=crud_service.delete)
                else:
                    return YangConfig(device=self.device,
                                      ydk_obj=ydk_obj,
                                      ncp=NetconfServiceProvider,
                                      crud_service=crud_service.create)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, 
                                         unconfig=True, **kwargs)

