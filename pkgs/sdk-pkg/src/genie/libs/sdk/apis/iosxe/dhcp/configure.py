"""Common configure functions for dhcp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def create_dhcp_pool(
    device, pool_name, network, mask, router_id,lease_days,lease_hrs,lease_mins
):
    """ Create DHCP pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
            network ('str'): IP of the network pool
            mask ('str'): Subnet mask of the network pool
            router_id ('str'): Default router ID
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface
    """
    log.info(
        "Configuring DHCP pool with name={}, network={}, mask={}, and "
        "Router ID {} Lease Time days={},hrs={},mins={}".format(pool_name, network, mask, router_id,lease_days,lease_hrs,lease_mins)
    )

    try:
        device.configure(
            [
            "ip dhcp pool {}".format(pool_name),
	    "network {} {}".format(network,mask),
            "default-router {}".format(router_id),
            "lease {} {} {}".format(lease_days,lease_hrs,lease_mins)
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure DHCP pool {pool_name}".format(
                pool_name=pool_name
            )
        )

def remove_dhcp_pool(
    device, pool_name
):
    """ Remove DHCP pool
        Args:
            device ('obj'): device to use
            pool_name ('str'): name of the pool to be created
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface
    """
    log.info(
        "Removing DHCP pool with name={}".format(pool_name)
    )

    try:
        device.configure(
            [
            "no ip dhcp pool {}".format(pool_name),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove DHCP pool {pool_name}".format(
                pool_name=pool_name
            )
        )


def enable_dhcp_snooping_vlan(device, vlan):
    """ Enable DHCP snooping on vlan
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan-id to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring DHCP snooping on vlan
    """
    log.info("Enabling DHCP snooping on vlan")
    try:
        device.configure(["ip dhcp snooping vlan {}".format(vlan)])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable DHCP snooping on vlan {vlan}".format(
                vlan=vlan
            )
        )
		
def disable_dhcp_snooping_vlan(device, vlan):
    """ Disable DHCP snooping on vlan
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan-id to configure
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling DHCP snooping on vlan
    """
    log.info("Disabling DHCP snooping on vlan")
    try:
        device.configure(["no ip dhcp snooping vlan {}".format(vlan)])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable DHCP snooping on vlan {vlan}".format(
                vlan=vlan
            )
        )

def exclude_ip_dhcp(device, ip):
    """ Exclude IP in DHCP
        Args:
            device ('obj'): device to use
            ip ('str'): ip to exclude
        Returns:
            None
        Raises:
            SubCommandFailure: Failed excluding IP in DHCP config
    """
    log.info("Excluding IP in DHCP")
    try:
        device.configure(["ip dhcp excluded-address {}".format(ip)])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not exclude {ip} in DHCP config".format(
                ip=ip
            )
        )

def disable_dhcp_snooping_info(device):
    """ Disable DHCP snooping information
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling DHCP snooping information
    """
    log.info("Disabling DHCP snooping information")
    try:
        device.configure(["no ip dhcp snooping information option"])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable DHCP snooping information"
            )
        
def remove_dhcp_snooping_binding(
    device, vlan
):
    """ Remove DHCP snooping binding
        Args:
            device ('obj'): device to use
            vlan ('str'): vlan-id to remove binding
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface
    """
    log.info(
        "Removing DHCP snooping binding with vlan = {}".format(vlan)
    )

    try:
        device.execute(
            [
            "clear ip dhcp snooping binding vlan {}".format(vlan),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove DHCP snooping binding for vlan {vlan}".format(
                vlan = vlan
            )
        )

