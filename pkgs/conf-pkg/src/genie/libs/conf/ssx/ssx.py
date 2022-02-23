__all__ = (
    'ssx',
)

# genie
from genie.decorator import managedattribute
from genie.conf.base.base import DeviceFeature, InterfaceFeature

# genie.libs
from genie.conf.base.attributes import DeviceSubAttributes, \
    SubAttributesDict,\
    AttributesHelper, \
    KeyedSubAttributes

# Structure Hierarchy:
# ssx
# +- DeviceAttributes
#     +- HardwareTelemetryAttributes   
#         +- ExporterAttributes
#         +- RecordAttributes
#         +- MonitorAttributes
#
class Ssx(DeviceFeature):

    # feature hardware-telemetry
    enable_hardware_telemetry = managedattribute(
        name='enable_hardware_telemetry',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable feature hardware-telemetry.")

    # hardware-telemetry ssx
    enable_hardware_telemetry_ssx = managedattribute(
        name='enable_hardware_telemetry_ssx',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Enable hardware-telemetry ssx")

    # apply ssx monitor at system
    ssx_system_monitor = managedattribute(
        name='ssx_system_monitor',
        default=None,
        type=(None, managedattribute.test_istype(list)),
        doc="system monitor.")

    # ssx system id
    ssx_id = managedattribute(
        name='ssx_id',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="ssx id.")

    exp_name = managedattribute(
        name='exp_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="exporter name.")

    rec_name = managedattribute(
        name='rec_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="recorder name.")

    mon_name = managedattribute(
        name='mon_name',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="monitor name.")

    exp_id = managedattribute(
        name='exp_id',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="exporter instance id.")

    rec_id = managedattribute(
        name='rec_id',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="recorder instance id.")

    mon_id = managedattribute(
        name='mon_id',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="monitor instance id.")

    source_ip = managedattribute(
        name='source_ip',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="exporter source ip.")

    dest_ip = managedattribute(
        name='dest_ip',
        default=None,
        type=(None, managedattribute.test_istype(str)),
        doc="exporter destination ip.")

    source_port = managedattribute(
        name='source_port',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="exporter source port number.")

    dest_port = managedattribute(
        name='dest_port',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="exporter destination port number.")

    dscp = managedattribute(
        name='dscp',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="Differentiated Services Code Point value..")

    egress_queue_drops = managedattribute(
        name='egress_queue_drops',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Tail drops per output queue.")

    egress_queue_peak = managedattribute(
        name='egress_queue_peak',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Buffer peak counters per output queue.")

    egress_queue_depth = managedattribute(
        name='egress_queue_depth',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Instant buffer utilization per output queue.")

    ingress_queue_drops = managedattribute(
        name='ingress_queue_drops',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Overflow drops per input queue.")

    ingress_queue_depth = managedattribute(
        name='ingress_queue_depth',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Instant buffer utilization per input queue.")

    egress_queue_microburst = managedattribute(
        name='egress_queue_microburst',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Microburst records.")

    ethernet_counters = managedattribute(
        name='ethernet_counters',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="RMON counters per MAC channel.")

    egress_pool_group_depth = managedattribute(
        name='egress_pool_group_depth',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Streams the buffer occupancy per pool group.")

    egress_buffer_depth = managedattribute(
        name='egress_buffer_depth',
        default=None,
        type=(None, managedattribute.test_istype(bool)),
        doc="Streams the buffer occupancy per slice.")

    record_interval = managedattribute(
        name='record_interval',
        default=None,
        type=(None, managedattribute.test_istype(int)),
        doc="record interval milliseconds.")

    
    class DeviceAttributes(DeviceSubAttributes):

        class HardwareTelemetryAttributes(KeyedSubAttributes): 
            def __init__(self, parent, key):
                super().__init__(parent=parent)  

            # Exporter
            class ExporterAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.exp_id = key
                    super().__init__(parent=parent)

            exporter_attr = managedattribute(
                name='exporter_attr',
                read_only=True,
                doc=ExporterAttributes.__doc__)

            @exporter_attr.initter
            def exporter_attr(self):
                return SubAttributesDict(self.ExporterAttributes, parent=self)

            # Record
            class RecordAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.rec_id = key
                    super().__init__(parent=parent)

            record_attr = managedattribute(
                name='record_attr',
                read_only=True,
                doc=RecordAttributes.__doc__)

            @record_attr.initter
            def record_attr(self):
                return SubAttributesDict(self.RecordAttributes, parent=self)

            # Monitor
            class MonitorAttributes(KeyedSubAttributes):
                def __init__(self, parent, key):
                    self.mon_id = key
                    super().__init__(parent=parent)

            monitor_attr = managedattribute(
                name='monitor_attr',
                read_only=True,
                doc=MonitorAttributes.__doc__)

            @monitor_attr.initter
            def monitor_attr(self):
                return SubAttributesDict(self.MonitorAttributes, parent=self)

        hwtele_attr = managedattribute(
            name='hwtele_attr',
            read_only=True,
            doc=HardwareTelemetryAttributes.__doc__)

        @hwtele_attr.initter
        def hwtele_attr(self):
            return SubAttributesDict(self.HardwareTelemetryAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def build_config(self, devices=None, apply=True, attributes=None):
        cfgs = {}
        attributes = AttributesHelper(self, attributes)
        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr', 
                keys=devices, sort=True):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2)
            
        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs

    def build_unconfig(self, devices=None, apply=True, attributes=None):
        cfgs = {}
        attributes = AttributesHelper(self, attributes)
        if devices is None:
            devices = self.devices
        devices = set(devices)

        for key, sub, attributes2 in attributes.mapping_items(
                'device_attr', sort=True):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2)

        if apply:
            for device_name, cfg in sorted(cfgs.items()):
                self.testbed.config_on_devices(cfg, fail_invalid=True)
        else:
            return cfgs
