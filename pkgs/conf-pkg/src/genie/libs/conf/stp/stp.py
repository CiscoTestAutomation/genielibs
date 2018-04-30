
__all__ = (
        'Stp',
        )

# import python
import operator

# import genie
from genie.decorator import managedattribute
from genie.conf.base.config import CliConfig
from genie.conf.base.base import DeviceFeature, InterfaceFeature
from genie.conf.base.attributes import DeviceSubAttributes,\
                                       SubAttributesDict,\
                                       AttributesHelper, \
                                       KeyedSubAttributes
# import genie.libs
from genie.conf.base.attributes import InterfaceSubAttributes


# Structure
# Stp
#  +- Device
#      +- Mode
#          +- Pvst
#          |   +- Vlan
#          |   |   +- Interface
#          |   +- Interface
#          +- Pvrstag
#          |   +- Interface
#          |       +- Vlan
#          +- Pvstag
#          |   +- Interface
#          |       +- Vlan
#          +- Mst
#          |   +- Instance
#          |       +- Interface
#          |   +- Interface
#          +- Mstag
#              +- Interface
#                  +- Instance

class Stp(DeviceFeature, InterfaceFeature):

    # callable to check regexp
    @staticmethod
    def test_isregexp(reg):
        '''Create a transformation function that allows only an object
        contained in the specified reg.

        Use with the managedattribute 'type' argument to accept only an object
        contained in the specified reg (where `value in reg`)

        Upon success, the resulting transformation function returns the value
        unchanged.

        Args:
            reg: Any reg, such as an regexp pattern ('\d+')

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_in({1, 2, 3}))

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_in(range(10)))
        '''

        msg = 'Not string like %r.' % (reg,)
        import re

        def f(value):
            if not re.search(reg, value):
                raise ValueError(msg)
            return value

        return f

    # callable to check regexp
    @staticmethod
    def test_isincrements_in_range(base, container):
        '''Create a transformation function that allows only an object
        in increments of base number, and in a range of numbers

        Args:
            base: Any integer, such as 16, 4096

        Example:

            attr = managedattribute(
                name='attr',
                type=managedattribute.test_isincrements(16))
        '''

        msg = 'Not in increments of %r.' % (base,)

        def f(value):
            if value not in container:
                raise ValueError('Not in %r.' % (container,))

            if value%base:
                raise ValueError(msg)
            return value

        return f

    # add method to managedattribute
    managedattribute.test_isregexp = test_isregexp
    managedattribute.test_isincrements_in_range = test_isincrements_in_range

    # device attributes
    bridge_assurance = managedattribute(
        name='bridge_assurance',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    etherchannel_misconfig_guard = managedattribute(
        name='etherchannel_misconfig_guard',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    bpduguard_timeout_recovery = managedattribute(
        name='bpduguard_timeout_recovery',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    loop_guard = managedattribute(
        name='loop_guard',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    bpdu_guard = managedattribute(
        name='bpdu_guard',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    bpdu_filter = managedattribute(
        name='bpdu_filter',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    hold_count = managedattribute(
        name='hold_count',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # mode mst attributes
    mst_domain = managedattribute(
        name='mst_domain',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    m_max_hop = managedattribute(
        name='m_max_hop',
        default=None,
        type=(None, managedattribute.test_in(range(1, 256))))

    m_hello_time = managedattribute(
        name='m_hello_time',
        default=None,
        type=(None, managedattribute.test_in(range(1, 11))))

    m_max_age = managedattribute(
        name='m_max_age',
        default=None,
        type=(None, managedattribute.test_in(range(6, 41))))

    m_forwarding_delay = managedattribute(
        name='m_forwarding_delay',
        default=None,
        type=(None, managedattribute.test_in(range(4, 31))))

    mst_id = managedattribute(
        name='mst_id',
        default=None,
        type=(None, managedattribute.test_istype(int)))
    
    m_vlans = managedattribute(
        name='m_vlans',
        default=None,
        type=(None, managedattribute.test_istype(str)))
    
    m_name = managedattribute(
        name='m_name',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    m_revision = managedattribute(
        name='m_revision',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    m_bridge_priority = managedattribute(
        name='m_bridge_priority',
        default=None,
        type=(None, managedattribute.test_isincrements_in_range(
                        base=4096, container=range(0, 61441))))

    m_inst_if_cost = managedattribute(
        name='m_inst_if_cost',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    m_inst_if_port_priority = managedattribute(
        name='m_inst_if_port_priority',
        default=None,
        type=(None, managedattribute.test_isincrements_in_range(
                        base=16, container=range(0, 241))))
    
    m_if_edge_port = managedattribute(
        name='m_if_edge_port',
        default=None,
        type=(None, managedattribute.test_in(['edge_enable','edge_disable','edge_auto'])))
    
    m_if_link_type = managedattribute(
        name='m_if_link_type',
        default=None,
        type=(None, managedattribute.test_in(['p2p','shared','auto'])))
    
    m_if_guard = managedattribute(
        name='m_if_guard',
        default=None,
        type=(None, managedattribute.test_in(['root','loop', 'none'])))

    m_if_bpdu_guard = managedattribute(
        name='m_if_bpdu_guard',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    m_if_bpdu_filter = managedattribute(
        name='m_if_bpdu_filter',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    m_if_hello_time = managedattribute(
        name='m_if_hello_time',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # mode mstag attributes
    mag_domain = managedattribute(
        name='mag_domain',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    mag_if_name = managedattribute(
        name='mag_if_name',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    mag_if_revision = managedattribute(
        name='mag_if_revision',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    mag_if_bridge_id = managedattribute(
        name='mag_if_bridge_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))
    
    mag_id = managedattribute(
        name='mag_id',
        default=None,
        type=(None, managedattribute.test_in(range(0, 4095))))

    mag_if_root_id = managedattribute(
        name='mag_if_root_id',
        default=None,
        type=(None, managedattribute.test_isregexp('\w+\.\w+\.\w+')))
    
    mag_if_vlans = managedattribute(
        name='mag_if_vlans',
        default=None,
        type=(None, managedattribute.test_istype(str)))
    
    mag_if_priority = managedattribute(
        name='mag_if_priority',
        default=None,
        type=(None, managedattribute.test_in(range(0, 61441))))

    mag_if_root_priority = managedattribute(
        name='mag_if_root_priority',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    # attribtues for pvst mode
    pvst_id = managedattribute(
        name='pvst_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    p_max_age = managedattribute(
        name='p_max_age',
        default=None,
        type=(None, managedattribute.test_in(range(6, 41))))

    p_hold_count = managedattribute(
        name='p_hold_count',
        default=None,
        type=(None, managedattribute.test_in(range(1, 11))))

    p_forwarding_delay = managedattribute(
        name='p_forwarding_delay',
        default=None,
        type=(None, managedattribute.test_in(range(4, 31))))

    vlan_id = managedattribute(
        name='vlan_id',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    v_hello_time = managedattribute(
        name='v_hello_time',
        default=None,
        type=(None, managedattribute.test_in(range(1, 11))))

    v_max_age = managedattribute(
        name='v_max_age',
        default=None,
        type=(None, managedattribute.test_in(range(6, 41))))

    v_forwarding_delay = managedattribute(
        name='v_forwarding_delay',
        default=None,
        type=(None, managedattribute.test_in(range(4, 31))))

    v_bridge_priority = managedattribute(
        name='v_bridge_priority',
        default=None,
        type=(None, managedattribute.test_isincrements_in_range(
                        base=4096, container=range(0, 61441))))

    v_interface = managedattribute(
        name='v_interface',
        default=None,
        type=(None, managedattribute.test_istype(str)))
    
    v_if_cost = managedattribute(
        name='v_if_cost',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    v_if_port_priority = managedattribute(
        name='v_if_port_priority',
        default=None,
        type=(None, managedattribute.test_isincrements_in_range(
                        base=16, container=range(0, 241))))

    p_if_edge_port = managedattribute(
        name='p_if_edge_port',
        default=None,
        type=(None, managedattribute.test_in(['edge_enable','edge_disable','edge_auto'])))

    p_if_link_type = managedattribute(
        name='p_if_link_type',
        default=None,
        type=(None, managedattribute.test_in(['p2p','shared','auto'])))

    p_if_guard = managedattribute(
        name='p_if_guard',
        default=None,
        type=(None, managedattribute.test_in(['root','loop','none'])))

    p_if_bpdu_guard = managedattribute(
        name='p_if_bpdu_guard',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    p_if_bpdu_filter = managedattribute(
        name='p_if_bpdu_filter',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    p_if_hello_time = managedattribute(
        name='p_if_hello_time',
        default=None,
        type=(None, managedattribute.test_in([1, 2])))

    # attributes for mode pvrstag
    prag_domain = managedattribute(
        name='prag_domain',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    prag_if_v_root_priority = managedattribute(
        name='prag_if_v_root_priority',
        default=None,
        type=(None, managedattribute.test_in(range(0, 61441))))

    prag_if_v_root_id = managedattribute(
        name='prag_if_v_root_id',
        default=None,
        type=(None, managedattribute.test_isregexp('\w+\.\w+\.\w+')))
    
    prag_if_v_root_cost = managedattribute(
        name='prag_if_v_root_cost',
        default=None,
        type=(None, managedattribute.test_in(range(0, 4294967296))))
    
    prag_if_v_priority = managedattribute(
        name='prag_if_v_priority',
        default=None,
        type=(None, managedattribute.test_in(range(0, 61441))))

    prag_if_v_bridge_id = managedattribute(
        name='prag_if_v_bridge_id',
        default=None,
        type=(None, managedattribute.test_isregexp('\w+\.\w+\.\w+')))

    prag_if_v_port_priority = managedattribute(
        name='prag_if_v_port_priority',
        default=None,
        type=(None, managedattribute.test_in(range(0, 241))))

    prag_if_v_max_age = managedattribute(
        name='prag_if_v_max_age',
        default=None,
        type=(None, managedattribute.test_in(range(6, 41))))

    prag_if_v_hello_time = managedattribute(
        name='prag_if_v_hello_time',
        default=None,
        type=(None, managedattribute.test_in([1,2])))

    # attributes for mode pvstag
    pag_domain = managedattribute(
        name='pag_domain',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    pag_if_v_root_priority = managedattribute(
        name='pag_if_v_root_priority',
        default=None,
        type=(None, managedattribute.test_in(range(0, 65536))))

    pag_if_v_root_id = managedattribute(
        name='pag_if_v_root_id',
        default=None,
        type=(None, managedattribute.test_isregexp('\w+\.\w+\.\w+')))
    
    pag_if_v_root_cost = managedattribute(
        name='pag_if_v_root_cost',
        default=None,
        type=(None, managedattribute.test_in(range(0, 4294967296))))
    
    pag_if_v_priority = managedattribute(
        name='pag_if_v_priority',
        default=None,
        type=(None, managedattribute.test_in(range(0, 65536))))

    pag_if_v_bridge_id = managedattribute(
        name='pag_if_v_bridge_id',
        default=None,
        type=(None, managedattribute.test_isregexp('\w+\.\w+\.\w+')))

    pag_if_v_port_priority = managedattribute(
        name='pag_if_v_port_priority',
        default=None,
        type=(None, managedattribute.test_in(range(0, 256))))

    pag_if_v_max_age = managedattribute(
        name='pag_if_v_max_age',
        default=None,
        type=(None, managedattribute.test_in(range(6, 41))))

    pag_if_v_hello_time = managedattribute(
        name='pag_if_v_hello_time',
        default=None,
        type=(None, managedattribute.test_in([1,2])))


    class DeviceAttributes(DeviceSubAttributes):

        class ModeAttributes(KeyedSubAttributes):
            def __init__(self, parent, key):
                self.mode = key
                super().__init__(parent)

            mode = property(operator.attrgetter('_mode'))

            @mode.setter
            def mode(self, d):
                assert d in ['mstp', 'mstag', 'pvst', 'rapid-pvst', 'pvrstag', 'pvstag'], \
                    "should be 'mstp', 'mstag', 'pvst', 'rapid-pvst', 'pvrstag', 'pvstag' "
                self._mode = d

            # ---------------
            #    mode MST
            # ---------------
            class MstAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.mst_domain = key
                    super().__init__(parent)

                # +- Mst
                # |   +- Interface
                class InterfaceAttributes(InterfaceSubAttributes):
                    pass

                interface_attr = managedattribute(
                    name='interface_attr',
                    read_only=True,
                    doc=InterfaceAttributes.__doc__)

                @interface_attr.initter
                def interface_attr(self):
                    return SubAttributesDict(self.InterfaceAttributes, parent=self)

                # +- Mst
                # |   +- Instance
                # |       +- Interface
                class InstanceAttributes(KeyedSubAttributes):
                    def __init__(self, parent, key):
                        self.mst_id = key
                        super().__init__(parent)

                    class InterfaceAttributes(InterfaceSubAttributes):
                        pass

                    interface_attr = managedattribute(
                        name='interface_attr',
                        read_only=True,
                        doc=InterfaceAttributes.__doc__)

                    @interface_attr.initter
                    def interface_attr(self):
                        return SubAttributesDict(self.InterfaceAttributes, parent=self)

                instance_attr = managedattribute(
                    name='instance_attr',
                    read_only=True,
                    doc=InstanceAttributes.__doc__)

                @instance_attr.initter
                def instance_attr(self):
                    return SubAttributesDict(self.InstanceAttributes, parent=self)

            mst_attr = managedattribute(
                name='mst_attr',
                read_only=True,
                doc=MstAttributes.__doc__)

            @mst_attr.initter
            def mst_attr(self):
                return SubAttributesDict(self.MstAttributes, parent=self)

            # ---------------
            #    mode Mstag
            # ---------------
            class MstagAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.mag_domain = key
                    super().__init__(parent)

                # +- Mstag
                # |   +- Interface
                # |       +- Instance
                class InterfaceAttributes(InterfaceSubAttributes):

                    class InstanceAttributes(KeyedSubAttributes):
                        def __init__(self, parent, key):
                            self.mag_id = key
                            super().__init__(parent)

                    instance_attr = managedattribute(
                        name='instance_attr',
                        read_only=True,
                        doc=InstanceAttributes.__doc__)

                    @instance_attr.initter
                    def instance_attr(self):
                        return SubAttributesDict(self.InstanceAttributes, parent=self)

                interface_attr = managedattribute(
                    name='interface_attr',
                    read_only=True,
                    doc=InterfaceAttributes.__doc__)

                @interface_attr.initter
                def interface_attr(self):
                    return SubAttributesDict(self.InterfaceAttributes, parent=self)

            mstag_attr = managedattribute(
                name='mstag_attr',
                read_only=True,
                doc=MstagAttributes.__doc__)

            @mstag_attr.initter
            def mstag_attr(self):
                return SubAttributesDict(self.MstagAttributes, parent=self)


            # ---------------
            #    mode Pvst
            # ---------------
            class PvstAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.pvst_id = key
                    super().__init__(parent)

                # +- Pvst
                # |   +- Interface
                class InterfaceAttributes(InterfaceSubAttributes):
                    pass

                interface_attr = managedattribute(
                    name='interface_attr',
                    read_only=True,
                    doc=InterfaceAttributes.__doc__)

                @interface_attr.initter
                def interface_attr(self):
                    return SubAttributesDict(self.InterfaceAttributes, parent=self)

                # +- Pvst
                # |   +- Vlan
                # |       +- Interface
                class VlanAttributes(KeyedSubAttributes):
                    def __init__(self, parent, key):
                        self.vlan = key
                        super().__init__(parent)

                    class InterfaceAttributes(InterfaceSubAttributes):
                        pass

                    interface_attr = managedattribute(
                        name='interface_attr',
                        read_only=True,
                        doc=InterfaceAttributes.__doc__)

                    @interface_attr.initter
                    def interface_attr(self):
                        return SubAttributesDict(self.InterfaceAttributes, parent=self)

                vlan_attr = managedattribute(
                    name='vlan_attr',
                    read_only=True,
                    doc=VlanAttributes.__doc__)

                @vlan_attr.initter
                def vlan_attr(self):
                    return SubAttributesDict(self.VlanAttributes, parent=self)

            pvst_attr = managedattribute(
                name='pvst_attr',
                read_only=True,
                doc=PvstAttributes.__doc__)

            @pvst_attr.initter
            def pvst_attr(self):
                return SubAttributesDict(self.PvstAttributes, parent=self)


            # ---------------
            #    mode Pvrstag
            # ---------------
            class PvrstagAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.prag_domain = key
                    super().__init__(parent)

                # +- Pvrstag
                # |   +- Interface
                # |       +- Vlan
                class InterfaceAttributes(InterfaceSubAttributes):
                    
                    class VlanAttributes(KeyedSubAttributes):
                        def __init__(self, parent, key):
                            self.prag_vlan = key
                            super().__init__(parent)

                    vlan_attr = managedattribute(
                        name='vlan_attr',
                        read_only=True,
                        doc=VlanAttributes.__doc__)

                    @vlan_attr.initter
                    def vlan_attr(self):
                        return SubAttributesDict(self.VlanAttributes, parent=self)

                interface_attr = managedattribute(
                    name='interface_attr',
                    read_only=True,
                    doc=InterfaceAttributes.__doc__)

                @interface_attr.initter
                def interface_attr(self):
                    return SubAttributesDict(self.InterfaceAttributes, parent=self)

            pvrstag_attr = managedattribute(
                name='pvrstag_attr',
                read_only=True,
                doc=PvrstagAttributes.__doc__)

            @pvrstag_attr.initter
            def pvrstag_attr(self):
                return SubAttributesDict(self.PvrstagAttributes, parent=self)

            # ---------------
            #    mode Pvstag
            # ---------------
            class PvstagAttributes(PvrstagAttributes):
                def __init__(self, parent, key):
                    self.pag_domain = key
                    super().__init__(parent)

                # +- Pvstag
                # |   +- Interface
                # |       +- Vlan

            pvstag_attr = managedattribute(
                name='pvstag_attr',
                read_only=True,
                doc=PvrstagAttributes.__doc__)

            @pvstag_attr.initter
            def pvstag_attr(self):
                return SubAttributesDict(self.PvstagAttributes, parent=self)


        mode_attr = managedattribute(
            name='mode_attr',
            read_only=True,
            doc=ModeAttributes.__doc__)

        @mode_attr.initter
        def mode_attr(self):
            return SubAttributesDict(self.ModeAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
