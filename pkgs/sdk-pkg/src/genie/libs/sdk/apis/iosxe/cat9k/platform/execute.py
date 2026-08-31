# Python
import logging

from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def execute_clear_platform_software_fed_switch_punt_entries(
        device, switch_number, timeout=60):
    """Clear FED punt entry counters for a switch.

    Args:
        device (`obj`): Device object.
        switch_number (`int`): Switch number whose counters are cleared.
        timeout (`int`, optional): Command timeout in seconds. Defaults to 60.

    Returns:
        None

    Raises:
        SubCommandFailure: If the command cannot be executed.
    """
    command = (
        f"show platform software fed switch {switch_number} "
        "punt entries clear"
    )

    try:
        device.execute(command, timeout=timeout)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not clear FED punt entry counters on switch "
            f"{switch_number} for {device.name}. Error:\n{error}"
        ) from error


def execute_set_config_register(device, config_register, timeout=300):
    '''Set config register to load image in boot variable
        Args:
            device ('obj'): Device object
            config_register ('str'): Hexadecimal value to set the config register to
            timeout ('int'): Max time to set config-register in seconds
    '''
    # Collect all connections to process
    conn_list = getattr(device, 'subconnections', None) or [device.default]

    log.warning("Setting manual boot on device instead of executing config register")

    # Iterate through each connection to apply the configuration.
    for conn in conn_list:
        try:
            # If the device state is in rommon configure rommon variable
            if conn.state_machine.current_state == 'rommon':
                cmd = f'MANUAL_BOOT=YES'
                conn.execute(cmd, timeout=timeout)
            # If the device is in standby state, skip it.
            # Otherwise, the standby will fail if locked.
            elif conn.role == "standby":
                continue
            else:
                cmd = f'boot manual'
                conn.configure(cmd, timeout=timeout)
        except Exception as e:
            raise Exception("Failed to set boot manual for '{d}'\n{e}".\
                            format(d=device.name, e=str(e)))
