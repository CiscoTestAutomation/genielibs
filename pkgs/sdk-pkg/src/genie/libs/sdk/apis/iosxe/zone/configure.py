"""Common configure functions for zone based firewall"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_zone_security(device, zone_name):
    """ Configure zone security

        Args:
            device ('obj'): Device object
            zone_name ('str' or 'list'): Zone name(s) to create
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if isinstance(zone_name, str):
        zone_name = [zone_name]
    log.debug(f"Configuring zone security {zone_name}")
    cmd = [f"zone security {zone}" for zone in zone_name]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure zone security. Error:\n{e}"
        )


def unconfigure_zone_security(device, zone_name):
    """ Unconfigure zone security

        Args:
            device ('obj'): Device object
            zone_name ('str' or 'list'): Zone name(s) to remove
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if isinstance(zone_name, str):
        zone_name = [zone_name]
    log.debug(f"Unconfiguring zone security {zone_name}")
    cmd = [f"no zone security {zone}" for zone in zone_name]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure zone security. Error:\n{e}"
        )


def configure_zone_pair_security(
        device,
        zone_pair_name,
        source_zone,
        destination_zone,
        service_policy=None):
    """ Configure zone-pair security

        Args:
            device ('obj'): Device object
            zone_pair_name ('str'): Name of the zone-pair
            source_zone ('str'): Source zone name
            destination_zone ('str'): Destination zone name
            service_policy ('str', optional): Inspect policy-map to attach.
                Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"zone-pair security {zone_pair_name} source {source_zone} "
        f"destination {destination_zone}"
    ]
    if service_policy is not None:
        cmd.append(f"service-policy type inspect {service_policy}")
    log.debug(f"Configuring zone-pair security {zone_pair_name}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure zone-pair security "
            f"{zone_pair_name}. Error:\n{e}"
        )


def unconfigure_zone_pair_security(
        device,
        zone_pair_name,
        source_zone,
        destination_zone,
        service_policy=None,
        remove_zone_pair=True):
    """ Unconfigure zone-pair security

        Args:
            device ('obj'): Device object
            zone_pair_name ('str'): Name of the zone-pair
            source_zone ('str'): Source zone name
            destination_zone ('str'): Destination zone name
            service_policy ('str', optional): Inspect policy-map to detach.
                Defaults to None
            remove_zone_pair ('bool', optional): Also delete the zone-pair
                with 'no zone-pair security ...'. Defaults to True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    if service_policy is not None:
        cmd.extend([
            f"zone-pair security {zone_pair_name} source {source_zone} "
            f"destination {destination_zone}",
            f"no service-policy type inspect {service_policy}",
            "exit",
        ])
    if remove_zone_pair:
        cmd.append(
            f"no zone-pair security {zone_pair_name} source {source_zone} "
            f"destination {destination_zone}"
        )
    log.debug(f"Unconfiguring zone-pair security {zone_pair_name}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure zone-pair security "
            f"{zone_pair_name}. Error:\n{e}"
        )


def configure_zone_member_security(device, interface, zone_name):
    """ Configure zone-member security on an interface

        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            zone_name ('str'): Zone name to attach
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}",
        f"zone-member security {zone_name}",
    ]
    log.debug(
        f"Configuring zone-member security {zone_name} on {interface}"
    )
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure zone-member security on "
            f"{interface}. Error:\n{e}"
        )


def unconfigure_zone_member_security(device, interface, zone_name):
    """ Unconfigure zone-member security on an interface

        Args:
            device ('obj'): Device object
            interface ('str'): Interface name
            zone_name ('str'): Zone name to detach
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}",
        f"no zone-member security {zone_name}",
    ]
    log.debug(
        f"Unconfiguring zone-member security {zone_name} on {interface}"
    )
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure zone-member security on "
            f"{interface}. Error:\n{e}"
        )
