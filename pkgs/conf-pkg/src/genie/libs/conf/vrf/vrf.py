
__all__ = (
    'Vrf',
    'VrfSubAttributes',
)

# python
import re
import functools
from enum import Enum
from enum import Enum
from genie.libs import parser
from genie.abstract import Lookup
# ats
from pyats.datastructures import WeakList

# genie
from genie.utils.cisco_collections import typedset
from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature, Interface
from genie.conf.base.attributes import DeviceSubAttributes,\
                                       SubAttributesDict,\
                                       AttributesHelper, \
                                       KeyedSubAttributes

# genie.libs
from genie.libs.conf.address_family import AddressFamily,\
                                           AddressFamilySubAttributes
from genie.libs.conf.base import RouteDistinguisher, RouteTarget
from genie.libs.conf.route_policy import RoutePolicy
from .vpn_id import VpnId

from genie.ops.base import Base as ops_Base
from genie.ops.base import Context

class VrfSubAttributes(KeyedSubAttributes):

    vrf_name = managedattribute(
        name='vrf_name',
        read_only=True)  # key

    @property
    def vrf(self):
        vrf_name = self.vrf_name
        if vrf_name == 'default':
            return None
        testbed = self.testbed
        for vrf in testbed.object_instances(cls=Vrf):
            if vrf.name == vrf_name:
                return vrf
        raise AttributeError('No Vrf instance found with name %r' % (vrf_name,))

    def __init__(self, parent, key):
        self._vrf_name = key
        super().__init__(parent=parent)

    @classmethod
    def _sort_key(cls, key):
        # key = cls._sanitize_key(key)
        return (
            (0 if key == 'default' else 1),
            key)

    @classmethod
    def _sanitize_key(cls, key):
        if key is None:
            # allow indexing with a vrf=None
            key = 'default'
        elif isinstance(key, Vrf):
            key = getattr(key, 'name', key)
        return key

    @classmethod
    def _assert_key_allowed(cls, key):
        if not isinstance(key, str):
            raise KeyError(
                '{cls} only accepts Vrf instances and Vrf names, not {key!r}'.
                format(cls=cls.__name__, key=key))
        allowed_keys = getattr(cls, 'allowed_keys', None)
        if allowed_keys is not None:
            if key not in allowed_keys:
                raise KeyError(
                    '{cls} only accepts {allowed_keys}, not {key!r}'.\
                    format(cls=cls.__name__,
                           allowed_keys=allowed_keys,
                           key=key))

    @property
    def interfaces(self):
        vrf_name = self.vrf_name
        for interface in self.parent.interfaces:
            if (interface.vrf.name if interface.vrf else 'default') == \
                    vrf_name:
                yield interface


