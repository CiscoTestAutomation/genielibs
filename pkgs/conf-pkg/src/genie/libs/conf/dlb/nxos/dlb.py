
'''
DLB Genie Conf Object Implementation for NXOS - CLI.
'''

# Python
from abc import ABC

# Genie
from genie.conf.base.attributes import AttributesHelper
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.config import CliConfig

# Dlb Hierarchy
# --------------
# Dlb
#     +-- DeviceAttributes
#       +- DlbAttributes

class Dlb(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)
            # enable dlb feature - hardware profile dlb 
            with configurations.submode_context(attributes.format('hardware profile dlb', force=True)):
                if unconfig and attributes.iswildcard:
                    configurations.submode_unconfig()
                
                # mode <mode>
                if attributes.value('mode'):
                    configurations.append_line(attributes.format('mode {mode}'))
                
                # dlb-interface <interface_list>
                if attributes.value('dlb_interface'):
                    interfaces = attributes.value('dlb_interface')
                    intf_str = ''
                    if interfaces == 'all':
                        intf_str = 'all'
                    elif isinstance(interfaces, list):
                        intf_names = []
                        for i in interfaces:
                            if hasattr(i, 'name'):
                                intf_names.append(i.name)
                            else:
                                intf_names.append(str(i))
                        intf_str = ' , '.join(intf_names)
                    
                    if intf_str:
                        configurations.append_line(f'dlb-interface {intf_str}')

                # mac-address <mac>
                if attributes.value('mac_address'):
                    configurations.append_line(attributes.format('mac-address {mac_address}'))

                # flowlet-aging <aging>
                if attributes.value('flowlet_aging'):
                    configurations.append_line(attributes.format('flowlet-aging {flowlet_aging}'))

                # dre-thresholds <key> <value> ...
                if attributes.value('dre_thresholds'):
                    thresholds = attributes.value('dre_thresholds')
                    threshold_str = ''
                    
                    # Support both formats:
                    # 1. Dict format: {'level-1': '15', 'level-2': '20', ...}
                    # 2. List format: [{'level': '1', 'percentage': '15'}, ...]
                    if isinstance(thresholds, dict):
                        for key, value in thresholds.items():
                            threshold_str += f' {key} {value} '
                    elif isinstance(thresholds, list):
                        for item in thresholds:
                            if isinstance(item, dict) and 'level' in item and 'percentage' in item:
                                threshold_str += f" level-{item['level']} {item['percentage']} "
                    
                    if threshold_str:
                        configurations.append_line(f'dre-thresholds {threshold_str}')

                # static-pinning
                if attributes.value('static_pinning'):
                    configurations.append_line('static-pinning')
                    for item in attributes.value('static_pinning'):
                        # item is expected to be a dict with 'source' and 'destination' keys
                        if isinstance(item, dict) and 'source' in item and 'destination' in item:
                            src = item['source']
                            dst = item['destination']
                            if hasattr(src, 'name'): src = src.name
                            if hasattr(dst, 'name'): dst = dst.name
                            configurations.append_line(f'source {src} destination {dst}')

                # decay-factor <value>
                if attributes.value('decay_factor') is not None:
                    configurations.append_line(attributes.format('decay-factor {decay_factor}'))

                # sampling-interval <value> nsecs
                if attributes.value('sampling_interval') is not None:
                    sampling = attributes.value('sampling_interval')
                    # If it's just a number, add 'nsecs' suffix
                    if isinstance(sampling, int):
                        configurations.append_line(f'sampling-interval {sampling} nsecs')
                    else:
                        # If it's already a string, use as-is (allows for 'nsecs' already included)
                        configurations.append_line(f'sampling-interval {sampling}')

                # load-awareness / no load-awareness
                if attributes.value('load_awareness') is not None:
                    if attributes.value('load_awareness'):
                        configurations.append_line('load-awareness')
                    else:
                        configurations.append_line('no load-awareness')

            if apply:
                if configurations:
                    self.device.configure(configurations)
            else:
                return CliConfig(device=self.device, unconfig=unconfig,
                                 cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes, unconfig=True, **kwargs)
