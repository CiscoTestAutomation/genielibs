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
from genie.abstract import Lookup
from genie.ops.base import Context
from genie.ops.base import Base as ops_Base
from genie.libs import parser

__all__ = (
        'Msdp',
        )
# Table of contents:
#   class Msdp:
#      class DeviceAttributes:
#         class VrfAttributes:
#            class PeerAttributes:

class Msdp(DeviceFeature, LinkFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        # VrfAttributes
        class VrfAttributes(KeyedSubAttributes):
            def __init__(self, key, *args, **kwargs):
                self.vrf_name = key
                super().__init__(*args, **kwargs)

            # PeerAttribute
            class PeerAttributes(KeyedSubAttributes):
                def __init__(self, key, *args, **kwargs):
                    self.address = key
                    super().__init__(*args, **kwargs)

            peer_attr = managedattribute(
                name='peer_attr',
                read_only=True,
                doc=PeerAttributes.__doc__)

            @peer_attr.initter
            def peer_attr(self):
                return SubAttributesDict(self.PeerAttributes, parent=self)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=True,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)


    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    # ============       managedattributes ============#
    vrf_name = managedattribute(
        name='vrf_name',
        default=None,
        type=managedattribute.test_istype(str),
        doc='vrf name')

    enabled = managedattribute(
        name='enabled',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='enabling msdp feature')

    originating_rp = managedattribute(
        name='originating_rp',
        default=None,
        type=managedattribute.test_istype(str),
        doc='set originating rp')

    global_connect_retry_interval = managedattribute(
        name='global_connect_retry_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='set global connect retry interval')

    address = managedattribute(
        name='address',
        default=None,
        type=managedattribute.test_istype(str),
        doc='set address')

    peer_as = managedattribute(
        name='peer_as',
        default=None,
        type=managedattribute.test_istype(str),
        doc='set peer as')

    connected_source = managedattribute(
        name='connected_source',
        default=None,
        type=managedattribute.test_istype(str),
        doc='set connected source')

    enable = managedattribute(
        name='enable',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='set connection status')

    description = managedattribute(
        name='description',
        default=None,
        type=managedattribute.test_istype(str),
        doc='set description')

    mesh_group = managedattribute(
        name='mesh_group',
        default=None,
        type=managedattribute.test_istype(str),
        doc='set mesh group')

    sa_filter_in = managedattribute(
        name='sa_filter_in',
        default=None,
        type=managedattribute.test_istype(str),
        doc='set filter in')

    sa_filter_out = managedattribute(
        name='sa_filter_out',
        default=None,
        type=managedattribute.test_istype(str),
        doc='set filter out')

    sa_limit = managedattribute(
        name='sa_limit',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='set sa limit')

    keepalive_interval = managedattribute(
        name='keepalive_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='set keepalive interval')

    holdtime_interval = managedattribute(
        name='holdtime_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='set keepalive timeout')

    # =========================================================
    #   build_config
    # =========================================================
    def build_config(self, devices=None, apply=True, attributes=None,
                     **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True, attributes=None,
                       **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr',
                keys=devices, sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
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
        if kwargs.get('attributes', None):
            kwargs['attributes'].append('vrfs_list')

        # Abstracting the show running bgp as per device os
        ret = Lookup.from_device(device)
        cmd = ret.parser.show_msdp.ShowRunningConfigMsdp

        maker = ops_Base(device=device, **kwargs)

        # get vrfs for usage on attribtues of specific vrf
        maker.add_leaf(cmd=cmd,
                       src='[vrf]',
                       dest='vrfs_list',
                       pip_str='vrf',
                       action=lambda x: list(x.keys()))

        # A workaround to pass the context as lin maker it expects Context.cli
        # not just a string 'cli.
        maker.context_manager[cmd] = Context.cli
        maker.make()

        maker.vrfs_list = getattr(maker, 'vrfs_list', [])
        maker.vrfs_list.append('default')
        maker.vrfs_list = set(maker.vrfs_list)

        for vrf in maker.vrfs_list:

            # -----  global attributes -----
            global_src = '[vrf][{vrf}][global]'.format(vrf=vrf)
            global_dest = 'msdp[vrf_attr][{vrf}]'.format(vrf=vrf)

            # connect_retry_interval
            maker.add_leaf(cmd=cmd,
                           src=global_src + '[timer][connect_retry_interval]',
                           dest=global_dest + '[global_connect_retry_interval]',
                           pip_str='reconnect-interval',
                           vrf=vrf)

            # originating_rp
            maker.add_leaf(cmd=cmd,
                           src=global_src + '[originating_rp]',
                           dest=global_dest + '[originating_rp]',
                           pip_str='originator-id',
                           vrf=vrf)

            # -----  peer attributes -----
            peer_src = '[vrf][{vrf}][peer][(?P<peer>.*)]'.format(vrf=vrf)
            peer_dest = 'msdp[vrf_attr][{vrf}][peer_attr][(?P<peer>.*)]'.format(vrf=vrf)

            # description
            maker.add_leaf(cmd=cmd,
                           src=peer_src + '[description]',
                           dest=peer_dest + '[description]',
                           pip_str='description',
                           vrf=vrf)

            # connected_source, peer_as
            for src, dest in {'[connect_source]': '[connected_source]',
                              '[peer_as]': '[peer_as]'
                              }.items():

                maker.add_leaf(cmd=cmd,
                               src=peer_src + src,
                               dest=peer_dest + dest,
                               pip_str='connect-source',
                               vrf=vrf)

            #keepalive_interval, holdtime_interval
            for src, dest in {'[timer][keepalive_interval]': '[keepalive_interval]',
                              '[timer][holdtime_interval]': '[holdtime_interval]'
                              }.items():

                maker.add_leaf(cmd=cmd,
                               src=peer_src + src,
                               dest=peer_dest + dest,
                               pip_str='keepalive',
                               vrf=vrf)


        maker.make()

        if kwargs.get('attributes', None):
            kwargs['attributes'].remove('vrfs_list')

        # Take a copy of the object dictionary
        if not hasattr(maker, 'msdp'):
            maker.msdp = {}
        new_msdp = maker.msdp

        # List of mapped conf objects
        conf_obj_list = []

        # Main structure attributes in the conf object
        structure_keys = ['vrf_attr',
                          'peer_attr']

        # Instiantiate a PIM conf object
        conf_obj = self()

        # Pass the class method not the instnace.
        maker.dict_to_obj(conf=conf_obj,\
                          struct=structure_keys,\
                          struct_to_map=new_msdp)

        conf_obj_list.append(conf_obj)

        # List of mapped conf objects
        return conf_obj_list
