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
        configs.append("permit {protocol} any any".format(protocol=protocol))

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

def configure_ipv6_acl(
        device,
        acl_name,
        service_type,
        src_nw,
        dst_nw,
        rule,
        host_option=True,
        prefix=None,
        dst_port=None,
        log_option=None,
        sequence_num=None
):
    """ Configure IPv6 ACL

        Args:
            device (`obj`): Device object
            acl_name ('str'): access-list name
            service_type ('str'): service type to configure
            src_nw ('str'): name of the source network object-group or any
            dst_nw ('str'): name of the destination network object-group or any
            rule ('str'): ACL rule permit/deny
            host_option('bool',optional): True to configure ace with host keyword, False if host keyword not required. Default value is True
            prefix('str',optional): Prefix value in case of network,default value is None
            dst_port ('str',optional): Acl destination port,default value is None
            log_option ('str',optional): Option to log ACL match,default value is None
            sequence_num ('str',optional): specific sequence number,default value is None

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = f'ipv6 access-list {acl_name}\n'

    if sequence_num:
        cmd += f'sequence {sequence_num} '

    cmd += f'{rule} {service_type} '

    if src_nw == 'any':
        cmd += 'any '
    elif host_option:
        cmd += f'host {src_nw} '

    else:
        cmd += f'{src_nw}/{prefix} '

    if dst_nw == 'any':
        cmd += 'any '
    elif host_option:
        cmd += f'host {dst_nw} '
    else:
        cmd += f'{dst_nw}/{prefix} '

    if dst_port:
        cmd += f'eq {dst_port} '

    if log_option:
        cmd += f'{log_option} '

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure IPv6 ACL {acl} on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )

def unconfigure_ipv6_acl_ace(
        device,
        acl_name,
        service_type,
        src_nw,
        dst_nw,
        rule,
        host_option=True,
        prefix=None,
        dst_port=None,
        log_option=None,
        sequence_num=None
):
    """ Unconfigure IPv6 ACL ACE

        Args:
            device (`obj`): Device object
            acl_name ('str'): access-list name
            service_type ('str'): service type to configure
            src_nw ('str'): name of the source network object-group or any
            dst_nw ('str'): name of the destination network object-group or any
            rule ('str'): ACL rule permit/deny
            host_option('bool',optional): True to configure ace with host keyword, False if host keyword not required. Default value is True
            prefix('str',optional): Prefix value in case of network option,default value is None
            dst_port ('str',optional): Acl destination port,default value is None
            log_option ('str',optional): Option to log ACL match counters,default value is None
            sequence_num ('str',optional): specific sequence number,default value is None

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cmd = f'ipv6 access-list {acl_name}\n'

    if sequence_num:
        cmd += f'no sequence {sequence_num} '

    else:
        cmd += f'no {rule} {service_type} '

        if src_nw == 'any':
            cmd += 'any '
        elif host_option:
            cmd += f'host {src_nw} '

        else:
            cmd += f'{src_nw}/{prefix} '

        if dst_nw == 'any':
            cmd += 'any '
        elif host_option:
            cmd += f'host {dst_nw} '
        else:
            cmd += f'{dst_nw}/{prefix} '

        if dst_port:
            cmd += f'eq {dst_port} '

        if log_option:
            cmd += f'{log_option} '

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure IPv6 ACL {acl} on the device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )

def config_extended_acl_with_evaluate(
    device,
    acl_name,
    reflect_name,
    sequence_num=None
):
    """ Configure extended ACL with evaluate on device 
        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            reflect_name ('str'): evaluate reflect name
            sequence_num ('str',optional): specific sequence number,default value is None
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure access-list with evalute
    """
    try:
        if sequence_num is not None:
            device.configure([
                "ip access-list extended {acl}".format(acl=acl_name),
                "{sequence_num} evaluate {reflect_name}".format(sequence_num=sequence_num, reflect_name=reflect_name)
            ])
        else:
            device.configure([
                "ip access-list extended {acl}".format(acl=acl_name),
                "evaluate {reflect_name}".format(reflect_name=reflect_name)
            ])            
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure Access-list {acl} on device {dev} with evalute. Error:\n{error}".format(
                acl=acl_name,
                dev=device,
                error=e,
            )
        )

