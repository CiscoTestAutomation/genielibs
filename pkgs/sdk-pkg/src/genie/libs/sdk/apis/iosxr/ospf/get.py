"""Common get info functions for ospf"""

# Python
import re
import logging

# pyats
from pyats.utils.objects import find, R

# unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_ospf_process_id_on_interface(device, interface):
    """ Get ospf interface process id

        Args:
            device ('obj'): device object
            interface ('str'): interface name

        Returns:
            ospf_id ('str'): ospf process id
    """
    log.info("Getting ospf interface {intf} process id from device {dev}"
        .format(intf=interface, dev=device.name))

    cmd = 'show ospf vrf all-inclusive interface {intf}'.format(intf=interface)
    try:
        out = device.parse(cmd)
    except Exception as e:
        log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
        return None

    reqs = R(['vrf', '(?P<vrf>.*)', 'address_family',
              '(?P<af>.*)', 'instance', '(?P<instance>.*)',
              'areas', '(?P<area>.*)', 'interfaces', interface,
              'process_id', '(?P<pid>.*)'])

    found = find([out], reqs, filter_=False, all_keys=True)

    if found:
        return found[0][0]
    else:
        return None
