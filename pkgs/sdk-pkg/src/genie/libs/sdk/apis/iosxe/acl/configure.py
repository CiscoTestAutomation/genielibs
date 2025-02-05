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
    sequence_num=None,
    log_option=None,
    time_range=None,
    port_type=None
):
    """ Configure extended ACL on device
        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            permission ('str'): (permit | deny), default value is None
            protocol ('str'): protocol, default value is None
            src_ip ('str'): source start ip, default value is None
            src_step ('str'): (None | '0.0.0.1'), increment step for source ip, default value is None
            src_wildcard ('str'): source wildcard, default value is None
            dst_ip ('str'): destination start ip, default value is None
            dst_step ('str'): increment step for destination ip, default value is None
            dst_wildcard ('str'): destination wildcard, default value is None
            dst_port ('str'): Acl destination port, default value is None
            entries ('int'): Acl entries, default value is None
            acl_type ('str', optional): type of ACL like with or without host keyword, default value is None
            sequence_num ('str',optional): specific sequence number,default value is None
            log_option ('str',optional): (None | log), Option to log ACL match,default value is None
            time_range ('str',optional): name of the time-range, default value is None
            port_type ('str',optional): name of the port_type ex : 'eq', 'gt', 'lt', 'neq', default value is None
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure access-list
    """
    configs = []
    configs.append("ip access-list extended {}".format(acl_name))
    if permission in ['permit', 'deny']:
        if acl_type and src_ip and dst_ip and dst_wildcard is None:
            # Build config string
            cmd = "{sequence} {permission} {protocol} host {src_ip} host {dst_ip} ".format(
                sequence=sequence_num,
                permission=permission,
                protocol=protocol,
                src_ip=src_ip,
                dst_ip=dst_ip)
            if log_option:
                cmd += log_option
            if time_range:
                cmd += f"time-range {time_range}"
            configs.append(cmd)
        elif acl_type and dst_ip is None:
            cmd = "{sequence} {permission} {protocol} host {src_ip} any ".format(
                sequence=sequence_num,
                permission=permission,
                protocol=protocol,
                src_ip=src_ip)
            if log_option:
                cmd += log_option
            if time_range:
                cmd += f"time-range {time_range}"
            configs.append(cmd)     
        elif acl_type and src_ip and dst_ip and dst_wildcard:
            cmd = "{sequence} {permission} {protocol} host {src_ip} {dst_ip} {dst_wildcard}".format(
                sequence=sequence_num,
                permission=permission,
                protocol=protocol,
                src_ip=src_ip,
                dst_ip=dst_ip,
                dst_wildcard=dst_wildcard)
            configs.append(cmd)                    
        elif acl_type is None and protocol is not None and src_ip=='any' and dst_ip=="any":  
            if (protocol in ["tcp", "udp"]) and (port_type in ['eq', 'gt', 'lt', 'neq']) and (time_range is not None):
                configs.append(
                    "{sequence_num} {permission} {protocol} any any {port_type} {dst_port} time-range {time_range}".format(permission=permission, 
                    protocol=protocol,
                    dst_port=dst_port,
                    port_type=port_type, 
                    sequence_num=sequence_num,
                    time_range=time_range))  
            elif (protocol in ["tcp", "udp"]) and (port_type in ['eq', 'gt', 'lt', 'neq']) and (time_range is None):
                configs.append(
                    "{sequence_num} {permission} {protocol} any any {port_type} {dst_port}".format(permission=permission, 
                    protocol=protocol,
                    dst_port=dst_port,
                    port_type=port_type, 
                    sequence_num=sequence_num,))  
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
                        cmd = "{sequence} {permission} {protocol} {src_ip} ".format(
                                sequence=i + 1,
                                permission=permission,
                                protocol=protocol,
                                src_ip=src_ip_inc)
                        if src_wildcard:
                            cmd += f"{src_wildcard} "
                        cmd += f"{dst_ip_inc} "
                        if dst_wildcard:
                            cmd += f"{dst_wildcard} "
                        if dst_port:
                            cmd += f"eq {dst_port} "
                        if time_range:
                            cmd += f"time-range {time_range}"
                        if log_option:
                            cmd += log_option
                        configs.append(cmd)

                if entries == 1:
                    cmd = "{sequence} {permission} {protocol} {src_ip} ".format(
                            sequence=sequence_num,
                            permission=permission,
                            protocol=protocol,
                            src_ip=src_ip)
                    if src_wildcard:
                        cmd += f"{src_wildcard} "
                    cmd += f"{dst_ip} "
                    if dst_wildcard:
                        cmd += f"{dst_wildcard} "
                    if dst_port:
                        cmd += f"eq {dst_port} "
                    if time_range:
                        cmd += f"time-range {time_range}"
                    if log_option:
                        cmd += log_option
                    configs.append(cmd)
                    sequence_num = str(int(sequence_num) + 1)

            if src_wildcard != "0.0.0.0":
                if entries > 1:
                    for i in range(entries):
                        src_ip = IPv4Address(src_ip)
                        src_step = IPv4Address(src_step)
                        dst_ip = IPv4Address(dst_ip)
                        dst_step = IPv4Address(dst_step)
                        src_ip_inc = src_ip + i
                        dst_ip_inc = dst_ip + i
                        cmd = "{sequence} {permission} {protocol} {src_ip} ".format(
                                sequence=i + entries + 1,
                                permission=permission,
                                protocol=protocol,
                                src_ip=src_ip_inc)
                        if src_wildcard:
                            cmd += f"{src_wildcard} "
                        cmd += f"host {dst_ip_inc} "
                        if dst_port:
                            cmd += f"eq {dst_port} "
                        if time_range:
                            cmd += f"time-range {time_range}"
                        if log_option:
                            cmd += log_option
                        configs.append(cmd)

                if entries == 1:
                    cmd = "{sequence} {permission} {protocol} {src_ip} ".format(
                            sequence=sequence_num,
                            permission=permission,
                            protocol=protocol,
                            src_ip=src_ip)
                    if src_wildcard:
                        cmd += f"{src_wildcard} "
                    if dst_ip != "any":
                        cmd += "host "
                    cmd += f"{dst_ip} "
                    if dst_port:
                        cmd += f"eq {dst_port} "
                    if time_range:
                        cmd += f"time-range {time_range}"
                    if log_option:
                        cmd += log_option
                    configs.append(cmd)
    else:
        cmd = "permit {protocol} any any ".format(protocol=protocol)
        if log_option:
            cmd += log_option
        configs.append(cmd)

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
        src_ip=None,
        src_wildcard=None,
        dst_ip=None,
        dst_wildcard=None,
        acl_type=None,
        sequence_num=None
):
    """ Unconfigure Access-list Entry (ACE) from Access-list

        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            permission ('str'): (permit | deny)
            protocol ('str'): protocol
            src_ip ('str', optional): source start ip
            src_wildcard ('str', optional): source wildcard
            dst_ip ('str', optional): destination start ip
            dst_wildcard ('str', optional): destination wildcard
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
        sequence_num=None,
        time_range=None
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
            time_range ('str',optional): name of the time-range, default value is None

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

    if time_range:
        cmd += f'time-range {time_range}'

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

def unconfigure_ipv6_acl(
        device,
        acl_name,
):
    """ Unconfigure IPv6 ACL

        Args:
            device (`obj`): Device object
            acl_name ('str'): access-list name to unconfigure
        Returns:
            None
        Raises:
            SubCommandFailure
            
    """
    configs=f"no ipv6 access-list {acl_name}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure route map {acl_name} on device {device.name}. Error:\n{e}")

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
    reflect="",
    reflect_acl_name="",
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
    if permission == 'permit':
        # Build config string
        if acl_type == 'host' and protocol is not None and port_type is None:
            if src_ip is not None and dst_ip is not None and echo is None:
                configs.append(
                    "{sequence} {permission} {protocol} host {src_ip} host {dst_ip} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num,
                    permission=permission, 
                    protocol=protocol, 
                    src_ip=src_ip, 
                    dst_ip=dst_ip,
                    reflect=reflect,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value)) 
            elif (src_ip is not None and  src_ip != 'any') and  (dst_ip is None or dst_ip == 'any') and echo is None:
                configs.append(
                    "{sequence} {permission} {protocol} host {src_ip} any {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, 
                    permission=permission, 
                    protocol=protocol,
                    src_ip=src_ip, 
                    reflect=reflect,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value))  
            elif (src_ip is None or src_ip == 'any') and (dst_ip is not None and dst_ip != 'any') and echo is None:
                configs.append(
                    "{sequence} {permission} {protocol} any host {dst_ip} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, 
                    permission=permission, 
                    protocol=protocol,
                    reflect=reflect,
                    dst_ip=dst_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value)) 
            elif src_ip is not None and dst_ip is not None and echo=="echo" and protocol=="icmp":
                configs.append(
                    "{sequence} {permission} {protocol} host {src_ip} host {dst_ip} echo {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, 
                    src_ip=src_ip,
                    permission=permission, 
                    reflect=reflect,
                    protocol=protocol,
                    dst_ip=dst_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value)) 
                
        elif acl_type == 'host' and (protocol in ["tcp", "udp"]) and (port_type in ['eq', 'gt', 'lt', 'neq']):
            if src_port is not None and dst_port is not None and src_ip is not None and dst_ip is not None:
                configs.append(
                    "{sequence} {permission} {protocol} host {src_ip} {port_type} {src_port} host {dst_ip} {port_type} {dst_port} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol, 
                    src_ip=src_ip, 
                    reflect=reflect,
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
                    "{sequence} {permission} {protocol} host {src_ip} {port_type} {src_port} any {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol,
                    src_ip=src_ip, 
                    reflect=reflect,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout,
                    timeout_value=timeout_value, 
                    src_port=src_port, 
                    port_type=port_type,
                    sequence=sequence_num))  
            elif (src_ip is None or src_ip == 'any') and (dst_ip !=None and dst_ip != 'any') and src_port is None and dst_port is not None:
                configs.append(
                    "{sequence} {permission} {protocol} any host {dst_ip} {port_type} {dst_port} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol,
                    dst_ip=dst_ip, 
                    reflect_acl_name=reflect_acl_name, 
                    reflect=reflect,
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
                    "{sequence} {permission} {protocol} any any {port_type} {dst_port} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(permission=permission, 
                    protocol=protocol,
                    reflect_acl_name=reflect_acl_name, 
                    timeout=timeout, 
                    reflect=reflect,
                    dst_port=dst_port,
                    timeout_value=timeout_value, 
                    port_type=port_type, 
                    sequence=sequence_num))  
            elif protocol=="igmp" and host_query is not None:
                configs.append(
                    "{sequence} {permission} {protocol} any any host-query {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, permission=permission, 
                    protocol=protocol,
                    reflect_acl_name=reflect_acl_name, 
                    reflect=reflect,
                    timeout=timeout,
                    timeout_value=timeout_value))                       
            else:
                configs.append(
                    "{sequence} {permission} {protocol} any any {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(sequence=sequence_num, permission=permission, 
                    protocol=protocol,
                    reflect=reflect,
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
                                    "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {dst_ip} {dst_wildcard} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        reflect=reflect,
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
                                    "{sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        reflect=reflect,
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
                                    "{sequence} {permission} {protocol} {src_ip} {src_wildcard} any {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        reflect=reflect,
                                        protocol=protocol,
                                        src_ip=src_ip_inc,
                                        src_wildcard=src_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout,timeout_value=timeout_value))   

                    elif entries == 1:
                        if src_ip is not None and dst_ip is not None and port_type is None:
                            configs.append(
                                "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {dst_ip} {dst_wildcard} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip,
                                    src_wildcard=src_wildcard,
                                    dst_ip=dst_ip,
                                    reflect=reflect,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name,timeout=timeout,timeout_value=timeout_value))
                        elif src_ip is None and dst_ip is not None and protocol is not None:
                            configs.append(
                                "{sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    reflect=reflect,
                                    permission=permission,
                                    protocol=protocol,                                
                                    dst_ip=dst_ip,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name,timeout=timeout,timeout_value=timeout_value))   
                        elif src_ip is not None and dst_ip is None and protocol is not None:
                            configs.append(
                                "{sequence} {permission} {protocol} {src_ip} {src_wildcard} any {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    reflect=reflect,
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
                                    "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} {dst_ip} {dst_wildcard} {port_type} {dst_port} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(sequence=i + 1,
                                    permission=permission,
                                    protocol=protocol,
                                    src_ip=src_ip_inc,
                                    reflect=reflect,
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
                                        "{sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} {port_type} {dst_port} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                            sequence=i + 1,
                                            permission=permission,
                                            reflect=reflect,
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
                                    "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} any {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                        sequence=i + 1,
                                        permission=permission,
                                        protocol=protocol,
                                        reflect=reflect,
                                        src_ip=src_ip_inc,
                                        src_wildcard=src_wildcard,
                                        reflect_acl_name=reflect_acl_name,timeout=timeout, 
                                        timeout_value=timeout_value,port_type=port_type, 
                                        src_port=src_port))   

                    elif entries == 1:
                        if src_ip is not None and dst_ip is not None and src_port is not None and dst_port is not None:
                            configs.append(
                                "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} {dst_ip} {dst_wildcard} {port_type} {dst_port} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    reflect=reflect,
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
                                "{sequence} {permission} {protocol} any {dst_ip} {dst_wildcard} {port_type} {dst_port} {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    reflect=reflect,
                                    protocol=protocol,port_type=port_type,                               
                                    dst_ip=dst_ip, 
                                    dst_port=dst_port,
                                    dst_wildcard=dst_wildcard,
                                    reflect_acl_name=reflect_acl_name, 
                                    timeout=timeout,
                                    timeout_value=timeout_value))   
                        elif src_ip is not None and src_port is not None and dst_port is None and dst_ip is None:
                            configs.append(
                                "{sequence} {permission} {protocol} {src_ip} {src_wildcard} {port_type} {src_port} any {reflect} {reflect_acl_name} {timeout} {timeout_value}".format(
                                    sequence=sequence_num,
                                    permission=permission,
                                    reflect=reflect,
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

def configure_scale_ipv6_accesslist_config(device, acl_name, acl_list):
    """ Configure the huge(more than 1k static acl) acls under ipv6 access-list
        Args:
            device ('obj'): device to use
            acl_name ('str'): name of acl
            acl_list ('str') : acl_lists
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure acls under ipv6 access-list
    """
    log.info(f"Configuring acls under ipv6 access-list")
    configs=[
        f"ipv6 access-list {acl_name}",
        f"{acl_list}",
    ]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure acl under ipv6 access-list. Error:\n{e}")

def config_refacl_global_timeout(device, timeout):
    """ Configures timeout for reflexive acl globally 

        Args:
            device ('obj'): device to use
            timeout ('str'): time out value to apply, range:30-2147483
    """
    try:
        device.configure(
            "ip reflexive-list timeout {timeout}".format(
                timeout=timeout
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure Timeout on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,
            )
        )

def unconfig_refacl_global_timeout(device, timeout):
    """ Unconfigures timeout for reflexive acl globally 

        Args:
            device ('obj'): device to use
            timeout ('str'): time out value to apply, range:30-2147483
    """
    try:
        device.configure(
            "no ip reflexive-list timeout {timeout}".format(
                timeout=timeout
            )
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ACL on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,
            )
        )
def config_ip_tcp_mss(device, seg_size, global_config_key, interface=None):
    """ Configures tcp Maximum Segment Size 

        Args:
            device ('obj'): device to use
            global_config_key ('str'): set global_config_key to 1 for global else set it to 0 for interface level config
            seg_size ('str'): segment size value to apply, range:0-10000
            interface('str'): interface on which mss needs to be configured
    """
    if global_config_key == '1':
        try:
            device.configure(
                "ip tcp mss {seg_size}".format(
                    seg_size=seg_size
            )
        )
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Failed to configure tcp mss on the device {dev}. Error:\n{error}".format(
                    dev=device.name,
                    error=e,
                )
            )
    else:
        try:
            device.configure(
                ["interface {interface}".format(interface=interface), "ip tcp adjust-mss {seg_size}".format(
                    seg_size=seg_size
            )]
        )
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Failed to configure tcp mss on the device {dev}. Error:\n{error}".format(
                    dev=device.name,
                    error=e,

            )
        )

def unconfig_ip_tcp_mss(device, seg_size, global_config_key, interface=None):
    """ Unconfigures tcp Maximum Segment Size

        Args:
            device ('obj'): device to use
            global_config_key ('str'): set global_config_key to 1 for global else set it to 0 for interface level config
            seg_size ('str'): segment size value to apply, range:0-10000
            interface ('str'): interface on which mss needs to be unconfigured.
    """
    if global_config_key == '1':
        try:
            device.configure(
                "no ip tcp mss {seg_size}".format(
                    seg_size=seg_size
            )
        )
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Failed to unconfigure tcp mss on the device {dev}. Error:\n{error}".format(
                    dev=device.name,
                    error=e,
                )
            )
                
    else:
        try:
            device.configure(
                ["interface {interface}".format(interface=interface), "no ip tcp adjust-mss {seg_size}".format(
                    seg_size=seg_size
                    
            )]
        )
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Failed to unconfigure tcp mss on the device {dev}. Error:\n{error}".format(
                    dev=device.name,
                    error=e,

            )
        )

def configure_mac_access_group_mac_acl_in_out(device, interface_id, acl_name, acl_direction):
    """ configures mac access group ACL in/out

        Args:
            device ('obj'): device to use
            interface_id ('str'): interface on which mss needs to be configured.
    """
    cmd = [
        f"interface {interface_id}",
        f"mac access-group {acl_name} {acl_direction}"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure mac access group ACL in/out on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,

        )
    )

def configure_mac_acl(device, name, action, source, dest, ethertype=''):
    """ Configuring MAC ACL
        Example: mac access-list extended MAC-ACL
                permit host 001.00a.00a host 001.00b.00b etype-6000

        Args:
            device ('obj'): device to use
            name ('str'): name of the ACL to which the entry belongs
            action ('str'): (permit | deny) permits or denies Layer 2 traffic
            source ('str'): (src-MAC-addr) defines a source MAC address (e.g. 001.00a.00a)
            dest ('str'): (dst-MAC-addr) defines a destination MAC address (e.g. 001.00b.00b)
            ethertype ('str'): {optional} ethertype 

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    config = [f"mac access-list extended {name}"]
    action = action.strip().lower()
    if action in ('permit', 'deny'):
        config.append(f"{action} host {source} host {dest} {ethertype}")
    else:
        raise SubCommandFailure("Invalid action type")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure mac acl on the device {device.name}. Error:\n{e}")


