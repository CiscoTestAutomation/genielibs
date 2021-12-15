'''NXOS n5k execute functions for platform'''

# Python
import logging

# Logger
log = logging.getLogger(__name__)


def execute_delete_boot_variable(device, timeout=300):
    ''' Delete the boot variables
        Args:
            device ('obj'): Device object
            timeout ('int'): Max time to delete boot vars in seconds
    '''

    try:
        device.configure(["no boot system", "no boot kickstart"], timeout=timeout)
    except Exception as e:
        raise Exception("Failed to delete system boot variable on '{}'\n{}".format(device.name, str(e)))
    else:
        log.info("Deleted system and kickstart BOOT variable")

    device.api.is_current_boot_variable_as_expected(device=device, system=None, kickstart=None)
