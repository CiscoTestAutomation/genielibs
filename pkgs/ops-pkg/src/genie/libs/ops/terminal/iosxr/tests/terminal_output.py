'''ShowTerminal Genie Ops Object Outputs for IOSXR.'''

from genie.conf.base.utils import QDict

class TerminalOutput(object):

    ShowTerminal = QDict({
        'line': 'con0_RP0_CPU0',
        'location': '0/RP0/CPU0',
        'type': 'Console',
        'length': 0,
        'width': 0,
        'baud_rate': {
            'tx': 9600,
            'rx': 9600
        },
        'parity': 'No',
        'stopbits': 2,
        'databits': 8,
        'allowed_transport': [
            'none'
        ]
    })

    # ShowTerminal Info Structure
    ShowTerminalInfo = {
        'line': 'con0_RP0_CPU0',
        'location': '0/RP0/CPU0',
        'type': 'Console',
        'length': 0,
        'width': 0,
        'baud_rate': {
            'tx': 9600,
            'rx': 9600
        },
        'parity': 'No',
        'stopbits': 2,
        'databits': 8,
        'input_transport': [
            'none'
        ],
        'output_transport': [
            'none'
        ]
    }