def configure_mac_acl_etherType(device, name, action, ethertype=None, mask=None):
    """ Configuring MAC ACL
        Example: mac access-list extended aclname
                 permit any any 0x8892 0x0

        Args:
            device ('obj'): device to use
            name ('str'): name of the ACL to which the entry belongs
            action ('str'): (permit | deny) permits or denies Layer 2 traffic
            ethertype ('str'): {optional} ethertype
            mask('str') : ether type mask

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    config = [f"mac access-list extended {name}"]
    action = action.strip().lower()
    if action in ('permit', 'deny'):
        config.append(f"{action} any any {ethertype} {mask}")
    else:
        raise SubCommandFailure("Invalid action type only permit and deny are valid actions")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure mac acl on the device {device.name}. Error:\n{e}")



def configure_access_map_match_ip_address_action_forward(device, vlan_access_name):
    """ Configuring access map match ip address action forward 

        Args:
            device ('obj'): device to use
            vlan_access_name ('str'): name of vlan to access 

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    cmd = [
        f"vlan access-map {vlan_access_name}",
        f"match ip address {vlan_access_name}",
        "action forward",
        "exit"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure access map match ip address action forward  on the device {device.name}. Error:\n{e}")

def configure_filter_vlan_list(device, vlan_access_name, vlan_id):
    """ Configuring vlan filter vlan-list
        Args:
            device ('obj'): device to use
            vlan_access_name ('str'): name of vlan to access 
            vlan_id ('str'): vlan id for vlan list 
        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    cmd = [
        f"vlan filter {vlan_access_name} vlan-list {vlan_id}"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure vlan filter vlan-list on the device {device.name}. Error:\n{e}")

def configure_acl_with_src_dsc_net(device,
                            acl_name,
                            action,
                            src_net,
                            src_wild_mask,
                            dsc_net,
                            dsc_wild_mask):
    """ configure ACL
        Args:
            device (`obj`): Device object
            acl_name ('str'): ACL name
            action ('str')Optional: Permit or Deny
            src_net ('str'): Source network
            dsc_net ('str'): Destination network
            src_wild_mask('str'): Source wild card mask
            dst_wild_mask('str'): Destination wild card mask
    """
    log.info(
        "Configures acl's with source and destination network"
    )

    configs = []
    configs.append(f"access-list {acl_name} {action} ip {src_net} {src_wild_mask} {dsc_net} {dsc_wild_mask}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
                raise SubCommandFailure(f"Failed to configure acl for source and \
                destination networks on device  {device.name}. Error:\n{e}")

def unconfigure_acl_with_src_dsc_net(device,
                              acl_name):
    """ Unconfigures acl
        Args:
            device (`obj`): Device object
            acl_name ('str'): ACL name
    """
    log.info(
        "unconfiguring acl's"
    )

    configs = []
    configs.append(f"no access-list {acl_name}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure access map match source and \
                destination networks on device  {device.name}. Error:\n{e}")
def configure_interface_ipv6_acl(device, interface, acl_name, ipv6_address):
    """ 
    API for the CLI :- 
        interface {interface}\nipv6 access-list {acl_name}\npermit ipv6 any host {ipv6_address}
        e.g.
        Args:
            device ('obj'): Device object
            interface ('str'): interface name
            acl_name ('str'): name of the acl
            ipv6_address('str'): ipv6 address
        Return:
            None
        Raise:
            SubCommandFailure
    """
    cmd = f"interface {interface}\nipv6 access-list {acl_name}\npermit ipv6 any host {ipv6_address}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure acl on device {dev} with evalute. Error:\n{error}".format(
                dev=device, error=e)
            )

def configure_standard_acl(device, acl_name, sequence_number=None, action=None, host=None, ip_host=None):
    """ unconfigure Access-list
        Args:
            device ('obj'): Device object
            acl_name ('str'): Access-list name or Standard IP access-list number range <100-199> , expanded range <2000-2699>
            sequence_number('str'): Sequence Number range <1-2147483647>
            action ('str'): permit / deny 
            host('str'): host specific key word host
            ip_host('str') : host ip address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"ip access-list standard {acl_name}\n"

    if host and ip_host:
        cmd += f"{sequence_number} {action} host {ip_host}\n"
    elif ip_host:
        cmd += f"{sequence_number} {action} {ip_host}\n"
    else:
        cmd += f"{sequence_number} {action} any\n"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure {acl} on device {dev}. Error:\n{error}".format(
                acl=acl_name, dev=device.name, error=e))

