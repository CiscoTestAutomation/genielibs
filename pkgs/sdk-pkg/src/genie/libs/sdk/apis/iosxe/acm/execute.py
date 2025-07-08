'''IOSXE execute functions for acm'''

# Python
import logging

# Genie
from genie.harness.utils import connect_device
from genie.utils.timeout import Timeout

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import StateMachineError,SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def acm_rules_match_mode(device, mode_name, command_line, action_skip=True, default_mode=False, unconfig_mode=False):
    """ acm rules
        Args:
            device ('obj'): Device object
            mode_name ('str'): mode name ex- mdt-subscription-mode/rogue-rule/main-cpu
            command_line ('str'): command line  ex- no update-policy/no match/no main-cpu
            action_skip (boolean): default True
            default_mode (boolean): default False(default match mode)
            unconfig_mode (boolean): default False(no match mode)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if default_mode:
        cmd = [f'default match mode {mode_name} command {command_line}']
    elif unconfig_mode:
        cmd = [f'no match mode {mode_name} command {command_line}']
    else:
        cmd = [f'match mode {mode_name} command {command_line}']

    if action_skip:
        cmd.append('action skip')

    try:
        device.configure(cmd, rules=True)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure acm rules match mode on {device}. Error:\n{e}"
        )

def acm_confirm_commit(device):
    """ acm confirm-commit
        Args:
            device (`obj`): Device object  
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute('acm confirm-commit')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute acm confirm-commit on {device}. Error:\n{e}"
        )

def acm_cancel_commit(device):
    """ acm cancel-commit
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute('acm cancel-commit')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute acm cancel-commit on {device}. Error:\n{e}"
        )

def acm_rules(device, file_path, vrf_name=None, timeout=90):
    """ acm rules flash:abc 
        Args:
            device ('obj'): Device object
            file_path ('str'): Path of the file ex: flash:abc
            vrf_name ('str'): vrf name optional
            timeout (`str`): timeout in seconds(default 90sec)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if vrf_name:
        cmd = f"acm rules {file_path} vrf {vrf_name}"
    else:
        cmd = f"acm rules {file_path}"
    try:
        device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute acm rules on {device}. Error:\n{e}"
        )


def acm_save(device, path=None, file=None, vrf=None, timeout=60):
        """acm save

        Args:
            device (`obj`): Device object
            path (`str`, optional): Destination path (e.g., SCP/FTP path)
            file (`str`, optional): File name for saving the configuration
            vrf (`str`, optional): VRF to use for the save operation
            timeout (`int`, optional): Timeout in seconds. Default is 60

        Returns:
            None

        Raises:
            SubCommandFailure: If the save operation fails
        """
        dialog = Dialog(
            [
                Statement(
                    pattern=r".*[confirm]",
                    action="sendline()",
                    loop_continue=True,
                    continue_timer=False,
                )
            ]
        )
        try:
            if path and file:
                command = f"acm save {path}{file}"
            else:
                command = "acm save startup-config"

            if vrf:
               command += f" vrf {vrf}"

            device.execute(command, reply=dialog, timeout=timeout)
        except SubCommandFailure as e:
            raise SubCommandFailure("Could not save acm from device""{device}".format(file=file, device=device.name)) 


def acm_rollback(device, sno_number, timeout=60, password=None):
    """ Perform ACM rollback to a checkpoint and commit the config

        Args:
            device (`obj`): Device object with execute method
            sno_number (`int`): rollback checkpoint index (e.g. 1, 2, etc.)
            timeout (`int`, optional): Timeout in seconds. Default is 60
            password (`str`, optional): Password for SCP if prompted

        Returns:
            None

        Raises:
            SubCommandFailure: If rollback or commit fails
    """
    
    dialog = Dialog([
        Statement(pattern=r".*\[confirm\].*",
                  action="sendline()",
                  loop_continue=True,
                  continue_timer=False),
        
        
        Statement(pattern=r'(?i).*password[:\s]*',  
                  action=lambda spawn: spawn.sendline(password) if password else spawn.sendline(''),
                  loop_continue=True,
                  continue_timer=False),
        
        
        Statement(pattern=r".*you may save configuration and re-enter the command\. \[y/n/q\]",
                  action="sendline(y)",
                  loop_continue=True,
                  continue_timer=False),

        Statement(pattern=r".*SUCCESS.*",
                  action=None,
                  loop_continue=False,
                  continue_timer=False),

        Statement(pattern=r".*FAILED.*",
                  action=None,
                  loop_continue=False,
                  continue_timer=False),
    ])

    try:
        log.info(f"Performing ACM rollback to checkpoint {sno_number} on {device.name}.")

        cmd = f"acm rollback {sno_number}"

        output = device.execute(cmd, reply=dialog, timeout=timeout)
        

        log.info(f"Rollback to checkpoint {sno_number} completed on {device.name}")
        
    except Exception as e:
        log.error(f"Failed to rollback to checkpoint {sno_number} on {device.name}: {e}")
        raise SubCommandFailure(f"Failed to rollback to checkpoint {sno_number} on {device.name}: {e}")
    
def acm_configlet_create(device, file_path, vrf_name=None, timeout=90):
    """Create ACM configlet
    Args:
        device ('obj'): Device object
        file_path ('str'): file path ex- flash:abc/tftp://..../abc
        timeout (int): timeout default 90sec
        vrf_name ('str'): vrf name
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if vrf_name:
        cmd = f'acm configlet create {file_path} vrf {vrf_name}'
    else:
        cmd = f'acm configlet create {file_path}'

    try:
        device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not create acm configlet on {device}. Error:\n{e}"
        )

def acm_configlet_remove(device, file_path):
    """Remove ACM configlet
    Args:
        device ('obj'): Device object
        file_path ('str'): file path etc- flash:abc/tftp:abc
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f'acm configlet remove {file_path}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not remove acm configlet on {device}. Error:\n{e}"
        )

def acm_configlet_delete(device, file_path, index_line_num):
    """Delete a line from ACM configlet

    Args:
        device (obj): Device object
        file_path (str): File path (e.g., flash:abc/tftp:abc)
        index_line_num (str): Index number of the configlet file
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"acm configlet modify {file_path} delete {index_line_num}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not delete line from ACM configlet on {device}. Error:\n{e}"
        )

def acm_configlet_insert(device, file_path, index_line_num, insert_data):
    """Insert data into ACM configlet file at a specific index

    Args:
        device (obj): Device object
        file_path (str): File path (e.g., flash:abc/tftp:abc)
        index_line_num (str): Index number of the configlet file
        insert_data (str): Data to insert at the specified index
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"acm configlet modify {file_path} insert {index_line_num} {insert_data}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not insert data into ACM configlet on {device}. Error:\n{e}"
        )

def acm_configlet_replace(device, file_path, index_line_num, replace_data):
    """Replace data in ACM configlet

    Args:
        device (obj): Device object
        file_path (str): File path (e.g., flash:abc/tftp:abc)
        index_line_num (str): Index number of the configlet file
        replace_data (str): Data to replace at the specified index
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"acm configlet modify {file_path} replace {index_line_num} {replace_data}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not replace data in ACM configlet on {device}. Error:\n{e}"
        )
