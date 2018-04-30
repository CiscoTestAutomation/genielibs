
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
    from ydk.models.ned import ned
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
            ydk_obj = ned.Native.Router.Ospf()
            ospf_intfs = []
            for sub, attributes2 in attributes.mapping_values('vrf_attr', sort=VrfSubAttributes._sort_key):
                ospf_intfs.extend(sub.build_config(apply=False, attributes=attributes2,
                                 unconfig=unconfig, ydk_obj=ydk_obj, **kwargs))

            # instantiate crud service
            crud_service = CRUDService()
            if apply:

                # create netconf connection
                ncp = NetconfServiceProvider(self.device)

                if unconfig:
                    crud_service.delete(ncp,ydk_obj)
                else:
                    crud_service.create(ncp, ydk_obj)
                    for inter in ospf_intfs:
                        inter.apply()
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

                    for inter in ospf_intfs:
                        ydks.append(inter)
                return ydks

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class VrfAttributes(ABC):

            def build_config(self, ydk_obj, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                id = attributes.value('ospf_name', force = True)
                vrf = attributes.value('vrf', force = True)

                if id:
                    ydk_obj.id = int(id)

                if vrf:
                    ydk_obj.vrf = vrf.name

                    # ! router ospf 1
                    # !  router-id 1.1.1.1
                if attributes.value('instance_router_id'):
                    ydk_obj.router_id = str(attributes.value('instance_router_id'))

                if attributes.value('auto_cost_ref_bw'):
                    ospf_auto_cost = ydk_obj.AutoCost()
                    ospf_auto_cost.reference_bandwidth = int(attributes.value('auto_cost_ref_bw'))
                    ydk_obj.auto_cost = ospf_auto_cost

                    # ! router ospf 1
                    # !  nsr
                v = attributes.value('nsr')
                if v == True:
                    ydk_obj.nsr = Empty()

                ospf_intfs = []
                for sub, attributes2 in attributes.mapping_values('area_attr', keys=self.area_attr.keys()):
                    ospf_intfs.extend(sub.build_config(apply=False, attributes=attributes2, \
                                     unconfig=unconfig, ydk_obj=ydk_obj, **kwargs))
                return ospf_intfs
            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class AreaAttributes(ABC):

                def build_config(self, ydk_obj, apply=True, attributes=None, unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    ospf_intfs = []
                    for sub, attributes2 in attributes.mapping_values('interface_attr'):
                        ospf_intfs.append(sub.build_config(apply=False, attributes=attributes2, \
                                         unconfig=unconfig, area_id = self.area_id, ydk_obj=ydk_obj, **kwargs))

                    return ospf_intfs
                
                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

                class InterfaceAttributes(ABC):

                    def build_config(self, ydk_obj, apply=True, attributes=None, unconfig=False, **kwargs):
                        assert not apply
                        if kwargs.get('area_id',None) is not None:
                            setattr(self,'area_id',kwargs['area_id'])
                        # instantiate crud service
                        crud_service = CRUDService()
                        attributes = AttributesHelper(self, attributes)
                        configurations = CliConfigBuilder(unconfig=unconfig)
                        intf_name = attributes.value('interface_name')
                        if intf_name.startswith('Gig'):
                            ydk_obj_intf =ned.Native.Interface.Gigabitethernet()
                            keep = string.digits + '//'
                            ydk_obj_intf.name =  ''.join(i for i in attributes.value('interface_name') if i in keep)

                            if attributes.value('area_id') is not None:
                                ospf_process = ydk_obj_intf.ip.ospf.ProcessId()
                                ospf_process.id = int(attributes.value('ospf_name'))
                                ospf_process.area = attributes.value('area_id')
                                ydk_obj_intf.ip.ospf.process_id.append(ospf_process)

                            if attributes.value('area_interface_cost') is not None:
                                ydk_obj_intf.ip.ospf.cost = attributes.value('area_interface_cost')

                            return YangConfig(device=self.device,
                                              ydk_obj=ydk_obj_intf,
                                              ncp=NetconfServiceProvider,
                                              crud_service=crud_service.create)

                        elif intf_name.startswith('Loop'):
                            ydk_obj_intf =ned.Native.Interface.Loopback()
                            keep = string.digits
                            ydk_obj_intf.name =  int(''.join(i for i in attributes.value('interface_name') if i in keep))
                            # name is a mandatory arguments

                            if attributes.value('area_id') is not None:
                                ospf_process = ydk_obj_intf.ip.ospf.ProcessId()
                                ospf_process.id = int(attributes.value('ospf_name'))
                                ospf_process.area = attributes.value('area_id')
                                ydk_obj_intf.ip.ospf.process_id.append(ospf_process)

                            if attributes.value('area_interface_cost') is not None:
                                ydk_obj_intf.ip.ospf.cost = attributes.value('area_interface_cost')

                            if unconfig:
                                return YangConfig(device=self.device,
                                                  ydk_obj=ydk_obj_intf,
                                                  ncp=NetconfServiceProvider,
                                                  crud_service=crud_service.delete)
                            else:
                                return YangConfig(device=self.device,
                                                  ydk_obj=ydk_obj_intf,
                                                  ncp=NetconfServiceProvider,
                                                  crud_service=crud_service.create)

                    def build_unconfig(self, apply=True, attributes=None, **kwargs):
                        return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

