'''IOSXE execute functions for vlan'''

# Python
import logging

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

# Logger
log = logging.getLogger(__name__)

def execute_vtp_primary(device, keyword=None):
    ''' Execute 'vtp primary {keyword}' on the device
        Args:
            device ('obj'): Device object
            keyword('str', optional): executing keyword for vlan feature/mst/forces
        Returns:
            output

    '''

    log.info("Executing 'vtp primary' on the device")
    
    output = None
    # Unicon Statement/Dialog
    dialog = Dialog([
             Statement(
             pattern=r".*Do you want to continue? [confirm]",
             action='sendline()',
             loop_continue=True,
             continue_timer=False)
             ])
    
    command = f'vtp primary'
    if keyword:
        command = f'vtp primary {keyword}'

    try:
       output = device.execute(
                command,
                reply=dialog,
                append_error_pattern=['.*Command cannot be executed.*'])
    except SubCommandFailure as e:
        raise SubCommandFailure(
		    "Could not execute vtp primary. Error\n:{e}")          
    return output
