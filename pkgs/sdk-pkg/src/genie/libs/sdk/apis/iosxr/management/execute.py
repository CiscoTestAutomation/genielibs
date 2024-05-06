'''IOSXR execute functions for management'''

# Python
import logging

# Logger
log = logging.getLogger(__name__)

def clear_standby_console(device):
    ''' Clears the standby console line.
    '''

    # RP/0/RP0/CPU0:f3a-r1-pod10#clear line console location ?
    #   0/0/CPU0    Fully qualified location specification
    #   0/1/CPU0    Fully qualified location specification
    #   0/RP0/CPU0  Fully qualified location specification
    #   0/RP1/CPU0  Fully qualified location specification
    #   WORD        Fully qualified location specification

    lines = device.parse('show line').get('tty')
    consoles = [line for line in lines.values() if line['type'] == 'CTY']
    standby_console = [line for line in consoles if line.get('active') is False]
    if standby_console:
        line = standby_console[0].get('tty')
        if line:
            line = line.replace('con', '')
            device.execute(f'clear line console location {line}')
