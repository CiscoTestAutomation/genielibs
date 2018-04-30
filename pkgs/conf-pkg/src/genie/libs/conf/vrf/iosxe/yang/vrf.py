"""Implement IOS-XR (iosxr) Specific Configurations for Vrf objects.
"""

# Table of contents:
#     class Vrf:
#         class DeviceAttributes:
#             def build_config/build_unconfig:
#             class AddressFamilyAttributes:
#                 def build_config/build_unconfig:

from abc import ABC
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.libs.conf.address_family import AddressFamily,\
     AddressFamilySubAttributes
from genie.conf.base.config import YangConfig
try:
    from ydk.models.ned import ned
    from ydk.types import DELETE, Empty
    from ydk.services import CRUDService

    from ydk.services import CodecService
    from ydk.providers import CodecServiceProvider

    # patch a netconf provider
    from ydk.providers import NetconfServiceProvider as _NetconfServiceProvider
    from ydk.providers._provider_plugin import _ClientSPPlugin

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
except Exception:
    pass

class Vrf(object):

    class DeviceAttributes(object):

        def build_config(self, apply=True, attributes=None, unconfig=False, **kwargs):
            assert not kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            ydk_obj = ned.Native.Vrf()
            vrf_obj = ydk_obj.Definition()
            ydk_obj.definition.append(vrf_obj)
            if attributes.value('name'):
                vrf_obj.name = attributes.value('name')

            # iosxr: vrf vrf1 / address-family ipv4 unicast (config-vrf-af)
            for key, sub, attributes2 in attributes.mapping_items(
                    'address_family_attr', keys=self.address_families, sort=True):
                sub.build_config(apply=False, attributes=attributes2, unconfig=unconfig, vrf_obj=vrf_obj)

            # instantiate crud service
            crud_service = CRUDService()
            if apply:

                # create netconf connection
                ncp = NetconfServiceProvider(self.device)

                crud_service.create(ncp, ydk_obj)

                if unconfig:
                    crud_service.delete(ncp, ydk_obj)
            else:
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

                #return YangConfig(device=self.device,
                #                  ydk_obj=ydk_obj,
                #                  ncp=NetconfServiceProvider,
                #                  crud_service=crud_service.delete)


        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class AddressFamilyAttributes(object):

            def build_config(self, vrf_obj, apply=True, attributes=None, unconfig=False, **kwargs):
                assert not apply
                assert not kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                if attributes.value('address_family').value == 'ipv4 unicast':
                    vrf_obj.address_family.ipv4 = vrf_obj.AddressFamily.Ipv4()

                if attributes.value('address_family').value == 'ipv6 unicast':
                    vrf_obj.address_family.ipv6 = vrf_obj.AddressFamily.Ipv6()

                if unconfig and attributes.iswildcard:
                    if attributes.value('address_family').value == 'ipv4 unicast':
                        vrf_obj.address_family.ipv4 = None

                    if attributes.value('address_family').value == 'ipv6 unicast':
                        vrf_obj.address_family.ipv6 = None

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=False, **kwargs)

