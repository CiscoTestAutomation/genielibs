
__all__ = (
    'Dlb',
)

# Genie
from genie.decorator import managedattribute
from genie.conf.base.base import DeviceFeature
from genie.conf.base.attributes import DeviceSubAttributes, SubAttributesDict, AttributesHelper

# Dlb Hierarchy
# --------------
# Dlb
#     +-- DeviceAttributes
#       +- DlbAttributes
class Dlb(DeviceFeature):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ==========================================================================
    #                           CONF CLASS STRUCTURE
    # ==========================================================================

    # +- DeviceAttributes
    class DeviceAttributes(DeviceSubAttributes):
        pass

    device_attr = managedattribute(
        name="device_attr", read_only=True, doc=DeviceAttributes.__doc__
    )

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)
    # ----------------------------------------------------------------------------
    # DLB Attributes
    # ----------------------------------------------------------------------------

    # ==========================================================================
    #                           MANAGED ATTRIBUTES
    # ==========================================================================
    # mode <mode>
    mode = managedattribute(
        name='mode',
        default=None,
        type=managedattribute.test_istype(str),
        doc='DLB mode')
    
    # dlb-interface <interface_list>
    dlb_interface = managedattribute(
        name='dlb_interface',
        default=None,
        type=managedattribute.test_istype((list, str)),
        doc='List of DLB interfaces or "all" for all interfaces')

    # mac-address <mac>
    mac_address = managedattribute(
        name='mac_address',
        default=None,
        type=managedattribute.test_istype(str),
        doc='MAC address')
    # flowlet-aging <flowlet_aging>
    flowlet_aging = managedattribute(
        name='flowlet_aging',
        default=None,
        type=managedattribute.test_istype((str, int)),
        doc='Flowlet aging time in microseconds')

    # dre-thresholds <dre_thresholds>
    dre_thresholds = managedattribute(
        name='dre_thresholds',
        default=None,
        type=managedattribute.test_istype((dict, list)),
        doc='DRE thresholds - can be dict with level-X keys or list of dicts with level and percentage keys')
    # static-pinning <static_pinning>
    static_pinning = managedattribute(
        name='static_pinning',
        default=None,
        type=managedattribute.test_istype(list),
        doc="Static pinning configuration - list of dicts with 'source' and 'destination' keys")
    # decay-factor <decay_factor>
    decay_factor = managedattribute(
        name='decay_factor',
        default=None,
        type=managedattribute.test_istype(int),
        doc='Decay factor for load balancing (0-15, default 2)')
    # sampling-interval <sampling_interval>
    sampling_interval = managedattribute(
        name='sampling_interval',
        default=None,
        type=managedattribute.test_istype((int, str)),
        doc='Sampling interval in nanoseconds (512 to 16,384,000 nsecs)')
    # load-awareness <load_awareness>
    load_awareness = managedattribute(
        name='load_awareness',
        default=None,
        type=managedattribute.test_istype(bool),
        doc='Enable/disable load awareness (default True)')

    # ==========================================================================
    #                           BUILD CONFIGURATION
    # ==========================================================================
    def build_config(self, devices=None, apply=True, attributes=None, **kwargs):
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
    # ----------------------------------------------------------------------------
    # BUILD UNCONFIGURATION
    # ----------------------------------------------------------------------------
    def build_unconfig(self, devices=None, apply=True, attributes=None, **kwargs):
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
