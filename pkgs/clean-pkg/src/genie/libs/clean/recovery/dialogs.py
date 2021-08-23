'''Common Unicon Statement/Dialogs'''

# Python
import time

# Unicon
from unicon.eal.dialogs import DialogMaker, statement_decorator


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

    @statement_decorator(r'Escape character is .*\n', loop_continue=True, continue_timer=False)
    def escape_char_handler(spawn, session):
        time.sleep(0.5)
        spawn.sendline()

    @statement_decorator(r'^.*Connection refused', loop_continue=True, continue_timer=False)
    def connection_refused_handler(spawn, session):
        '''Handles connection refused scenarios '''
        raise Exception('Connection refused to the device even '
                        'after  clearing the line')