def unconfigure_standard_acl(device, acl_name, sequence_number=None, action=None, host=None, ip_host=None):
    """ unconfigure Access-list
        Args:
            device ('obj'): Device object
            acl_name ('str'): Access-list name or Standard IP access-list number range <100-199> , expanded range <2000-2699>
            sequence_number('str'): Sequence Number range <1-2147483647>
            action ('str'): permit / deny 
            host('str'): host specific key word host
            ip_host('str') : host ip address
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"ip access-list standard {acl_name}\n"

    if host and ip_host:
        cmd += f"no {sequence_number} {action} host {ip_host}\n"
    elif ip_host:
        cmd += f"no {sequence_number} {action} {ip_host}\n"
    else:
        cmd += f"no {sequence_number} {action} any\n"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure {acl} on device {dev}. Error:\n{error}".format(
                acl=acl_name, dev=device.name, error=e, ) )
def configure_as_path_acl(device, acces_list_number=None, action=None, reg_exp=None):
    """ configure Access-list for as-path
        Args:
            device ('obj'): Device object
            acces_list_number (`int`): Access-list identifier ranges from <1-500>
            action('str'): permit or deny
            reg_exp ('str'): regular expression which matches for the acl
            
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"ip as-path access-list {acces_list_number} {action} {reg_exp}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure acl on device {dev}. Error:\n{error}".format(
                dev=device.name, error=e,) )

