'''IOSXE execute functions for platform-licensing'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def license_smart_factory_reset(device):
    """ Clears licensing information from the trusted store and memory
        Example : license smart factory reset

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Clearing licensing info on {device.name}')
    config = 'license smart factory reset'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to clear licensing info on device {device.name}. Error:\n{e}')

def disable_debug_all(device):
    """ Turns off debugging
        Example : no debug all

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Turns off debugging on {device.name}')
    config = 'no debug all'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to turn off debugging on device {device.name}. Error:\n{e}')

def enable_license_smart_authorization_return(device, device_type, mode, path_name=''):
    """ Enable license smart authorization return
        Example : license smart authorization return all online

        Args:
            device ('obj'): device to use
            device_type ('str'): type of device for authorization code return (eg. all, local)
            mode ('str'): authorization code return mode (eg. offline, online)
            path_name ('str'): offline path name
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Enable license smart authorization return on {device.name}')
    if mode.lower() == "offline":
        config = f'license smart authorization return {device_type} {mode} {path_name}'
    else:
        config = f'license smart authorization return {device_type} {mode}'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to enable license smart authorization on device {device.name}. Error:\n{e}')

def enable_license_smart_clear_eventlog(device):
    """ Enable license smart clear eventlog
        Example : license smart clear eventlog

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Enable license smart clear eventlog on {device.name}')
    config = 'license smart clear eventlog'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to enable license smart clear eventlog on device {device.name}. Error:\n{e}')

def execute_license_smart_save_usage_all_file(device, path):
    """ Executes license smart save usage all file
        Example : license smart save usage all file bootflash:test.txt
        Args:
            device ('obj'): device to use
            path ('str'): Absolute path to the file, including the filename (eg. bootflash:test.txt)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f'License smart save usage all file {path} on {device.name}')
    cmd = f'license smart save usage all file {path}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to license smart save usage all file on device {device.name}. Error:\n{e}'
        )

def execute_more_file_count(device, filepath, regex):
    """ Executes more file <filepath> | count <regex>
        Example : more bootflash:test.txt | count Ready
        Args:
            device ('obj'): device to use
            filepath ('str'): path to the file, including the filename (eg. bootflash:test.txt)
            regex ('str'): regular expression for the count (eg. Ready)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f'Executing more {filepath} | count {regex} on {device.name}')
    cmd = f'more {filepath} | count {regex}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to execute more {filepath} | count {regex} on device {device.name}. Error:\n{e}'
        )

def execute_license_smart_save_usage_unreported_file(device, path):
    """ Executes license smart save usage unreported file
        Example : license smart save usage unreported file bootflash:test.txt
        Args:
            device ('obj'): device to use
            path ('str'): Absolute path to the file, including the filename (eg. bootflash:test.txt)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f'Executing license smart save usage unreported file {path} on {device.name}')
    cmd = f'license smart save usage unreported file {path}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to execute license smart save usage unreported file {path} on device {device.name}. Error:\n{e}'
        )

def execute_license_smart_trust_idtoken(device, token_value, device_type):
    """ Configures license smart trust idtoken
        Example : license smart trust idtoken test all force
        Args:
            device ('obj'): device to use
            token_value ('str'): Id Token value (e.g. test)
            device_type ('str'): establish trust on device (e.g. local, all)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f'Configuring license smart trust idtoken on {device.name}')
    config = f'license smart trust idtoken {token_value} {device_type} force'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to configure license smart trust idtoken on device {device.name}. Error:\n{e}'
        )


def execute_license_smart_save_usage_rum_id_file(device, rum_id, path):
    """ Executes license smart save usage rum-Id {rum_id} file {path}
        Args:
            device ('obj'): device to use
            rum_id ('str'): rum id
            path ('str'): Absolute path to the file, including the filename (eg. bootflash:test.txt)
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'license smart save usage rum-Id {rum_id} file {path}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to execute license smart save usage rum-Id {rum_id} file {path} on device {device.name}. Error:\n{e}'
        )
