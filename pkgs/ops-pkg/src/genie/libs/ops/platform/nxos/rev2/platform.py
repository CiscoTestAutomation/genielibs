# python
import re

# super class
from genie.libs.ops.platform.platform import Platform as SuperPlatform

# Genie Xbu_shared
from genie.libs.parser.nxos import show_platform
from genie.metaparser import MetaParser
from genie.metaparser.util import merge_dict

from genie.libs.ops.utils.common import convert_to_seconds


class Platform(SuperPlatform):
    '''Platform Ops Object for NXOS devices'''

    def learn(self):
        '''Learn Platform object
        
        Collects platform information from NXOS device including:
        - Inventory details (chassis, modules, line cards)
        - Virtual Device Context (VDC) information
        - Boot configuration
        - System version and installed packages
        - Disk usage and memory information
        '''

        # Attribute filtering is not working for "placeholder" info, disabling and restoring after
        show_inventory_option = 'all'
        show_module_revision = '1'

        # Temporarily disable attribute filtering to collect all inventory data
        attrs = self.attributes
        self.attributes = None
        self.maker.attributes = None

        # Collect inventory data into placeholder 'Slot' for later processing
        # This allows us to gather all hardware info before organizing it by type
        self.add_leaf(cmd=show_platform.ShowInventory,
                      src='[name][(?P<slot>.*)][description]',
                      dest='Slot[(?P<slot>.*)][description]',
                      option=show_inventory_option)

        self.add_leaf(cmd=show_platform.ShowInventory,
                      src='[name][(?P<slot>.*)][serial_number]',
                      dest='Slot[(?P<slot>.*)][serial_number]',
                      option=show_inventory_option)

        self.add_leaf(cmd=show_platform.ShowInventory,
                      src='[name][(?P<slot>.*)][pid]',
                      dest='Slot[(?P<slot>.*)][pid]',
                      option=show_inventory_option)

        self.add_leaf(cmd=show_platform.ShowInventory,
                      src='[name][(?P<slot>.*)][slot]',
                      dest='Slot[(?P<slot>.*)][slot]',
                      option=show_inventory_option)

        # Restore attribute filtering after inventory collection
        self.attributes = attrs
        self.maker.attributes = attrs

        # Collect Virtual Device Context (VDC) information
        # VDCs allow partitioning of a physical NXOS device into multiple logical devices
        src_vdc_detail = '[vdc][(?P<id>.*)]'
        dest_vdc_detail = '[virtual_device][(?P<id>.*)]'

        self.add_leaf(cmd=show_platform.ShowVdcDetail,
                      src=src_vdc_detail+'[name]',
                      dest=dest_vdc_detail+'[vd_name]')

        self.add_leaf(cmd=show_platform.ShowVdcDetail,
                      src=src_vdc_detail+'[state]',
                      dest=dest_vdc_detail+'[vd_status]')

        # Collect VDC membership status - which modules belong to which VDC
        src_vdc_membership = '[virtual_device][(?P<id>.*)][membership]'
        dest_vdc_membership = '[virtual_device][(?P<id>.*)][membership]'

        self.add_leaf(cmd=show_platform.ShowVdcMembershipStatus,
                      src=src_vdc_membership+'[(?P<vdc_name>.*)][(?P<vd_ms_name>.*)][vd_ms_status]',
                      dest=dest_vdc_membership+'[(?P<vdc_name>.*)][(?P<vd_ms_name>.*)][status]')

        self.add_leaf(cmd=show_platform.ShowVdcMembershipStatus,
                      src=src_vdc_membership+'[(?P<vdc_name>.*)][(?P<vd_ms_name>.*)][vd_ms_type]',
                      dest=dest_vdc_membership+'[(?P<vdc_name>.*)][(?P<vd_ms_name>.*)][type]')

        # Collect crossbar (xbar) module information - fabric modules connecting line cards
        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[xbar]',
                      dest='[slot][oc]',
                      revision=show_module_revision)

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[xbar][(?P<xbar>.*)][status]',
                      dest='[slot][oc][(?P<xbar>.*)][state]',
                      revision=show_module_revision)

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[xbar][(?P<xbar>.*)][module_type]',
                      dest='[slot][oc][(?P<xbar>.*)][name]',
                      revision=show_module_revision)

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[xbar]',
                      dest='[xbar]',
                      revision=show_module_revision)

        # Collect module information (line cards, supervisors)
        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot]',
                      dest='[module]',
                      revision=show_module_revision)

        # Collect Route Processor (Supervisor) information
        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][model]',
                      dest='[slot][rp][(?P<slot>.*)][name]',
                      revision=show_module_revision)

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][status]',
                      dest='[slot][rp][(?P<slot>.*)][state]',
                      revision=show_module_revision)

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][serial_number]',
                      dest='[slot][rp][(?P<slot>.*)][sn]',
                      revision=show_module_revision)

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][status]',
                      dest='[slot][rp][(?P<slot>.*)][redundancy_state]',
                      revision=show_module_revision)

        # Note: 'subslot' is not available on NXOS (unlike IOS-XE)

        # Collect disk usage information
        self.add_leaf(cmd=show_platform.Dir,
                      src='[dir]',
                      dest='[dir]')

        self.add_leaf(cmd=show_platform.Dir,
                      src='[disk_used_space]',
                      dest='[disk_used_space]')

        self.add_leaf(cmd=show_platform.Dir,
                      src='[disk_free_space]',
                      dest='[disk_free_space]')

        self.add_leaf(cmd=show_platform.Dir,
                      src='[disk_total_space]',
                      dest='[disk_total_space]')

        # Collect system version and software information
        self.add_leaf(cmd=show_platform.ShowVersion,
                      src='[platform][hardware][memory]',
                      dest='[main_mem]')

        self.add_leaf(cmd=show_platform.ShowVersion,
                      src='[platform][software][kickstart]',
                      dest='[kickstart_version]')

        self.add_leaf(cmd=show_platform.ShowVersion,
                      src='[platform][software][kickstart_image_file]',
                      dest='[kickstart_image]')

        self.add_leaf(cmd=show_platform.ShowVersion,
                      src='[platform][software][system_version]',
                      dest='[version]')

        self.add_leaf(cmd=show_platform.ShowVersion,
                      src='[platform][software][system_image_file]',
                      dest='[image]')

        self.add_leaf(cmd=show_platform.ShowVersion,
                      src='[platform][os]',
                      dest='[os]')

        self.add_leaf(cmd=show_platform.ShowVersion,
                      src='[platform][hardware][model]',
                      dest='[rtr_type]')

        # Collect installed packages
        self.add_leaf(cmd=show_platform.ShowInstallActive,
                      src='[active_packages][active_package_module_0][active_package_name]',
                      dest='[installed_packages]')

        # Collect redundancy and uptime information
        self.add_leaf(cmd=show_platform.ShowRedundancyStatus,
                      src='[active_supervisor_time]',
                      dest='[rp_uptime]',
                      action=convert_to_seconds)

        # Collect boot configuration - images used on next reload
        self.add_leaf(cmd=show_platform.ShowBoot,
                      src='[next_reload_boot_variable][sup_number][sup-1][kickstart_variable]',
                      dest='[rp_kickstart_boot_image]')

        self.add_leaf(cmd=show_platform.ShowBoot,
                      src='[next_reload_boot_variable][sup_number][sup-1][system_variable]',
                      dest='[rp_boot_image]')

        self.add_leaf(cmd=show_platform.ShowBoot,
                      src='[next_reload_boot_variable][kickstart_variable]',
                      dest='[rp_kickstart_boot_image]')

        self.add_leaf(cmd=show_platform.ShowBoot,
                      src='[next_reload_boot_variable][system_variable]',
                      dest='[rp_boot_image]')

        self.make(final_call=True)
        
        # Process and reorganize the collected Slot data by hardware type
        if hasattr(self, 'Slot'):
            line_cards = []
            slot_value = None
            new_dict = {}
            new_dict['slot'] = {}

            for slot in self.Slot:

                # Extract chassis information
                if 'Chassis' in slot:
                    new_dict['chassis'] = self.Slot['Chassis']['pid'].strip()
                    new_dict['chassis_sn'] = self.Slot['Chassis']['serial_number'].strip()

                # Process slotted modules (line cards, supervisors)
                elif 'Slot' in slot:
                    slot_value = self.Slot[slot]['slot']

                    # Categorize as Route Processor (Supervisor)
                    if 'Supervisor Module' in self.Slot[slot]['description']:

                        slot_dict = new_dict.setdefault('slot', {}).setdefault('rp', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['pid']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        if 'serial_number' in self.Slot[slot]:
                            slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                    # Categorize as Line Card (Ethernet modules)
                    elif 'Ethernet Module' in self.Slot[slot]['description'] or "Eth Module" in self.Slot[slot]['description']:
                        slot_dict = new_dict.setdefault('slot', {}).setdefault('lc', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['description']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        if 'serial_number' in self.Slot[slot]:
                            slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                    # Categorize as Other Card (fabric, power, etc.)
                    else:
                        slot_dict = new_dict.setdefault('slot', {}).setdefault('oc', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['description']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        if 'serial_number' in self.Slot[slot]:
                            slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                # Process Nexus modules
                elif 'Module' in slot:
                    slot_value = self.Slot[slot]['slot']
                    # Nexus modules
                    if 'Nexus' in self.Slot[slot]['description']:
                        slot_dict = new_dict.setdefault('slot', {}).setdefault('oc', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['description']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                    # Non-supervisor modules are line cards
                    if 'Supervisor' not in self.Slot[slot]['description']:
                        slot_dict = new_dict.setdefault('slot', {}).setdefault('lc', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['description']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                # Process Power Supply Units
                elif 'Power Supply' in slot:
                    slot_value = self.Slot[slot]['slot']
                    slot_dict = new_dict.setdefault('slot', {}).setdefault('psu', {}).setdefault(slot_value, {})
                    slot_dict.update({'name': self.Slot[slot]['description']})
                    slot_dict.update({'pid': self.Slot[slot]['pid']})
                    slot_dict.update({'sn': self.Slot[slot]['serial_number']})
                
                # Process Fan modules
                elif 'Fan' in slot:
                    slot_value = self.Slot[slot]['slot']
                    slot_dict = new_dict.setdefault('slot', {}).setdefault('fan', {}).setdefault(slot, {})
                    slot_dict.update({'name': self.Slot[slot]['description']})
                    slot_dict.update({'pid': self.Slot[slot]['pid']})
                    slot_dict.update({'sn': self.Slot[slot]['serial_number']})
                
                # Process transceiver modules
                elif 'transceiver' in slot:
                    slot_value = self.Slot[slot]['slot']
                    slot_number, slot_key = slot.split(" ", 1)
                    slot_dict = new_dict.setdefault('slot', {}).setdefault('transceiver', {}).setdefault(slot_number, {}).setdefault(slot_key, {})
                    slot_dict.update({'name': self.Slot[slot]['description']})
                    slot_dict.update({'pid': self.Slot[slot]['pid']})
                    slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                # Other hardware types (oc)
                else:
                    slot_value = self.Slot[slot]['slot']
                    slot_dict = new_dict.setdefault('slot', {}).setdefault('oc', {}).setdefault(slot, {})
                    slot_dict.update({'name': self.Slot[slot].get('description', '')})
                    slot_dict.update({'pid': self.Slot[slot].get('pid', '')})
                    slot_dict.update({'sn': self.Slot[slot].get('serial_number', '')})

            # Merge the reorganized data into the main dictionary
            merge_dict(self.__dict__, new_dict)

            del self.Slot
            
            # Add boot and uptime info to each RP/Supervisor
            for slot_number in self.slot.get('rp', {}):
                try:
                    self.slot['rp'][str(slot_number)]['rp_boot_image'] = self.rp_boot_image
                except Exception:
                    pass
                try:
                    self.slot['rp'][str(slot_number)]['rp_kickstart_boot_image'] = self.rp_kickstart_boot_image
                except Exception:
                    pass
                try:
                    self.slot['rp'][str(slot_number)
                                    ]['rp_uptime'] = self.rp_uptime
                except Exception:
                    pass
            # Process line cards - match with module data to get status            
            if 'lc' in self.slot:
                delete_dup_lc = []
                for item in self.slot['lc']:
                    # Get serial number for matching with module data
                    if 'sn' in self.slot['lc'][item]:
                        serial = self.slot['lc'][item]['sn']
                    else:
                        serial = None

                    # Match line card with module data using serial number to get status
                    if hasattr(self, 'module'):
                        for key in self.module['lc']:
                            for mod_name in self.module['lc'][key]:
                                if 'serial_number' not in self.module['lc'][key][mod_name]:
                                    continue
                                if self.module['lc'][key][mod_name]['serial_number'] == serial:
                                    linecard_status = self.module['lc'][key][mod_name]['status']
                                    self.slot['lc'][item].update({'state':linecard_status})
                                    # Non-ethernet modules should also be in 'oc' category
                                    if not any(x in self.slot['lc'][item]['name'].lower() for x in ['sup', 'ethernet', 'eth']):
                                      self.slot.setdefault('oc',{}).setdefault(item, {}).update(self.slot['lc'][item])
                                      self.slot['oc'][item].update({'state':linecard_status})

                    # Match with crossbar data for fabric module status
                    if hasattr(self, 'xbar'):
                        for key in self.xbar:
                            if 'serial_number' not in self.xbar[key]:
                                continue
                            if self.xbar[key]['serial_number'] == serial:
                                linecard_status = self.xbar[key]['status']
                                self.slot.setdefault('oc',{}).setdefault(item,{}).update({'state':linecard_status})

                    # If item is already in RP, mark for removal from LC to avoid duplication
                    if self.slot.get('rp', {}).get(item, {}).get('sn') == serial:
                       delete_dup_lc.append(item)

                # Remove duplicates (items that are supervisors, not line cards)
                for del_itm in delete_dup_lc:
                    del self.slot['lc'][del_itm]

                # Remove empty 'lc' dict if no line cards found
                if getattr(self, 'module', {}) and (not self.module['lc'] and 'lc' in self.slot) or \
                   ('lc' in self.slot and not self.slot['lc']):
                    self.slot.pop('lc')

            # Process other cards (fabric, power, etc.) - match with module/xbar data
            if 'oc' in self.slot:
                for item in self.slot['oc']:
                    # Get serial number for matching
                    if 'sn' in self.slot['oc'][item]:
                        serial = self.slot['oc'][item]['sn']
                    else:
                        serial = None
                    
                    # Match with module data to get status
                    if hasattr(self, 'module'):
                        for key in self.module['lc']:
                            for mod_name in self.module['lc'][key]:
                                if 'serial_number' not in self.module['lc'][key][mod_name]:
                                    continue
                                if self.module['lc'][key][mod_name]['serial_number'] == serial:
                                    linecard_status = self.module['lc'][key][mod_name]['status']
                                    self.slot['oc'][item].update({'state':linecard_status})

                    # Match with crossbar data for status
                    if hasattr(self, 'xbar'):
                        for key in self.xbar:
                            if 'serial_number' not in self.xbar[key]:
                                continue
                            if self.xbar[key]['serial_number'] == serial:
                                linecard_status = self.xbar[key]['status']
                                self.slot['oc'][item].update({'state':linecard_status})

                    # Remove duplicate entries between oc and lc
                    if 'oc' in self.slot and 'lc' in self.slot:
                      if item in self.slot['oc'] and item in self.slot['lc']:
                        if self.slot['oc'][item] == self.slot['lc'][item]:
                          self.slot['lc'].pop(item)

            # Clean up temporary attributes used for processing
            if hasattr(self, 'rp_boot_image'):
                del self.rp_boot_image

            if hasattr(self, 'rp_kickstart_boot_image'):
                del self.rp_kickstart_boot_image

            if hasattr(self, 'module'):
                del self.module

            if hasattr(self, 'xbar'):
                del self.xbar

        # Process virtual device membership - flatten nested structure
        # VDC membership is collected as nested dict, but we only need the first value
        if hasattr(self, 'virtual_device'):
            for virt_dev in self.virtual_device.values():
                membership = virt_dev.get('membership', {})
                if membership:
                    # Extract the first membership value
                    virt_dev['membership'] = next(iter(membership.values()))