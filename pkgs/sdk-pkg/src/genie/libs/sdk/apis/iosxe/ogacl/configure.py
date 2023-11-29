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
    
def configure_object_group(device, group, object_group_name, protocol=None, option=None, port=None, network_option=None, ip_address_1=None, ip_address_2=None):
    """Configure object group service name
       Args:
            device ('obj'): device object
            group ('str'): group name
            object_group_name ('str'): object-group name
            protocol('str') : eg: tcp,udp,tcp-udp,eigrp
            option ('str') : eg: lt,eq,gt
            port ('str') : eg: telnet,ssh
            network_option ('str') : eg: host,range
            ip_address_1 ('str') : eg: 1.1.1.1 test
            ip_address_2 ('str') : eg 2.2.2.2 /24
       Return:
            None
       Raises:
            SubCommandFailure
    """
    config= [
               f'object-group {group} {object_group_name}' 
            ]
    if group=="service" and protocol not in ['udp','tcp','tcp-udp','icmp']:
        config.append(protocol)
    elif group=="service" and protocol in ['udp','tcp','tcp-udp','icmp']:
        if option in ['lt','gt','eq','range']:
            config.append(f"{protocol} {option} {port}")
        else :
            config.append(f"{protocol} {port}")
    elif group=="network" and network_option=="range":
        config.append(f"{network_option} {ip_address_1} {ip_address_2}")
    elif group=="network" and network_option=="host":
        config.append(f"{network_option} {ip_address_1}")
    elif group=="network" and network_option==None:
        config.append(f"{ip_address_1} {ip_address_2}")

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to Configure object group service name on {device.name}\n{e}'
        )
    


def configure_ipv4_object_group_network(device, og_name, description, ipv4_address, netmask):
    """ Configure ipvv4 object group of network type

        Args:
            device (`obj`): Device object
            og_name ('str'): object-group name
            description ('str'): description name
            ipv4_address ('str'): IPv6 address
            netmask ('str'): netmask

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("object-group network {}".format(og_name))
    configs.append("description {}".format(description))
    configs.append("{ipv4_address} {netmask}".format(ipv4_address=ipv4_address, netmask=netmask))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ipv4 object-group {og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ipv4_object_group(device, og_name):
    """ unconfigure ipv4 object-group

        Args:
            device (`obj`): Device object
            og_name ('str'): object-group name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("no object-group network {}".format(og_name))
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure entry in ipv4 object-group {og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )

def configure_ipv4_object_group_service(device, og_name, description, services):
    """ Configure ipv4 object group of service type

            Args:
                device (`obj`): Device object
                og_name ('str'): object-group name
                description ('str'): description name
                services ('list'): services provided in list

            Returns:
                None

            Raises:
                SubCommandFailure
        """
    configs = []
    configs.append("object-group service {}".format(og_name))
    configs.append("description {}".format(description))
    for service in services:
        configs.append(service)

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ipv4 object-group  service{og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ipv4_object_group_service(device, og_name):
    """ unconfigure ipv4 object-group service

        Args:
            device (`obj`): Device object
            og_name ('str'): object-group name

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    configs = "no object-group service {}".format(og_name)

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ipv4 object-group service {og_name} on device {dev}. Error:\n{error}".format(
                og_name=og_name,
                dev=device.name,
                error=e,
            )
        )

def configure_ipv4_ogacl_src_dst_nw(device, ogacl_name, rule, src_nw, dst_nw):
    """ Configure IPv4 ogacl src dst network

        Args:
            device (`obj`): Device object
            ogacl_name ('str'): og access-list name
            rule ('str'): ACL rule permit/deny
            src_nw ('str'): name of source network object-group or any
            dst_nw ('str'): name of destination network object-group or any

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("ip access-list extended {}".format(ogacl_name))
    configs.append("{rule} ip object-group {src_nw} object-group {dst_nw}".format(rule=rule, src_nw=src_nw, dst_nw=dst_nw))
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure IPv4 OG ACL {ogacl} on device {dev}. Error:\n{error}".format(
                ogacl=ogacl_name,
                dev=device.name,
                error=e,
            )
        )

