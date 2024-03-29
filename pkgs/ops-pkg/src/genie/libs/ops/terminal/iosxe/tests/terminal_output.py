'''Terminal Genie Ops Object Outputs for IOSXE.'''

from genie.conf.base.utils import QDict

class TerminalOutput(object):

    ShowTerminal = QDict({
        'line': '0',
        'location': '',
        'type': '',
        'length': 0,
        'width': 0,
        'baud_rate': {
            'tx': 9600,
            'rx': 9600
        },
        'parity': 'no',
        'stopbits': 1,
        'databits': 8,
        'input_transport': [
            'none'
        ],
        'output_transport': [
            'pad',
            'telnet',
            'rlogin',
            'ssh'
        ]
    })

    # ShowTerminal Info Structure
    ShowTerminalInfo = {
        'line': '0',
        'location': '',
        'type': '',
        'length': 0,
        'width': 0,
        'baud_rate': {
            'tx': 9600,
            'rx': 9600
        },
        'parity': 'no',
        'stopbits': 1,
        'databits': 8,
        'input_transport': [
            'none'
        ],
        'output_transport': [
            'pad',
            'telnet',
            'rlogin',
            'ssh'
        ]
    }