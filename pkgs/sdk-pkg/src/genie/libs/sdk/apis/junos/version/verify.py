"""Common get functions for version"""

# Python
import re
import time
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_junos_version(
    device,
    expected_junos_version
):
    """ Get the hostname from 'show version'

        Args:
            device ('obj'): device to use
            expected_junos_version ('str'): Expected JUNOS version
        
        Returns:
            hostname ('str'): Hostname

        Raises:
            N/A
    """

    try:
        out = device.parse("show version")
    except SchemaEmptyParserError:
        log.info('Parser is empty')
        return None

    version_ = out.q.get_values('junos-version', 0)

    if expected_junos_version == version_:
        return True
    return False