def unconfigure_as_path_acl(device, acces_list_number=None, action=None, reg_exp=None):
    """ unconfigure Access-list for as-path
        Args:
            device ('obj'): Device object
            acces_list_number ('int'): Access-list identifier ranges from <1-500>
            action('str'): permit or deny
            reg_exp ('str'): regular expression which matches for the acl
            
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"no ip as-path access-list {acces_list_number} {action} {reg_exp}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure acl on device {dev}. Error:\n{error}".format(
                dev=device.name, error=e,))

    
def unconfigure_mac_acl(device, name, action, source, dest, ethertype=None):
    """ Un configuring MAC ACL
        Example: mac access-list extended MAC-ACL
                no permit host 001.00a.00a host 001.00b.00b etype-6000

        Args:
            device ('obj'): device to use
            name ('str'): name of the ACL to which the entry belongs
            action ('str'): (permit | deny) permits or denies Layer 2 traffic
            source ('str'): (src-MAC-addr) defines a source MAC address (e.g. 001.00a.00a)
            dest ('str'): (dst-MAC-addr) defines a destination MAC address (e.g. 001.00b.00b)
            ethertype ('str'): ethertype

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    config = [f"mac access-list extended {name}"]
    action = action.strip().lower()
    if action in ('permit', 'deny'):
        config.append(f"no {action} host {source} host {dest} {ethertype}")
    else:
        raise SubCommandFailure("Invalid action type")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to un configure mac acl on the device {device.name}. Error:\n{e}")

