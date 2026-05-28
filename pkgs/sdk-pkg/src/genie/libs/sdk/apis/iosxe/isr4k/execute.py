'''isr4k execute functions'''
import logging

# Logger
log = logging.getLogger(__name__)


def execute_rommon_reset(device, timeout=300):
    '''To execute the reset command in rommon mode
        Args:
            device ('obj'): Device object
            timeout ('int'): Max time to set config-register in seconds
    '''

    # If the device state is in rommon configure rommon variable
    if device.state_machine.current_state == 'rommon':
        try:
            device.execute("reset", timeout=timeout)
        except Exception as e:
            raise Exception(f"Failed to execute reset for '{device.name}'\n{e}")
    else:
        log.info(f"Device '{device.name}' is not in rommon mode; current state is '{device.state_machine.current_state}'. Skipping rommon reset.")
