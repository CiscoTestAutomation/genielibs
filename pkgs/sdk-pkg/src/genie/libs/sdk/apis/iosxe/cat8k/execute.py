'''cat8k execute functions'''
import logging

# Logger
log = logging.getLogger(__name__)


def execute_rommon_reset(device, timeout=300):
    '''To execute the reset command in rommon mode
        Args:
            device ('obj'): Device object
            timeout ('int'): Max time to set config-register in seconds
    '''
    # Collect all connections to process
    conn_list = getattr(device, 'subconnections', None) or [device.default]

    # Iterate through each connection to apply the configuration.
    for conn in conn_list:
        # If the device state is in rommon configure rommon variable
        if conn.state_machine.current_state == 'rommon':
            try:
                conn.execute("reset", timeout=timeout)
            except Exception as e:
                raise Exception(f"Failed to execute reset for '{device.name}'\n{e}")

        else:
            log.info(f"Device '{device.name}' is not in rommon mode; current state is '{conn.state_machine.current_state}'. Skipping rommon reset.")

