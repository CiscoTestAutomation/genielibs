"""Common get info functions for protocols"""

import logging
# pyATS
from pyats.utils.objects import find, R

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys

log = logging.getLogger(__name__)


def get_protocols_bgp_process(device, vrf=None):
    """ Returns bgp process id from show protocols

        Args:
            device ('obj'): device to run on
        Returns:
            bgp process id
        Raises:
            None
    """
    log.info("Getting bgp process id on {}".format(device.hostname))

    try:
        out = device.parse("show ip protocols")
    except SchemaEmptyParserError:
        return None

    vrf = vrf if vrf else "default"

    if (
        out
        and "protocols" in out
        and "bgp" in out["protocols"]
        and "instance" in out["protocols"]["bgp"]
        and vrf in out["protocols"]["bgp"]["instance"]
    ):
        return out["protocols"]["bgp"]["instance"][vrf].get("bgp_id", None)

def get_ospf_router_id(device, vrf='(.*)', address_family='(.*)', instance='(.*)'):
    """ Get ospf router-id - show ip protocols

        Args:
            device ('obj'): device to run on
            vrf ('str'): vrf name
            address_family ('str'): address family
            instance ('str'): instance value
        Returns:
            str: single router id
            None: if empty
        Raises:
            None
    """
    log.info("Getting OSPF router-id")
    router_id = None
    cmd = 'show ip protocols'

    try:
        out = device.parse(cmd)
    except Exception as e:
        log.error("Failed to parse '{}':\n{}".format(cmd, e))
        return router_id

    reqs = R(['protocols', 'ospf',
              'vrf', vrf,
              'address_family', address_family,
              'instance', instance,
              'router_id', '(?P<router_id>.*)'])

    found = find([out], reqs, filter_=False, all_keys=True)

    if found:
        key_list = GroupKeys.group_keys(reqs=reqs.args, ret_num={}, 
                                        source=found, all_keys=True)
        return key_list.pop()['router_id']
    else:
        log.error("No ospf router id was found")
 
    return router_id

