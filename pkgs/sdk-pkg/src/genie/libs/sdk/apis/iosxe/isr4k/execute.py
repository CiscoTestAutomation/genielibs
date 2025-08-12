'''isr4k execute functions'''
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
    try:
         # If the device state is in rommon configure rommon variable
        if device.state_machine.current_state == 'rommon':
            cmd = f'confreg {config_register}'
            device.execute(cmd, timeout=timeout)
        else:
            cmd = f'config-register {config_register}'
            device.configure(cmd, timeout=timeout)
    except Exception as e:
        raise Exception(f"Failed to set config register for '{device.name}'\n{e}")


