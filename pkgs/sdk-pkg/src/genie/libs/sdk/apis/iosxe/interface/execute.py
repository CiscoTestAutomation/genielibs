"""Execute Interface related command"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def execute_test_idprom_fake_insert(device, interface):
    """ 
        Args:
            device ('obj'): device to use  
            interface ('str'): Interface for which we are doing SFP Fake-insert
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "test idprom interface {test_intf} fake-insert".format(test_intf=interface)

    try:
        out = device.execute(cmd)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to perform SFP OIR Fake-insert')
    return out

def execute_test_idprom_fake_remove(device, interface):
    """   
        Args:
            device ('obj'): device to use  
            interface ('str'): Interface for which we are doing SFP Fake-remove
        Returns:
            Return the test command execution output
        Raises:
            SubCommandFailure
    """
    cmd = "test idprom interface {test_intf} fake-remove".format(test_intf=interface)

    try:
        out = device.execute(cmd)
    except SubCommandFailure:
        raise SubCommandFailure('Failed to perform SFP OIR Fake-remove')
    return out