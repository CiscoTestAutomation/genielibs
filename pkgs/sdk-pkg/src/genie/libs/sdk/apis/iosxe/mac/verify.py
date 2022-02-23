"""Common verification functions for mac"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# utils
from genie.libs.sdk.apis.utils import time_to_int, has_configuration

log = logging.getLogger(__name__)


def verify_mac_from_address_family(device, address_family, expected_mac,
    evi=None, max_time=30, check_interval=10
):
    """ Verify mac from particular address family in "show l2vpn evpn mac"
        also for the particular evi (if given)

        Args:
            device ('obj'): device to use
            address_family ('str'): address family
            expected_mac ('str'): Expected mac
            evi ('str'):evi instance
            max_time ('int', optional): maximum time to wait in seconds,
                default is 30
            check_interval ('int', optional): how often to check in seconds,
                default is 10
        Returns:
            result ('bool'): verified result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        mac_table = device.api.get_mac_table_from_address_family(address_family)

        if mac_table and evi:
            if (evi in mac_table.keys()) and (expected_mac in mac_table[evi]):
                return True

        elif mac_table:
            # Getting mac addr from dictionary to list for better verification
            mac_list = []
            for mac in mac_table.values():
                mac_list.extend(mac)
            # Checking whether the expected mac address is present in mactable
            if expected_mac in mac_list:
                return True
        else:
            timeout.sleep()

    if not mac_table:
        log.error("Could not get mac details along with evi, output is empty")
    else:
        log.error('Expected mac address is "{expected_mac}" '
            'actual mac address is "{mac_table}"'.format(expected_mac=
                expected_mac, mac_table=mac_table)
        )

    return False
