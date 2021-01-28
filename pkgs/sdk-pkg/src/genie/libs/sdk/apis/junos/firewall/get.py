"""Common get info functions for Firewall"""

# Python
import re
import logging
import copy
import ipaddress

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout
from genie.utils import Dq

# unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def get_firewall_counter(device,
                         filters,
                         counter_name,
                         field='packet-count',
                         output=None,
                         max_time=60,
                         check_interval=10):
    """ Get specific field value from show firewall counter filter

        Args:
            device (`obj`): Device object
            filters (`str`): Firewall filter argument
            counter_name (`str`): Firewall counter name argument
            field (`str`): field to check in parse_output
                           Default to `packet-count`
            max_time (`int`): Max time, defaults to 60 seconds
            check_interval (`int`): Check interval, defaults to 10 seconds
            output (`str`): output of show firewall counter filter {filters} {counter_name}
                            Default to None
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    try:
        out = device.parse(
            'show firewall counter filter {filters} {counter_name}'.format(
                filters=filters, counter_name=counter_name, output=output))
    except SchemaEmptyParserError:
        return None

    #"firewall-information": {
    #    "filter-information": {
    #        "counter": {
    #            "byte-count": "1061737740",
    #            "counter-name": "v6_last_policer",
    #            "packet-count": "7860915"
    #        },
    #        "filter-name": "v6_local-access-control"
    #    }
    #}
    field_value = out.q.get_values(field, 0)
    if field_value:
        return field_value
    else:
        return None
