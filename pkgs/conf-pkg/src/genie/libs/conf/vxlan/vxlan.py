# Python
from enum import Enum


# Genie package
from genie.decorator import managedattribute
from genie.conf.base import Base, \
                            DeviceFeature, \
                            LinkFeature, \
                            Interface
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, \
                                       SubAttributesDict, \
                                       AttributesHelper, \
                                       KeyedSubAttributes
from genie.libs import parser
from genie.abstract import Lookup
from genie.ops.base import Base as ops_Base
from genie.ops.base import Context
# Genie Xbu_shared
from genie.libs.conf.base.feature import consolidate_feature_args

__all__ = (
        'Vxlan',
        )
# Table of contents:
#  class DeviceAttributes
#     class EvpnMsiteBgwAttributes
#     class EvpnAttributes
#         class VniAttributes
#             class RouteTargetAttributes

class Vxlan(DeviceFeature, LinkFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        #  EvpnMsiteBgwAttributes
        class EvpnMsiteBgwAttributes(KeyedSubAttributes):
            def __init__(self, parent,key):
                self.evpn_msite_bgw = key
                super().__init__(parent)

        #  EvpnAttributes
        class EvpnAttributes(KeyedSubAttributes):
            def __init__(self, key, *args, **kwargs):
                super().__init__(*args, **kwargs)

            # VniAttribute
            class VniAttributes(KeyedSubAttributes):
                def __init__(self, parent,key):
                    self.evpn_vni = key
                    super().__init__(parent)

                # RouteAttributes
                class RouteTargetAttributes(KeyedSubAttributes):
                    def __init__(self, key, *args, **kwargs):
                        self.evpn_vni_rt = key
                        super().__init__(*args, **kwargs)

                route_target_attr = managedattribute(
                    name='route_target_attr',
                    read_only=True,
                    doc=RouteTargetAttributes.__doc__)

                @route_target_attr.initter
                def route_target_attr(self):
                    return SubAttributesDict(self.RouteTargetAttributes, parent=self)


            vni_attr = managedattribute(
                name='vni_attr',
                read_only=True,
                doc=VniAttributes.__doc__)

            @vni_attr.initter
            def vni_attr(self):
                return SubAttributesDict(self.VniAttributes, parent=self)

        evpn_attr = managedattribute(
            name='evpn_attr',
            read_only=True,
            doc=EvpnAttributes.__doc__)

        @evpn_attr.initter
        def evpn_attr(self):
            return SubAttributesDict(self.EvpnAttributes, parent=self)

        evpn_msite_attr = managedattribute(
            name='evpn_msite_attr',
            read_only=True,
            doc=EvpnMsiteBgwAttributes.__doc__)

        @evpn_msite_attr.initter
        def evpn_msite_attr(self):
            return SubAttributesDict(self.EvpnMsiteBgwAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ============ managedattributes ============#
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='activate features nv overlay , nv overlay evpn and vn-segment-vlan-based')
    enabled_nv_overlay = managedattribute(
        name='enabled_nv_overlay',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='activate feature nv overlay')

    enabled_vn_segment_vlan_based = managedattribute(
        name='enabled_vn_segment_vlan_based',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='activate feature vn-segment-vlan-based')

    enabled_nv_overlay_evpn = managedattribute(
        name='enabled_nv_overlay_evpn',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='nv overlay evpn')

    fabric_fwd_anycast_gw_mac = managedattribute(
        name='fabric_fwd_anycast_gw_mac',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='fabric forwarding anycast-gateway-mac')

    evpn_msite_bgw = managedattribute(
        name='evpn_msite_bgw',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='evpn multisite border-gateway')

    evpn_msite_bgw_delay_restore_time = managedattribute(
        name='evpn_msite_bgw_delay_restore_time',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='delay restore time')

    evpn_msite_dci_advertise_pip = managedattribute(
        name='evpn_msite_dci_advertise_pip',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='dci advertise pip')

    evpn_msite_split_horizon_per_site = managedattribute(
        name='evpn_msite_split_horizon_per_site',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='split-horizon per-site')

    evpn_vni = managedattribute(
        name='evpn_vni',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='vni id')

    evpn_vni_rd = managedattribute(
        name='evpn_vni_rd',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='vni route distinguisher')

    evpn_vni_rt = managedattribute(
        name='evpn_vni_rt',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='vni route target')

    class routeType(Enum):
        IMPORT = 'import'
        EXPORT = 'export'
        BOTH = 'both'

    evpn_vni_rt_type = managedattribute(
        name='evpn_vni_rt_type',
        default=None,
        type=(None, routeType),
        doc='vni route target type')

    enabled_ngmvpn = managedattribute(
        name='enabled_ngmvpn',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='activate features ngmvpn')

    advertise_evpn_multisite = managedattribute(
        name='advertise_evpn_multisite',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='advertise evpn multisite')

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


    @classmethod
    def learn_config(self, device, **kwargs):
        '''
            A method that learn the device configurational state and create
            a conf object with the same configuration.

            Args:
                self (`obj`): Conf object.
                device (`obj`): The device that will be used to parse the
                    command.
        '''

        # Abstracting the show running trm as per device os
        ret = Lookup.from_device(device)
        cmd = ret.parser.show_trm.ShowRunningConfigTrm
        maker = ops_Base(device=device)

        maker.add_leaf(cmd=cmd,
                       src='[advertise_evpn_multicast]',
                       dest='trm[advertise_evpn_multicast]')


        # A workaround to pass the context as in maker it expects Context.cli
        # not just a string 'cli.
        maker.context_manager[cmd] = Context.cli
        maker.make()
        # Take a copy of the object dictionary
        if not hasattr(maker, 'trm'):
            maker.trm= {}
        new_trm = maker.trm

        # List of mapped conf objects
        conf_obj_list = []

        # Main structure attributes in the conf object
        structure_keys = ['']

        conf_obj = self()
        # Pass the class method.
        maker.dict_to_obj(conf=conf_obj, \
                          struct=structure_keys, \
                          struct_to_map=new_trm)


        conf_obj_list.append(conf_obj)

        # List of mapped conf objects
        return conf_obj_list
