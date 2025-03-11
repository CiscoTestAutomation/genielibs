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
    '''Platform Ops Object'''

    show_module = 'show module'
    show_module_revision = '1'
    show_inventory = 'show inventory'
    show_inventory_option = 'all'

    def learn(self):
        '''Learn Platform object'''

        # Attribute filtering is not working for "placeholder" info, disabling and restoring after

        # save attributes
        attrs = self.attributes
        self.attributes = None
        self.maker.attributes = None

        # Store output in placeholder "Slot"
        self.add_leaf(cmd=self.show_inventory,
                      src='[name][(?P<slot>.*)][description]',
                      dest='Slot[(?P<slot>.*)][description]',
                      option=self.show_inventory_option)

        self.add_leaf(cmd=self.show_inventory,
                      src='[name][(?P<slot>.*)][serial_number]',
                      dest='Slot[(?P<slot>.*)][serial_number]',
                      option=self.show_inventory_option)

        self.add_leaf(cmd=self.show_inventory,
                      src='[name][(?P<slot>.*)][pid]',
                      dest='Slot[(?P<slot>.*)][pid]',
                      option=self.show_inventory_option)

        self.add_leaf(cmd=self.show_inventory,
                      src='[name][(?P<slot>.*)][slot]',
                      dest='Slot[(?P<slot>.*)][slot]',
                      option=self.show_inventory_option)

        # restore attributes
        self.attributes = attrs
        self.maker.attributes = attrs

        # Place holder to make it more readable
        src_vdc_detail = '[vdc][(?P<id>.*)]'
        dest_vdc_detail = '[virtual_device][(?P<id>.*)]'

        self.add_leaf(cmd=show_platform.ShowVdcDetail,
                      src=src_vdc_detail+'[name]',
                      dest=dest_vdc_detail+'[vd_name]')

        self.add_leaf(cmd=show_platform.ShowVdcDetail,
                      src=src_vdc_detail+'[state]',
                      dest=dest_vdc_detail+'[vd_status]')

        # Place holder to make it more readable
        src_vdc_membership = '[virtual_device][(?P<id>.*)][membership]'
        dest_vdc_membership = '[virtual_device][(?P<id>.*)][membership]'

        self.add_leaf(cmd=show_platform.ShowVdcMembershipStatus,
                      src=src_vdc_membership+'[(?P<vdc_name>.*)][(?P<vd_ms_name>.*)][vd_ms_status]',
                      dest=dest_vdc_membership+'[(?P<vdc_name>.*)][(?P<vd_ms_name>.*)][status]')

        self.add_leaf(cmd=show_platform.ShowVdcMembershipStatus,
                      src=src_vdc_membership+'[(?P<vdc_name>.*)][(?P<vd_ms_name>.*)][vd_ms_type]',
                      dest=dest_vdc_membership+'[(?P<vdc_name>.*)][(?P<vd_ms_name>.*)][type]')

        self.add_leaf(cmd=self.show_module,
                      src='[xbar]',
                      dest='[slot][oc]',
                      revision=self.show_module_revision)

        self.add_leaf(cmd=self.show_module,
                      src='[xbar][(?P<xbar>.*)][status]',
                      dest='[slot][oc][(?P<xbar>.*)][state]',
                      revision=self.show_module_revision)

        self.add_leaf(cmd=self.show_module,
                      src='[xbar][(?P<xbar>.*)][module_type]',
                      dest='[slot][oc][(?P<xbar>.*)][name]',
                      revision=self.show_module_revision)

        self.add_leaf(cmd=self.show_module,
                      src='[xbar]',
                      dest='[xbar]',
                      revision=self.show_module_revision)

        self.add_leaf(cmd=self.show_module,
                      src='[slot]',
                      dest='[module]',
                      revision=self.show_module_revision)

        self.add_leaf(cmd=self.show_module,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][model]',
                      dest='[slot][rp][(?P<slot>.*)][name]',
                      revision=self.show_module_revision)

        self.add_leaf(cmd=self.show_module,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][status]',
                      dest='[slot][rp][(?P<slot>.*)][state]',
                      revision=self.show_module_revision)

        self.add_leaf(cmd=self.show_module,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][serial_number]',
                      dest='[slot][rp][(?P<slot>.*)][sn]',
                      revision=self.show_module_revision)

        self.add_leaf(cmd=self.show_module,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][status]',
                      dest='[slot][rp][(?P<slot>.*)][redundancy_state]',
                      revision=self.show_module_revision)

        # 'subslot' is not available on NXOS

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

        self.add_leaf(cmd=show_platform.ShowInstallActive,
                      src='[active_packages][active_package_module_0][active_package_name]',
                      dest='[installed_packages]')

        self.add_leaf(cmd=show_platform.ShowRedundancyStatus,
                      src='[active_supervisor_time]',
                      dest='[rp_uptime]',
                      action=convert_to_seconds)

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
        if 'Slot' in self.__dict__:
            line_cards = []
            slot_value = None
            new_dict = {}
            new_dict['slot'] = {}
            for slot in self.Slot:

                if 'Chassis' in slot:
                    new_dict['chassis'] = self.Slot['Chassis']['pid'].strip()
                    new_dict['chassis_sn'] = self.Slot['Chassis']['serial_number'].strip()

                elif 'Slot' in slot:
                    slot_value = self.Slot[slot]['slot']

                    if 'Supervisor Module' in self.Slot[slot]['description']:

                        slot_dict = new_dict.setdefault('slot', {}).setdefault('rp', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['pid']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        if 'serial_number' in self.Slot[slot]:
                            slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                    elif 'Ethernet Module' in self.Slot[slot]['description']:
                        slot_dict = new_dict.setdefault('slot', {}).setdefault('lc', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['description']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        if 'serial_number' in self.Slot[slot]:
                            slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                    else:
                        slot_dict = new_dict.setdefault('slot', {}).setdefault('oc', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['description']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        if 'serial_number' in self.Slot[slot]:
                            slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                elif 'Module' in slot:
                    slot_value = self.Slot[slot]['slot']
                    if 'Nexus' in self.Slot[slot]['description']:
                        slot_dict = new_dict.setdefault('slot', {}).setdefault('oc', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['description']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                    if 'Supervisor' not in self.Slot[slot]['description']:
                        slot_dict = new_dict.setdefault('slot', {}).setdefault('lc', {}).setdefault(slot_value, {})
                        slot_dict.update({'name': self.Slot[slot]['description']})
                        slot_dict.update({'pid': self.Slot[slot]['pid']})
                        slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                elif 'Power Supply' in slot:
                    slot_value = self.Slot[slot]['slot']
                    slot_dict = new_dict.setdefault('slot', {}).setdefault('psu', {}).setdefault(slot_value, {})
                    slot_dict.update({'name': self.Slot[slot]['description']})
                    slot_dict.update({'pid': self.Slot[slot]['pid']})
                    slot_dict.update({'sn': self.Slot[slot]['serial_number']})

                else:
                    slot_value = self.Slot[slot]['slot']
                    slot_dict = new_dict.setdefault('slot', {}).setdefault('oc', {}).setdefault(slot, {})
                    slot_dict.update({'name': self.Slot[slot].get('description', '')})
                    slot_dict.update({'pid': self.Slot[slot].get('pid', '')})
                    slot_dict.update({'sn': self.Slot[slot].get('serial_number', '')})

            merge_dict(self.__dict__, new_dict)

            del self.Slot
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

            if 'lc' in self.slot:
                delete_dup_lc = []
                for item in self.slot['lc']:
                    if 'sn' in self.slot['lc'][item]:
                        serial = self.slot['lc'][item]['sn']
                    else:
                        serial = None

                    if 'module' in self.__dict__:

                        for key in self.module['lc']:
                            for mod_name in self.module['lc'][key]:
                                if 'serial_number' not in self.module['lc'][key][mod_name]:
                                    continue
                                if self.module['lc'][key][mod_name]['serial_number'] == serial:
                                    linecard_status = self.module['lc'][key][mod_name]['status']
                                    self.slot['lc'][item].update({'state':linecard_status})
                                    if not any(x in self.slot['lc'][item]['name'].lower() for x in ['sup', 'ethernet', 'eth']):
                                      self.slot.setdefault('oc',{}).setdefault(item, {}).update(self.slot['lc'][item])
                                      self.slot['oc'][item].update({'state':linecard_status})

                    if 'xbar' in self.__dict__:
                        for key in self.xbar:
                            if 'serial_number' not in self.xbar[key]:
                                continue
                            if self.xbar[key]['serial_number'] == serial:
                                linecard_status = self.xbar[key]['status']
                                self.slot.setdefault('oc',{}).setdefault(item,{}).update({'state':linecard_status})

                    if self.slot.get('rp', {}).get(item, {}).get('sn') == serial:
                       delete_dup_lc.append(item)

                for del_itm in delete_dup_lc:
                    del self.slot['lc'][del_itm]

                if getattr(self, 'module', {}) and (not self.module['lc'] and 'lc' in self.slot) or \
                   ('lc' in self.slot and not self.slot['lc']):
                    self.slot.pop('lc')

            if 'oc' in self.slot:
                for item in self.slot['oc']:
                    if 'sn' in self.slot['oc'][item]:
                        serial = self.slot['oc'][item]['sn']
                    else:
                        serial = None
                    if 'module' in self.__dict__:
                        for key in self.module['lc']:
                            for mod_name in self.module['lc'][key]:
                                if 'serial_number' not in self.module['lc'][key][mod_name]:
                                    continue
                                if self.module['lc'][key][mod_name]['serial_number'] == serial:
                                    linecard_status = self.module['lc'][key][mod_name]['status']
                                    self.slot['oc'][item].update({'state':linecard_status})
                    if 'xbar' in self.__dict__:
                        for key in self.xbar:
                            if 'serial_number' not in self.xbar[key]:
                                continue
                            if self.xbar[key]['serial_number'] == serial:
                                linecard_status = self.xbar[key]['status']
                                self.slot['oc'][item].update({'state':linecard_status})

                    if 'oc' in self.slot and 'lc' in self.slot:
                      if item in self.slot['oc'] and item in self.slot['lc']:
                        if self.slot['oc'][item] == self.slot['lc'][item]:
                          self.slot['lc'].pop(item)

            try:
                del self.rp_boot_image
            except Exception:
                pass
            try:
                del self.rp_kickstart_boot_image
            except Exception:
                pass

            if hasattr(self, 'module'):
                del self.module
            try:
                del self.xbar
            except Exception:
                pass

        if 'virtual_device' in self.__dict__:
            for virt_dev in self.virtual_device:
                if 'membership' in self.virtual_device[virt_dev]:
                    for item in self.virtual_device[virt_dev]['membership']:
                        self.virtual_device[virt_dev]['membership'] = \
                          self.virtual_device[virt_dev]['membership'][item]

        # if there is a linecard or RP with the same serial number as the chassis, remove it
        for lc_type in ['lc', 'rp']:
            new_dict_lc_type = self.slot.get(lc_type, {}).copy()
            for lc_slot, lc_kv in self.slot.get(lc_type, {}).items():
                if hasattr(self, 'chassis_sn') and lc_kv.get('sn') == self.chassis_sn:
                    new_dict_lc_type.pop(lc_slot)
            if new_dict_lc_type:
                self.slot[lc_type] = new_dict_lc_type
            else:
                self.slot.pop(lc_type, None)