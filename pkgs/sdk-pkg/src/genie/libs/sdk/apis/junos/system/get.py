"""Common get functions for system"""

# Python
import re
import logging
from datetime import datetime

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_system_uptime(device):
    """Return system uptime

    Args:
        device (obj): Device object

    Returns:
        str: Returns system uptime in seconds
    """ 

    try:
        out = device.parse('show system uptime')
    except SchemaEmptyParserError:
        return None

    seconds = out.get('system-uptime-information', {})\
                        .get('uptime-information', {})\
                        .get('up-time', {})\
                        .get('@junos:seconds')

    if seconds:
        return int(seconds)
    else:
        return None


def get_system_current_time(device):
    """Return system timestamp

    Args:
        device (obj): Device object

    Returns:
        (Datetime): Return system timestamp
    """

    try:
        out = device.parse('show system uptime')
    except SchemaEmptyParserError:
        return None

    time_text = out.get('system-uptime-information', {}) \
                        .get('current-time', {}) \
                        .get('date-time', {}) \
                        .get('#text')

    timestamp = datetime.strptime(' '.join(time_text.split(' ')[0:2]), '%Y-%m-%d %H:%M:%S')

    return timestamp