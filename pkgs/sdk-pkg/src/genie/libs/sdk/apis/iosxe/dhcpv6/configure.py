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

def enable_dhcp_ldra(device, **kwargs):
    """
    Enabling DHCP ldra
        Args:
            device ('obj'): device to use
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to enable ldra
    """
    log.info("Enabling DHCP ldra")
    try:
        return device.configure(
            [
                "ipv6 dhcp-ldra enable"
            ], **kwargs
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable DHCP ldra globally"
            )

def remove_enable_dhcp_ldra(device, **kwargs):
    """
    Removing enable DHCP ldra
        Args:
            device ('obj'): device to use
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove enable ldra
    """
    log.info("Removing enable DHCP ldra")
    try:
        return device.configure(
            [
                "no ipv6 dhcp-ldra enable"
            ], **kwargs
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove enable DHCP ldra globally"
            )

def disable_dhcp_ldra(device, **kwargs):
    """
    Disabling DHCP ldra
        Args:
            device ('obj'): device to use
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to disable ldra
    """
    log.info("Disabling DHCP ldra")
    try:
        return device.configure(
            [
                "ipv6 dhcp-ldra disable"
            ], **kwargs
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable DHCP ldra globally"
            )

def remove_disable_dhcp_ldra(device, **kwargs):
    """
    Removing disable DHCP ldra
        Args:
            device ('obj'): device to use
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove disable ldra
    """
    log.info("Removing disable DHCP ldra")
    try:
        return device.configure(
            [
                "no ipv6 dhcp-ldra disable"
            ], **kwargs
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove disable DHCP ldra globally"
            )

def configure_ldra_remote_id(device, remote_id=None, **kwargs):
    """
    Configuring DHCP ldra remote-id
        Args:
            device ('obj'): device to use
            remote_id ('str'): remote-id for ldra
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to configure ldra remote-id
    """
    log.info("Configuring DHCP ldra remote-id")
    try:
        if remote_id:
            return device.configure(
                [
                    "ipv6 dhcp-ldra remote-id {}".format(remote_id)
                ], **kwargs
            )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure DHCP ldra remote-id"
            )

def remove_ldra_remote_id(device, remote_id=None, **kwargs):
    """
    Remove DHCP ldra remote-id
        Args:
            device ('obj'): device to use
            remote_id ('str'): remote-id for ldra
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove ldra remote-id
    """
    log.info("Removing DHCP ldra remote-id")
    try:
        if remote_id:
            return device.configure(
                [
                    "no ipv6 dhcp-ldra remote-id {}".format(remote_id)
                ], **kwargs
            )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove DHCP ldra remote-id"
            )

def configure_ldra_policy_vlan(device, vlan_id=None, policy=None, **kwargs):
    """
    Configuring DHCP ldra policy on vlan
        Args:
            device ('obj'): device to use
            vlan_id ('str'): vlan_id to attach policy
            policy ('str'): policy to attach in vlan
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to configure ldra policy on vlan
    """
    log.info("Configuring ldra policy on vlan {}".format(vlan_id))
    try:
        if vlan_id and policy:
            return device.configure(
                [
                    "vlan configuration {}".format(vlan_id),
                    "ipv6 dhcp ldra attach-policy {}".format(policy)
                ], **kwargs
            )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure ldra policy on vlan {}".format(vlan_id)
            )

def remove_ldra_policy_vlan(device, vlan_id=None, policy=None, **kwargs):
    """
    Remove DHCP ldra policy on vlan
        Args:
            device ('obj'): device to use
            vlan_id ('str'): vlan_id to attach policy
            policy ('str'): policy to attach in vlan
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove ldra policy on vlan
    """
    log.info("Removing ldra policy on vlan {}".format(vlan_id))
    try:
        if vlan_id and policy:
            return device.configure(
                [
                    "vlan configuration {}".format(vlan_id),
                    "no ipv6 dhcp ldra attach-policy {}".format(policy)
                ], **kwargs
            )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove ldra policy on vlan {}".format(vlan_id)
            )

def configure_ldra_interface(
        device, interface=None, vlan_id=None, policy=None, interface_id=None, **kwargs):
    """
    Configuring DHCP ldra on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            vlan_id ('str'): vlan_id to attach policy
            policy ('str'): policy to attach in vlan
            interface_id ('str'): interface-id for ldra interface
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to configure ldra on interface
    """
    log.info("Configuring ldra on interface {}".format(interface))
    try:
        if interface and vlan_id:
            cmd_list = [
                "interface {}".format(interface),
                "switchport",
                "switchport access vlan {}".format(vlan_id)
                ]
            if policy:
                cmd_list.append("ipv6 dhcp-ldra attach-policy {}".format(policy))
            if interface_id:
                cmd_list.append("ipv6 dhcp-ldra interface-id {}".format(interface_id))
            return device.configure(cmd_list, **kwargs)

    except SubCommandFailure as err:
        raise SubCommandFailure(
            "Could not configure ldra on interface {}, Reason: {}".format(interface, err)
            )

def remove_ldra_interface(
        device, interface=None, vlan_id=None, policy=None, interface_id=None, **kwargs):
    """
    Remove DHCP ldra remote-id
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            vlan_id ('str'): vlan_id to attach policy
            policy ('str'): policy to attach in vlan
        Returns:
            str: Response of command
        Raises:
            SubCommandFailure: Failed to remove ldra on interface
    """
    log.info("Removing ldra on interface {}".format(vlan_id))
    try:
        if interface and vlan_id:
            cmd_list = [
                "interface {}".format(interface)
                ]
            if policy:
                cmd_list.append("no ipv6 dhcp-ldra attach-policy {}".format(policy))
            if interface_id:
                cmd_list.append("no ipv6 dhcp-ldra interface-id {}".format(interface_id))
            cmd_list.append("no switchport access vlan {}".format(vlan_id))
            cmd_list.append("no switchport")
            return device.configure(cmd_list, **kwargs)

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove ldra on interface {}".format(interface)
            )
