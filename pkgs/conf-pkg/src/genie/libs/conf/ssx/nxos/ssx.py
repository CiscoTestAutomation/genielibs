'''
NXOS specific configurations for SSX feature object.
'''

# Python
from abc import ABC

# Genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper

# Structure Hierarchy:
# ssx
# +- DeviceAttributes
#     +- HardwareTelemetryAttributes
#         +- ExporterAttributes
#         +- RecordAttributes
#         +- MonitorAttributes
#


class Ssx(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # featue hardware-telemetry
            if attributes.value('enable_hardware_telemetry'):
                if unconfig is False:
                    configurations.append_line(
                        attributes.format('feature hardware-telemetry'))

            # Make sure that only enabled was provided in attributes
                # If wildcard,  then delete everything
                elif unconfig and\
                    attributes.attributes == {'enable_hardware_telemetry': {True: None}} or \
                        attributes.iswildcard:
                    configurations.append_line(
                        'no feature hardware-telemetry', raw=True)
                    if apply:
                        if configurations:
                            self.device.configure(configurations)
                    else:
                        return CliConfig(device=self.device, unconfig=unconfig,
                                         cli_config=configurations)

            # +- DeviceAttributes
            #     +- SsxAttributes
            for sub, attributes2 in attributes.mapping_values('hwtele_attr',
                                                              sort=True, keys=self.hwtele_attr):
                configurations.append_block(
                    sub.build_config(apply=False,
                                     attributes=attributes2,
                                     unconfig=unconfig))

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

        class HardwareTelemetryAttributes(ABC):

            def build_config(self, apply=True, attributes=None, unconfig=False,
                             **kwargs):
                assert not kwargs, kwargs
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # hardware-telemetry ssx
                with configurations.submode_context(attributes.format(
                        'hardware-telemetry ssx', force=True)):
                    if unconfig and attributes.iswildcard:
                        configurations.submode_unconfig()

                    # +- DeviceAttributes
                    #     +- ExporterAttributes
                    for sub, attributes2 in attributes.mapping_values('exporter_attr',
                                                                      sort=True, keys=self.exporter_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    #+- SsxAttributes
                    #    +- RecordAttributes
                    for sub, attributes2 in attributes.mapping_values('record_attr',
                                                                      sort=True, keys=self.record_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    #+- SsxAttributes
                    #     +- MonitorAttributes
                    for sub, attributes2 in attributes.mapping_values('monitor_attr',
                                                                      sort=True, keys=self.monitor_attr):
                        configurations.append_block(
                            sub.build_config(apply=False,
                                             attributes=attributes2,
                                             unconfig=unconfig))

                    if attributes.value('ssx_system_monitor'):
                        for monitor in attributes.value('ssx_system_monitor'):
                            attributes.obj.monitor_ssx = monitor
                            configurations.append_line(
                                attributes.format('ssx system monitor {monitor_ssx}'))

                    if attributes.value('ssx_id'):
                        configurations.append_line(
                            attributes.format('ssx system system-id {ssx_id}'))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class ExporterAttributes(ABC):

                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)
                    with configurations.submode_context(attributes.format(
                            'ssx exporter {exp_id}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        if attributes.value('source_ip'):
                            configurations.append_line(
                                attributes.format('source {source_ip}'))

                        if attributes.value('dest_ip'):
                            configurations.append_line(
                                attributes.format('destination {dest_ip} use-vrf default'))

                        if attributes.value('source_port') and attributes.value('dest_port'):
                            configurations.append_line(
                                attributes.format('transport udp src-port {source_port} dst-port {dest_port}'))

                        if attributes.value('dscp'):
                            configurations.append_line(
                                attributes.format('dscp {dscp}'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class RecordAttributes(ABC):
                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(attributes.format(
                            'ssx record {rec_id}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        if attributes.value('egress_queue_drops'):
                            configurations.append_line(
                                attributes.format('collect egress queue drops'))

                        if attributes.value('egress_queue_peak'):
                            configurations.append_line(
                                attributes.format('collect egress queue peak'))

                        if attributes.value('egress_queue_depth'):
                            configurations.append_line(
                                attributes.format('collect egress queue depth'))

                        if attributes.value('ingress_queue_drops'):
                            configurations.append_line(
                                attributes.format('collect ingress queue drops'))

                        if attributes.value('ingress_queue_depth'):
                            configurations.append_line(
                                attributes.format('collect ingress queue depth'))

                        if attributes.value('egress_queue_microburst'):
                            configurations.append_line(
                                attributes.format('collect egress queue microburst'))

                        if attributes.value('ethernet_counters'):
                            configurations.append_line(
                                attributes.format('collect ethernet counters'))

                        if attributes.value('egress_pool_group_depth'):
                            configurations.append_line(
                                attributes.format('collect egress pool-group depth'))

                        if attributes.value('egress_buffer_depth'):
                            configurations.append_line(
                                attributes.format('collect egress buffer depth'))

                        if attributes.value('record_interval'):
                            configurations.append_line(
                                attributes.format('interval {record_interval}'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)

            class MonitorAttributes(ABC):
                def build_config(self, apply=True, attributes=None, unconfig=False,
                                 **kwargs):
                    assert not kwargs, kwargs
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    with configurations.submode_context(attributes.format(
                            'ssx monitor {mon_id}', force=True)):
                        if unconfig and attributes.iswildcard:
                            configurations.submode_unconfig()

                        if attributes.value('rec_name'):
                            configurations.append_line(
                                attributes.format('record {rec_name}'))

                        if attributes.value('exp_name'):
                            configurations.append_line(
                                attributes.format('exporter {exp_name}'))

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)
