"""Common configure functions for OGACL"""

# Python
import logging
from ipaddress import IPv6Address

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_ipv6_object_group_network(
        device,
        og_name,
        og_mode,
        ipv6_address,
        ipv6_network=None,
        prefix=None
):
    """ Configure ipv6 object group of network type

        Args:
            device (`obj`): Device object
            og_name ('str'): object-group name
            og_mode ('str'): object-group mode host or network
            ipv6_address ('str'): IPv6 address
            ipv6_network ('str'): IPv6 network address
            prefix ('str'): Prefix length

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("object-group v6-network {}".format(og_name))

    if og_mode == "host" :
        #Build config string
        configs.append("host {ipv6}".format(ipv6=ipv6_address))

    elif og_mode == "network":
        configs.append("{ipv6network}/{prefix}".format(ipv6network=ipv6_network,prefix=prefix))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ipv6 object-group {og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ipv6_object_group_network_entry(
        device,
        og_name,
        og_mode,
        ipv6_address,
        ipv6_network=None,
        prefix=None
):
    """ unconfigure ipv6 object-group network entry

        Args:
            device (`obj`): Device object
            og_name ('str'): object-group name
            og_mode ('str'): object-group mode
            ipv6_address ('str'): IPv6 address
            ipv6_network ('str'): IPv6 network address
            prefix ('str'): Prefix length

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("object-group v6-network {}".format(og_name))

    if og_mode == "host":
        #Build config string
        configs.append("no host {ipv6}".format(ipv6=ipv6_address))

    elif og_mode == "network":
        configs.append("no {ipv6network}/{prefix}".format(ipv6network=ipv6_network,prefix=prefix))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure entry in ipv6 object-group {og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )

def configure_ipv6_object_group_service(
        device,
        og_name,
        ipv6_service
):
    """ Configure ipv6 object group of service type

            Args:
                device (`obj`): Device object
                og_name ('str'): object-group name
                ipv6_service ('str'): IPv6 service to add str

            Returns:
                None

            Raises:
                SubCommandFailure
        """
    configs = []
    configs.append("object-group v6-service {}".format(og_name))

    # Build config string
    configs.append("{}".format(ipv6_service))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ipv6 object-group {og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ipv6_object_group_service_entry(
        device,
        og_name,
        ipv6_service
):
    """ Unconfigure ipv6 object group service entry

            Args:
                device (`obj`): Device object
                og_name ('str'): object-group name
                ipv6_service ('str'): IPv6 service to add int or str

            Returns:
                None

            Raises:
                SubCommandFailure
        """
    configs = []
    configs.append("object-group v6-service {}".format(og_name))

    # Build config string
    configs.append("no {}".format(ipv6_service))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ipv6 object-group {og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ipv6_object_group_network(
        device,
        og_name
):
    """ unconfigure ipv6 object-group network

        Args:
            device (`obj`): Device object
            og_name ('str'): object-group name

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    configs = "no object-group v6-network {}".format(og_name)

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure entry in ipv6 object-group {og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )


def unconfigure_ipv6_object_group_service(
        device,
        og_name
):
    """ unconfigure ipv6 object-group service

        Args:
            device (`obj`): Device object
            og_name ('str'): object-group name

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    configs = "no object-group v6-service {}".format(og_name)

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure entry in ipv6 object-group {og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )

def configure_ipv6_ogacl(
        device,
        acl_name,
        service_og,
        src_nw,
        dst_nw,
        rule,
        service_type=None,
        log_option=None,
        sequence_num=None
):
    """ Configure IPv6 Object-Group ACL

        Args:
            device (`obj`): Device object
            acl_name ('str'): access-list name
            service_og ('str'): name of Service object-group
            src_nw ('str'): name of source network object-group or any
            dst_nw ('str'): name of destination network object-group or any
            rule ('str'): ACL rule permit/deny
            service_type ('str',optional): service type to configure,default value is None
            log_option ('str',optional): Option to log ACL match,default value is None
            sequence_num ('str',optional): specific sequence number,default value is None

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = ''
    cmd += f'ipv6 access-list {acl_name}\n'

    if sequence_num:
        cmd += f'sequence {sequence_num} '

    cmd += f'{rule} '

    if service_type:
        cmd += f'{service_type} '
    elif service_og == 'any':
        cmd += 'any '
    else:
        cmd += f'object-group {service_og} '

    if src_nw == 'any':
        cmd += 'any '
    else:
        cmd += f'object-group {src_nw} '

    if dst_nw == 'any':
        cmd += 'any '
    else:
        cmd += f'object-group {dst_nw} '

    if log_option:
        cmd += f'{log_option}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure IPv6 OG ACL {acl} on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ipv6_ogacl_ace(
        device,
        acl_name,
        service_og,
        src_nw,
        dst_nw,
        rule,
        service_type=None,
        log_option=None,
        sequence_num=None
):
    """ Unconfigure Access-list Entry (ACE) from IPv6 Object-Group ACL

        Args:
            device (`obj`): Device object
            acl_name ('str'): access-list name
            service_og ('str'): Service object-group
            src_nw ('str'): source network object-group or any
            dst_nw ('str'): destination network object-group or any
            rule ('str'): ACL rule permit/deny
            service_type ('str',optional): service type to configure,default value is None
            log_option ('str',optional): Option to log ACL match,default value is None
            sequence_num ('str',optional): specific sequence number,default value is None

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = ''
    cmd += f'ipv6 access-list {acl_name}\n'

    if sequence_num:
        cmd += f'no sequence {sequence_num} '

    else:
        cmd += f'no {rule} '

        if service_type:
            cmd += f'{service_type} '
        elif service_og == 'any':
            cmd += 'any '
        else:
            cmd += f'object-group {service_og} '

        if src_nw == 'any':
            cmd += 'any '
        else:
            cmd += f'object-group {src_nw} '

        if dst_nw == 'any':
            cmd += 'any '
        else:
            cmd += f'object-group {dst_nw} '

        if log_option:
            cmd += f'{log_option}'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure IPv6 OG ACL {acl} entry on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ipv6_acl(
        device,
        acl_name
):
    """ Unconfigure IPv6 ACL

        Args:
            device (`obj`): Device object
            acl_name ('str'): access-list name

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    configs = "no ipv6 access-list {}".format(acl_name)

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

def configure_ipv6_acl_on_interface(device, interface, acl_name, inbound=True):
    """ Configures IPv6 acl on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            acl_name ('str'): acl name to apply
            inbound ('bool', option): True for inbound acl, False for outbound acl, default value is True
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
            "interface {intf}\nipv6 traffic-filter {acl} {direction}".format(
                intf=interface, acl=acl_name, direction=direction
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure acl {acl} on interface {interface} Error:\n{error}".format(
                acl=acl_name, interface=interface, error=e,
            )
        )

def unconfigure_ipv6_acl_on_interface(device, interface, acl_name, inbound=True):
    """ Remove acl from an interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            acl_name ('str'): acl to apply
            inbound ('bool', optional): True for inbound acl, False for outbound acl. Default value is True
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
            "interface {intf}\nno ipv6 traffic-filter {acl} {direction}".format(
                intf=interface, acl=acl_name, direction=direction
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove acl {acl} on interface {interface} Error:\n{error}".format(
                acl=acl_name, interface=interface, error=e,
            )
        )
