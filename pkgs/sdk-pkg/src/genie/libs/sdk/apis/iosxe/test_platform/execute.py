"""IOSXE execute functions for test platform"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)


def execute_test_platform(device, test_cli, timeout=60):
    """
    Execute 'test platform {test_cli}' command on the device.

    Args:
        device (obj): Device object
        test_cli (str): The test CLI command to execute
        timeout (int, optional): Maximum time to wait for command completion in seconds. 
                                 Default is 60 seconds.
    
    Returns:
        str: Command output
        
    Raises:
        SubCommandFailure: Failed to execute the command

    Examples:
        # General test platform cli
        test platform hardware fantray switch 1
        test platform software trace slot fp act forwarding-manager rotate
    """
    
    log.info(f"Executing test platform {test_cli} on {device}")
    
    # Construct the command
    command = f"test platform {test_cli}"
    
    try:
        # Execute the command on the device
        return device.execute(command, timeout=timeout)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute test platform {test_cli} on {device}. Error:\n{e}"
        )
