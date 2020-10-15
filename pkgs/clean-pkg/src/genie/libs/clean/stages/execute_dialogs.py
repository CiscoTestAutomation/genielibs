'''Common Unicon Statement/Dialogs'''

# Python
import re
import time

# Unicon
from unicon.eal.dialogs import Statement, DialogMaker, statement_decorator


class BreakBootDialog(DialogMaker):
    '''Dialog to stop the device to boot at reload time'''

    @statement_decorator(r'Escape character is .*\n', loop_continue=True, continue_timer=False)
    def escape_char_handler(spawn, session):
        spawn.sendline()
        time.sleep(0.5)

    @statement_decorator(r'^.*Connection refused', loop_continue=True, continue_timer=False)
    def connection_refused_handler(spawn, session):
        '''Handles connection refused scenarios '''
        raise Exception('Connection refused to the device even '
                        'after  clearing the line')


class RommonDialog(DialogMaker):

    # If the device is already on the choose an image screen, we dont
    # want to hit enter as that will boot a random image. sending 'c'
    # will return to the 'grub >' prompt
    @statement_decorator(r'Escape character is .*\n', loop_continue=True, continue_timer=False)
    def escape_char_handler(spawn, session):
        spawn.send('c')
        time.sleep(0.5)
        # '\033' == <ESC>
        spawn.send('\033')
        time.sleep(0.5)

        # check to see if the above worked otherwise hit enter
        spawn.read_update_buffer()
        if re.compile(r'Escape character is .*\n').match(spawn.buffer):
            spawn.sendline()

    @statement_decorator(r'^.*Connection refused', loop_continue=True, continue_timer=False)
    def connection_refused_handler(spawn, session):
        '''Handles connection refused scenarios '''
        raise Exception('Connection refused to the device even '
                        'after  clearing the line')
