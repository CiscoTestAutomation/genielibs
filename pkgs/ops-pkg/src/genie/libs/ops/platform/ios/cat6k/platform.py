# Genie package
import re
import copy
# super class
from genie.libs.ops.platform.platform import Platform as SuperPlatform
from genie.libs.ops.utils.common import convert_to_bool, \
                                        convert_to_lower
from genie.libs.parser.ios.cat6k import show_platform


class Platform(SuperPlatform):
    """Platform Ops Object"""
    def slot_num(self, item):
        p = re.compile(r'.*(?P<slot>\d+)')
        m = p.match(item)
        if m:
            item = m.groupdict()['slot']
        return item

    def learn(self):
        """Learn Platform object"""
        # Global callable
        self.callables = {'slot_num': self.slot_num}

        # === ShowVersion ===
        # chassis
        # chassis_sn        N/A
        # rtr_type          N/A
        # os
        # version
        # image
        # config_register
        # main_mem
        for key in ['chassis', 'version', 'system_image',
                    'curr_config_register', 'main_mem']:
            if key == 'system_image':
                dest_key = 'image'
            elif key == 'curr_config_register':
                dest_key = 'config_register'
            else:
                dest_key = key
            self.add_leaf(cmd=show_platform.ShowVersion,
                          src='[version][{key}]'.format(key=key),
                          dest='[{key}]'.format(key=dest_key))

        # will update value in bottom logic
        self.add_leaf(cmd=show_platform.ShowVersion,
                      src='[version][chassis]',
                      dest='[rtr_type]')

        self.add_leaf(cmd=show_platform.ShowVersion,
                      src='[version][os]',
                      dest='[os]',
                      action=convert_to_lower)

        # === Dir ===
        # dir
        self.add_leaf(cmd=show_platform.Dir,
                      src='[dir][dir]',
                      dest='[dir]')

        # === ShowRedundancy ===
        # redundancy_mode
        # switchover_reason
        # redundancy_communication
        red_sys_keys = {
            'oper_red_mode': 'redundancy_mode',
            'last_switchover_reason': 'switchover_reason',
        }
        for k, v in red_sys_keys.items():
            self.add_leaf(cmd=show_platform.ShowRedundancy,
                          src='[red_sys_info][{k}]'.format(k=k),
                          dest='{v}'.format(v=v))

        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[red_sys_info][communications]',
                      dest='redundancy_communication',
                      action=convert_to_bool)

        # === ShowInventory ===
        # swstack                       N/A

        # === show_issu.ShowIssuRollbackTimer ===
        # issu_rollback_timer_state     N/A
        # issu_rollback_timer_reason    N/A

        # === Not found in parser module===
        # virtual_device                N/A
        #   vd_id                       N/A
        #       name                    N/A
        #       status                  N/A
        #       membership              N/A
        #           vd_ms_name          N/A
        #               type            N/A
        #               status          N/A

        # === ShowModule, ShowInventory ===
        # slot
        #   rp
        #       slot
        #            name               N/A
        #            state              N/A
        #            swstack_role       N/A
        rp_src = '[slot][(?P<slot>.*)][rp][(?P<pid>.*)]'
        rp_dest = '[slot][rp][(?P<slot>.*)]'

        # === ShowRedundancy ===
        #            redundancy_state
        #            uptime
        #            system_image
        #            boot_image         N/A
        #            config_register    N/A
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[slot][(?P<slot>{slot_num})][curr_sw_state]',
                      dest='red[(?P<slot>{slot_num})][redundancy_state]',
                      action=convert_to_lower)

        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[slot][(?P<slot>{slot_num})][uptime_in_curr_state]',
                      dest='red[(?P<slot>{slot_num})][uptime]')

        # rp_system_image
        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[slot][(?P<slot>{slot_num})][image_ver]',
                      dest='red[(?P<slot>{slot_num})][system_image]')

        self.add_leaf(cmd=show_platform.ShowRedundancy,
                      src='[slot][(?P<slot>{slot_num})][config_register]',
                      dest='red[(?P<slot>{slot_num})][config_register]')

        # === ShowInventory, ShowModule ===
        #            sn                 N/A
        #            subslot            N/A
        #               subslot         N/A
        #                   name        N/A
        #                   state       N/A
        #                   sn          N/A

        # === show_issu.ShowIssuStateDetail ===
        #            issu                           N/A
        #                in_progress                N/A
        #                last_operation             N/A
        #                terminal_state_reached     N/A
        #                runversion_executed        N/A

        # === ShowPlatform ===
        #   lc                          N/A
        #       slot                    N/A
        #           name                N/A
        #           state               N/A
        #           sn                  N/A
        #           subslot             N/A
        #               subslot         N/A
        #                   name        N/A
        #                   state       N/A
        #                   sn          N/A

        # === ShowInventory ===
        #   oc
        #       slot
        #           name
        #           state
        #           sn
        for key in ['name', 'descr', 'pid', 'vid', 'sn']:
            self.add_leaf(cmd=show_platform.ShowInventory,
                          src='[index][(?P<index>.*)][{key}]'.format(key=key),
                          dest='[slot][(?P<index>.*)][{key}]'.format(key=key))

        self.make(final_call=True)

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
            elif 'C6' in self.chassis:
                self.rtr_type = 'CAT6K'
            else:
                self.rtr_type = self.chassis

        # Creating a dictionary holder
        slot_dict = {}
        sub_dicts = {}
        slots_list = []

        if hasattr(self, 'slot'):
            for s in self.slot:
                descr = self.slot[s]['descr']
                name = self.slot[s]['name']
                pid = self.slot[s]['pid']

                # get slot lable from name
                # 1
                slot_label_match = re.compile(r'^(?P<slot_label>\d+)$')

                if slot_label_match.match(name):
                    slot_label = slot_label_match.match(name).groupdict()['slot_label']

                # Cisco Systems Catalyst 6500 3-slot Chassis System
                if 'Chassis' in descr:
                    continue

                # ========================================
                #         oc
                # ========================================
                # WS-C6503-E-FAN 1
                # PS 1 PWR-1400-AC
                oc_name_pattern = re.compile(r'.*[PWR|FAN|CLK].*')
                if oc_name_pattern.match(name):
                    slot_label = name
                    for key in self.slot[s]:
                        if key in ['name', 'state', 'sn']:
                            slot_dict.setdefault('oc', {}).\
                                     setdefault(slot_label, {}).\
                                     setdefault(key, self.slot[s][key])

                    continue

                # ========================================
                #         subslot
                # ========================================
                # switching engine sub-module of 2
                elif 'sub-module' in name:
                    subslot_match = re.compile(r'.* sub-module of (?P<slot>\d+)')
                    slot = subslot_match.match(name).groupdict()['slot']

                    # subslot_content example:
                    # {
                    #     'WS-F6K-PFC3BXL': {
                    #         'name': 'switching engine sub-module of 1',
                    #         'sn': 'SAL11434LYG'
                    #     }
                    # }
                    subslot_content = {}
                    for key in self.slot[s]:
                        if key in ['name', 'state', 'sn']:
                            subslot_content.setdefault(name, {}).\
                                            setdefault(key, self.slot[s][key])

                    # check if the slot exists
                    if slot in slots_list:
                        # merge subslot dictionaries that have same slot
                        sub_dicts[slot].update(subslot_content)

                    else:
                        slots_list.append(slot)
                        sub_dicts.update({slot: subslot_content})

                    # sub_dicts example:
                    # {'1': {
                    #       'WS-F6K-PFC3BXL': {
                    #           'name': 'switching engine sub-module of 1',
                    #           'sn': 'SAL11434LYG'},
                    #       'WS-SUP720': {
                    #           'name': 'msfc sub-module of 1',
                    #           'sn': 'SAL11434N9G'}},
                    #  '2': {
                    #       'WS-F6700-DFC3CXL': {
                    #           'name': 'switching engine sub-module of 2',
                    #           'sn': 'SAL1214LAG5'}}}
                    continue

                # ========================================
                #         lc
                # ========================================
                # WS-X6748-GE-TX
                elif '-X' in pid:
                    for key in self.slot[s]:
                        if key in ['name', 'state', 'sn']:
                            slot_dict.setdefault('lc', {}).\
                                     setdefault(slot_label, {}).\
                                     setdefault(key, self.slot[s][key])

                        # feed subslot
                        if name in sub_dicts.keys():
                            lc_sub_dict = sub_dicts[name]
                            slot_dict['lc'][slot_label].update({'subslot': lc_sub_dict})
                    continue

                # ========================================
                #         rp
                # ========================================
                # WS-SUP720-3BXL 2 ports Supervisor Engine 720 Rev. 5.6
                elif 'Supervisor' in descr:
                    for key in self.slot[s]:
                        if key in ['name', 'state', 'sn']:
                            slot_dict.setdefault('rp', {}).\
                                     setdefault(slot_label, {}).\
                                     setdefault(key, self.slot[s][key])

                            # feed subslot
                            if name in sub_dicts.keys():
                                rp_sub_dict = sub_dicts[name]
                                slot_dict['rp'][slot_label].update({'subslot': rp_sub_dict})
                    continue

        self.slot = slot_dict

        # Assign redundancy to the corresponding rp slot
        if hasattr(self, 'red'):
            for red in self.red:
                if 'rp' in self.slot:
                    if red in self.slot['rp'].keys():
                        for key in self.red[red]:
                            self.slot['rp'][red][key] = self.red[red][key]

            del self.red

        # change the os type to alias
        if hasattr(self, 'os') and 'ios' in self.os:
            self.os = 'ios'