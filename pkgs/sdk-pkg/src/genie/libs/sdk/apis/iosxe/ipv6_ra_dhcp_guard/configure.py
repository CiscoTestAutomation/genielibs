
"""Common configure functions for ipv6 raguard  and dhcpv6 guard policy"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_ipv6_raguard_policy(device, policy_name, device_role):
    """ Configure IPv6 RA Guard Policy
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be configured
            device_role ('str'): role of the  device
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring IPv6 RA guard policy
    """
    log.info(
        "Configuring IPv6 RA Guard Policy with name={policy_name}, role={device_role} "
        .format(policy_name=policy_name, device_role=device_role)
    )

    try:
       device.configure(
            [
            "ipv6 nd raguard policy {policy_name}".format(policy_name=policy_name),
            "device-role {device_role}".format(device_role=device_role)
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure IPv6 RA Guard Policy {policy_name}".format(
                policy_name=policy_name
            )
        )
       
def configure_dhcpv6_guard_policy(device, policy_name, device_role):
    """ Configure DHCPv6 Guard Policy
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be configured
            device_role ('str'): role of the  device
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring DHCPv6 guard policy
    """
    log.info(
        "Configuring DHCPv6 Guard Policy with name={policy_name}, role={device_role} "
        .format(policy_name=policy_name, device_role=device_role)
    )

    try:
       if device_role == 'server' or device_role == 'client' or device_role == 'monitor':
          device.configure(
             [
             "ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
             "device-role {device_role}".format(device_role=device_role)
             ]
           )
       else:
          device.configure(
             [
             "ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
             "{device_role}".format(device_role=device_role)
             ]
           )


    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure DHCPv6 Guard Policy {policy_name}".format(
                policy_name=policy_name
            )
        )

def remove_ipv6_raguard_policy(device, policy_name):
    """ Configure IPv6 RA Guard Policy
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be removed
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing IPv6 RA guard policy
    """
    log.debug(
        "Removing IPv6 RA Guard Policy with name={policy_name} "
        .format(policy_name=policy_name)
    )

    try:
       device.configure(
            [
            "no ipv6 nd raguard policy {policy_name}".format(policy_name=policy_name)            
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove IPv6 RA Guard Policy {policy_name}".format(
                policy_name=policy_name
            )
        )


def remove_dhcpv6_guard_policy(device, policy_name):
    """ Configure DHCPv6 Guard Policy
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be removed
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing DHCPv6 guard policy
    """
    log.debug(
        "Removing DHCPv6 Guard Policy with name={policy_name}"
        .format(policy_name=policy_name)
    )

    try:
       device.configure(
             [
             "no ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name)
             ]
           )
       
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove DHCPv6 Guard Policy {policy_name}".format(
                policy_name=policy_name
            )
        )

