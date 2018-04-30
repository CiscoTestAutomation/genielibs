# Python
import functools
from enum import Enum

# Ats

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

# Genie Xbu_shared
import genie.libs.conf.interface
from genie.libs.conf.base.feature import consolidate_feature_args

__all__ = (
        'Vlan',
        )

# Table of contents:
#     class Vlan:
#         class DeviceAttributes:
#             class AccessMapAttributes:
#             class VlanConfigurationAttributes:
#                 def build_config/build_unconfig

 # Vlan
 #  +-- DeviceAttributes
 #      +-- VlanAttributes
 #      +-- VlanConfigAttributes


class Vlan(DeviceFeature, LinkFeature):

    @property
    def interfaces(self):
        interfaces = set()
        interfaces.update(*[link.interfaces for link in self.links])
        return frozenset(interfaces)

    def __init__(self, vlan_id=None, vlan=None, *args, **kwargs):
            if vlan_id:  # old structure
                self.vlan_id = int(vlan_id)
            if vlan:  # new structure
                self.vlan = vlan
            super().__init__(*args, **kwargs)


    vlan_id = managedattribute(
        name='vlan_id',
        default=None,
        type=managedattribute.test_istype(int),
        doc='A single-tagged VLAN')

    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Shutdown VLAN switching')

    class Media(Enum):
        enet = 'enet'
        fddi = 'fddi'

    media = managedattribute(
        name='media',
        default=None,
        type=(None, Media),
        doc='Vlan media type')

    name = managedattribute(
        name='name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Vlan name')

    are = managedattribute(
        name='are',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Maximum number of All Route Explorer hops for this VLAN')

    bridge = managedattribute(
        name='bridge',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='''Value of the bridge number for FDDI Net or
            Token Ring Net type VLANs''')

    bridge_type = managedattribute(
        name='bridge_type',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Vlan bridge type')

    stp_type = managedattribute(
        name='stp_type',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Spanning tree type of the VLAN')

    ste = managedattribute(
        name='ste',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Maximum number of Spanning Tree Explorer hops for this VLAN')

    class Status(Enum):
        ACTIVE = 'active'
        SUSPENDED = 'suspend'

    status = managedattribute(
        name='Status',
        default=None,
        type=(None, Status),
        doc='Vlan state')

    class Tpid(Enum):
        DEFAULT = 'TPID_0x8100'
        QNQ = 'TPID_0x8A88'
        ALTERANTE = 'TPID_0x9100'
        ALTERANTE2 = 'TPID_0X9200'

    tpid = managedattribute(
        name='tpid',
        default=None,
        type=(None, Tpid),
        doc='''Tag protocol identifier field (TPID)
            that is accepted on the VLAN''')

    class Backupcrf(Enum):
        enable = 'enable'
        disable = 'disable'

    backupcrf = managedattribute(
        name='backupcrf',
        default=None,
        type=(None, Backupcrf),
        doc='Backup CRF mode of the VLAN')

    parent_id = managedattribute(
        name='parent_id',
        default=None,
        type=(None, managedattribute.test_isinstance(int)),
        doc='ID number of the Parent VLAN of FDDI or Token Ring type VLANs')

    tb_vlan1 = managedattribute(
        name='tb_vlan1',
        default=None,
        type=(None, managedattribute.test_isinstance(int)),
        doc='ID number of the first translational VLAN for this VLAN')

    tb_vlan2 = managedattribute(
        name='tb_vlan2',
        default=None,
        type=(None, managedattribute.test_isinstance(int)),
        doc='ID number of the second translational VLAN for this VLAN')

    said = managedattribute(
        name='said',
        default=None,
        type=(None, managedattribute.test_isinstance(int)),
        doc='IEEE 802.10 SAID')

    ring = managedattribute(
        name='ring',
        default=None,
        type=(None, managedattribute.test_isinstance(int)),
        doc='Ring number of FDDI or Token Ring type VLANs')

    dot1q_tag_native = managedattribute(
        name='dot1q_tag_native',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Tag native vlan')

    accounting_type = managedattribute(
        name='accounting_type',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Input/Output accounting packets')

    group_name = managedattribute(
        name='group_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Vlan group name')

    configuration_id_list = managedattribute(
        name='configuration_id_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Vlan id list')

    group_id_list = managedattribute(
        name='group_id_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='List of vlans in this group')

    private_vlan_type = managedattribute(
        name='private_vlan_type',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Configure a private VLAN')

    private_vlan_association_action = managedattribute(
        name='private_vlan_association_action',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Vlan private association action, add/remove')

    private_vlan_association_ids = managedattribute(
        name='private_vlan_association_ids',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='VLAN IDs of the private VLANs to be configured')

    remote_span = managedattribute(
        name='remote_span',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Configure as Remote SPAN VLAN')

    access_map_action = managedattribute(
        name='access_map_action',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Vlan access-map action value, Drop packets/Forward packets')

    access_map_sequence = managedattribute(
        name='access_map_sequence',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Sequence to insert to/delete from existing vlan access-map entry')

    datalink_flow_monitor = managedattribute(
        name='datalink_flow_monitor',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Apply a Flow Monitor for vlan NetFlow configuration commands')

    redirect_interface = managedattribute(
        name='redirect_interface',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Redirect matched packets to the specified interface(s)')

    access_map_match = managedattribute(
        name='access_map_match',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Access-list match type, IP/IPV6/Mac')

    access_list = managedattribute(
        name='access_list',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Access-list name')

    # ============NXOS specific===========================
    egress_load_balance = managedattribute(
        name='egress_load_balance',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Load balancing on the egress interface')

    # ========================XE and NX new Structure=================
    vlan = managedattribute(
        name='vlan',
        default=None,
        type=managedattribute.test_istype(str),
        doc='A VLAN id')

    class State(Enum):
        ACTIVE = 'active'
        SUSPEND = 'suspended'
        UNSUPPORT = 'unsupport'
        SHUTDOWN = 'shutdown'

    state = managedattribute(
        name = 'state',
        default = None,
        type = (None, State),
        doc = 'Obtain vlan state')

    # ====================================================
    #  NXOS specific managed attributes for new structure
    # ====================================================

    # enabled
    enabled = managedattribute(
        name='enabled',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable feature interface-vlan and feature vn-segment-vlan-based')

    # enabled_interface_vlan
    enabled_interface_vlan = managedattribute(
        name='enabled_interface_vlan',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable feature interface-vlan')

    # enabled_vn_segment_vlan_based
    enabled_vn_segment_vlan_based = managedattribute(
        name='enabled_vn_segment_vlan_based',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='Enable feature vn-segment-vlan-based')

    vn_segment_id = managedattribute(
        name='vn_segment_id',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc='Segment id')

    class Mode(Enum):
        CE = 'ce'
        FABRICPATH = 'fabricpath'

    mode = managedattribute(
        name='mode',
        default=None,
        type=(None, Mode),
        doc='Vlan mode')

    config_vlan_id = managedattribute(
        name='config_vlan_id',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc='Configuration vlan id')

    ip_igmp_snooping = managedattribute(
        name='ip_igmp_snooping',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc='IGMP Snooping information for the vlan')

    # =============================================
    # Device attributes
    # =============================================
    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):

        @property
        def interfaces(self):
            device = self.device
            interfaces = set(self.parent.interfaces)
            interfaces = {intf for intf in interfaces if intf.device is device}
            return frozenset(interfaces)

        class AccessMapAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.access_map_id = key
                super().__init__(parent=parent)

        access_map_attr = managedattribute(
            name='access_map_attr',
            read_only=True,
            doc=AccessMapAttributes.__doc__)

        @access_map_attr.initter
        def access_map_attr(self):
            return SubAttributesDict(self.AccessMapAttributes, parent=self)

        # added for new vlan structure
        class VlanAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.vlan = key
                super().__init__(parent)

        vlan_attr = managedattribute(
            name='vlan_attr',
            read_only=True,
            doc=VlanAttributes.__doc__)

        @vlan_attr.initter
        def vlan_attr(self):
            return SubAttributesDict(self.VlanAttributes, parent=self)

        class VlanConfigAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.vlan = key
                super().__init__(parent)

        config_vlan_attr = managedattribute(
            name='config_vlan_attr',
            read_only=True,
            doc=VlanConfigAttributes.__doc__)

        @config_vlan_attr.initter
        def config_vlan_attr(self):
            return SubAttributesDict(self.VlanConfigAttributes, parent=self)

        # added for old vlan structure
        class VlanConfigurationAttributes(KeyedSubAttributes):

            def __init__(self, parent, key):
                self.vlan_configuration_id = key
                super().__init__(parent=parent)

        vlan_configuration_attr = managedattribute(
            name='vlan_configuration_attr',
            read_only=True,
            doc=VlanConfigurationAttributes.__doc__)

        @vlan_configuration_attr.initter
        def vlan_configuration_attr(self):
            return SubAttributesDict(self.VlanConfigurationAttributes,
                                     parent=self)

        class InterfaceAttributes(genie.conf.base.attributes.
                                  InterfaceSubAttributes):
            # Fix parent recursion
            @property
            def parent(self):
                return self._device_attr

            @property
            def device_name(self):
                return self._device_attr.device_name

            # Fix parent recursion
            @property
            def device(self):
                return self._device_attr.device

            def __init__(self, parent, key, **kwargs):
                self._device_attr = parent
                super().__init__(parent=None, key=key, **kwargs)

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

