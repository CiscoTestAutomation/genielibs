'''asr1k execute functions'''
import logging

# Logger
log = logging.getLogger(__name__)

def execute_set_config_register(device, config_register, timeout=300):
    '''Set config register to load image in boot variable
        Args:
            device ('obj'): Device object
            config_register ('str'): Hexadecimal value to set the config register to
            timeout ('int'): Max time to set config-register in seconds
    '''
    # Collect all connections to process
    conn_list = getattr(device, 'subconnections', None) or [device.default]

    # Iterate through each connection to apply the configuration.
    for conn in conn_list:
        try:
            # If the device state is in rommon configure rommon variable
            if conn.state_machine.current_state == 'rommon':
                cmd = f'confreg {config_register}'
                conn.execute(cmd, timeout=timeout)
            else:
                cmd = f'config-register {config_register}'
                conn.configure(cmd, timeout=timeout)
        except Exception as e:
            raise Exception("Failed to set config register for '{d}'\n{e}".\
                            format(d=device.name, e=str(e)))


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