def delete_mac_acl(device, name):
    """ Delete MAC ACL
        Example: no mac access-list extended MAC-ACL

        Args:
            device ('obj'): Device object
            name ('str'): name of the ACL to which the entry belongs

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    config = [f"no mac access-list extended {name}"]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to delete mac acl on the device {device.name}. Error:\n{e}")

def unconfigure_mac_access_group_mac_acl_in_out(device, interface_id, acl_name, acl_direction):
    """ unconfigures mac access group ACL in/out
        Args:
            device ('obj'): device to use
            interface_id ('str'): interface on which mss needs to be configured.
            acl_name ('str'): define the acl name
            acl_direction ('str'): acl_direction is (in / out)
    """
    cmd = [
        f"interface {interface_id}",
        f"no mac access-group {acl_name} {acl_direction}"
            ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
        "Failed to unconfigure mac access group ACL in/out on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                error=e,
        )
    )

def configure_ip_acl(device, name, action, source, dest):
    """ Configuring ip ACL
        Example: ip access-lists extended ip_acl
                permit ip host 100.1.1.2 host 150.1.1.2
        Args:
            device ('obj'): device to use
            name ('str'): name of the ACL to which the entry belongs
            action ('str'): (permit | deny) permits or denies Layer 2 traffic
            source ('str'): defines a source ip address (e.g. 100.1.1.2)
            dest ('str'): defines a destination ip address (e.g.150.1.1.2)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    action = action.strip().lower()
    if action not in ('permit', 'deny'):
        log.info("Invalid action type")
    config = [f"ip access-list extended {name}",
              f"{action} ip host {source} host {dest}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip acl on the device {device.name}. Error:\n{e}")

