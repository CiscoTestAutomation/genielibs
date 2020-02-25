# Genie package
import re
import copy
# super class
from genie.libs.ops.platform.platform import Platform as SuperPlatform

# Genie Parsers
from genie.libs.parser.iosxe.show_platform import Dir
from genie.libs.parser.iosxe.c9500 import show_platform
from genie.libs.parser.iosxe.c9500.show_issu import ShowIssuStateDetail,\
                                                    ShowIssuRollbackTimer


class Platform(SuperPlatform):
    '''Platform Ops Object'''

    ########################################################################
    #                               info
    ########################################################################
    # chassis
    # chassis_sn
    # rtr_type
    # os
    # version
    # image
    # config_register
    # main_mem
    # dir
    # redundancy_mode
    # switchover_reason
    # redundancy_communication
    # swstack                              N/A
    # issu_rollback_timer_state
    # issu_rollback_timer_reason
    # virtual_device                       N/A
    #     vd_id                            N/A
    #         name                         N/A
    #         status                       N/A
    #         membership                   N/A
    #             vd_ms_type               N/A
    #                 type                 N/A
    #                 status               N/A

    # Callables
    def slot_num(self, item):
        p = re.compile(r'.*(?P<slot>\d+)')
        m = p.match(item)
        if m:
            item = m.groupdict()['slot']
        return item

    def convert_to_bool(self, item):
        if item and 'up' in item.lower():
            return True
        else:
            return False

    def convert_to_lower(self, item):
        return item.lower()

    def learn(self):
        '''Learn Platform object'''

        # Global callable
        self.callables = {'slot_num': self.slot_num}

        # Place holder to make it more readable
        src_ver = '[version]'

        # === DeviceAttributes ===
        # chassis
        self.add_leaf(cmd=show_platform.ShowVersion,
                      src=src_ver + '[chassis]',
                      dest='chassis')

        self.add_leaf(cmd=show_platform.ShowVersion,
                      src=src_ver + '[system_sn]',
                      dest='chassis_sn')

        # rtr_type
        self.add_leaf(cmd=show_platform.ShowVersion,
                      src=src_ver + '[chassis]',
                      dest='rtr_type')

        # os
        self.add_leaf(cmd=show_platform.ShowVersion,
                      src=src_ver + '[os]',
                      dest='os')

        # version
        self.add_leaf(cmd=show_platform.ShowVersion,
                      src=src_ver + '[version]',
                      dest='version')

        # image
        self.add_leaf(cmd=show_platform.ShowVersion,
                      src=src_ver + '[system_image]',
                      dest='image')

        # kickstart_version
        # N/A

        # kickstart_image
        # N/A

        # installed_packages
        # N/A

        # config_register
        self.add_leaf(cmd=show_platform.ShowVersion,
                      src=src_ver + '[curr_config_register]',
                      dest='config_register')

        # main_mem
        self.add_leaf(cmd=show_platform.ShowVersion,
                      src=src_ver + '[main_mem]',
                      dest='main_mem')

        # dir
        self.add_leaf(cmd=Dir,
                      src='[dir][dir]',
                      dest='dir')

        # redundancy_mode
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[red_sys_info][oper_red_mode]',
                      dest='redundancy_mode')

        # switchover_reason
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[red_sys_info][last_switchover_reason]',
                      dest='switchover_reason')

        # redundancy_communication
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[red_sys_info][communications]',
                      dest='redundancy_communication',
                      action=self.convert_to_bool)

        # issu_rollback_timer_state
        self.add_leaf(cmd=ShowIssuRollbackTimer,
                      src='[rollback_timer_state]',
                      dest='issu_rollback_timer_state')

        # issu_rollback_timer_reason
        self.add_leaf(cmd=ShowIssuRollbackTimer,
                      src='[rollback_timer_reason]',
                      dest='issu_rollback_timer_reason')

        ########################################################################
        #                               slot
        ########################################################################
        # rp
        #     slot
        #         name
        #         state
        #         swstack_role                    N/A
        #         redundancy_state
        #         uptime
        #         system_image
        #         boot_image
        #         config_register
        #         sn
        #         subslot
        #             subslot
        #                 name
        #                 state
        #                 sn
        #         issu
        #             in_progress
        #             last_operation
        #             terminal_state_reached
        #             runversion_executed
        # lc
        #     slot
        #         name
        #         state
        #         sn
        #         subslot
        #             subslot
        #                 name
        #                 state
        #                 sn
        # oc
        #     slot
        #         name
        #         state
        #         sn


        #  name
        #  state
        #  insert_time
        #  slot
        #  cpld_ver
        #  fw_ver
        #  subslot
        keys = ['name', 'state', 'insert_time', 'slot', 'cpld_ver', 'fw_ver', 'subslot']
        for key in keys:
            self.add_leaf(cmd=show_platform.ShowPlatform,
                          src='[slot][(?P<slot>.*)][{key}]'.format(key=key),
                          dest='[slot][(?P<slot>.*)][{key}]'.format(key=key))

        # rp_redundancy_state
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[slot][(?P<slot>{slot_num})][curr_sw_state]',
                      dest='red[(?P<slot>{slot_num})][redundancy_state]',
                      action=self.convert_to_lower)

        # rp_uptime
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[slot][(?P<slot>{slot_num})][uptime_in_curr_state]',
                      dest='red[(?P<slot>{slot_num})][uptime]')

        # rp_system_image
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[slot][(?P<slot>{slot_num})][image_ver]',
                      dest='red[(?P<slot>{slot_num})][system_image]')

        # rp_boot_image
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[slot][(?P<slot>{slot_num})][boot]',
                      dest='red[(?P<slot>{slot_num})][boot_image]')

        # rp_kickstart_boot_image
        # N/A

        # rp_config_register
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[slot][(?P<slot>{slot_num})][config_register]',
                      dest='red[(?P<slot>{slot_num})][config_register]')

        #  name
        #  descr
        #  pid
        #  vid
        #  sn
        keys = ['name', 'descr', 'pid', 'vid', 'sn']
        for key in keys:
            self.add_leaf(cmd=show_platform.ShowInventory,
                          src='[index][(?P<index>.*)][{key}]'.format(key=key),
                          dest='[slot][(?P<index>.*)][{key}]'.format(key=key))

        # === issu ===
        # issu
        #   in_progress
        #   last_operation
        for src_key in ['issu_in_progress', 'last_operation']:
            dest_key = src_key if src_key != 'issu_in_progress' else 'in_progress'
            self.add_leaf(cmd=ShowIssuStateDetail,
                      src='[slot][(?P<slot>.*)][{key}]'.format(key=src_key),
                      dest='[slot][(?P<slot>.*)][issu][{key}]'.format(key=dest_key))

        self.make(final_call=True)
        # Creating a dictionary holder
        new_dict= {}
        interface_match = re.compile(r'\S+(?P<slot>\d)\/(?P<subslot>\d+\/\d+)$')
        power_match = re.compile(r'Power +Supply +Module +(?P<slot>\d+)$')
        supervisor_match = re.compile(r'Slot +(?P<supervisor_slot>\d+) +Supervisor$')
        fan_match = re.compile(r'Fan +Tray +(?P<fan_slot>\d+)$')

        # Assign rtr_type as per the corresponding platform
        if hasattr(self, 'chassis'):
            if 'C3' in self.chassis:
                self.rtr_type = 'Edison'
            elif 'ASR1' in self.chassis:
                self.rtr_type = 'ASR1K'
            elif 'CSR1000V' in self.chassis:
                self.rtr_type = 'CSR1000V'
            elif 'C11' in self.chassis:
                self.rtr_type = 'ISR'
            elif 'C9' in self.chassis:
                self.rtr_type = 'C9500'
            else:
                self.rtr_type = self.chassis

        if hasattr(self, 'slot'):
            for slot in self.slot:
                if 'name' in self.slot[slot]:
                    ret_key = self.slot[slot]['name']
                elif 'pid' in self.slot[slot]:
                    ret_key = self.slot[slot]['pid']

                # Logic as per the platform
                # Need to support all IOSXE platforms
                if 'Chassis' in ret_key:
                    continue
                elif 'C9500' in ret_key:
                    for key in self.slot[slot]:
                        if key in ['descr', 'pid', 'vid', 'cpld_ver', 'fw_ver', 'insert_time', 'slot']:
                            continue
                        new_dict.setdefault('rp', {}).setdefault(str(slot), {}).setdefault(key, self.slot[slot][key])
                        if 'subslot' in new_dict['rp'][str(slot)]:
                            for subslot in self.slot[slot][key]:
                                if new_dict.get('rp').get(str(slot)).get('subslot').get(subslot).get('insert_time', None):
                                    del new_dict['rp'][str(slot)]['subslot'][subslot]['insert_time']
                                if new_dict.get('rp').get(str(slot)).get('subslot').get(subslot).get('subslot', None):
                                    del new_dict['rp'][str(slot)]['subslot'][subslot]['subslot']
                elif 'Supervisor' in ret_key:
                    res = supervisor_match.match(ret_key)
                    supervisor_slot = res.groupdict()['supervisor_slot']
                    for key in self.slot[slot]:
                        if key in ['descr', 'pid', 'vid', 'cpld_ver', 'fw_ver', 'insert_time', 'slot']:
                            continue
                        new_dict.setdefault('rp', {}).setdefault(supervisor_slot, {}).setdefault(key, self.slot[slot][key])
                elif 'Power' in ret_key:
                    res = power_match.match(ret_key)
                    power_slot = 'P{}'.format(res.groupdict()['slot'])
                    for key in self.slot[slot]:
                        if key in ['descr', 'pid', 'vid', 'cpld_ver', 'fw_ver', 'insert_time', 'slot']:
                            continue
                        new_dict.setdefault('oc', {}).setdefault(power_slot, {}).setdefault(key, self.slot[slot][key])
                elif('HundredGigE' in ret_key) or ('FortyGigabitEthernet' in ret_key):
                    res = interface_match.match(ret_key)
                    for key in self.slot[slot]:
                        if key in ['descr', 'pid', 'vid']:
                            continue
                        new_dict.setdefault('rp', {}).setdefault(res.groupdict()['slot'], {}).\
                            setdefault('subslot', {}).setdefault(res.groupdict()['subslot'], {}).setdefault(key, self.slot[slot][key])
                else:
                    res = fan_match.match(ret_key)
                    if res:
                        continue
                    for key in self.slot[slot]:
                        if key in ['descr', 'pid', 'vid', 'insert_time', 'slot']:
                            continue
                        new_dict.setdefault('oc', {}).setdefault(str(slot), {}).setdefault(key, self.slot[slot][key])

        self.slot = new_dict

        # Assign redundancy to the corresponding rp slot
        if hasattr(self, 'red'):
            for red in self.red:
                if red in self.slot['rp'].keys():
                    for key in self.red[red]:
                        self.slot['rp'][red][key] = self.red[red][key]

            del self.red

        # change the os type to alias
        if hasattr(self, 'os') and 'IOS-XE' in self.os:
            self.os = 'iosxe'
