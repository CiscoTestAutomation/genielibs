"""Common get functions for version"""

# Python
import re
import time
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def get_hostname(
    device,
):
    """ Get the hostname from 'show version'

        Args:
            device ('obj'): device to use
        
        Returns:
            hostname ('str'): Hostname

        Raises:
            N/A
    """

    try:
        output = device.parse("show version")
    except SchemaEmptyParserError:
        log.info('Parser is empty')
        return None

    hostname = output.q.get_values('host-name', 0)

    if hostname:
        return hostname
    return None