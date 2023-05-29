"""Common verify functions for MLD"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_mld_group_exists(device, interface, grp_addr, max_time=15,
                            check_interval=5, **kwargs):
    """Verify if an mld group exists
        Args:
            device ('obj'): Device object
            interface('str'): Interface on which the MLD mcast membership is learned
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
            out = device.parse('show ipv6 mld groups detail')
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
                        log.fatal(f"{key} mismatch: expect {str(value)}"
                                 f" actual {str(grp_info.get_values(key))}")

                if entry_found:
                    return True

        timeout.sleep()

    log.debug(f"No {grp_addr} group membership"
              " learned on {interface}")
    return False

def verify_mld_group_not_exists(device, interface, grp_addr, max_time=15, check_interval=5):
    """Verify an mld group does not exist
        Args:
            device ('obj'): Device object
            interface('str'): Interface on which the MLD mcast membership is learned
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
            out = device.parse('show ipv6 mld groups detail')
        except SchemaEmptyParserError:
            return True

        intf_info = out.q.contains('vrf').contains('default').contains(
                        'interface').contains(interface)

        if not intf_info or \
            not intf_info.contains('group').contains(grp_addr):
                return True

        timeout.sleep()

    log.debug(f"{grp_addr} group membership"
              " is learned on {interface}")
    return False