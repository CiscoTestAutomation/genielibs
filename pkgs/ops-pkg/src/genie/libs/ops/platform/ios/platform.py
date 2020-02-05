# super class
from genie.libs.ops.platform.platform import Platform as SuperPlatform
from genie.libs.ops.utils.common import convert_to_lower
# Genie Parsers

class Platform(SuperPlatform):
    """Platform Ops Object"""

    def learn(self):
        """Learn Platform object"""

        # === ShowVersion ===
        # chassis
        # chassis_sn
        # rtr_type
        # os
        # version
        # image
        # config_register
        # main_mem
        for key in ['chassis', 'chassis_sn', 'rtr_type',
                    'version', 'system_image', 'curr_config_register', 'main_mem']:
            if key == 'system_image':
                dest_key = 'image'
            elif key == 'curr_config_register':
                dest_key = 'config_register'
            else:
                dest_key = key
            self.add_leaf(cmd='show version',
                          src='[version][{key}]'.format(key=key),
                          dest='[{key}]'.format(key=dest_key))

        self.add_leaf(cmd='show version',
                      src='[version][os]',
                      dest='[os]',
                      action=convert_to_lower)

        # === Dir ===
        # dir
        self.add_leaf(cmd='dir',
                      src='[dir][dir]',
                      dest='[dir]')

        # === ShowRedundancy ===
        # redundancy_mode               N/A
        # switchover_reason             N/A
        # redundancy_communication      N/A

        # === ShowInventory ===
        # swstack
        self.add_leaf(cmd='show inventory',
                      src='[main][swstack]',
                      dest='[swstack]')

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

        # === ShowPlatform, ShowInventory ===
        # slot
        #   rp
        #       slot
        #            name               N/A
        #            state              N/A
        #            swstack_role       N/A
        rp_src = '[slot][(?P<slot>.*)][rp][(?P<pid>.*)]'
        rp_dest = '[slot][rp][(?P<slot>.*)]'

        # === ShowRedundancy ===
        #            redundancy_state   N/A
        #            uptime             N/A
        #            system_image       N/A
        #            boot_image         N/A
        #            config_register    N/A

        # === ShowInventory, ShowPlatform ===
        #            sn                 N/A
        #            subslot            
        #               subslot         
        #                   name        
        #                   state       N/A
        #                   sn
        self.add_leaf(cmd='show inventory',
                      src=rp_src+'[subslot][(?P<subslot>.*)][(?P<pid2>.*)][pid]',
                      dest=rp_dest+'[subslot][(?P<subslot>.*)][name]')

        self.add_leaf(cmd='show inventory',
                      src=rp_src+'[subslot][(?P<subslot>.*)][(?P<pid2>.*)][sn]',
                      dest=rp_dest+'[subslot][(?P<subslot>.*)][sn]')

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
        #           state       N/A
        #           sn
        other_src = '[slot][(?P<slot>.*)][other][(?P<pid>.*)]'
        other_dest = '[slot][oc][(?P<slot>.*)]'

        for key in ['name', 'state', 'sn']:
            self.add_leaf(cmd='show inventory',
                          src=other_src+'[{key}]'.format(key=key),
                          dest=other_dest+'[{key}]'.format(key=key))

        self.make(final_call=True)