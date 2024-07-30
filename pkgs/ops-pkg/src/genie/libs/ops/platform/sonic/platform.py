'''
Genie Ops Object for sonic.
'''
# super class
from genie.libs.ops.platform.platform import Platform as SuperPlatform

class Platform(SuperPlatform):
    '''Platform Ops Object'''

    def learn(self):
        '''Learn Platform object'''

        # Place holder to make it more readable
        src_ver = ''

        # === DeviceAttributes ===

        # os
        self.add_leaf(cmd='show version',
                      src=src_ver + '[sonic_os_version]',
                      dest='os')
        
        # version
        self.add_leaf(cmd='show version',
                      src=src_ver + '[sonic_software_version]',
                      dest='version')

        # chassis
        self.add_leaf(cmd='show platform inventory',
                      src='[chassis][(?P<chassis>.*)][product_id]',
                      dest='chassis')
        
        # chassis_sn
        self.add_leaf(cmd='show platform inventory',
                      src='[chassis][(?P<chassis>.*)][serial_num]',
                      dest='chassis_sn')
        
        # slot section
        # rp name
        self.add_leaf(cmd='show platform inventory',
                      src='[rp][(?P<rp>.*)][name]',
                      dest='[slot][rp][(?P<rp>.*)][name]')
        
        # rp serial_num
        self.add_leaf(cmd='show platform inventory',
                      src='[rp][(?P<rp>.*)][serial_num]',
                      dest='[slot][rp][(?P<rp>.*)][sn]')

        self.make(final_call=True)

        