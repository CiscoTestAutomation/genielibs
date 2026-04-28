'''ie3k execute functions'''

import logging
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)


def execute_rommon_reset(device, timeout=300):
    '''Execute the reset command in rommon mode.

    Args:
        device ('obj'): Device object.
        timeout ('int'): Max time to set config-register in seconds.

    Returns:
        None

    Raises:
        Exception: If failed to execute reset command in rommon mode.
    '''
    dialog = Dialog([
        Statement(
            pattern=r'Are you sure you want to reset the system \(y/n\)\?',
            action='sendline(y)',
            loop_continue=True,
            continue_timer=False,
        )
    ])

    # Collect all connections to process
    conn_list = getattr(device, 'subconnections', None) or [device.default]

    # Iterate through each connection to apply the configuration.
    for conn in conn_list:
        if conn.state_machine.current_state == 'rommon':
            try:
                conn.execute("reset", reply=dialog, timeout=timeout)
            except Exception as e:
                raise Exception(f"Failed to execute reset for '{device.name}'\n{e}")
        else:
            log.info(
                f"Device '{device.name}' is not in rommon mode;"
                f" current state is '{conn.state_machine.current_state}'."
                f" Skipping rommon reset."
            )
