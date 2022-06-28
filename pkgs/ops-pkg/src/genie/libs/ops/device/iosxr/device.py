'''
Device Genie Ops Object for IOSXR - CLI.
'''

# super class
from genie.libs.ops.device.device import Device as SuperDevice
from genie.libs.ops.device.device import schema

# Parser
from genie.metaparser.util.schemaengine import Schema
from genie.libs.parser.iosxr.show_cdp import ShowCdpNeighborsDetail
from genie.libs.parser.iosxr.show_lldp import ShowLldpNeighborsDetail
from genie.libs.parser.iosxr.show_interface import ShowInterfaces
from genie.libs.parser.iosxr.show_platform import ShowVersion, ShowInventory
from genie.libs.ops.device.device import ShowRunningConfig

from datetime import datetime

import re

class Device(SuperDevice):
    '''Device Genie Ops Object'''

    # show command - ops key mapper
    cmd_leaf_map = {
        'show cdp neighbors detail': 'neighbors',
        'show interfaces': 'interfaces',
        'show inventory': 'inventory',
        'show lldp neighbors detail': 'neighbors',
        'show version': 'version',
    }

    # Callables
    def cast_isoformat(self, item):
        '''cast item to date in isoformat'''
        # Fri Dec 13 16:42:11 PST 2019
        # remove timezone as it cannot be parsed to isoformat
        date_item = re.sub(
            r"^(\w+)\s(\w+)\s(\d+)\s(\d+:\d+:\d+)\s(\S+\s)(\d+)$", 
            r"\1 \2 \3 \4 \6",
            item)
        return datetime.strptime(date_item, '%a %b %d %H:%M:%S %Y').isoformat()

    def cast_bool(self, item):
        '''cast item to boolean'''
        true_values = ['up', 'ok', 'on', 'not present']
        return item in true_values

    def get_keys(self, item):
        '''return all keys from item'''
        if isinstance(item, dict):
            return list(item.keys())
        return []

    def get_numeric_value(self, item):
        '''return the numeric value at the beginning of a string'''
        return re.sub(
            '^(?P<num>[0-9]+)\s*(?P<unit>.*)$',
            r'\1',
            item
        )
    
    def get_unit_value(self, item):
        '''return the unit value at the end of a string'''
        return re.sub(
            '^(?P<num>[0-9]+)\s*(?P<unit>.*)$',
            r'\2',
            item)

    def learn(self):
        '''Learn Device Ops'''
        info_dest = 'info'

        cdp_src = '[index][(?P<index>.*)]'
        cdp_dest = '{}[neighbors][data][cdp][(?P<index>.*)]'.format(info_dest)

        cdp_keys = {
            'device_id': 'name',
            'local_interface': 'local_interface',
            'port_id': 'interface'
        }

        for key_src, key_dest in cdp_keys.items():
            self.add_leaf(cmd=ShowCdpNeighborsDetail,
                          src='{}[{}]'.format(cdp_src, key_src),
                          dest='{}[{}]'.format(cdp_dest, key_dest))

        self.add_leaf(cmd=ShowCdpNeighborsDetail,
                      src='{}[entry_addresses]'.format(cdp_src),
                      dest='{}[addresses]'.format(cdp_dest),
                      action=self.get_keys)

        # LLDP Neighbors Detail
        lldp_src = '[interfaces][(?P<itf>.*)][port_id][(?P<port_id>.*)]' \
                   '[neighbors][(?P<neighbor>.*)]'

        lldp_dest = '{}[neighbors][data][lldp][(?P<neighbor>.*)]' \
                    .format(info_dest)

        lldp_keys = {
            'neighbor_id': 'name',
            'local_interface': 'local_interface',
        }

        for key_src, key_dest in lldp_keys.items():
            self.add_leaf(cmd=ShowLldpNeighborsDetail,
                          src='{}[{}]'.format(lldp_src, key_src),
                          dest='{}[{}]'.format(lldp_dest, key_dest))

        self.add_leaf(
            cmd=ShowLldpNeighborsDetail,
            src=lldp_src,
            dest='{}[interface][(?P<port_id>.*)]' \
                 .format(lldp_dest))

        self.make()

        if hasattr(self, 'info') and 'neighbors' in self.info:
            index = 1
            names = []
            for cmd in ['cdp', 'lldp']:
                for key, value in self.info['neighbors']['data'].get(cmd, {}).items():
                    if self.info['neighbors']['data'][cmd][key]['name'] not in names:
                        names.append(
                            self.info['neighbors']['data'][cmd][key]['name'])
                        n_dict = self.info['neighbors'].setdefault(str(index), {})
                        n_dict.update(value)
                        # add port_id as interface on lldp neighbors
                        if cmd == 'lldp':
                            interface_name = list(self.info['neighbors']['data'][cmd][key]['interface'].keys())[0]
                            n_dict['interface'] = interface_name
                        index += 1
            # remove data as it is no longer necessary
            del self.info['neighbors']['data']

        # Interfaces
        intf_src = '[(?P<itf>.*)]'
        intf_dest = '{}[interfaces][(?P<itf>.*)]'.format(info_dest)

        for key in ['enabled', 'mac_address', 'media_type', 'mtu']:
            self.add_leaf(cmd=ShowInterfaces,
                          src='{}[{}]'.format(intf_src, key),
                          dest='{}[{}]'.format(intf_dest, key))

        intf_keys = {
            'duplex_mode': 'duplex',
            'oper_status': 'status'
        }

        for key, value in intf_keys.items():
            self.add_leaf(
                cmd=ShowInterfaces,
                src='{}[{}]'.format(intf_src, key),
                dest='{}[{}]'.format(intf_dest, value))

        self.add_leaf(
            cmd=ShowInterfaces,
            src='{}[port_speed]'.format(intf_src),
            dest='{}[speed]'.format(intf_dest),
            action=self.get_numeric_value)

        self.add_leaf(
            cmd=ShowInterfaces,
            src='{}[port_speed]'.format(intf_src),
            dest='{}[speed_unit]'.format(intf_dest),
            action=self.get_unit_value)

        for key in ['line_protocol', 'link_state']:
            self.add_leaf(
                cmd=ShowInterfaces,
                src='{}[{}]'.format(intf_src, key),
                dest='{}[{}]'.format(intf_dest, key),
                action=self.cast_bool)

        # Inventory
        inv_src = '[module_name][(?P<inv>.*)]'
        inv_dest = '{}[inventory][data][(?P<inv>.*)]'.format(info_dest)

        self.add_leaf(
            cmd=ShowInventory,
            src='{}[descr]'.format(inv_src),
            dest='{}[description]'.format(inv_dest))

        for key in ['pid', 'vid', 'sn']:
            self.add_leaf(
                cmd=ShowInventory,
                src='{}[{}]'.format(inv_src, key),
                dest='{}[{}]'.format(inv_dest, key))
        self.make()

        if hasattr(self, 'info') and 'inventory' in self.info:
            for index, (key, value) in enumerate(
              self.info['inventory']['data'].items(), start=1):
                inv_dict = self.info['inventory'].setdefault(str(index), {})
                inv_dict['name'] = key
                inv_dict.update(value)

            del (self.info['inventory']['data'])

        # Version
        ver_dest = f'{info_dest}[version]'

        version_keys = {
            'software_version': 'version',
            'built_by': 'built_by'
        }

        for key, value in version_keys.items():
            self.add_leaf(
                cmd=ShowVersion,
                src=f'[{key}]',
                dest=f'{ver_dest}[{value}]')

        self.add_leaf(
            cmd=ShowVersion,
            src='[built_on]',
            dest=f'{ver_dest}[built_date]',
            action=self.cast_isoformat)

        self.make()

        # Get os and platform from device
        if hasattr(self, 'info') and 'version' in self.info:
            version = self.info.setdefault('version', {})
            version['os'] = self.device.os
            version['platform'] = self.device.platform or ''

        # Running-config
        self.add_leaf(
            cmd=ShowRunningConfig,
            src='[config]',
            dest='info[config][running]'
        )
        self.make()

        # copies raw_data from device to model instance
        # works if the model is instantiated with raw_data = True
        if self.raw_data and hasattr(self, 'info'):
            # loop through unique leaves created
            for cmd, output in self.maker.outputs.items():
                value = output['']
                if isinstance(value, dict) and hasattr(value, 'raw_output'):
                    for record in value.raw_output:
                        cmd_leaf = self.cmd_leaf_map.get(
                            record['command'], None)
                        if cmd_leaf and cmd_leaf in self.info:
                            cmd_leaf = self.info[cmd_leaf]
                            raw_dict = cmd_leaf.setdefault('raw_data', {})
                            raw_dict.update({
                                record['command']: record['output']
                            })

        self.make(final_call=True)

        # validate schema only if no filters were applied and info was created
        if hasattr(self, 'info') and not any((self.attributes, self.commands)):
            Schema(schema).validate(self.info)
