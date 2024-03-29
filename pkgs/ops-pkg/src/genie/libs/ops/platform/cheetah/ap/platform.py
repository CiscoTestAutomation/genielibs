'''
Genie Ops Object for CHEETAH/AP - CLI.
'''
# super class
from genie.libs.ops.platform.platform import Platform as SuperPlatform

class Platform(SuperPlatform):
    '''Platform Ops Object'''

    def learn(self):
        '''Learn Platform object'''

        # Place holder to make it more readable
        src_ver = '[version]'

        # === DeviceAttributes ===

        # chassis
        self.add_leaf(cmd='show version',
                      src=src_ver + '[chassis]',
                      dest='chassis')

        self.add_leaf(cmd='show version',
                      src=src_ver + '[processor_board_id]',
                      dest='chassis_sn')

        # os
        self.add_leaf(cmd='show version',
                      src=src_ver + '[os]',
                      dest='os')

        # version
        self.add_leaf(cmd='show version',
                      src=src_ver + '[ap_running_image]',
                      dest='version')

        # main_mem
        self.add_leaf(cmd='show version',
                      src=src_ver + '[main_mem]',
                      dest='main_mem')

        self.make(final_call=True)
