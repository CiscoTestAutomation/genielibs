"""Common verify functions for TACACS server"""

# Python
import logging
import re

log = logging.getLogger(__name__)


def verify_ping_from_server(server, ip_address, count, interface):
    """Verify ping from server

        Args:
            server (`obj`): Server Device object
            ip_address (`str`): IP address to ping
            count (`int`): repeat ping count
            interface (`str`): source ip/interface value
        Returns:
            True
            False
        Raises:
            None
    """
    try:
        out = server.ping(addr=ip_address, count=count, interface=interface)
    except Exception as e:
        log.error(
            "Ping from server failed with address"
            " {} and source ip {}".format(ip_address, interface)
        )
        return False

    p1 = re.compile(
        r"{} +packets +transmitted, +{} +received, +0%"
        " +packet +loss, +time +\w+".format(count, count)
    )
    m = p1.search(out)
    if m:
        return True
    else:
        return False
