"""Common configure functions for dhcpv6"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def create_dhcp_pool_ipv6(device, pool_name, ipv6_prefix, lifetime, pref_lifetime):
    """ Create DHCP IPv6 pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
            ipv6_prefix ('str'): IPv6 prefix
            lifetime ('int'): lifetime in seconds
            pref_lifetime ('int'): preferred lifetime in seconds
        Returns:
            None
        Raises:
            SubCommandFailure: Failed creating IPv6 DHCP pool
    """
    log.info(
        "Configuring IPv6 DHCP pool with name={pool_name}, ipv6_prefix={ipv6_prefix}, lifetime={lifetime}, and "
        "Preferred Lifetime {pref_lifetime} ".format(pool_name=pool_name, ipv6_prefix=ipv6_prefix, lifetime=lifetime, pref_lifetime=pref_lifetime)
    )

    try:
        device.configure(
            [
            "ipv6 dhcp pool {pool_name}".format(pool_name=pool_name),
	    "address prefix {ipv6_prefix} lifetime {lifetime} {pref_lifetime}".format(ipv6_prefix=ipv6_prefix, lifetime=lifetime, pref_lifetime=pref_lifetime)
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure IPv6 DHCP pool {pool_name}".format(
                pool_name=pool_name
            )
        )

def remove_dhcp_pool_ipv6(device, pool_name):
    """ Remove DHCP IPv6 pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing IPv6 DHCP pool
    """
    log.info(
        "Removing IPv6 DHCP pool with name={pool_name}".format(pool_name=pool_name)
    )

    try:
        device.configure(
            [
            "no ipv6 dhcp pool {pool_name}".format(pool_name=pool_name),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove IPv6 DHCP pool {pool_name}".format(
                pool_name=pool_name
            )
        )


