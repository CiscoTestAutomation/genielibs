'''Common get info functions for running-config'''
# Python
import re
import logging

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
