"""functions for UCD"""

# Python
import logging

log = logging.getLogger(__name__)


def analyze_core_by_ucd(device,
                        core_file,
                        gdb_command='bt full',
                        ucd_command='/ws/cvanka-sjc/ucd/ucd -c',
                        timeout=300):
    """ analyze core by UCD
        # CISCO INTERNAL

        Args:
            device (`obj`): Device object
            core_file (`str`): core file name with path to analyze by UCD
            gdb_command (`str`, optional): gdb command in GDB
                                           Defaults to `bt full`
            ucd_command (`str`, optional): ucd command with path and options
                                           Defaults to `/ws/cvanka-sjc/ucd/ucd -c`
            timeout (`int`, optional): timeout to expire for device.receive()
                                       Defaults to 300 seconds

        Returns:
            out (`str`): Output of UCD
    """

    # initialize
    bt_output = ''
    out = ''

    # execute UCD command
    if device.transmit('{ucd_command} {core_file}\r'.format(
            ucd_command=ucd_command, core_file=core_file)):
        out = device.receive(r".*\(gdb\)", timeout=timeout)
    if out and device.transmit('set pagination off\r'):
        out = device.receive(r".*\(gdb\)", timeout=timeout)
    if out and device.transmit(
            '{gdb_command}\r'.format(gdb_command=gdb_command)):
        out = device.receive(r".*\(gdb\)", timeout=timeout)
        bt_output = device.receive_buffer()

    device.transmit('quit\r')

    return bt_output
