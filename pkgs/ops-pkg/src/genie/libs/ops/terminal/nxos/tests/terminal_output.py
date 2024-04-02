'''ShowTerminal Genie Ops Object Outputs for IOSXR.'''

from genie.conf.base.utils import QDict

class TerminalOutput(object):

    ShowTerminal = QDict({
        'tty': '/dev/ttyS0',
        'type': 'vt102',
        'length': 0,
        'width': 511
    })

    # ShowTerminal Info Structure
    ShowTerminalInfo = {
        'line': '/dev/ttyS0',
        'type': 'vt102',
        'length': 0,
        'width': 511
    }