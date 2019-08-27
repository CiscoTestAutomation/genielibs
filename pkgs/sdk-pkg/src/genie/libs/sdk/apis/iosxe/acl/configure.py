"""Common configure functions for interface"""

# Python
import logging
from ipaddress import IPv4Address

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def config_extended_acl(
    device,
    acl_name,
    permission,
    protocol,
    src_ip,
    src_step,
    src_wildcard,
    dst_ip,
    dst_step,
    dst_wildcard,
    dst_port,
    entries,
):
    """ Configure extended ACL on device

        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            permission ('str'): (permit | deny)
            protocol ('str'): protocol
            src_ip ('str'): source start ip
            src_step ('str'): increment step for source ip
            src_wildcard ('str'): source wildcard
            dst_ip ('str'): destination start ip
            dst_step ('str'): increment step for destination ip
            dst_wildcard ('str'): destination wildcard
            dst_port ('str'): Acl destination port
            entries ('int'): Acl entries

        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure access-list
    """
    config = "ip access-list extended {}\n".format(acl_name)
    src_ip = IPv4Address(src_ip)
    src_step = IPv4Address(src_step)
    dst_ip = IPv4Address(dst_ip)
    dst_step = IPv4Address(dst_step)

    if dst_wildcard != "0.0.0.0":
        cmd = (
            " {sequence} {permission} {protocol} {src_ip} {src_wildcard} "
            "{dst_ip} {dst_wildcard} eq {dst_port}\n"
        )
    else:
        cmd = (
            " {sequence} {permission} {protocol} {src_ip} {src_wildcard} "
            "host {dst_ip} eq {dst_port}\n"
        )

    for i in range(entries):
        src_ip += int(src_step)
        dst_ip += int(dst_step)

        config += cmd.format(
            sequence=i + 1,
            permission=permission,
            protocol=protocol,
            src_ip=src_ip,
            src_wildcard=src_wildcard,
            dst_ip=dst_ip,
            dst_wildcard=dst_wildcard,
            dst_port=dst_port,
        )

    config += " {} permit ip any any\n".format(i + 2)
    out = device.configure(config)

    if "% Duplicate sequence" in out or "%Failed" in out:
        raise SubCommandFailure("Failed to configure access-list")

    return out


def config_acl_on_interface(device, interface, acl_name, inbound=True):
    """ Configures acl on interface 

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            acl_name ('str'): acl to apply
    """
    if inbound:
        log.info(
            "Configure inbound {acl} on {intf}".format(
                acl=acl_name, intf=interface
            )
        )
        direction = "in"
    else:
        log.info(
            "Configure outbound {acl} on {intf}".format(
                acl=acl_name, intf=interface
            )
        )
        direction = "out"

    try:
        device.configure(
            "interface {intf}\nip access-group {acl} {direction}".format(
                intf=interface, acl=acl_name, direction=direction
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure acl {acl} on interface {interface}".format(
                acl=acl_name, interface=interface
            )
        )
