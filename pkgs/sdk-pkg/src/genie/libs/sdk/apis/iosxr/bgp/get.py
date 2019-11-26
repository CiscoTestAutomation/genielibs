"""Common get info functions for bgp"""

# Python
import re
import logging

# unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_bgp_as(device, instance=''):
    """ Get bgp id from show running-config

        Args:
            device ('obj'): device object
            instance ('str'): instance name
        Returns:
            str: bgp_as
    """

    # router bgp 666
    if instance:
        p = re.compile(r'router bgp (?P<bgp_as>\d+) instance +{}'.format(instance))
        log.info("Getting instance {ins} BGP as from device {dev}"
            .format(ins=instance, dev=device.name))
    else:
        p = re.compile(r'router bgp (?P<bgp_as>\d+)$')
        log.info("Getting BGP as from device {dev}".format(dev=device.name))

    cmd = 'show running-config | include router bgp'
    out = device.execute(cmd)
    bgp = p.findall(out)

    if bgp:
        if len(bgp) == 1:
            log.info("Found BGP as {id} on device {dev}"
                .format(id=bgp[0], dev=device.name))
        else:
            log.info("Found multiple bgp as {id} on device {dev}, "
                     "returning the first bgp as".format(
                         id=bgp[0], dev=device.name))
        return bgp[0]

    return None
