# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# CEF
from genie.libs.sdk.apis.iosxe.cef.get import get_cef_repair_path_of_route


def is_routing_repair_path_in_cef(
    device,
    prefix,
    max_time=60,
    check_interval=10,
    vrf='default',
    address_family='ipv4',
):
    """ Verify 'repair path' is presente in express forwarding

        Args:
            device ('obj'): Device object
            route ('str'): Route address
            max_time ('int'): Max time in seconds retrieving and checking output
            check_interval ('int')
            vrf ('str'): VRF name
            address_family ('str'): Address family
        Raises:
            None
        Returns:
            True
            False
    """

    timeout = Timeout(max_time=max_time, interval=check_interval)

    while timeout.iterate():
        is_present = get_cef_repair_path_of_route(
            device=device,
            prefix=prefix,
            vrf=vrf,
            address_family=address_family,
        )
        if is_present:
            return True

        timeout.sleep()

    return False
