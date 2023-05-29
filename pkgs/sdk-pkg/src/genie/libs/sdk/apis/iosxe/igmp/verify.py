"""Common verify functions for interface"""

# Python
import re
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# ipaddress
import ipaddress

# Genie
from pyats.utils.objects import find, R
from genie.utils.timeout import Timeout
from genie.libs.parser.utils.common import Common
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_igmp_groups_under_vrf(device, vrf, grp_list, grp_cnt, interface, max_time=60, check_interval=10):
    """Verify igmp groups

        Args:
            device (`obj`): Device object
            vrf (`str`): vrf name
            grp_list (`list`): list of multicast group ip and source ip
                              Eg: [["228.1.1.1","121.1.1.1"]]
            grp_cnt (`int`): number of group ip configured
            max_time (`int`, optional): Max time to check status (Default is 60)
            check_interval (`int`, optional): check interval (Default is 10)
        Returns:
            result(`bool`): verify result
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            cmd = 'show ip igmp vrf {vrf} groups'.format(vrf=vrf)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        res = True
        for grpip, last_reporter in grp_list:
            ip_list = [str(ipaddress.ip_address(grpip) + i)
                       for i in range(grp_cnt) if i]
            ip_list.append(grpip)
            for ip in ip_list:
                if ip in out.q.get_values('igmp_group_address'):
                    interface_learnet = out.q.contains(
                        ip).get_values('interface')[0]
                    if interface.lower() == interface_learnet.lower():
                        learnet_last_reporter = out.q.contains(
                            ip).get_values('last_reporter')[0]
                        if last_reporter == learnet_last_reporter:
                            continue
                        else:
                            log.debug(
                                f"Last reporter for {ip} is {learnet_last_reporter}, "
                                f"expected last reporter {last_reporter}")
                            res = False
                    else:
                        log.debug(
                            f"Interface learnet for {ip} is {interface_learnet}, expected interface {interface}")
                        res = False
                else:
                    log.debug(f"ip {ip} not learnet in igmp groups")
                    res = False
        if res:
            return True
        timeout.sleep()

    return False


def verify_igmp_group_exists(device, interface, grp_addr, max_time=15,
                             check_interval=5, **kwargs):
    """Verify if an igmp group exists
        Args:
            device ('obj'): Device object
            interface('str'): Interface on which the IGMP mcast membership is learned
            grp_addr ('str'): Multicast group ip and source ip
            max_time ('int', Optional): Max time to check status (Default is 15)
            check_interval ('int', Optional): Check interval (Default is 5)
        Returns:
            result('bool'): True or False
        Raises:
            None
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse('show ip igmp groups detail')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        intf_info = out.q.contains('vrf').contains('default').contains(
                        'interface').contains(interface)

        if intf_info:
            grp_info = intf_info.contains('group').contains(grp_addr)
            if grp_info:
                entry_found = True

                for key, value in kwargs.items():
                    if not grp_info.contains(key) or \
                       value not in grp_info.get_values(key)[0]:
                        entry_found = False
                        log.info(f"{key} mismatch: expect {str(value)}"
                                 f" actual {str(grp_info.get_values(key))}")

                if entry_found:
                    return True

        timeout.sleep()

    log.debug(f"No {grp_addr} group membership"
              " learned for {interface}")
    return False

def verify_igmp_group_not_exists(device, interface, grp_addr, max_time=15, check_interval=5):
    """Verify an igmp group does not exists
        Args:
            device ('obj'): Device object
            interface('str'): Interface on which the mcast membership is learned
            grp_addr ('str'): Multicast group ip and source ip
            max_time ('int', Optional): Max time to check status (Default is 15)
            check_interval ('int', Optional): Check interval (Default is 5)
        Returns:
            result('bool'): True or False
        Raises:
            None
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse('show ip igmp groups detail')
        except SchemaEmptyParserError:
            return True

        intf_info = out.q.contains('vrf').contains('default').contains(
                        'interface').contains(interface)

        if not intf_info or \
            not intf_info.contains('group').contains(grp_addr):
                return True

        timeout.sleep()

    log.debug(f"{grp_addr} group membership"
              " is learned for {interface}")
    return False
