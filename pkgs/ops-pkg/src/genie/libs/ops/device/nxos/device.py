'''
Device Genie Ops Object for NXOS - CLI.
'''

# super class
from attr import has
from genie.libs.ops.device.device import Device as SuperDevice
from genie.libs.ops.device.device import schema

# Parser
from genie.metaparser.util.schemaengine import Schema
from genie.libs.parser.nxos.show_cdp import ShowCdpNeighborsDetail
from genie.libs.parser.nxos.show_lldp import ShowLldpNeighborsDetail
from genie.libs.parser.nxos.show_interface import ShowInterface
from genie.libs.parser.nxos.show_environment import ShowEnvironment
from genie.libs.parser.nxos.show_platform import ShowVersion, ShowInventory
from genie.libs.parser.nxos.show_fdb import ShowMacAddressTable
from genie.libs.ops.device.device import ShowRunningConfig

from datetime import datetime


class Device(SuperDevice):
    '''Device Genie Ops Object'''

    # show command - ops key mapper
    cmd_leaf_map = {
        'show cdp neighbors detail': 'neighbors',
        'show interface': 'interfaces',
        'show inventory': 'inventory',
        'show lldp neighbors detail': 'neighbors',
        'show mac address-table': 'mac_table',
        'show version': 'version',
    }

    # Callables
    def cast_isoformat(self, item):
        '''cast item to date in isoformat'''
        # 8/20/2019 7:00:00 [08/20/2019 15:52:22]
        # extracts date within []
        item_date = item[item.find('[')+1:-1]
        return datetime.strptime(item_date, '%m/%d/%Y %H:%M:%S').isoformat()

    def cast_bool(self, item):
        '''cast item to boolean'''
        true_values = ['up', 'ok', 'not present']
        return item in true_values

    def get_keys(self, item):
        '''return all keys from item'''
        if isinstance(item, dict):
            return list(item.keys())
        return []

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
                      src='{}[interface_addresses]'.format(cdp_src),
                      dest='{}[addresses]'.format(cdp_dest),
                      action=self.get_keys)

        # LLDP Neighbors Detail
        lldp_src = '[interfaces][(?P<itf>.*)][port_id][(?P<port_id>.*)]' \
                   '[neighbors][(?P<neighbor>.*)]'

        lldp_dest = '{}[neighbors][data][lldp][(?P<neighbor>.*)]' \
                    .format(info_dest)

        lldp_keys = {
            'system_name': 'name',
            'local_interface': 'local_interface',
            'port_id': 'interface'
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
            self.add_leaf(cmd=ShowInterface,
                          src='{}[{}]'.format(intf_src, key),
                          dest='{}[{}]'.format(intf_dest, key))

        intf_keys = {
            'duplex_mode': 'duplex',
            'port_speed': 'speed',
            'port_speed_unit': 'speed_unit',
            'oper_status': 'status'
        }

        for key, value in intf_keys.items():
            self.add_leaf(
                cmd=ShowInterface,
                src='{}[{}]'.format(intf_src, key),
                dest='{}[{}]'.format(intf_dest, value))

        for key in ['line_protocol', 'link_state']:
            self.add_leaf(
                cmd=ShowInterface,
                src='{}[{}]'.format(intf_src, key),
                dest='{}[{}]'.format(intf_dest, key),
                action=self.cast_bool)

        # Inventory
        inv_src = '[name][(?P<inv>.*)]'
        inv_dest = '{}[inventory][data][(?P<inv>.*)]'.format(info_dest)

        self.add_leaf(
            cmd=ShowInventory,
            src='{}[serial_number]'.format(inv_src),
            dest='{}[sn]'.format(inv_dest))

        for key in ['description', 'pid', 'vid']:
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

        # Mac Address-Table
        mac_src = '[mac_table][vlans][(?P<vlan>.*)]' \
                  '[mac_addresses][(?P<mac>.*)][interfaces][(?P<intf>.*)]'
        mac_dest = '{}[mac_table][vlans][(?P<vlan>.*)]' \
                   '[mac_addresses][(?P<mac>.*)][interfaces][(?P<intf>.*)]' \
                   .format(info_dest)

        mac_keys = {'age': 'age', 'entry_type': 'type'}

        for key, value in mac_keys.items():
            self.add_leaf(
                cmd=ShowMacAddressTable,
                src='{}[{}]'.format(mac_src, key),
                dest='{}[{}]'.format(mac_dest, value))

        # Version

        ver_src = '[platform]'
        ver_dest = '{}[version]'.format(info_dest)

        self.add_leaf(
            cmd=ShowVersion,
            src='{}[software][system_version]'.format(ver_src),
            dest='{}[version]'.format(ver_dest))

        self.add_leaf(
            cmd=ShowVersion,
            src='{}[software][system_image_file]'.format(ver_src),
            dest='{}[system_image]'.format(ver_dest))

        self.add_leaf(
            cmd=ShowVersion,
            src='{}[software][system_compile_time]'.format(ver_src),
            dest='{}[built_date]'.format(ver_dest),
            action=self.cast_isoformat)

        self.make()

        # Get os and platform from device
        if hasattr(self, 'info') and 'version' in self.info:
            self.info['version']['os'] = self.device.os
            self.info['version']['platform'] = self.device.platform or ''

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