def configure_ipv4_ogacl_service(device, ogacl_name, rule, service, src, dst):
    """ Configure IPv4 OG ACL service
        Args:
            device (`obj`): Device object
            ogacl_name ('str'): og access-list name
            rule ('str'): ACL rule permit/deny
            service ('str'): provide service group name
            src ('str'): name of source  object-group or any
            dst('str'): name of destination  object-group or any

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("ip access-list extended {}".format(ogacl_name))
    configs.append("{rule} object-group {service} {src} {dst}".format(rule=rule, service=service, src=src, dst=dst))
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure IPv4 OG ACL service {ogacl} on device {dev}. Error:\n{error}".format(
                ogacl=ogacl_name,
                dev=device.name,
                error=e,
            )
        )

def configure_ipv4_ogacl_ip(device, ogacl_name, rule, ip_src, ip_dst):
    """ Configure IPv4 OG ACL ip
        Args:
            device (`obj`): Device object
            ogacl_name ('str'): og access-list name
            rule ('str'): ACL rule permit/deny
            ip_src ('str'): ip address or any
            ip_dst('str'): ip address or any

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("ip access-list extended {}".format(ogacl_name))
    configs.append("{rule} ip {ip_src} {ip_dst}".format(rule=rule, ip_src=ip_src, ip_dst=ip_dst))
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure IPv4 OG ACL ip {ogacl} on device {dev}. Error:\n{error}".format(
                ogacl=ogacl_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ipv4_ogacl(device, ogacl_name):
    """ Configure IPv4 OG ACL
        Args:
            device (`obj`): Device object
            ogacl_name ('str'): og access-list name
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = ("no ip access-list extended {}".format(ogacl_name))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to un configure IPv4 OG ACL {ogacl} on device {dev}. Error:\n{error}".format(
                ogacl=ogacl_name,
                dev=device.name,
                error=e,
            )
        )

def configure_ipv4_ogacl_on_interface(device, interface, ogacl_name, inbound=True):
    """ Configures IPv4 ogacl on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            ogacl_name ('str'): ogacl name to apply
            inbound ('bool', option): True for inbound acl, False for outbound acl, default value is True
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if inbound:
        log.info(
            "Configure inbound {acl} on {intf}".format(
                acl=ogacl_name, intf=interface
            )
        )
        direction = "in"
    else:
        log.info(
            "Configure outbound {acl} on {intf}".format(
                acl=ogacl_name, intf=interface
            )
        )
        direction = "out"

    try:
        device.configure(
            "interface {intf}\nip access-group {acl} {direction}".format(
                intf=interface, acl=ogacl_name, direction=direction
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure ipv4 ogacl {ogacl} on interface {interface} Error:\n{error}".format(
                ogacl=ogacl_name, interface=interface, error=e,
            )
        )

def unconfigure_ipv4_ogacl_on_interface(device, interface, ogacl_name, inbound=True):
    """ Unconfigures IPv4 ogacl on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            ogacl_name ('str'): ogacl name to apply
            inbound ('bool', option): True for inbound acl, False for outbound acl, default value is True
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if inbound:
        log.info(
            "Remove inbound {acl} on {intf}".format(
                acl=ogacl_name, intf=interface
            )
        )
        direction = "in"
    else:
        log.info(
            "Remove outbound {acl} on {intf}".format(
                acl=ogacl_name, intf=interface
            )
        )
        direction = "out"

    try:
        device.configure(
            "interface {intf}\nno ip access-group {acl} {direction}".format(
                intf=interface, acl=ogacl_name, direction=direction
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Unconfigure ipv4 ogacl {ogacl} on interface {interface} Error:\n{error}".format(
                ogacl=ogacl_name, interface=interface, error=e,
            )
        )