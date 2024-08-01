''' Common Config functions for cat8k'''

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement


def configure_autoboot(device):
    """ Configure autoboot
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = 'config-reg 0x2102'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure Autoboot on asr1k device. Error:\n{e}')

    
def configure_breakout_cli(device, port_type, sub_slot='0/2', breakout_type='10g', timeout=60 ):
    """ Configure breakout 
        Args:
            device ('obj'): Device object
            port_type ('str'): Option can be all, native_port_0, native_port_4, native_port_8
            sub_slot ('str',optional): Option can be 0/2
            breakout_type ('str',optional): Option can be 10g
            timeout ('int',optional): option timeout can be in seconds
        Returns:
            None
        Raises:
            SubCommandFailure
    """ 
    
    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Do you want to proceed\?\s+\[confirm\]$',
                action='sendline()',
                loop_continue=True,
                continue_timer=False
            )
        ]
    )
    cmd = f"hw-module subslot {sub_slot} breakout {breakout_type} port {port_type}"

    try:
        device.configure(cmd, reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure breakout on {device.name} device. Error:\n{e}')


def unconfigure_breakout_cli(device, port_type, breakout_type, sub_slot='0/2',timeout=60):
    """ Unconfigure breakout 
        Args:
            device ('obj'): Device object
            port_type ('str'): Option can be all, native_port_0, native_port_4, native_port_8
            sub_slot ('str',optional): Option can be 0/2
            breakout_type ('str'): Option can be none,10g
            timeout ('int',optional): option timeout can be in seconds
        Returns:
            None
        Raises:
            SubCommandFailure
    """ 

    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Do you want to proceed\?\s+\[confirm\]$',
                action='sendline()',
                loop_continue=True,
                continue_timer=False
            )
        ]
    )
    if breakout_type == "10g":
        cmd = f"no hw-module subslot {sub_slot} breakout {breakout_type} port {port_type}"
    else:
        cmd = f"hw-module subslot {sub_slot} breakout {breakout_type} port {port_type}"

    try:
        device.configure(cmd, reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure breakout on {device.name} device. Error:\n{e}')


def configure_mode_change(device, sub_slot, mode_type, timeout=60):
    """ Configure mode change 
        Args:
            device ('obj'): Device object
            sub_slot ('str'): Option can be 0/1, 0/2
            mode_type ('str'): Option can be 10G, 40G, 100G
            timeout ('int',optional): option timeout can be in seconds
        Returns:
            None
        Raises:
            SubCommandFailure
    """ 
    
    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Do you want to proceed\?\s+\[confirm\]$',
                action='sendline()',
                loop_continue=True,
                continue_timer=False
            )
        ]
    )
    cmd = f"hw-module subslot {sub_slot} mode {mode_type}"

    try:
        device.configure(cmd, reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure mode change on {device.name} device. Error:\n{e}')
