"""Common verify functions for vpn"""

# Python
import os
import logging
import re
from genie.utils.timeout import Timeout

# Common

# VRF
from genie.libs.sdk.apis.iosxe.vrf.get import get_vrf_route_targets

log = logging.getLogger(__name__)


def verify_vpn_route_targets(
    device,
    route_targets,
    rt_type,
    address_family,
    vrf=None,
    route_distinguisher=None,
    max_time=15,
    check_interval=5,
):
    """ Verify route target are imported, exported or both

        Args:
            device ('obj'): Device object
            route_targets ('list'): list of route targets to check
                ex.)
                    [
                        '65109:4005',
                        '65109:4006'
                    ]
            rt_type ('str'): route target type
                ex.) rt_type = 'import' OR
                     rt_type = 'export' OR
                     rt_type = 'both'
            address_family ('str'): address family to check
            vrf ('str'): vrf name
            route_distinguisher ('str'): route distinguisher value
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
            
        Returns:
            True
            False
    """

    # Check if both route targets exists on device
    if route_targets:
        if not isinstance(route_targets, list):
            log.error("route_targets must be list")
            return False

    result = True

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True
        for rt in route_targets:
            current_rt = None
            try:
                current_rt = get_vrf_route_targets(
                    device=device,
                    rt_type=rt_type,
                    address_family=address_family,
                    vrf=vrf,
                    route_distinguisher=route_distinguisher,
                )
            except Exception as e:
                log.error(str(e))

            if not current_rt:
                log.info(
                    "Route target of type {} not found for VRF {} on device {}".format(
                        rt_type, vrf, device.name
                    )
                )
                result = False
        if result:
            return result
        timeout.sleep()
    return result