@functools.total_ordering
class Vrf(DeviceFeature):

    vnis = managedattribute(
        name='vnis',
        #finit=typedset(managedattribute.test_isinstance(Evi)).copy,  # circular dependency!
        #type=typedset(managedattribute.test_isinstance(Evi))._from_iterable)  # circular dependency!
        doc='A `set` of Evi associated objects')

    @vnis.initter
    def vnis(self):
        from genie.libs.conf.evpn import Vni
        return typedset(managedattribute.test_isinstance(Vni))

    @vnis.setter
    def vnis(self, value):
        from genie.libs.conf.evpn import Vni
        self._vnis = typedset(managedattribute.test_isinstance(Vni), value)

    @property
    def interfaces(self):
        return frozenset([interface
                          for interface in self.testbed.interfaces
                          if interface.vrf is self])

    name = managedattribute(
        name='name',
        read_only=True)  # read-only hash key

    description = managedattribute(
        name='description',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    amt_flush_routes = managedattribute(
        name='amt_flush_routes',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    amt_pseudo_interface = managedattribute(
        name='amt_pseudo_interface',
        default=None,
        type=(None, managedattribute.test_isinstance(Interface)))

    fallback_vrf = managedattribute(
        name='fallback_vrf',
        default=None,
        # Self-reference; Done after: type=(None, managedattribute.test_isinstance(Vrf))
    )

    mhost_ipv4_default_interface = managedattribute(
        name='mhost_ipv4_default_interface',
        default=None,
        type=(None, managedattribute.test_isinstance(Interface)))

    mhost_ipv6_default_interface = managedattribute(
        name='mhost_ipv6_default_interface',
        default=None,
        type=(None, managedattribute.test_isinstance(Interface)))

    scale_mode = managedattribute(
        name='scale_mode',
        default=None,
        type=(None, managedattribute.test_in((
            'big',
        ))))

    remote_route_filtering = managedattribute(
        name='remote_route_filtering',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    vpn_id = managedattribute(
        name='vpn_id',
        default=None,
        type=(None, managedattribute.test_isinstance(VpnId)))

    rd = managedattribute(
        name='rd',
        default=None,
        type=(None, RouteDistinguisher,
              managedattribute.test_in((
                  'auto',
              ))))

    address_families = managedattribute(
        name='address_families',
        finit=typedset(AddressFamily, {AddressFamily.ipv4_unicast}).copy,
        type=typedset(AddressFamily)._from_iterable)

    export_route_policy = managedattribute(
        name='export_route_policy',
        default=None,
        type=(None,
              managedattribute.test_istype(RoutePolicy)))

    export_route_targets = managedattribute(
        name='export_route_targets',
        finit=typedset(RouteTarget.ImportExport).copy,
        type=typedset(RouteTarget.ImportExport)._from_iterable)

    export_to_default_vrf_route_policy = managedattribute(
        name='export_to_default_vrf_route_policy',
        default=None,
        type=(None,
              managedattribute.test_istype(RoutePolicy)))

    export_to_vrf_allow_imported_vpn = managedattribute(
        name='export_to_vrf_allow_imported_vpn',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    export_to_vrf_import_stitching_rt = managedattribute(
        name='export_to_vrf_import_stitching_rt',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    import_from_default_vrf_route_policy = managedattribute(
        name='import_from_default_vrf_route_policy',
        default=None,
        type=(None,
              managedattribute.test_istype(RoutePolicy)))

    import_from_default_vrf_route_policy_maximum_prefixes = managedattribute(
        name='import_from_default_vrf_route_policy_maximum_prefixes',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    import_from_default_vrf_advertise_as_vpn = managedattribute(
        name='import_from_default_vrf_advertise_as_vpn',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    import_route_policy = managedattribute(
        name='import_route_policy',
        default=None,
        type=(None,
              managedattribute.test_istype(RoutePolicy)))

    import_route_targets = managedattribute(
        name='import_route_targets',
        finit=typedset(RouteTarget.ImportExport).copy,
        type=typedset(RouteTarget.ImportExport)._from_iterable)

    maximum_prefix = managedattribute(
        name='maximum_prefix',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    maximum_prefix_threshold = managedattribute(
        name='maximum_prefix_threshold',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    maximum_prefix_reinstall_threshold = managedattribute(
        name='maximum_prefix_reinstall_threshold',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    maximum_prefix_warning_only = managedattribute(
        name='maximum_prefix_warning_only',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    import_from_global_map = managedattribute(
        name='import_from_global_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    export_to_global_map = managedattribute(
        name='export_to_global_map',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    routing_table_limit_number = managedattribute(
        name='routing_table_limit_number',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    alert_percent_value = managedattribute(
        name='alert_percent_value',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    simple_alert = managedattribute(
        name='simple_alert',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    class RTTYPE(Enum):
        type1 = 'import'
        type2 = 'export'
        type3 = 'both'

    rt_type = managedattribute(
        name='rt_type',
        default=None,
        type=(None, RTTYPE),
        doc='import export or both')

    rt_mvpn = managedattribute(
        name='rt_mvpn',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    rt_evpn = managedattribute(
        name='rt_evpn',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    class PROTOCOL(Enum):
        type1 = 'mvpn'
        type2 = 'evpn'

    protocol = managedattribute(
        name='protocol',
        default=None,
        type=(None, PROTOCOL),
        doc='set mvpn or evpn ')

    vni = managedattribute(
        name='vni',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    vni_mode_l3 = managedattribute(
        name='vni_mode_l3',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    class DeviceAttributes(DeviceSubAttributes):

        @property
        def vnis(self):
            device = self.device
            return frozenset([vni
                              for vni in self.parent.vnis
                              if vni.device is device])

        @property
        def interfaces(self):
            device = self.device
            return frozenset([interface
                              for interface in self.parent.interfaces
                              if interface.device is device])

        export_route_targets = managedattribute(
            name='export_route_targets',
            type=typedset(RouteTarget.ImportExport)._from_iterable)

        @export_route_targets.defaulter
        def export_route_targets(self):
            return frozenset(self.parent.export_route_targets)

        import_route_targets = managedattribute(
            name='import_route_targets',
            type=typedset(RouteTarget.ImportExport)._from_iterable)

        @import_route_targets.defaulter
        def import_route_targets(self):
            return frozenset(self.parent.import_route_targets)

        address_families = managedattribute(
            name='address_families',
            type=typedset(AddressFamily)._from_iterable)

        @address_families.defaulter
        def address_families(self):
            return frozenset(self.parent.address_families)

        class AddressFamilyAttributes(AddressFamilySubAttributes):

            class RouteTargetAttributes(KeyedSubAttributes):

                def __init__(self, parent, key):
                    self.rt = key
                    super().__init__(parent)

                # ProtocolAttribute
                class ProtocolAttributes(KeyedSubAttributes):
                    def __init__(self, key, *args, **kwargs):
                        self.protocol = key
                        super().__init__(*args, **kwargs)

                protocol_attr = managedattribute(
                    name='protocol_attr',
                    read_only=True,
                    doc=ProtocolAttributes.__doc__)

                @protocol_attr.initter
                def protocol_attr(self):
                    return SubAttributesDict(self.ProtocolAttributes, parent=self)

            route_target_attr = managedattribute(
                name='route_target_attr',
                read_only=True,
                doc=RouteTargetAttributes.__doc__)

            @route_target_attr.initter
            def route_target_attr(self):
                return SubAttributesDict(self.RouteTargetAttributes, parent=self)

        def __init__(self, *args, **kwargs):
            self.address_family_attr = SubAttributesDict(
                self.AddressFamilyAttributes, parent=self)
            super().__init__(*args, **kwargs)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, name, *args, **kwargs):
        assert isinstance(name, str)
        self._name = name
        super().__init__(*args, **kwargs)

    def __eq__(self, other):
        if not isinstance(other, Vrf):
            return NotImplemented
        return (self.name, self.testbed) \
            == (other.name, other.testbed)

    def __lt__(self, other):
        if not isinstance(other, Vrf):
            return NotImplemented
        return (self.name, self.testbed) \
            < (other.name, other.testbed)

    def __hash__(self):
        return hash(self.name)

    def build_config(self, devices=None, apply=True,
                     attributes=None, **kwargs):
        cfgs = {}
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)

        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr', keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)

        cfgs = {key: value for key, value in cfgs.items() if value}
        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True,
                       attributes=None, **kwargs):
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

        cfgs = {key: value for key, value in cfgs.items() if value}
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

        # Abstracting the show running vrf as per device os
        ret = Lookup.from_device(device)
        cmd = ret.parser.show_vrf.ShowRunningConfigVrf
        maker = ops_Base(device=device)

        maker.add_leaf(cmd=cmd,
                       src='[vrf][(?P<vrf>.*)][rd]',
                       dest='vrf[vrf][(?P<vrf>.*)][rd]')
        maker.add_leaf(cmd=cmd,
                       src='[vrf][(?P<vrf>.*)]'
                           '[vni]',
                       dest='vrf[vrf][(?P<vrf>.*)]'
                            '[vni]')
        maker.add_leaf(cmd=cmd,
                       src='[vrf][(?P<vrf>.*)]'
                           '[vni_mode_l3] l3',
                       dest='vrf[vrf][(?P<vrf>.*)]'
                            '[vni_mode_l3] l3')
        maker.add_leaf(cmd=cmd,
                       src='[vrf][(?P<vrf>.*)]'
                           '[vrf_name]',
                       dest='vrf[vrf][(?P<vrf>.*)]'
                            '[vrf_name]')
        maker.add_leaf(cmd=cmd,
                       src='[vrf][(?P<vrf>.*)][address_family]'
                           '[(?P<af_name>.*)]',
                       dest='vrf[vrf][(?P<vrf>.*)][address_family_attr]'
                            '[(?P<af_name>.*)]')

        maker.add_leaf(cmd=cmd,
                       src='[vrf][(?P<vrf>.*)][address_family]'
                           '[(?P<af_name>.*)][route_target][(?P<rt>.*)][rt_type]',
                       dest='vrf[vrf][(?P<vrf>.*)][address_family_attr]'
                            '[(?P<af_name>.*)][route_target_attr][(?P<rt>.*)]'
                            '[rt_type]')

        maker.add_leaf(cmd=cmd,
                       src='[vrf][(?P<vrf>.*)][address_family]'
                           '[(?P<af_name>.*)][route_target][(?P<rt>.*)]'
                           '[protocol][(?P<protocol>.*)]',
                       dest='vrf[vrf][(?P<vrf>.*)][address_family_attr]'
                            '[(?P<af_name>.*)][route_target_attr][(?P<rt>.*)]'
                            '[protocol_attr][(?P<protocol>.*)]')

        # A workaround to pass the context as in maker it expects Context.cli
        # not just a string 'cli.
        maker.context_manager[cmd] = Context.cli

        maker.make()
        # Take a copy of the object dictionary
        if not hasattr(maker, 'vrf'):
            maker.vrf= {}
        new_vrf = maker.vrf

        # List of mapped conf objects
        conf_obj_list = []

        # Main structure attributes in the conf object
        structure_keys = ['address_family_attr',
                          'route_target_attr',
                          'protocol_attr']
        if len(new_vrf):
            for vrf in new_vrf['vrf'].keys():
                if 'address_family_attr' in new_vrf['vrf'][vrf]:
                    for af_name in new_vrf['vrf'][vrf]['address_family_attr'].keys():
                        if 'route_target' in new_vrf['vrf'][vrf]['address_family_attr'][af_name]:
                            del new_vrf['vrf'][vrf]['address_family_attr'][af_name]['route_target']

            for i in list(new_vrf['vrf']):
                if 'address_family_attr' not in new_vrf['vrf'][i]:
                    new_vrf['vrf'].pop(i)



            for vrf in new_vrf['vrf'].keys():
                conf_obj = self(name=vrf)
                # Pass the class method not the instnace.
                maker.dict_to_obj(conf=conf_obj, \
                                  struct=structure_keys, \
                                  struct_to_map=new_vrf['vrf'][vrf])

                conf_obj_list.append(conf_obj)

        # List of mapped conf objects
        return conf_obj_list


Vrf.fallback_vrf = Vrf.fallback_vrf.copy(
    type=(None, managedattribute.test_isinstance(Vrf)))

