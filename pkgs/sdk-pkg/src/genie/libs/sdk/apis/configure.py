'''Common configure functions'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def configure_hostname(device, hostname):
    """ To configure the hostname
        Args:
            device (`obj`): Device object
            hostname (`str`): Hostname to be configured.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(f'hostname {hostname}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure hostname on {device}. Error:\n{error}"
                .format(device=device.name, error=e)
        )