def delete_configure_ip_acl(device, name, action, source, dest):
    """ delete Configuring ip ACL
        Example: ip access-lists extended ip_acl
                no permit ip host 100.1.1.2 host 150.1.1.2
        Args:
            device ('obj'): device to use
            name ('str'): name of the ACL to which the entry belongs
            action ('str'): (permit | deny) permits or denies Layer 2 traffic
            source ('str'): defines a source ip address (e.g. 100.1.1.2)
            dest ('str'): defines a destination ip address (e.g.150.1.1.2)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    action = action.strip().lower()
    if action not in ('permit', 'deny'):
        log.info("Invalid action type")
    config = [f"ip access-list extended {name}",
              f"no {action} ip host {source} host {dest}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to delete configure ip acl on the device {device.name}. Error:\n{e}")

def delete_configure_ipv6_acl(device, name, action, source, dest):
    """ delete Configuring ip ACL
        Example: ipv6 access-lists  ip_acl
                no permit ip host 2001::1 host 3001::1
        Args:
            device ('obj'): device to use
            name ('str'): name of the ACL to which the entry belongs
            action ('str'): (permit | deny) permits or denies Layer 2 traffic
            source ('str'): (src-ip-addr) defines a source ip address (e.g. 2001::1)
            dest ('str'): (dst-ip-addr) defines a destination ip address (e.g.3001::1)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    action = action.strip().lower()
    if action not in ('permit', 'deny'):
        log.info("Invalid action type")
    config = [f"ipv6 access-list {name}",
              f"no {action} ipv6 host {source} host {dest}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to delete configure ip acl on the device {device.name}. Error:\n{e}")

def unconfigure_access_map_match_ip_address_action_forward(device, vlan_access_name):
    """ unconfiguring access map match ip address action forward 
        Args:
            device ('obj'): device to use
            vlan_access_name ('str'): name of vlan to access 
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    cmd = f"no vlan access-map {vlan_access_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure access map match ip address action forward on the device {device.name}. Error:\n{e}"
        )

def unconfigure_filter_vlan_list(device, vlan_access_name, vlan_id):
    """ unconfiguring vlan filter vlan-list
        Args:
            device ('obj'): device to use
            vlan_access_name ('str'): name of vlan to access 
            vlan_id ('str'): vlan id for vlan list 
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    cmd = f"no vlan filter {vlan_access_name} vlan-list {vlan_id}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure vlan filter vlan-list on the device {device.name}. Error:\n{e}"
        )


def configure_extended_acl(device, acl_name, permission, protocol, src_ip, dst_ip, sequence_num=None, 
                           src_wildcard=None, dst_wildcard=None, match=[]):
    """ Configure extended ACL on device
        Args:
            device ('obj'): device object
            acl_name ('str'): acl name
            permission ('str'): permit | deny
            protocol ('str'): protocol name
            src_ip ('str'): source ip
            dst_ip ('str'): destination ip
            sequence_num ('str', optional): specific sequence number. Default value is None
            src_wildcard ('str', optional): source wildcard, default value is None
            dst_wildcard ('str', optional): destination wildcard, default value is None
            match ('list', optional): match list with each dictionary contais match_criteria and value
                Ex: [
                    {
                        'match_criteria': 'range',
                        'value': '100 500'
                    },
                    {
                        'match_criteria': 'precedence',
                        'value': '4'
                    }
                ]
        Returns:
            config
        Raises:
            SubCommandFailure: Failed to configure extended access-list
    """

    config = [f'ip access-list extended {acl_name}']

    cmd = f'{f"{sequence_num} " if sequence_num else ""}{permission} {protocol} {src_ip}'\
              f'{f" {src_wildcard}" if src_wildcard else ""} {dst_ip}{f" {dst_wildcard}" if dst_wildcard else ""}'
    try:
        for each_match in match:
            if 'match_criteria' in each_match and 'value' in each_match:
                cmd += f" {each_match['match_criteria']} {each_match['value']}"
        config.append(cmd)
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure extended access-list. Error:\n{e}")


def configure_acl_with_ip_any(device, acl_name, action):
    """ configure ACL
        Args:
            device (`obj`): Device object
            acl_name ('str'): ACL name
            action ('str')Optional: Permit or Deny
    """

    config = [f"access-list {acl_name} {action} ip any any"]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure acl with ip any on device {device.name}. Error:\n{e}")