def unconfig_extended_acl_with_evaluate(device, acl_name, reflect_name,sequence_num=None):
    """ Unconfigure the extended acls
        Args:
            device ('obj'): device to use
            acl_name ('str'): name of acl
            reflect_name ('str'): name reflect acl 
            sequence_num ('str',optional): specific sequence number,default value is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        if sequence_num is not None:
            device.configure(
                ["ip access-list extended {}".format(acl_name),
                "no {sequence_num} evaluate {reflect_name}".format(reflect_name=reflect_name, 
                sequence_num=sequence_num)])
        else:
            device.configure(
                ["ip access-list extended {}".format(acl_name),
                "no evaluate {reflect_name}".format(reflect_name=reflect_name)])            
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not unconfigure extended acl with evaluate. Error:\n{error}".format(error=e))        

def config_extended_acl_with_reflect(
    device,
    acl_name,
    reflect_acl_name,
    protocol=None,
    permission="permit",
    src_ip=None,
    src_step=None,
    src_wildcard=None,
    dst_ip=None,
    dst_step=None,
    dst_wildcard=None,
    dst_port=None,
    entries=None,
    acl_type=None,
    sequence_num="",
    timeout_value="",
    timeout="",
    src_port=None,
    port_type=None,
    echo=None,
    host_query=None
):
    """ Configure extended ACL on device
        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            permission ('str'): permit 
            protocol ('str'): protocol
            src_ip ('str'): source start ip, default value is None
            src_step ('str'): increment step for source ip, default value is None
            src_wildcard ('str'): source wildcard, default value is None
            dst_ip ('str'): destination start ip, default value is None
            dst_step ('str'): increment step for destination ip, default value is None
            dst_wildcard ('str'): destination wildcard, default value is None
            src_port ('str'): Acl source port, default value is None
            dst_port ('str'): Acl destination port, default value is None
            entries ('int'): Acl entries, default value is None
            acl_type ('str', optional): type of ACL like with or without host keyword, default value is None
            port_type ('str', optional): type of ACL like with or without eq or gt or lt or neq keyword, default value is None
            sequence_num ('str',optional): specific sequence number,default value is ""
            reflect_acl_name ('str'): reflect acl name, it should be differnt name with extended ACL name, default value is None
            timeout ('str',optional): type of ACL like with or without timeout, default value is ""
            timeout_val ('int',optional): Timout value, default value is ""
            echo ('str',optional): type of ACL like with or without echo keyword, default value is None
            host_query ('str',optional): type of ACL like with or without host-query keyword, default value is None
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure access-list
    """
    configs = []
    configs.append("ip access-list extended {}".format(acl_name))
    if permission == 'permit' and reflect_acl_name is not None:
        # Build config string
        if acl_type == 'host' and protocol is not None and port_type is None:
            if src_ip is not None and dst_ip is not None and echo is None:
                configs.append(
                    "{sequence} {permission} {protocol} host {src_ip} host {dst_ip} reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num,
                    permission=permission, 
                    protocol=protocol, 
                    src_ip=src_ip, 
                    dst_ip=dst_ip,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value)) 
            elif (src_ip is not None and  src_ip != 'any') and  (dst_ip is None or dst_ip == 'any') and echo is None:
                configs.append(
                    "{sequence} {permission} {protocol} host {src_ip} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, 
                    permission=permission, 
                    protocol=protocol,
                    src_ip=src_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value))  
            elif (src_ip is None or src_ip == 'any') and (dst_ip is not None and dst_ip != 'any') and echo is None:
                configs.append(
                    "{sequence} {permission} {protocol} any host {dst_ip} reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, 
                    permission=permission, 
                    protocol=protocol,
                    dst_ip=dst_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value)) 
            elif src_ip is not None and dst_ip is not None and echo=="echo" and protocol=="icmp":
                configs.append(
                    "{sequence} {permission} {protocol} host {src_ip} host {dst_ip} echo reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, 
                    src_ip=src_ip,
                    permission=permission, 
                    protocol=protocol,
                    dst_ip=dst_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value)) 
                
        elif acl_type == 'host' and (protocol in ["tcp", "udp"]) and (port_type in ['eq', 'gt', 'lt', 'neq']):
            if src_port is not None and dst_port is not None and src_ip is not None and dst_ip is not None:
                configs.append(
                    "{sequence} {permission} {protocol} host {src_ip} {port_type} {src_port} host {dst_ip} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol, 
                    src_ip=src_ip, 
                    dst_ip=dst_ip,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout, 
                    src_port=src_port,
                    timeout_value=timeout_value, 
                    port_type=port_type, 
                    dst_port=dst_port,
                    sequence=sequence_num)) 
            elif (src_ip is not None and  src_ip != 'any') and  (dst_ip is None or dst_ip == 'any') and src_port is not None and dst_port is None:
                configs.append(
                    "{sequence} {permission} {protocol} host {src_ip} {port_type} {src_port} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol,
                    src_ip=src_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value, 
                    src_port=src_port, 
                    port_type=port_type,
                    sequence=sequence_num))  
            elif (src_ip is None or src_ip == 'any') and (dst_ip !=None and dst_ip != 'any') and src_port is None and dst_port is not None:
                configs.append(
                    "{sequence} {permission} {protocol} any host {dst_ip} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol,
                    dst_ip=dst_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value, 
                    dst_port=dst_port, 
                    port_type=port_type,
                    sequence=sequence_num)) 
            else:
                logging.debug("Conditions not met to configure")
        elif acl_type is None and protocol is not None and src_ip is None and dst_ip is None:  
            if (protocol in ["tcp", "udp"]) and (port_type in ['eq', 'gt', 'lt', 'neq']):
                configs.append(
                    "{sequence} {permission} {protocol} any any {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout, 
                    dst_port=dst_port,
                    timeout_value=timeout_value, 
                    port_type=port_type, 
                    sequence=sequence_num))  
            elif protocol=="igmp" and host_query is not None:
                configs.append(
                    "{sequence} {permission} {protocol} any any host-query reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, permission=permission, 
                    protocol=protocol,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value))                       
            else:
                configs.append(
                    "{sequence} {permission} {protocol} any any reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, permission=permission, 
                    protocol=protocol,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value))

        else:
            if (dst_wildcard != "0.0.0.0" or src_wildcard != "0.0.0.0") and (dst_ip is not None or src_ip is not None) and port_type is None:
                if entries is None:
                    entries = 0
                else:
                    entries=int(entries)
                    if entries > 1:
                        if src_ip is not None and dst_ip is not None and protocol is not None and dst_step is not None and src_step is not None and port_type is None:
                            for i in range(entries):
                                src_ip = IPv4Address(src_ip)
                                src_step = IPv4Address(src_step)
                                dst_ip = IPv4Address(dst_ip)
                                dst_step = IPv4Address(dst_step)
                                src_ip_inc = src_ip + i
                                dst_ip_inc = dst_ip + i
                                configs.append(
                                    "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {dst_ip} {dst_wildcard} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        src_ip=src_ip_inc,
                                        src_wildcard=src_wildcard,
                                        dst_ip=dst_ip_inc,
                                        dst_wildcard=dst_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout,timeout_value=timeout_value))
                        elif src_ip is None and dst_ip is not None and protocol is not None and dst_step is not None:
                            for i in range(entries):
                                dst_ip = IPv4Address(dst_ip)
                                dst_step = IPv4Address(dst_step)
                                dst_ip_inc = dst_ip + i
                                configs.append(
                                    "{sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        dst_ip=dst_ip_inc,
                                        dst_wildcard=dst_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout,timeout_value=timeout_value))                        
                        elif src_ip is not None and dst_ip is None and protocol is not None and src_step is not None:
                            for i in range(entries):
                                src_ip = IPv4Address(src_ip)
                                src_step = IPv4Address(src_step)
                                src_ip_inc = src_ip + i
                                configs.append(
                                    "{sequence} {permission} {protocol} {src_ip} {src_wildcard} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        src_ip=src_ip_inc,
                                        src_wildcard=src_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout,timeout_value=timeout_value))   

                    elif entries == 1:
                        if src_ip is not None and dst_ip is not None and port_type is None:
                            configs.append(
                                "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {dst_ip} {dst_wildcard} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip,
                                    src_wildcard=src_wildcard,
                                    dst_ip=dst_ip,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name,timeout=timeout,timeout_value=timeout_value))
                        elif src_ip is None and dst_ip is not None and protocol is not None:
                            configs.append(
                                "{sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,                                
                                    dst_ip=dst_ip,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name,timeout=timeout,timeout_value=timeout_value))   
                        elif src_ip is not None and dst_ip is None and protocol is not None:
                            configs.append(
                                "{sequence} {permission} {protocol} {src_ip} {src_wildcard} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip,
                                    src_wildcard=src_wildcard,
                                    reflect_acl_name=reflect_acl_name,timeout=timeout,timeout_value=timeout_value))     
            elif (dst_wildcard != "0.0.0.0" or src_wildcard != "0.0.0.0") and (dst_ip is not None or src_ip is not None) and (protocol in ["tcp", "udp"]) and (port_type in ['eq', 'gt', 'lt', 'neq']):
                if entries is None:
                    entries = 0
                else:
                    entries=int(entries)
                    if entries > 1:
                        if src_ip is not None and dst_ip is not None and dst_step is not None and src_step is not None and src_port is not None or dst_port is not None:
                            for i in range(entries):
                                src_ip = IPv4Address(src_ip)
                                src_step = IPv4Address(src_step)
                                dst_ip = IPv4Address(dst_ip)
                                dst_step = IPv4Address(dst_step)
                                src_ip_inc = src_ip + i
                                dst_ip_inc = dst_ip + i
                                configs.append(
                                    "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} {dst_ip} {dst_wildcard} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=i + 1,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip_inc,
                                    src_wildcard=src_wildcard,
                                    dst_ip=dst_ip_inc,
                                    dst_wildcard=dst_wildcard,
                                    port_type=port_type,
                                    reflect_acl_name=reflect_acl_name,
                                    timeout=timeout,
                                    timeout_value=timeout_value,
                                    src_port=src_port,
                                    dst_port=dst_port))
                        elif src_ip is None and dst_ip is not None and dst_step is not None and src_port is None or dst_port is not None:
                            for i in range(entries):
                                    dst_ip = IPv4Address(dst_ip)
                                    dst_step = IPv4Address(dst_step)
                                    dst_ip_inc = dst_ip + i
                                    configs.append(
                                        "{sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                            sequence=i + 1,
                                            permission=permission,
                                            protocol=protocol,
                                            dst_ip=dst_ip_inc,
                                            dst_wildcard=dst_wildcard,
                                            reflect_acl_name=reflect_acl_name,timeout=timeout,
                                            timeout_value=timeout_value,port_type=port_type,
                                            dst_port=dst_port))                        
                        elif src_ip is not None and dst_ip is None and protocol is not None and src_step is not None:
                            for i in range(entries):
                                src_ip = IPv4Address(src_ip)
                                src_step = IPv4Address(src_step)
                                src_ip_inc = src_ip + i
                                configs.append(
                                    "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        src_ip=src_ip_inc,
                                        src_wildcard=src_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout, 
                                        timeout_value=timeout_value,port_type=port_type, 
                                        src_port=src_port))   

                    elif entries == 1:
                        if src_ip is not None and dst_ip is not None and src_port is not None and dst_port is not None:
                            configs.append(
                                "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} {dst_ip} {dst_wildcard} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip, 
                                    src_port=src_port,
                                    src_wildcard=src_wildcard, 
                                    port_type=port_type,
                                    dst_ip=dst_ip, 
                                    dst_port=dst_port,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name, 
                                    timeout=timeout,
                                    timeout_value=timeout_value))
                        elif src_ip is None and dst_ip is not None and dst_port is not None and src_port is None:
                            configs.append(
                                "{sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,port_type=port_type,                               
                                    dst_ip=dst_ip, 
                                    dst_port=dst_port,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name, 
                                    timeout=timeout,
                                    timeout_value=timeout_value))   
                        elif src_ip is not None and src_port is not None and dst_port is None and dst_ip is None:
                            configs.append(
                                "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip, 
                                    port_type=port_type,
                                    src_wildcard=src_wildcard, 
                                    src_port=src_port,
                                    reflect_acl_name=reflect_acl_name, 
                                    timeout=timeout,
                                    timeout_value=timeout_value))                                                   
    else:
        if protocol is not None:
            configs.append("deny {protocol} any any".format(protocol=protocol))
        else:
            logging.info("Failed to apply relect access-list configs, conditions doesn't met ")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure Access-list {acl} with reflect on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )        

def unconfig_extended_acl_with_reflect(
    device,
    acl_name,
    reflect_acl_name,
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
    sequence_num="",
    timeout_value="",
    timeout="",
    src_port=None,
    port_type=None
):
    """ Unconfigure extended ACL on device
        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            permission ('str'): permit 
            protocol ('str'): protocol
            src_ip ('str'): source start ip, default value is None
            src_step ('str'): increment step for source ip, default value is None
            src_wildcard ('str'): source wildcard, default value is None
            dst_ip ('str'): destination start ip, default value is None
            dst_step ('str'): increment step for destination ip, default value is None
            dst_wildcard ('str'): destination wildcard, default value is None
            src_port ('str'): Acl source port, default value is None
            dst_port ('str'): Acl destination port, default value is None
            entries ('int'): Acl entries, default value is None
            acl_type ('str', optional): type of ACL like with or without host keyword, default value is None
            port_type ('str', optional): type of ACL like with or without eq or gt or lt or neq keyword, default value is None
            sequence_num ('str',optional): specific sequence number,default value is ""
            reflect_acl_name ('str'): reflect acl name, it should be differnt name with extended ACL name, default value is None
            timeout ('str',optional): type of ACL like with or without timeout, default value is ""
            timeout_val ('int',optional): Timout value, default value is ""
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure access-list
    """
    configs = []
    configs.append("ip access-list extended {}".format(acl_name))
    if permission == 'permit' and reflect_acl_name is not None:
        # Build config string
        if acl_type == 'host' and protocol is not None and port_type is None:
            if src_ip is not None and dst_ip is not None:
                configs.append(
                    "no {sequence} {permission} {protocol} host {src_ip} host {dst_ip} reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num,
                    permission=permission, 
                    protocol=protocol, 
                    src_ip=src_ip, 
                    dst_ip=dst_ip,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value)) 
            elif (src_ip is not None and  src_ip != 'any') and  (dst_ip is None or dst_ip == 'any'):
                configs.append(
                    "no {sequence} {permission} {protocol} host {src_ip} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, 
                    permission=permission, 
                    protocol=protocol,
                    src_ip=src_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value))  
            elif (src_ip is None or src_ip == 'any') and (dst_ip is not None and dst_ip != 'any'):
                configs.append(
                    "no {sequence} {permission} {protocol} any host {dst_ip} reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, 
                    permission=permission, 
                    protocol=protocol,
                    dst_ip=dst_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value)) 
            else: 
                logging.debug("Conditions not met to configure")
        elif acl_type == 'host' and (protocol in ["tcp", "udp"]) and (port_type in ['eq', 'gt', 'lt', 'neq']):
            if src_port is not None and dst_port is not None and src_ip is not None and dst_ip is not None:
                configs.append(
                    "no {sequence} {permission} {protocol} host {src_ip} {port_type} {src_port} host {dst_ip} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol, 
                    src_ip=src_ip, 
                    dst_ip=dst_ip,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout, 
                    src_port=src_port, 
                    dst_port=dst_port, 
                    timeout_value=timeout_value, 
                    port_type=port_type,
                    sequence=sequence_num)) 
            elif (src_ip is not None and  src_ip != 'any') and  (dst_ip is None or dst_ip == 'any') and src_port is not None and dst_port is None:
                configs.append(
                    "no {sequence} {permission} {protocol} host {src_ip} {port_type} {src_port} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol,
                    src_ip=src_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value, 
                    src_port=src_port, 
                    port_type=port_type,
                    sequence=sequence_num))  
            elif (src_ip is None or src_ip == 'any') and (dst_ip is not None and dst_ip != 'any') and src_port is None and dst_port is not None:
                configs.append(
                    "no {sequence} {permission} {protocol} any host {dst_ip} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol,
                    dst_ip=dst_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value, 
                    dst_port=dst_port, 
                    port_type=port_type,
                    sequence=sequence_num)) 
            else:
                logging.debug("Conditions not met to configure")
        elif acl_type==None and protocol!=None and src_ip==None and dst_ip==None:  
            if (protocol in ["tcp", "udp"]) and (port_type in ['eq', 'gt', 'lt', 'neq']):
                configs.append(
                    "no {sequence} {permission} {protocol} any any {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission,
                    protocol=protocol,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value, 
                    port_type=port_type, 
                    sequence=sequence_num,
                    dst_port=dst_port))                
            else:
                configs.append(
                    "no {sequence} {permission} {protocol} any any reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, 
                    permission=permission, 
                    protocol=protocol,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value))

        else:
            if (dst_wildcard != "0.0.0.0" or src_wildcard != "0.0.0.0") and (dst_ip is not None or src_ip is not None) and port_type is None:
                if entries is None:
                    entries = 0
                else:
                    entries=int(entries)
                    if entries > 1:
                        if src_ip is not None and dst_ip is not None and protocol is not None and dst_step is not None and src_step is not None and port_type is None:
                            for i in range(entries):
                                src_ip = IPv4Address(src_ip)
                                src_step = IPv4Address(src_step)
                                dst_ip = IPv4Address(dst_ip)
                                dst_step = IPv4Address(dst_step)
                                src_ip_inc = src_ip + i
                                dst_ip_inc = dst_ip + i
                                configs.append(
                                    "no {sequence} {permission} {protocol} {src_ip} {src_wildcard} {dst_ip} {dst_wildcard} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        src_ip=src_ip_inc,
                                        src_wildcard=src_wildcard,
                                        dst_ip=dst_ip_inc,
                                        dst_wildcard=dst_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout, timeout_value=timeout_value))
                        elif src_ip is None and dst_ip is not None and protocol is not None and dst_step is not None:
                            for i in range(entries):
                                dst_ip = IPv4Address(dst_ip)
                                dst_step = IPv4Address(dst_step)
                                dst_ip_inc = dst_ip + i
                                configs.append(
                                    "no {sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        dst_ip=dst_ip_inc,
                                        dst_wildcard=dst_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout, timeout_value=timeout_value))                        
                        elif src_ip is not None and dst_ip is None and protocol is not None and src_step is not None:
                            for i in range(entries):
                                src_ip = IPv4Address(src_ip)
                                src_step = IPv4Address(src_step)
                                src_ip_inc = src_ip + i
                                configs.append(
                                    "no {sequence} {permission} {protocol} {src_ip} {src_wildcard} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        src_ip=src_ip_inc,
                                        src_wildcard=src_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout, timeout_value=timeout_value))   

                    elif entries == 1:
                        if src_ip is not None and dst_ip is not None and port_type is None:
                            configs.append(
                                "no {sequence} {permission} {protocol} {src_ip} {src_wildcard} {dst_ip} {dst_wildcard} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip,
                                    src_wildcard=src_wildcard,
                                    dst_ip=dst_ip,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name, timeout=timeout,timeout_value=timeout_value))
                        elif src_ip is None and dst_ip is not None and protocol is not None:
                            configs.append(
                                "no {sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,                                
                                    dst_ip=dst_ip,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name, timeout=timeout,timeout_value=timeout_value))   
                        elif src_ip is not None and dst_ip is None and protocol is not None:
                            configs.append(
                                "no {sequence} {permission} {protocol} {src_ip} {src_wildcard} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip,
                                    src_wildcard=src_wildcard,
                                    reflect_acl_name=reflect_acl_name, timeout=timeout,timeout_value=timeout_value))     
            elif (dst_wildcard != "0.0.0.0" or src_wildcard != "0.0.0.0") and (dst_ip is not None or src_ip is not None) and (protocol in ["tcp", "udp"]) and (port_type in ['eq', 'gt', 'lt', 'neq']):
                if entries is None:
                    entries = 0
                else:
                    entries=int(entries)
                    if entries > 1:
                        if src_ip is not None and dst_ip is not None and dst_step is not None and src_step is not None and src_port is not None or dst_port is not None:
                            for i in range(entries):
                                src_ip = IPv4Address(src_ip)
                                src_step = IPv4Address(src_step)
                                dst_ip = IPv4Address(dst_ip)
                                dst_step = IPv4Address(dst_step)
                                src_ip_inc = src_ip + i
                                dst_ip_inc = dst_ip + i
                                configs.append("no {sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} {dst_ip} {dst_wildcard} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        src_ip=src_ip_inc,
                                        src_wildcard=src_wildcard,
                                        dst_ip=dst_ip_inc,
                                        dst_wildcard=dst_wildcard, port_type=port_type,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout, timeout_value=timeout_value,src_port=src_port, dst_port=dst_port))
                        elif src_ip is None and dst_ip is not None and dst_step is not None and src_port is None or dst_port is not None:
                            for i in range(entries):
                                    dst_ip = IPv4Address(dst_ip)
                                    dst_step = IPv4Address(dst_step)
                                    dst_ip_inc = dst_ip + i
                                    configs.append(
                                        "no {sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                            sequence=i + 1,
                                            permission=permission,
                                            protocol=protocol,
                                            dst_ip=dst_ip_inc,
                                            dst_wildcard=dst_wildcard,
                                            reflect_acl_name=reflect_acl_name,timeout=timeout, timeout_value=timeout_value,port_type=port_type, dst_port=dst_port))                        
                        elif src_ip is not None and dst_ip is None and protocol is not None and src_step is not None:
                            for i in range(entries):
                                src_ip = IPv4Address(src_ip)
                                src_step = IPv4Address(src_step)
                                src_ip_inc = src_ip + i
                                configs.append(
                                    "no {sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        src_ip=src_ip_inc,
                                        src_wildcard=src_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout, timeout_value=timeout_value,port_type=port_type, src_port=src_port))   

                    elif entries == 1:
                        if src_ip is not None and dst_ip is not None and src_port is not None and dst_port is not None:
                            configs.append(
                                "no {sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} {dst_ip} {dst_wildcard} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip, src_port=src_port,
                                    src_wildcard=src_wildcard, port_type=port_type,
                                    dst_ip=dst_ip, dst_port=dst_port,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name, timeout=timeout,timeout_value=timeout_value))
                        elif src_ip is None and dst_ip is not None and dst_port is not None and src_port is None:
                            configs.append(
                                "no {sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} {port_type} {dst_port} reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,port_type=port_type,                               
                                    dst_ip=dst_ip, dst_port=dst_port,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name, timeout=timeout,timeout_value=timeout_value))   
                        elif src_ip is not None and src_port is not None and dst_port is None and dst_ip is None:
                            configs.append(
                                "no {sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} any reflect {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip, port_type=port_type,
                                    src_wildcard=src_wildcard, src_port=src_port,
                                    reflect_acl_name=reflect_acl_name, timeout=timeout,timeout_value=timeout_value))                                                                                                                  
    else:
        if protocol is not None:
            configs.append("no deny {protocol} any any".format(protocol=protocol))
        else:
            logging.info("Failed to apply relect access-list configs, conditions doesn't met ")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure Access-list {acl} with reflect on device {dev}. Error:\n{error}".format(
                acl=acl_name,
                dev=device.name,
                error=e,
            )
        )        
