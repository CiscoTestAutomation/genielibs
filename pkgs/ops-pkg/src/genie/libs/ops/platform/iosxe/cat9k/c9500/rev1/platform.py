# Genie package
import re
import copy
# super class
from genie.libs.ops.platform.rev1.platform import Platform as SuperPlatform
from genie.libs.ops.utils.common import convert_to_bool, \
                                        convert_to_seconds, \
                                        slot_num
# Genie Parsers
from genie.libs.parser.iosxe import show_platform


class Platform(SuperPlatform):
    '''Platform Ops Object'''

    def learn(self):
        '''Learn Platform object'''

        # Global callable
        self.callables = {'slot_num': slot_num}

        # Place holder to make it more readable
        src_ver = '[version]'

        # === DeviceAttributes ===

        # chassis
        self.add_leaf(cmd='show version',
                      src=src_ver + '[chassis]',
                      dest='chassis')

        self.add_leaf(cmd='show version',
                      src=src_ver + '[system_sn]',
                      dest='chassis_sn')

        self.add_leaf(cmd='show version',
                      src=src_ver + '[mb_sn]',
                      dest='chassis_sn')

        self.add_leaf(cmd='show version',
                      src=src_ver + '[chassis_sn]',
                      dest='chassis_sn')

        # rtr_type
        self.add_leaf(cmd='show version',
                      src=src_ver + '[rtr_type]',
                      dest='rtr_type')

        # os
        self.add_leaf(cmd='show version',
                      src=src_ver + '[os]',
                      dest='os')

        # version
        self.add_leaf(cmd='show version',
                      src=src_ver + '[version]',
                      dest='version')

        # label
        self.add_leaf(cmd='show version',
                      src=src_ver + '[build_label]',
                      dest='label')

        # image
        self.add_leaf(cmd='show version',
                      src=src_ver + '[system_image]',
                      dest='image')

        # kickstart_version
        # N/A

        # kickstart_image
        # N/A

        # installed_packages
        # N/A

        # config_register
        self.add_leaf(cmd='show version',
                      src=src_ver + '[curr_config_register]',
                      dest='config_register')

        # main_mem
        self.add_leaf(cmd='show version',
                      src=src_ver + '[main_mem]',
                      dest='main_mem')

        # dir
        self.add_leaf(cmd='dir',
                      src='[dir][dir]',
                      dest='dir')

        # redundancy_mode
        self.add_leaf(cmd='show redundancy',
                      src='[red_sys_info][oper_red_mode]',
                      dest='redundancy_mode')

        # switchover_reason
        self.add_leaf(cmd='show redundancy',
                      src='[red_sys_info][last_switchover_reason]',
                      dest='switchover_reason')

        # redundancy_communication
        self.add_leaf(cmd='show redundancy',
                      src='[red_sys_info][communications]',
                      dest='redundancy_communication',
                      action=convert_to_bool)

        # swstack
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[main][swstack]',
                      dest='swstack')

        # sdr_owner
        # N/A

        # === VirtualDeviceAttributes ===
        # N/A

        # === MemberShipAttributes ===
        # N/A

        # === SlotAttributes ===
        # === RouteProcessorAttributes ===

        # rp_name
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][name]',
                      dest='[slot][rp][(?P<slot>.*)][name]')

        # pid
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][pid]',
                      dest='[slot][rp][(?P<slot>.*)][pid]')

        # rp_state
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][state]',
                      dest='[slot][rp][(?P<slot>.*)][state]')

        # rp_redundancy_state
        self.add_leaf(cmd='show redundancy',
                      src='[slot][(?P<slot>{slot_num})][curr_sw_state]',
                      dest='red[rp][(?P<slot>{slot_num})][redundancy_state]')

        # rp_uptime
        self.add_leaf(cmd='show redundancy',
                      src='[slot][(?P<slot>{slot_num})][uptime_in_curr_state]',
                      dest='red[rp][(?P<slot>{slot_num})][rp_uptime]')

        self.add_leaf(cmd='show redundancy',
                      src='[red_sys_info][available_system_uptime]',
                      dest='[rp_uptime]',
                      action=convert_to_seconds)

        # rp_system_image
        self.add_leaf(cmd='show redundancy',
                      src='[slot][(?P<slot>{slot_num})][image_ver]',
                      dest='red[rp][(?P<slot>{slot_num})][system_image]')

        # rp_boot_image
        self.add_leaf(cmd='show redundancy',
                      src='[slot][(?P<slot>{slot_num})][boot]',
                      dest='red[rp][(?P<slot>{slot_num})][boot_image]')

        # rp_kickstart_boot_image
        # N/A

        # rp_config_register
        self.add_leaf(cmd='show redundancy',
                      src='[slot][(?P<slot>{slot_num})][config_register]',
                      dest='red[rp][(?P<slot>{slot_num})][config_register]')

        # rp_swstack_role
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][role]',
                      dest='[slot][rp][(?P<slot>.*)][swstack_role]')

        # rp_sn
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][sn]',
                      dest='[slot][rp][(?P<slot>.*)][sn]')

        # rp_pid
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][pid]',
                      dest='[slot][rp][(?P<slot>.*)][pid]')

        # === SubSlotAttributes ===
        # === DaughterCardAttributes ===

        # rp_dc_name
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][name]',
                      dest='[slot][rp][(?P<slot>.*)][subslot][(?P<subslot>.*)][name]')

        # rp_dc_pid
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][pid]',
                      dest='[slot][rp][(?P<slot>.*)][subslot][(?P<subslot>.*)][pid]')

        # rp_dc_state
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][state]',
                      dest='[slot][rp][(?P<slot>.*)][subslot][(?P<subslot>.*)][state]')

        # rp_dc_sn
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][rp][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][sn]',
                      dest='[slot][rp][(?P<slot>.*)][subslot][(?P<subslot>.*)][sn]')

        # === LineCardAttributes ===

        # lc_name
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][lc][(?P<pid>.*)][name]',
                      dest='[slot][lc][(?P<slot>.*)][name]')

        # lc_pid
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][lc][(?P<pid>.*)][pid]',
                      dest='[slot][lc][(?P<slot>.*)][pid]')

        # lc_state
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][lc][(?P<pid>.*)][state]',
                      dest='[slot][lc][(?P<slot>.*)][state]')

        # lc_sn
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][lc][(?P<pid>.*)][sn]',
                      dest='[slot][lc][(?P<slot>.*)][sn]')

        # === SubSlotAttributes ===
        # === DaughterCardAttributes ===

        # lc_dc_name
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][lc][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][name]',
                      dest='[slot][lc][(?P<slot>.*)][subslot][(?P<subslot>.*)][name]')

        # lc_dc_pid
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][lc][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][pid]',
                      dest='[slot][lc][(?P<slot>.*)][subslot][(?P<subslot>.*)][pid]')

        # lc_dc_state
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][lc][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][state]',
                      dest='[slot][lc][(?P<slot>.*)][subslot][(?P<subslot>.*)][state]')

        # lc_dc_sn
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][lc][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][sn]',
                      dest='[slot][lc][(?P<slot>.*)][subslot][(?P<subslot>.*)][sn]')


        # === SwitchProcessorAttributes ===

        # sp_name
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][sp][(?P<pid>.*)][name]',
                      dest='[slot][sp][(?P<slot>.*)][name]')

        # sp_pid
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][sp][(?P<pid>.*)][pid]',
                      dest='[slot][sp][(?P<slot>.*)][pid]')

        # sp_state
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][sp][(?P<pid>.*)][state]',
                      dest='[slot][sp][(?P<slot>.*)][state]')

        # sp_sn
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][sp][(?P<pid>.*)][sn]',
                      dest='[slot][sp][(?P<slot>.*)][sn]')

        # === OtherCardAttributes ===

        # oc_name
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][other][(?P<pid>.*)][name]',
                      dest='[slot][oc][(?P<slot>.*)][name]')

        # oc_pid
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][other][(?P<pid>.*)][pid]',
                      dest='[slot][oc][(?P<slot>.*)][pid]')

        # oc_state
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][other][(?P<pid>.*)][state]',
                      dest='[slot][oc][(?P<slot>.*)][state]')

        # oc_sn
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][other][(?P<pid>.*)][sn]',
                      dest='[slot][oc][(?P<slot>.*)][sn]')

        # === SubSlotAttributes ===
        # === DaughterCardAttributes ===

        # oc_dc_name
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][other][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][name]',
                      dest='[slot][oc][(?P<slot>.*)][subslot][(?P<subslot>.*)][name]')

        # oc_dc_name
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][oc][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][pid]',
                      dest='[slot][oc][(?P<slot>.*)][subslot][(?P<subslot>.*)][name]')

        # oc_dc_state
        self.add_leaf(cmd='show platform', revision='1',
                      src='[slot][(?P<slot>.*)][other][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][state]',
                      dest='[slot][oc][(?P<slot>.*)][subslot][(?P<subslot>.*)][state]')

        # oc_dc_sn
        self.add_leaf(cmd='show inventory', revision='1',
                      src='[slot][(?P<slot>.*)][other][(?P<pid>.*)][subslot][(?P<subslot>.*)][(?P<pid2>.*)][sn]',
                      dest='[slot][oc][(?P<slot>.*)][subslot][(?P<subslot>.*)][sn]')

        self.make(final_call=True)

         # create new tree based on 'active' or 'standby' from 'red' dictionary
        if hasattr(self, 'red'):
            red2 = {}
            for key1 in self.red.keys():
                for key2 in self.red[key1].keys():
                    for k, v in self.red[key1][key2].items():
                        if 'ACTIVE' in v:
                            red2['active'] = self.red[key1][key2]
                        if 'STANDBY HOT' in v:
                            red2['standby'] = self.red[key1][key2]

            # merge 'red2' dict to 'self.name' dict
            name2 = copy.deepcopy(self.slot)
            if red2 and self.slot:
                for k1 in self.slot.keys():
                    for k2 in self.slot[k1].keys():
                                for k, v in self.slot[k1][k2].items():
                                    if 'rp' in k1 and 'active' in v:
                                        name2[k1][k2].update(red2['active'])
                                    if 'rp' in k1 and 'standby' in v:
                                        name2[k1][k2].update(red2['standby'])
                self.slot = name2
                del name2
                del red2
                del self.red

            # change the os type to alias
            if 'IOS-XE' in self.os:
                self.os = 'iosxe'