'''Common get info functions for running-config'''
# Python
import re
import logging
# unicon
from unicon.core.errors import SubCommandFailure

from genie.libs.sdk.apis.utils import get_config_dict
from genie.libs.sdk.apis.iosxe.running_config.get import \
    get_valid_config_from_running_config as base_get_valid_config_from_running_config

log = logging.getLogger(__name__)

def get_running_config_hostname(device):
    ''' Get device hostname

        Args:
            device (`obj`): Device object
        Returns:
            hostname (`str`): Device hostname
    '''
    log.info("Getting hostname from {}".format(device.name))
    hostname = ''
    try:
        out = device.execute('show running-config hostname')
        hostname = re.search(r'hostname +(?P<name>\S+)', out).groupdict()['name']
    except Exception as e:
        log.error("Failed to get hostname on device {}:\n{}".format(device.name, e))
        raise Exception from e

    return hostname

def get_running_config_dict(device, option=None):
    """ Get show running-config output

        Args:
            device (`obj`): Device object
            option (`str`): option command
        Returns:
            config_dict (`dict`): dict of show run output
    """
    if option:
        cmd = "show running-config {}".format(option)
    else:
        cmd = "show running-config"
    try:
        out = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not get running-config information "
            "on device {device}".format(device=device.name)
        )

    config_dict = get_config_dict(out)
    return config_dict

def get_valid_config_from_running_config(device, exclude=None, begin='hostname'):
    """ Returns a configuration from 'show running-config | begin version'.
        The API will exclude any configuration and sub configuration that
        matches regex from exclude. The returned string can be used to
        configure a device.

        Args:
            device ('obj'): Device to run on
            exclude ('str'): Regex of config to exclude
            begin ('str'): Begin command for show run

        Returns:
            String of configuration
    """
    return base_get_valid_config_from_running_config(device, exclude, begin)