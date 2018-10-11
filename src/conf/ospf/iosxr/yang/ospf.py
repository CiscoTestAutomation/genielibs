
from abc import ABC
import warnings
import string
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base import Interface

from genie.libs.conf.vrf import VrfSubAttributes
from genie.conf.base.config import YangConfig
try:
    from ydk.models.ydkmodels import Cisco_IOS_XR_ipv4_ospf_cfg as xr_ipv4_ospf_cfg
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

class Ospf(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):

            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            ospf = xr_ipv4_ospf_cfg.Ospf()
            process = ospf.processes.Process()
            id = attributes.value('ospf_name', force = True)
            process.process_name = str(id)
            ospf.processes.process.append(process)
            if not unconfig:
                process.start = Empty()
                # crud_service = CRUDService()
                # ncp = NetconfServiceProvider(self.device)
                # x = crud_service.read(ncp, process)
                # abc = YangConfig(device=self.device, ydk_obj=x, ncp=ncp, crud_service=crud_service)
                # print(abc)
                v = attributes.value('nsr')
                if v == True:
                    process.nsr = "true"
                for sub, attributes2 in attributes.mapping_values('vrf_attr', sort=VrfSubAttributes._sort_key):
                    sub.build_config(apply=False, attributes=attributes2,
                                     unconfig=unconfig, process=process, **kwargs)
            # instantiate crud service
            crud_service = CRUDService()
            if apply:

                # create netconf connection3
                ncp = NetconfServiceProvider(self.device)
                if unconfig:
                    crud_service.delete(ncp,process)
                else:
                    crud_service.create(ncp,process)
            else:
                if unconfig:
                    return YangConfig(device=self.device,
                                           ydk_obj=process,
                                           ncp=NetconfServiceProvider,
                                           crud_service=crud_service.delete)
                else:
                    return YangConfig(device=self.device,
                                           ydk_obj=process,
                                           ncp=NetconfServiceProvider,
                                           crud_service=crud_service.create)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class VrfAttributes(ABC):

            def build_config(self, process, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)
                vrf = attributes.value('vrf', force = True)
                if vrf:
                    vrf_obj = process.vrfs.Vrf()
                    vrf_obj.vrf_name = vrf.name
                    vrf_obj.vrf_start = Empty()
                    process.vrfs.vrf.append(vrf_obj)
                else:
                    vrf_obj = process.default_vrf


                    # ! router ospf 1
                    # !  router-id 1.1.1.1
                if attributes.value('instance_router_id'):
                    vrf_obj.router_id = str(attributes.value('instance_router_id'))

                if attributes.value('auto_cost_ref_bw'):
                    ospf_auto_cost = vrf_obj.AutoCost()
                    ospf_auto_cost.bandwidth = int(attributes.value('auto_cost_ref_bw'))
                    vrf_obj.auto_cost = ospf_auto_cost

                    # ! router ospf 1
                    # !  nsr
                for sub, attributes2 in attributes.mapping_values('area_attr', keys=self.area_attr.keys()):
                    sub.build_config(apply=False, attributes=attributes2, \
                                     unconfig=unconfig, vrf_obj=vrf_obj, **kwargs)
            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class AreaAttributes(ABC):

                def build_config(self, vrf_obj, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    area_area_id = vrf_obj.area_addresses.AreaAreaId()
                    area_area_id.area_id = int(self.area_id)
                    area_area_id.running = Empty()
                    vrf_obj.area_addresses.area_area_id.append(area_area_id)
                    for sub, attributes2 in attributes.mapping_values('interface_attr'):
                        sub.build_config(apply=False, attributes=attributes2, \
                                         unconfig=unconfig, area_area_id=area_area_id, **kwargs)
                
                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

                class InterfaceAttributes(ABC):

                    def build_config(self, area_area_id, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)
                        intf_name = attributes.value('interface_name')
                        name_scope = area_area_id.name_scopes.NameScope()
                        name_scope.interface_name = intf_name
                        name_scope.running = Empty()
                        area_area_id.name_scopes.name_scope.append(name_scope)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

