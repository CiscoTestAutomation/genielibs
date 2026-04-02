'''
Platform Genie Ops Object for IOSXR.
'''

# super class
from genie.libs.ops.platform.platform import Platform as SuperPlatform

# Parser
from genie.libs.parser.iosxr.show_platform import ShowVersion, ShowSdrDetail,\
                                ShowPlatform, ShowPlatformVm,\
                                ShowInstallActiveSummary, ShowInventory,\
                                ShowRedundancySummary, AdminShowDiagChassis,\
                                ShowRedundancy, Dir


class Platform(SuperPlatform):
    '''Platform Genie Ops Object'''

    def get_active_uptime(self, item):
        for node in item:
            if 'active' in item[node]['role'].lower():
                return item[node]['node_uptime_in_seconds']

    def _populate_slot_serial_numbers(self):
        """Map serial numbers from show inventory to slot entries.

        show inventory uses module names like '0/FC0', '0/0/CPU0',
        '0/RP0/CPU0' while show platform uses slot names like '0/FC0',
        '0/0', '0/RP0'. This method handles the naming differences.

        Uses _inventory_modules populated by add_leaf during make().
        """
        if not hasattr(self, 'slot') or not hasattr(self, '_inventory_modules'):
            return

        modules = self._inventory_modules
        if not modules or not isinstance(modules, dict):
            del self._inventory_modules
            return

        for slot_type in self.slot:
            if not isinstance(self.slot[slot_type], dict):
                continue
            for slot_name, slot_data in self.slot[slot_type].items():
                if not isinstance(slot_data, dict):
                    continue
                if slot_data.get('sn'):
                    continue
                for candidate in [slot_name, '{}/CPU0'.format(slot_name),
                                  'module {}'.format(slot_name),
                                  'module {}/CPU0'.format(slot_name)]:
                    if candidate in modules:
                        inv = modules[candidate]
                        if inv.get('sn'):
                            slot_data['sn'] = inv['sn']
                        if not slot_data.get('pid') and inv.get('pid'):
                            slot_data['pid'] = inv['pid']
                        break

        del self._inventory_modules

    def learn(self):
        '''Learn Platform Ops'''

        # ================
        # DeviceAttributes
        # ================

        # chassis
        self.add_leaf(cmd=ShowVersion,
                      src='[device_family]',
                      dest='[chassis]')

        # chassis_sn
        self.add_leaf(cmd=AdminShowDiagChassis,
                      src='[sn]',
                      dest='[chassis_sn]')

        self.add_leaf(cmd='show diag details',
                      src='[item][Rack 0-Chassis][chassis_serial_number]',
                      dest='[chassis_sn]')

        self.add_leaf(cmd='show diag details',
                      src='[item][Rack 0-Virtual][pcb_serial_number]',
                      dest='[chassis_sn]')

        # Backup in the event the above doesn't work
        self.add_leaf(cmd='show inventory',
                      src='[module_name][Rack 0][sn]',
                      dest='[chassis_sn]')

        # chassis
        self.add_leaf(cmd=AdminShowDiagChassis,
                      src='[pid]',
                      dest='[chassis]')

        self.add_leaf(cmd='show inventory',
                      src='[module_name][Rack 0][pid]',
                      dest='[chassis]')

        self.add_leaf(cmd='show diag details',
                      src='[item][Rack 0-Chassis][pid]',
                      dest='[chassis]')

        self.add_leaf(cmd='show diag details',
                      src='[item][Rack 0-Virtual][pid]',
                      dest='[chassis]')

        # rtr_type
        self.add_leaf(cmd=ShowVersion,
                      src='[device_family]',
                      dest='[rtr_type]')

        # os
        self.add_leaf(cmd=ShowVersion,
                      src='[operating_system]',
                      dest='[os]')

        # version
        self.add_leaf(cmd=ShowVersion,
                      src='[software_version]',
                      dest='[version]')

        # image
        self.add_leaf(cmd=ShowVersion,
                      src='[image]',
                      dest='[image]')

        # installed_packages
        self.add_leaf(cmd=ShowInstallActiveSummary,
                      src='[active_packages]',
                      dest='[installed_packages]')

        # config_register
        self.add_leaf(cmd=ShowVersion,
                      src='[config_register]',
                      dest='[config_register]')

        # main_mem
        self.add_leaf(cmd=ShowVersion,
                      src='[processor_memory_bytes]',
                      dest='[main_mem]')

        # dir
        self.add_leaf(cmd=Dir,
                      src='[dir]',
                      dest='[dir]')

        # sdr_owner
        self.add_leaf(cmd=ShowInstallActiveSummary,
                      src='[sdr]',
                      dest='[sdr_owner]')

        # =======================
        # VirtualDeviceAttributes
        # =======================

        # vd_id == sdr_id
        # vd_name == sdr_name
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][sdr_name][(?P<sdr_name>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_name][(?P<sdr_name>.*)]')

        # vd_dSDRsc_nod
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][dsdrsc_node][(?P<dsdrsc_node>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_dSDRsc_nod][(?P<dsdrsc_node>.*)]')

        # vd_dSDRsc_partner_node
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][dsdrsc_partner_node][(?P<dsdrsc_partner_node>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_dSDRsc_partner_node][(?P<dsdrsc_partner_node>.*)]')

        # vd_primary_node1
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][primary_node1][(?P<primary_node1>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_primary_node1][(?P<primary_node1>.*)]')

        # vd_primary_node2
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][primary_node2][(?P<primary_node2>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_primary_node2][(?P<primary_node2>.*)]')

        # vd_mac_addr
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][mac_address][(?P<mac_address>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][vd_mac_addr][(?P<mac_address>.*)]')

        # ====================
        # MembershipAttributes
        # ====================

        # vd_ms_name == node_name
        # vd_ms_type == type
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][type][(?P<type>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][vd_ms_type][(?P<type>.*)]')

        # vd_ms_status
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][node_status][(?P<node_status>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][vd_ms_status][(?P<node_status>.*)]')

        # vd_ms_red_state
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][red_state][(?P<red_state>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][vd_ms_red_state][(?P<red_state>.*)]')

        # vd_ms_partner_name
        self.add_leaf(cmd=ShowSdrDetail,
                      src='[sdr_id][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][partner_name][(?P<partner_name>.*)]',
                      dest='[virtual_device][(?P<sdr_id>.*)][membership][(?P<node_name>.*)][vd_ms_partner_name][(?P<partner_name>.*)]')

        # ==============
        # SlotAttributes
        # ==============

        # card_name
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][name][(?P<card_name>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][name][(?P<card_name>.*)]')

        # state
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][state][(?P<state>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][state][(?P<state>.*)]')

        # config_state
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][config_state][(?P<config_state>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][config_state][(?P<config_state>.*)]')

        # redundancy_state
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][redundancy_state][(?P<redundancy_state>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][redundancy_state][(?P<redundancy_state>.*)]')

        # subslot
        self.add_leaf(cmd=ShowPlatform,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][subslot][(?P<subslot>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][subslot][(?P<subslot>.*)]')

        # full_slot
        self.add_leaf(cmd=ShowPlatform, revision=None,
                      src='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][full_slot][(?P<full_slot>.*)]',
                      dest='[slot][(?P<slot_type>.*)][(?P<slot_name>.*)][full_slot][(?P<full_slot>.*)]')

        # rp_config_register
        self.add_leaf(cmd=ShowVersion,
                      src='[rp_config_register][(?P<rp_config_register>.*)]',
                      dest='[slot][rp][rp_config_register][(?P<rp_config_register>.*)]')

        # ==============
        # Redudancy
        # ==============

        # redundancy_communication
        self.add_leaf(cmd=ShowRedundancySummary,
                      src='[redundancy_communication]',
                      dest='[redundancy_communication]')

        # rp_uptime
        self.add_leaf(cmd=ShowRedundancy,
                      src='[node]',
                      dest='[rp_uptime]',
                      action=self.get_active_uptime)

        # Store full inventory modules for slot serial number augmentation
        self.add_leaf(cmd=ShowInventory,
                      src='[module_name]',
                      dest='[_inventory_modules]')

        # Make Ops object
        self.make(final_call=True)

        # Augment slot data with serial numbers from show inventory
        self._populate_slot_serial_numbers()

# vim: ft=python et sw=4
