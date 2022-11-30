'''
Device Genie Ops Object for Cat9k - CLI.
'''
from genie.libs.ops.device.iosxe.device import Device as SuperDevice
from genie.libs.parser.iosxe.show_platform import ShowBoot

class Device(SuperDevice):
    '''Device Genie Ops Object'''
    
    # Callables
    def learn(self):
        '''Learn Device Ops'''
        self.cmd_leaf_map.pop('show bootvar', None)
        self.cmd_leaf_map.update({'show boot': 'bootvar'})

        info_dest = 'info'

        bootvar_src = '[(?P<bv>.*)]'
        bootvar_dest = '{}[bootvar][(?P<bv>.*)]'.format(info_dest)

        self.add_leaf(
            cmd=ShowBoot,
            src=bootvar_src,
            dest=bootvar_dest)

        self.make()

        super().learn()

