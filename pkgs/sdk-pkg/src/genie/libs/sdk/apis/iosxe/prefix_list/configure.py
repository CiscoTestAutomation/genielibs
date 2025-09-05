"""Common configure functions for prefix-list"""

# Python
import logging

# Common
from genie.libs.sdk.apis.iosxe.bgp.get import get_bgp_summary
from genie.libs.sdk.apis.iosxe.interface.get import get_interface_netmask

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_prefix_list_prefix_list(device, prefix_list):
    """ Configures prefix-list on device

        Args:
            device('obj'): device to configure on
            prefix_list('list'): prefix list which contains dictionary
                dictionary contains following 3 keys:
                    prefix_list ('str'): prefix list value
                    seq ('int'): sequence number
                    route ('str'): IP address
                ex.)
                   [ {
                        'prefix_list': 1,
                        'seq': 5,
                        'route': '172.16.0.0/24'
                    },
                    {
                        'prefix_list': 2,
                        'seq': 5,
                        'route': '172.16.1.0/24'
                    },
                    {
                        'direction': 'in',
                        'permit': 'deny',
                        'route': '10.94.12.1',
                        'comparison_operator': '<',
                        'comparison_value': 36
                    } 
                    ]

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if not isinstance(prefix_list, list):
        raise SubCommandFailure("prefix_list must be a list")

    config = []

    for pf in prefix_list:
        if "prefix_list" in pf:
            config.append(
                "\nip prefix-list {prefix_list}".format(
                    prefix_list=pf["prefix_list"]
                )
            )

            if "seq" in pf:
                config.append(" seq {seq}".format(seq=pf["seq"]))

        if "direction" in pf:
            config.append(
                "\nip prefix-list {direction}".format(
                    direction=pf["direction"]
                )
            )

        if not "/" in pf["route"]:
            pf["route"] += get_interface_netmask(pf["route"])

        config.append(
            " {permit} {route}".format(permit=pf["permit"], route=pf["route"])
        )

        if "comparison_operator" in pf and "comparison_value" in pf:
            config.append(
                " {comparison_operator} {comparison_value}".format(
                    comparison_operator=pf["comparison_operator"],
                    comparison_value=pf["comparison_value"],
                )
            )

    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring prefix-list "
            "on device {device}, "
            "Error: {e}".format(device=device.name, e=str(e))
        ) from e

def configure_ip_prefix_list_deny_permit(device, prefix_list_name, option, 
                                        ip_address, subnet_id, 
                                        match_option=None, match_length=1):
    """ configure ip prefix-list on device
        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix list name to be used
            option (`str`): option for prefix list
                ex:)
                    deny         Specify packets to reject
                    permit       Specify packets to forward
            ip_address (`str`): ip address to be used
            subnet_id (`int`): subnet_id to be used, default value is 32n
            match_option (`str`,optional): prefix matching option
            match_length (`int`,optional): prefix matching length(keeping default length 1)
            ex:)
                <1-32>  Minimum prefix length
        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if match_option:
        cmd.append(f'ip prefix-list {prefix_list_name} {option} {ip_address}/{subnet_id} {match_option} {match_length}')
    else:
        cmd.append(f'ip prefix-list {prefix_list_name} {option} {ip_address}/{subnet_id}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure ip prefix-list on device. Error:\n{e}")

def configure_ip_prefix_list_description(device, prefix_list_name, desc_line):
    """ configure ip prefix-list on device
        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix list name to be used
            desc_line (`str`): description line for option description

        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip prefix-list {prefix_list_name} description {desc_line}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure ip prefix-list on device. Error:\n{e}")

def configure_ip_prefix_list_seq(device, prefix_list_name, ip_address, 
                                 subnet_id, seq_num, seq_rule,
                                 match_option=None, match_length=1):
    """ configure ip prefix-list on device
        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix list name to be used
            ip_address (`str`): ip address to be used
            subnet_id (`int`): subnet_id to be used, default value is 32
            seq_num (`int`): sequence number
            seq_rule (`str`): rule permit/deny when option is seq
            match_option (`str`,optional): prefix matching option
            match_length (`int`,optional): prefix matching length(keeping default length 1)
            ex:)
                <1-32>  Minimum prefix length

        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if match_option:
        cmd.append(f'ip prefix-list {prefix_list_name} seq {seq_num} {seq_rule} {ip_address}/{subnet_id} {match_option} {match_length}')
    else:
        cmd.append(f'ip prefix-list {prefix_list_name} seq {seq_num} {seq_rule} {ip_address}/{subnet_id}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure ip prefix-list on device. Error:\n{e}")

def unconfigure_ip_prefix_list_deny_permit(device, prefix_list_name, option, 
                                           ip_address, subnet_id, 
                                           match_option=None, match_length=1):
    """ unconfigure ip prefix-list on device
        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix list name to be used
            option (`str`): option for prefix list
                ex:)
                    deny         Specify packets to reject
                    permit       Specify packets to forward
            ip_address (`str`): ip address to be used
            subnet_id (`int`): subnet_id to be used, default value is 32n
            match_option (`str`,optional): prefix matching option
            match_length (`int`,optional): prefix matching length(keeping default length 1)
            ex:)
                <1-32>  Minimum prefix length
        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if match_option:
        cmd.append(f'no ip prefix-list {prefix_list_name} {option} {ip_address}/{subnet_id} {match_option} {match_length}')
    else:
        cmd.append(f'no ip prefix-list {prefix_list_name} {option} {ip_address}/{subnet_id}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure ip prefix-list on device. Error:\n{e}")

def unconfigure_ip_prefix_list_description(device, prefix_list_name, desc_line):
    """ Unconfigure ip prefix-list on device
        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix list name to be used
            desc_line (`str`): description line for option description

        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'no ip prefix-list {prefix_list_name} description {desc_line}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure ip prefix-list on device. Error:\n{e}")

def unconfigure_ip_prefix_list_seq(device, prefix_list_name, ip_address, 
                                   subnet_id, seq_num, seq_rule,
                                   match_option=None, match_length=1):
    """ configure ip prefix-list on device
        Args:
            device (`obj`): device to execute on
            prefix_list_name (`int`): prefix list name to be used
            ip_address (`str`): ip address to be used
            subnet_id (`int`): subnet_id to be used, default value is 32
            seq_num (`int`): sequence number
            seq_rule (`str`): rule permit/deny when option is seq
            match_option (`str`,optional): prefix matching option
            match_length (`int`,optional): prefix matching length(keeping default length 1)
            ex:)
                <1-32>  Minimum prefix length
        Return:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if match_option:
        cmd.append(f'no ip prefix-list {prefix_list_name} seq {seq_num} {seq_rule} {ip_address}/{subnet_id} {match_option} {match_length}')
    else:
        cmd.append(f'no ip prefix-list {prefix_list_name} seq {seq_num} {seq_rule} {ip_address}/{subnet_id}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure ip prefix-list on device. Error:\n{e}")
        
def configure_ipv6_prefix_list_with_permit_deny(device, prefix_list_name, option, 
                                       ipv6_address, prefix_length, seq_num = None,
                                       match_option=None, match_length=None):
    """ configure ipv6 prefix-list with sequence number on device
        Args:
            device (`obj`): device to execute on
            prefix_list_name (`str`): prefix list name to be used
            seq_num (`int`, optional): sequence number for the prefix list entry
            option (`str`): option for prefix list
                ex:)
                    deny         Specify packets to reject
                    permit       Specify packets to forward
            ipv6_address (`str`): IPv6 address to be used
            prefix_length (`int`): prefix length to be used (0-128 for IPv6)
            match_option (`str`, optional): prefix matching option
                ex:)
                    le           Less than or equal to
                    ge           Greater than or equal to
            match_length (`int`, optional): prefix matching length
                ex:)
                    <0-128>      Prefix length for IPv6
        Return:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = []
    if match_option and match_length and seq_num is not None:
        cmd.append(f'ipv6 prefix-list {prefix_list_name} seq {seq_num} {option} {ipv6_address}/{prefix_length} {match_option} {match_length}')
    elif seq_num is not None:
        cmd.append(f'ipv6 prefix-list {prefix_list_name} seq {seq_num} {option} {ipv6_address}/{prefix_length}')
    else:
        cmd.append(f'ipv6 prefix-list {prefix_list_name} {option} {ipv6_address}/{prefix_length}')
    
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure ipv6 prefix-list on device. Error:\n{e}")
        

