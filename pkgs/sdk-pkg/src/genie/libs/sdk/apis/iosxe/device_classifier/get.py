import logging
import re

log = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

def get_device_classifier_profile_names(device, interface):
    '''
    Verify portfast is enabled or not on interface
    Args:
        device ('obj'): device object
        interface ('str'): interface to check
    Returns:
        result: returns the classifier device names
    Raises:
        SubCommandFailure: If command not executed raises subcommand failure error
    '''

    log.info('Collect classifier device names')
    cmd = f'show device classifier attached interface {interface}'

    try:
        sh_device_classifier = device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure('Could not execute CLI on {device}. Error: {error}'.format(device = device, error = e))

    profile_names = []

    for line in sh_device_classifier.splitlines():
        line = line.strip()

        if 'MAC_Address' in line:
            continue

        match = re.findall(r'[\w\.]+\s+[\w\/]+\s+([\S]+)\s+[\S\s]+', line)
        if match:
            profile_names.append(match[0])

    return profile_names

