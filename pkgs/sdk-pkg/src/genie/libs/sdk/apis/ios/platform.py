import logging

log = logging.getLogger(__name__)

def execute_clear_line(device, line):
    device.execute('clear line {l}'.format(l=line),
                   error_pattern=['not available for clearing'])
