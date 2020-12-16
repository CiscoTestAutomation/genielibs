'''Common get info functions for running-config'''
# Python
import re
import logging
# unicon
from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.utils import get_config_dict

log = logging.getLogger(__name__)

def get_running_config_dict(device):
    """ Get show running-config output

        Args:
            device (`obj`): Device object
            option (`str`): option command
        Returns:
            config_dict (`dict`): dict of show run output
    """

    cmd = "show configuration"

    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not get running-config information "
            "on device {device}".format(device=device.name)
        )

    config_dict = get_config_dict(out)
    return config_dict