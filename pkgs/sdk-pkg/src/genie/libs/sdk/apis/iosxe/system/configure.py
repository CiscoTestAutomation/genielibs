"""Common configure functions for system"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure


log = logging.getLogger(__name__)


def config_license(device, license):
    """ Config license on Device

        Args:
            device (`obj`): Device object
            license (`str`): License name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure("license boot level {license}".format(license=license))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure license {license}, Error: {error}'.format(
                license=license, error=e)
        )
