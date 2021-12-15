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
    permission=None,
    protocol=None,
    src_ip=None,
    src_step=None,
    src_wildcard=None,
    dst_ip=None,
    dst_step=None,
    dst_wildcard=None,
    dst_port=None,
    entries=None,
    acl_type=None,
    sequence_num=None
):
    """ Configure extended ACL on device
        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            permission ('str'): (permit | deny), default value is None
            protocol ('str'): protocol, default value is None
            src_ip ('str'): source start ip, default value is None
            src_step ('str'): increment step for source ip, default value is None
            src_wildcard ('str'): source wildcard, default value is None
            dst_ip ('str'): destination start ip, default value is None
            dst_step ('str'): increment step for destination ip, default value is None
            dst_wildcard ('str'): destination wildcard, default value is None
            dst_port ('str'): Acl destination port, default value is None
            entries ('int'): Acl entries, default value is None
            acl_type ('str', optional): type of ACL like with or without host keyword, default value is None
            sequence_num ('str',optional): specific sequence number,default value is None
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure access-list
    """
    configs = []
    configs.append("ip access-list extended {}".format(acl_name))
    if permission in ['permit', 'deny']:
        if acl_type:
            # Build config string
            configs.append("{sequence} {permission} {protocol} host {src_ip} host {dst_ip}".format(
                sequence=sequence_num,
                permission=permission,
                protocol=protocol,
                src_ip=src_ip,
                dst_ip=dst_ip))
        else:
            if dst_wildcard != "0.0.0.0":
                if entries > 1:
                    for i in range(entries):
                        src_ip = IPv4Address(src_ip)
                        src_step = IPv4Address(src_step)
                        dst_ip = IPv4Address(dst_ip)
                        dst_step = IPv4Address(dst_step)
                        src_ip_inc = src_ip + i
                        dst_ip_inc = dst_ip + i
                        configs.append(
                            " {sequence} {permission} {protocol} {src_ip} {src_wildcard} {dst_ip} {dst_wildcard} eq {dst_port}".format(
                                sequence=i + 1,
                                permission=permission,
                                protocol=protocol,
                                src_ip=src_ip_inc,
                                src_wildcard=src_wildcard,
                                dst_ip=dst_ip_inc,
                                dst_wildcard=dst_wildcard,
                                dst_port=dst_port))

                if entries == 1:
                    configs.append(
                        " {sequence} {permission} {protocol} {src_ip} {src_wildcard} {dst_ip} {dst_wildcard} eq {dst_port}".format(
                            sequence=sequence_num,
                            permission=permission,
                            protocol=protocol,
                            src_ip=src_ip,
                            src_wildcard=src_wildcard,
                            dst_ip=dst_ip,
                            dst_wildcard=dst_wildcard,
                            dst_port=dst_port))

            if src_wildcard != "0.0.0.0":
                if entries > 1:
                    for i in range(entries):
                        src_ip = IPv4Address(src_ip)
                        src_step = IPv4Address(src_step)
                        dst_ip = IPv4Address(dst_ip)
                        dst_step = IPv4Address(dst_step)
                        src_ip_inc = src_ip + i
                        dst_ip_inc = dst_ip + i
                        configs.append(
                            " {sequence} {permission} {protocol} {src_ip} {src_wildcard} {dst_ip} {dst_wildcard} eq {dst_port}".format(
                                sequence=i + 1,
                                permission=permission,
                                protocol=protocol,
                                src_ip=src_ip_inc,
                                src_wildcard=src_wildcard,
                                dst_ip=dst_ip_inc,
                                dst_wildcard=dst_wildcard,
                                dst_port=dst_port))

                if entries == 1:
                    configs.append(
                        " {sequence} {permission} {protocol} {src_ip} {src_wildcard} host {dst_ip} eq {dst_port}".format(
                            sequence=sequence_num,
                            permission=permission,
                            protocol=protocol,
                            src_ip=src_ip,
                            src_wildcard=src_wildcard,
                            dst_ip=dst_ip,
                            dst_port=dst_port))
    else:
        configs.append("permit ip any any")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure Access-list {acl} on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )

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

def unconfig_extended_acl(device,acl_name):
    """ Unconfigure the extended acls
        Args:
            device ('obj'): device to use
            acl_name ('str'): name of acl
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(["no ip access-list extended {acl_name}".format(acl_name=acl_name)])
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not unconfigure extended acl. Error:\n{error}".format(error=e))

def scale_accesslist_config(device,acl_name,acl_list):
    """ Configure the huge(more than 1k static acl) extended acls
        Args:
            device ('obj'): device to use
            acl_name ('str'): name of acl
            acl_list ('str') : acl_lists
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = "ip access-list extended {}\n".format(acl_name)
    cmd = "{}\n".format(acl_list)
    config += cmd
    try:
        out = device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure extended acl. Error:\n{error}".format(error=e))

    if "% Duplicate sequence" in out or "%Failed" in out:
        raise SubCommandFailure("Failed to configure access-list")

    return out

def unconfigure_acl(device, acl_name, extended=True):
    """ unconfigure Access-list

        Args:
            device (`obj`): Device object
            acl_name (`str`): Access-list name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if extended:
        configs = "no ip access-list extended {acl}".format(acl=acl_name)
    else:
        configs = "no ip access-list standard {acl}".format(acl=acl_name)

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure {acl} on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ace(
        device,
        acl_name,
        permission,
        protocol,
        src_ip,
        src_wildcard,
        dst_ip,
        dst_wildcard,
        acl_type=None,
        sequence_num=None
):
    """ Unconfigure Access-list Entry (ACE) from Access-list

        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            permission ('str'): (permit | deny)
            protocol ('str'): protocol
            src_ip ('str'): source start ip
            src_wildcard ('str'): source wildcard
            dst_ip ('str'): destination start ip
            dst_wildcard ('str'): destination wildcard
            acl_type ('str', optional): type of ACL like with or without host keyword, default value is None
            sequence_num ('str',optional): specific sequence number, default value is None

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("ip access-list extended {}".format(acl_name))
    if sequence_num:
        configs.append("no {sequence_num}".format(sequence_num=sequence_num))

    elif acl_type == 'host':
        configs.append("no {permission} {protocol} host {src_ip} host {dst_ip}".format(
            permission=permission,
            protocol=protocol,
            src_ip=src_ip,
            dst_ip=dst_ip))

    elif src_wildcard and dst_wildcard :
        configs.append("no {permission} {protocol} {src_ip} {src_wc}{dst_ip} {dst_wc}".format(
            permission=permission,
            protocol=protocol,
            src_ip=src_ip,
            src_wc=src_wildcard,
            dst_ip=dst_ip,
            dst_wc=dst_wildcard))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ace from {acl} on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )


def remove_acl_from_interface(device, interface, acl_name, inbound=True):
    """ Remove acl from an interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            acl_name ('str'): acl to apply
            inbound (boolean, optional): True for inbound acl, False for outbound acl. Default value is True
    """
    if inbound:
        log.info(
            "Remove inbound {acl} on {intf}".format(
                acl=acl_name, intf=interface
            )
        )
        direction = "in"
    else:
        log.info(
            "Remove outbound {acl} on {intf}".format(
                acl=acl_name, intf=interface
            )
        )
        direction = "out"

    try:
        device.configure(
            "interface {intf}\nno ip access-group {acl} {direction}".format(
                intf=interface, acl=acl_name, direction=direction
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove acl {acl} on interface {interface}".format(
                acl=acl_name, interface=interface
            )
        )
