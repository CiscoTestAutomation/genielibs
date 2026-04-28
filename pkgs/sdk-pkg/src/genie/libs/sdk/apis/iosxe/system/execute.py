"""Common execute functions for system"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def execute_test_system_secure_db(device):
    """Execute test system secure database command
    
    Args:
        device: The device to execute the command on
        
    Returns:
        The command output
        
    Raises:
        SubCommandFailure: If the command fails
    """
    try:
        device.execute("test system secure db")
        log.debug(f"System secure db executed successfully on {device.name}")
    except SubCommandFailure as e:
        log.error(f"Failed to execute system secure db on {device.name}: {e}")
        raise

def execute_test_system_secure_all(device):
    """Execute test system secure all command
    
    Args:
        device: The device to execute the command on
        
    Returns:
        The command output
        
    Raises:
        SubCommandFailure: If the command fails
    """
    try:
        device.execute("test system secure all")
        log.debug(f"System secure all executed successfully on {device.name}")
    except SubCommandFailure as e:
        log.error(f"Failed to execute system secure all on {device.name}: {e}")
        raise