def configure_arp_acl(device, name, action, source, sender_mac='', mac_mask='', sender_host='', log=''):
    """ Configuring ARP ACL

        Args:
            device ('obj'): device to use
            name ('str'): name of the ACL to which the entry belongs
            action ('str'): (permit | deny) permits or denies Layer 2 traffic
            source ('str'): defines a sender Host IP address
            sender_mac ('str'): Sender MAC address
            mac_mask ('str'): Sender MAC address mask.Mandatory when "sender_mac" field is specified
            sender_host ('str'): Sender host MAC address
            log_on_match ('str'): Log on match, mention as "log" if required
            
        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    config = [f"arp access-list {name}"]
    action = action.strip().lower()
    if action in ('permit', 'deny') and sender_mac and log:
        config.append(f"{action} ip host {source} mac {sender_mac} {mac_mask} log")
    elif action in ('permit', 'deny') and sender_mac:
        config.append(f"{action} ip host {source} mac {sender_mac} {mac_mask}")
    elif action in ('permit', 'deny') and sender_host and log:
        config.append(f"{action} ip host {source} mac host {sender_host} log")
    elif action in ('permit', 'deny') and sender_host:
        config.append(f"{action} ip host {source} mac host {sender_host}") 
    elif action in ('permit', 'deny') and log:
        config.append(f"{action} ip host {source} mac any log")   
    elif action in ('permit', 'deny'):
        config.append(f"{action} ip host {source} mac any")     
    else:
        raise SubCommandFailure("Invalid parameters")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure arp acl on the device {device.name}. Error:\n{e}")

def configure_access_map_match_ip_mac_address(device, vlan_access_name, value, acl_name, action):
    """ Configuring access map match ip mac address

        Args:
            device ('obj'): device to use
            vlan_access_name ('str'): name of vlan to access 
            vlaue ('str'): describe mac (or) ip
            acl_name ('str'): name of acl_name
            action ('str'): forward (or) drop
        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    cmd = [
        f"vlan access-map {vlan_access_name}",
        f"match {value} address {acl_name}",
        f"action {action}",
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure access map match ip mac address on the device {device.name}. Error:\n{e}")

def configure_acl_protocol_port(device, ip_protocol_version, acl_name, acl_action, protocol, port_operation, src_port, dst_port):
    """ Configure acl protocol port

        Args:
            device ('obj'): device to use
            ip_protocol_version ('str'): define ip (or) ipv6
            acl_name ('str'): name of acl
            acl_action ('str'): permit (or) deny
            protocol ('str'): protocol details
            port_operation ('str'): name of port operation ex: range , eq, gt, lt
            src_port (int): src port details
            dst_port (int): dst port details
        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    cmd = []
    if ip_protocol_version == "ip":
        cmd.append(f"{ip_protocol_version} access-list extended {acl_name}")
    else:
        cmd.append(f"{ip_protocol_version} access-list {acl_name}")
    cmd.append(f"{acl_action} {protocol} any any {port_operation} {src_port} {dst_port}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure acl protocol port {device.name}. Error:\n{e}")

def configure_ip_acl_with_any(device, acl_name, acl_action):
    """ Configuring ip ACL with any
        Example: ip access-lists extended ip_acl
                permit ip any any
        Args:
            device ('obj'): device to use
            acl_name ('str'): name of the ACL to which the entry belongs
            acl_action ('str'): (permit | deny) permits or denies Layer 2 traffic
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    acl_action = acl_action.strip().lower()
    assert acl_action in ('permit', 'deny'), f"{acl_action} is an invalid action type"
    config = [f"ip access-list extended {acl_name}",
              f"{acl_action} ip any any"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip acl  with any on the device {device.name}. Error:\n{e}")

def configure_type_access_list_action(device, type, name, action, action_type=None, action_suffix=None):
    """ Configuring ip/mac access-list with permission
        Example: Mac access-list extended PACL_MAC_Permit 
                 no permit any any {logging}
                 permit any any {logging}
                 or
                 ip access-list extended PACL_IP_Deny 
                 No Deny ip any any {logging}
                 Deny ip any any {logging}
        Args:
            device ('obj'): device to use
            type ('str'): (ip | mac) which type it belongs to
            name ('str'): name of the ACL to which the entry belongs
            action ('str'): (permit | deny) permits or denies traffic
            action_type ('str')(optional): defines the action/permission type (Ex : ip)
            action_suffix ('str')(optional): suffix that can ass in the last of the command (Ex : logging)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    action = action.strip().lower()
    if action_type:
        if action_suffix:
            config = [f"{type} access-list extended {name}",
                    f"{action} {action_type} any any {action_suffix}"] 
        else:
            config = [f"{type} access-list extended {name}",
                    f"{action} {action_type} any any"]     
    else:
        if action_suffix:
            config = [f"{type} access-list extended {name}",
                    f"{action} any any {action_suffix}"]        
        else:
            config = [f"{type} access-list extended {name}",
                    f"{action} any any"]  
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure {type} acl on the device {device.name}. Error:\n{e}")

def configure_access_list_extend_with_dst_address_and_port(device, access_list_name, sequence_number, access_type, protocol_name, dst_address, dst_wildcard_bits, port_num1, port_num2):
    """ Configures access-list extend with destination address and ports
        Args:
             device ('obj'): device to use
             access_list_name ('str'): access list name
             sequence_number ('int'):  sequence number
             access_type ('str'): access type(i.e deny/permit)
             protocol_name ('str'): protocol name(i.e udp/tcp)
             dst_address ('str'): destinamtion address
             dst_wildcard_bits ('str'): destination wildcard bits
             port_num1 ('int'): first port number 
             port_num2 ('int'): second port number 
             
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"configure access-list extend with {dst_address} and {port_num1} and {port_num2}")

    config = [f"ip access-list extended {access_list_name}",
	      f"{sequence_number} {access_type} {protocol_name} any {dst_address} {dst_wildcard_bits} range {port_num1} {port_num2}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure access-list extend with {dst_address} and {port_num1} and {port_num2}.  Error:\n{e}")

def configure_access_list_extend_with_port(device, access_list_name, sequence_number, access_type, protocol_name, port_num1, port_num2, port_num3, port_num4):
    """ Configures access-list extend with ranges
        Args:
             device ('obj'): device to use
             access_list_name ('str'): access list name
             sequence_number ('int'):  sequence number
             access_type ('str'): access type(i.e deny/permit)
             protocol_name ('str'): protocol name(i.e udp/tcp)
             port_num1 ('int'): first port number 
             port_num2 ('int'): second port number 
             port_num3 ('int'): third port number 
             port_num4 ('int'): fourth port number 
             
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"configure access-list extend with ranges on device {device}")

    config = [f"ip access-list extended {access_list_name}",
		f"{sequence_number} {access_type} {protocol_name} any range {port_num1} {port_num2} any range {port_num3} {port_num4}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure access-list extend with ranges on device {device}.Error:\n{e}") 

def configure_access_list_extend_with_dst_address_and_gt_port(device, access_list_name, sequence_number, access_type, protocol_name, port_num1, port_num2, dst_address, port_num3):
    """ Configures access-list extend with destination address and gt port config
        Args:
             device ('obj'): device to use
             access_list_name ('str'): access list name
             sequence_number ('int'):  sequence number
             access_type ('str'): access type(i.e deny/permit)
             protocol_name ('str'): protocol name(i.e udp/tcp)
             port_num1 ('int'): first port number 
             port_num2 ('int'): second port number 
             dst_address ('str'): destinamtion address
             port_num3 ('int'): third port number 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"configure access-list extend with destination address and gt port config on device {device}")

    config = [f"ip access-list extended {access_list_name}",
		f"{sequence_number} {access_type} {protocol_name} any range {port_num1} {port_num2} host {dst_address} gt {port_num3}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure access-list extend with  destination address and gt port config on device {device}.Error:\n{e}") 
            
