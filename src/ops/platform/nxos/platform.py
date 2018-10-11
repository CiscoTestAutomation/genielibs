# python
import re

# Genie package
from genie.ops.base import Base

# Genie Xbu_shared
from genie.libs.parser.nxos import show_platform
from genie.metaparser import MetaParser
from genie.metaparser.util import merge_dict


class Platform(Base):
    '''Platform Ops Object'''

    def convert_to_seconds(self, item):
        # 0 days, 7 hours, 57 minutes, 30 seconds

        p = re.compile(r'((?P<day>\d+) +(day|days), *)?'
                        '((?P<hour>\d+) +(hour|hours), *)?'
                        '((?P<minute>\d+) +(minute|minutes), *)?'
                        '((?P<second>\d+) +(seconds|seconds))$')
        m = p.match(item)
        time_in_seconds = 0
        if m:
            if m.groupdict()['day']:
                time_in_seconds += int(m.groupdict()['day']) * 86400
            if m.groupdict()['hour']:
                time_in_seconds += int(m.groupdict()['hour']) * 3600
            if m.groupdict()['minute']:
                time_in_seconds += int(m.groupdict()['minute']) * 60
            if m.groupdict()['second']:
                time_in_seconds += int(m.groupdict()['second'])
        return time_in_seconds

    def learn(self):
        '''Learn Platform object'''
        self.add_leaf(cmd=show_platform.ShowInventory,
                      src='[name][(?P<slot>.*)][description]',
                      dest='Slot[(?P<slot>.*)][description]')

        self.add_leaf(cmd=show_platform.ShowInventory,
                      src='[name][(?P<slot>.*)][serial_number]',
                      dest='Slot[(?P<slot>.*)][serial_number]')

        self.add_leaf(cmd=show_platform.ShowInventory,
                      src='[name][(?P<slot>.*)][pid]',
                      dest='Slot[(?P<slot>.*)][pid]')

        self.add_leaf(cmd=show_platform.ShowInventory,
                      src='[name][(?P<slot>.*)][slot]',
                      dest='Slot[(?P<slot>.*)][slot]')

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

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[xbar]',
                      dest='[xbar]')

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot]',
                      dest='[module]')

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][model]',
                      dest='[slot][rp][(?P<slot>.*)][name]')

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][status]',
                      dest='[slot][rp][(?P<slot>.*)][state]')

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][serial_number]',
                      dest='[slot][rp][(?P<slot>.*)][sn]')

        self.add_leaf(cmd=show_platform.ShowModule,
                      src='[slot][rp][(?P<slot>.*)][(?P<rp_name>.*)][status]',
                      dest='[slot][rp][(?P<slot>.*)][redundancy_state]')

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
                      src='[platform][software][system]',
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
                      action=self.convert_to_seconds)

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

        self.make()

        if 'Slot' in self.__dict__:
            line_cards = []
            slot_value = None
            new_dict = {}
            new_dict['slot'] = {}
            new_dict['chassis'] = self.Slot['Chassis']['description'].strip()
            new_dict['chassis_sn'] = self.Slot['Chassis']['serial_number'].strip()
            for slot in self.Slot:
                if 'Slot' in slot:
                    slot_value = self.Slot[slot]['slot']
                    if 'Nexus' in self.Slot[slot]['description']:
                        if 'oc' not in new_dict['slot']:
                            new_dict['slot']['oc']= {}
                        if slot_value not in new_dict['slot']['oc']:
                            new_dict['slot']['oc'][slot_value]= {}
                        new_dict['slot']['oc'][slot_value]['name'] = self.Slot[slot]['description']
                        if 'serial_number' in self.Slot[slot]:
                            new_dict['slot']['oc'][slot_value]['sn'] = self.Slot[slot]['serial_number']
                    elif 'Supervisor' not in self.Slot[slot]['description']:
                        if 'lc' not in new_dict['slot']:
                            new_dict['slot']['lc'] = {}
                        if slot_value not in new_dict['slot']['lc']:
                            new_dict['slot']['lc'][slot_value] = {}
                        new_dict['slot']['lc'][slot_value]['name'] = self.Slot[slot]['description']
                        if 'serial_number' in self.Slot[slot]:
                            new_dict['slot']['lc'][slot_value]['sn'] = self.Slot[slot]['serial_number']

                elif 'Module' in slot:
                    slot_value = self.Slot[slot]['slot']
                    if 'Nexus' in self.Slot[slot]['description']:
                        if 'oc' not in new_dict['slot']:
                            new_dict['slot']['oc']= {}
                        if slot_value not in new_dict['slot']['oc']:
                            new_dict['slot']['oc'][slot_value]= {}
                        new_dict['slot']['oc'][slot_value]['name'] = self.Slot[slot]['description']
                        new_dict['slot']['oc'][slot_value]['sn'] = self.Slot[slot]['serial_number']
                    if 'Supervisor' not in self.Slot[slot]['description']:
                        if 'lc' not in new_dict['slot']:
                            new_dict['slot']['lc'] = {}
                        if slot_value not in new_dict['slot']['lc']:
                            new_dict['slot']['lc'][slot_value] = {}
                        new_dict['slot']['lc'][slot_value]['name'] = self.Slot[slot]['description']
                        new_dict['slot']['lc'][slot_value]['sn'] = self.Slot[slot]['serial_number']
            merge_dict(self.__dict__, new_dict)
            del self.Slot
            for slot_number in self.slot['rp']:
                try:
                    self.slot['rp'][str(slot_number)]['rp_boot_image'] = self.rp_boot_image
                except Exception:
                    pass
                try:
                    self.slot['rp'][str(slot_number)]['rp_kickstart_boot_image'] = self.rp_kickstart_boot_image
                except Exception:
                    pass
                self.slot['rp'][str(slot_number)]['rp_uptime'] = self.rp_uptime
            if 'lc' in self.slot:
                for item in self.slot['lc']:
                    if 'sn' in self.slot['lc'][item]:
                        serial = self.slot['lc'][item]['sn']
                    else:
                        serial = None
                    if 'module' in self.__dict__:
                        for key in self.module['lc']:
                            for mod_name in self.module['lc'][key]:
                                if self.module['lc'][key][mod_name]['serial_number'] == serial:
                                    linecard_status = self.module['lc'][key][mod_name]['status']
                                    self.slot['lc'][item].update({'state':linecard_status})
                    if 'xbar' in self.__dict__:
                        for key in self.xbar:
                            if self.xbar[key]['serial_number'] == serial:
                                linecard_status = self.xbar[key]['status']
                                self.slot['lc'][item].update({'state':linecard_status})
            if 'oc' in self.slot:
                for item in self.slot['oc']:
                    if 'sn' in self.slot['oc'][item]:
                        serial = self.slot['oc'][item]['sn']
                    else:
                        serial = None
                    if 'module' in self.__dict__:
                        for key in self.module['lc']:
                            for mod_name in self.module['lc'][key]:
                                if self.module['lc'][key][mod_name]['serial_number'] == serial:
                                    linecard_status = self.module['lc'][key][mod_name]['status']
                                    self.slot['oc'][item].update({'state':linecard_status})
                    if 'xbar' in self.__dict__:
                        for key in self.xbar:
                            if self.xbar[key]['serial_number'] == serial:
                                linecard_status = self.xbar[key]['status']
                                self.slot['oc'][item].update({'state':linecard_status})
            try:
                del self.rp_boot_image
            except Exception:
                pass
            try:
                del self.rp_kickstart_boot_image
            except Exception:
                pass
            
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