def unconfigure_ipv6_prefix_list_with_permit_deny(device, prefix_list_name, option, 
                                       ipv6_address, prefix_length, seq_num = None,
                                       match_option=None, match_length=None):
    """ configure ipv6 prefix-list with sequence number on device
        Args:
            device (`obj`): device to execute on
            prefix_list_name (`str`): prefix list name to be used
            seq_num (`int`, optional): sequence number for the prefix list entry
            option (`str`): option for prefix list
                ex:)
                    deny         Specify packets to reject
                    permit       Specify packets to forward
            ipv6_address (`str`): IPv6 address to be used
            prefix_length (`int`): prefix length to be used (0-128 for IPv6)
            match_option (`str`, optional): prefix matching option
                ex:)
                    le           Less than or equal to
                    ge           Greater than or equal to
            match_length (`int`, optional): prefix matching length
                ex:)
                    <0-128>      Prefix length for IPv6
        Return:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = []
    if match_option and match_length and seq_num is not None:
        cmd.append(f'no ipv6 prefix-list {prefix_list_name} seq {seq_num} {option} {ipv6_address}/{prefix_length} {match_option} {match_length}')
    elif seq_num is not None:
        cmd.append(f'no ipv6 prefix-list {prefix_list_name} seq {seq_num} {option} {ipv6_address}/{prefix_length}')
    else:
        cmd.append(f'no ipv6 prefix-list {prefix_list_name} {option} {ipv6_address}/{prefix_length}')
    
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure ipv6 prefix-list on device. Error:\n{e}")