def configure_access_list_extend_with_range_and_eq_port(device, access_list_name, sequence_number, access_type, protocol_name, port_num1, port_num2, port_num3):
    """ Configures access-list extend with range and eq port config
        Args:
             device ('obj'): device to use
             access_list_name ('str'): access list name
             sequence_number ('int'):  sequence number
             access_type ('str'): access type(i.e deny/permit)
             protocol_name ('str'): protocol name(i.e udp/tcp)
             port_num1 ('int'): first port number 
             port_num2 ('int'): second port number 
             port_num3 ('int'): third port number 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"configure access-list extend with range and eq port config on device {device}")

    config = [f"ip access-list extended {access_list_name}",
		f"{sequence_number} {access_type} {protocol_name} any range {port_num1} {port_num2} any eq {port_num3}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure access-list extend with range and eq port config on device {device}.Error:\n{e}")  

def configure_access_list_extend(device, access_list_name, sequence_number, access_type, protocol_name):
    """ Configures access-list extend
        Args:
             device ('obj'): device to use
             access_list_name ('str'): access list name
             sequence_number ('int'):  sequence number
             access_type ('str'): access type(i.e deny/permit)
             protocol_name ('str'): protocol name(i.e udp/tcp)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"configure access-list extend on device {device}")

    config = [f"ip access-list extended {access_list_name}",
		f"{sequence_number} {access_type} {protocol_name} any any"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure access-list extend on device {device}.Error:\n{e}") 

def configure_ip_sgacl(device, acl_action, ip_protocol_version):
    """Configure ip sgacl
        Example: ip access-list role-based PERMIT
                 permit ip log
        Args:
            device ('obj'): device to use
            acl_action ('str'): (permit | deny) permits or denies traffic
            ip_protocol_version ('str'): define ip (or) ipv6
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    acl_action = acl_action.strip().lower()
    if acl_action not in ('permit', 'deny'):
        log.error("Invalid action type")
    config = [f"{ip_protocol_version} access-list role-based {acl_action}",
              f"{acl_action} {ip_protocol_version} log"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip sgacl on the device {device.name}. Error:\n{e}")

def unconfigure_ip_sgacl(device, acl_action, ip_protocol_version):
    """Unconfigure ip sgacl
        Example: no ip access-list role-based PERMIT
        Args:
            device ('obj'): device to use
            acl_action ('str'): (permit | deny) permits or denies traffic
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    acl_action = acl_action.strip().lower()
    if acl_action not in ('permit', 'deny'):
        log.error("Invalid action type")
    config = [f"no {ip_protocol_version} access-list role-based {acl_action}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ip sgacl on the device {device.name}. Error:\n{e}")

def configure_protocol_acl_any_any(device, acl_name, permission, protocol):
    """ configure permit/deny protocol any any on acl
        Args:
            device ('obj'): Device object
            acl_name ('str'): access_list name
            permission ('str'): permit | deny
            protocol ('str'): protocol Name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"configure permit/deny protocol any any on acl {acl_name}")

    config = [
        f'ip access-list extended {acl_name}',
        f'{permission} {protocol} any any'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure permit/deny protocol any any on acl {acl_name}. Error:\n{e}")    

def unconfigure_protocol_acl_any_any(device, acl_name, permission, protocol):
    """ unconfigure permit/deny protocol any any on acl
        Args:
            device ('obj'): Device object
            acl_name ('str'): access_list name
            permission ('str'): permit | deny
            protocol ('str'): protocol Name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfigure permit/deny protocol any any on acl {acl_name}")

    config = [
        f'ip access-list extended {acl_name}',
        f'no {permission} {protocol} any any'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure permit/deny protocol any any on acl {acl_name}. Error:\n{e}")   
  
