"""Common get info functions for routing"""

# Python
import os
import logging
import re

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_arp_table_count(device):
    """
    Get arp table count

    Args:
        device(`obj`): Device str
    Returns:
        arp table count
    """
    try:
        output_arp = device.parse("show arp summary")
    except SchemaEmptyParserError as e:
        log.error(
            "Failed to parse 'show arp summary', Error: {}".format(str(e))
        )
        return None

    arp_count = output_arp["total_num_of_entries"].get("arp_table_entries", 0)

    return arp_count
