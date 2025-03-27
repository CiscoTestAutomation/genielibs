"""Common configure functions for PBR"""

import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_route_map_under_interface(device, interface, route_map, ipv6=False):
    """ Configure route-map on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            route_map (`str`): Route-map to be configured on interface
            ipv6 ('bool'): Indicate if this is ipv6 route map. Default false
        Returns:
            None

        Raises:
            SubCommandFailure

    """
    if not ipv6:
        configs = [
            "interface {intf}".format(intf=interface),
            "ip policy route-map {policy}".format(policy=route_map),
        ]  
    else:
        configs = [
            "interface {intf}".format(intf=interface),
            "ipv6 policy route-map {policy}".format(policy=route_map),
        ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure route-map under interface {interface} on device {dev}. Error:\n{error}"
            .format(
                interface=interface,
                dev=device.name,
                error=e,
            ))


def unconfigure_route_map_under_interface(device, interface, route_map, ipv6=False):
    """ unonfigure route-map on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to get address
            route_map (`str`): Route-map to be configured on interface
            ipv6 ('bool'): Indicate if this is ipv6 route map. Default false

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    if not ipv6:
        configs = [
            "interface {intf}".format(intf=interface),
            "no ip policy route-map  {policy}".format(policy=route_map),
        ]
    else:
        configs = [
            "interface {intf}".format(intf=interface),
            "no ipv6 policy route-map  {policy}".format(policy=route_map),
        ]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure route-map under interface {interface} on device {dev}. Error:\n{error}"
            .format(
                interface=interface,
                dev=device.name,
                error=e,
            ))

def configure_pbr_route_map(device,
                            route_map_name,
                            acl_name,
                            next_hop_ip,
                            default_next_hop=None,
                            vrf=None,
                            set_int=None,
                            set_vrf=None,
                            seq_num='10',
                            rule_type='permit',
                            is_ipv6=False):
    """ Configure route-map

        Args:
            device ('obj'): Device object
            route_map_name ('str'): Name of Route-map to be configured.
            acl_name ('str'): Name of ACL to be used with 'match' for the route_map
            next_hop_ip ('str'): Next-hop ip address to be used in 'set' actions.
            default_next_hop ('str', optional): Enable to use 'default next-hop' action.
                                                'next_hop_ip' Ip address will be used. Default is None.
            vrf ('str',optional): Vrf name to be used with 'set vrf' or other vrf related actions.
            set_int ('str',optional): Interface name to be used with 'set interface' action.
            set_vrf ('str',optional): Enable to use 'set vrf' action. Default is None.
            seq_num ('str',optional): Sequence number for the rule. Default is '10'.
            rule_type ('str', optional): (permit | deny) Permission to be applied for the specific sequence.
                                         Default is 'permit'.
            is_ipv6 ('bool',optional): (True | False) 'True' for ipv6 pbr configuration. Default is False.
        Returns:
            None

        Raises:
            SubCommandFailure

    """
    ip_type = 'ipv6' if is_ipv6 else 'ip'
    vrf_cfg = f'vrf {vrf} ' if vrf else ''
    default_cfg = 'default ' if default_next_hop else ''
    
    configs = [f"route-map {route_map_name} {rule_type} {seq_num}",
               f"match {ip_type} address {acl_name}",]
    if set_int:
        configs.append(f"set interface {set_int}")
    if vrf and set_vrf:
            configs.append(f"set vrf {vrf}")
    else:
        configs.append(f"set {ip_type} {default_cfg}{vrf_cfg}next-hop {next_hop_ip}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure route map {route_map_name} on device {device.name}. Error:\n{e}")

def configure_pbr_route_map_nhop_recursive(device,
                                           route_map_name,
                                           next_hop_ip,
                                           acl_name=None,
                                           vrf=None,
                                           seq_num='10',
                                           rule_type='permit',
                                           is_ipv6=False,
                                           force=False):

    """ Configure route-map with next-hop verify-availability
        Args:
            device ('obj'): Device object
            route_map_name ('str'): Name of Route-map to be configured.
            next_hop_ip ('str'): Next-hop ip address to be used in 'set' actions.
            acl_name ('str'): Name of ACL to be used with 'match' for the route_map
            vrf ('str',optional): Vrf name to be used with 'set vrf' or other vrf related actions.
            seq_num ('str',optional): Sequence number for the rule. Default is '10'.
            rule_type ('str', optional): (permit | deny) Permission to be applied for the specific sequence.
                                         Default is 'permit'.
            is_ipv6 ('bool',optional): (True | False) 'True' for ipv6 pbr configuration. Default is False.
            force ('bool',optional): (True | False) 'True' to force the configuration. Default is False.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    ip_type = 'ipv6' if is_ipv6 else 'ip'
    vrf_cfg = f'vrf {vrf} ' if vrf else ''
    force_cfg = ' force' if force else ''

    configs = [f"route-map {route_map_name} {rule_type} {seq_num}",
               f"match {ip_type} address {acl_name}",
               f"set {ip_type} next-hop recursive {vrf_cfg}{next_hop_ip}{force_cfg}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure route map {route_map_name} on device {device.name}. Error:\n{e}")
    
def configure_pbr_route_map_nhop_verify_availability(device,
                                                    route_map_name,
                                                    track,
                                                    next_hop_ip,
                                                    set_seq_num='10',
                                                    acl_name=None,
                                                    default_next_hop=None,
                                                    vrf=None,
                                                    seq_num='10',
                                                    rule_type='permit',
                                                    is_ipv6=False):

    """ Configure route-map with next-hop verify-availability
        Args:
            device ('obj'): Device object
            route_map_name ('str'): Name of Route-map to be configured.
            track ('int'): Track number for the set action.
            next_hop_ip ('str'): Next-hop ip address to be used in 'set' actions.
            set_seq_num ('int',optional): Sequence number for the set action. Default is 10.
            acl_name ('str'): Name of ACL to be used with 'match' for the route_map
            default_next_hop ('str', optional): Enable to use 'default next-hop' action.
                                                'next_hop_ip' Ip address will be used. Default is None.
            vrf ('str',optional): Vrf name to be used with 'set vrf' or other vrf related actions.
            seq_num ('str',optional): Sequence number for the rule. Default is '10'.
            rule_type ('str', optional): (permit | deny) Permission to be applied for the specific sequence.
                                         Default is 'permit'.
            is_ipv6 ('bool',optional): (True | False) 'True' for ipv6 pbr configuration. Default is False.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    ip_type = 'ipv6 ' if is_ipv6 else 'ip '
    vrf_cfg = f'vrf {vrf} ' if vrf else ''
    default_cfg = 'default ' if default_next_hop else ''

    configs = [f"route-map {route_map_name} {rule_type} {seq_num}",
               f"match {ip_type} address {acl_name}",]

    configs.append(f"set {ip_type}{default_cfg}{vrf_cfg}next-hop verify-availability {next_hop_ip} {set_seq_num} track {track}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure route map {route_map_name} on device {device.name}. Error:\n{e}")

def modify_pbr_route_map(device,
                         route_map_name,
                         acl_name=None,
                         next_hop_ip=None,
                         default_next_hop=None,
                         vrf=None,
                         set_int=None,
                         set_vrf=None,
                         seq_num='10',
                         rule_type='permit',
                         is_ipv6=False,
                         remove_acl=False,
                         remove_action=False):
    """ Modify route-map

        Args:
            device ('obj'): Device object
            route_map_name ('str'): Route map to be modified.
            acl_name ('str',optional): Name of ACL that is to be removed from route map.
            next_hop_ip ('str',optional): Next-hop ip address that is to be removed from route map.
                                          (used for default next hop ip address also.) 
            default_next_hop ('str', optional): Enable to remove Default Next-hop action. Default is None.
            vrf ('str',optional): Vrf name used in route map.
            set_int ('str',optional): Interface name to be removed from 'set interface' action.
            set_vrf ('str',optional): Enable to remove 'set vrf' action. Uses 'vrf' argument for vrf name
                                      Default value None.
            seq_num ('str',optional): Sequence number of the rule to be modified. Default is '10'
            rule_type ('str', optional): (permit | deny) Permission to be applied for the specific sequence.
                                         Default is 'permit'.
            is_ipv6 ('bool',optional): (True | False) set 'True' to modify ipv6 route-map. Default is 'False'.
            remove_acl ('bool',optional): (True | False) set 'True' to remove ACL mapping. 
                                          acl_name should be provided. 
            remove_action ('bool',optional): (True | False) set 'True' to remove 'set action' based on the arguments populated.

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    ip_type = 'ipv6' if is_ipv6 else 'ip'
    vrf_cfg = f'vrf {vrf} ' if vrf else ''
    default_cfg = 'default ' if default_next_hop else ''

    configs = [f"route-map {route_map_name} {rule_type} {seq_num}"]
    if remove_acl is True:
        configs.append(f"no match {ip_type} address {acl_name}")
    if remove_action is True:
        if set_int:
            configs.append(f"no set interface {set_int}")
        if vrf and set_vrf:
            configs.append(f"no set vrf {vrf}")
        else:
            configs.append(f"no set {ip_type} {default_cfg}{vrf_cfg}next-hop {next_hop_ip}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to modify route-map {route_map_name} on device {device.name}. Error:\n{e}")

def configure_pbr_route_map_add_set(device,
                            route_map_name,
                            next_hop_ip,
                            seq_num,
                            track="",
                            set_seq_num="",
                            rule_type='permit',
                            verify_availability=False,
                            recursive=False,
                            default_next_hop=None,
                            vrf=None,
                            is_ipv6=False,
                            force=False):
    
    """ Add a set action to an existing route-map
    
            Args:
                device ('obj'): Device object
                route_map_name ('str'): Name of Route-map to be configured.
                next_hop_ip ('str'): Next-hop ip address to be used in 'set' actions.
                seq_num ('str'): Sequence number for the rule.
                track ('str'): Track object to be used in 'set' actions.
                set_seq_num ('str'): Sequence number for the 'set' action.
                rule_type ('str', optional): (permit | deny) Permission to be applied for the specific sequence.
                                            Default is 'permit'.
                verify_availability ('bool', optional): Enable to use 'verify-availability' action. Default is False.
                recursive ('bool', optional): Enable to use 'recursive' action. Default is False.
                default_next_hop ('str', optional): Enable to use 'default next-hop' action.
                                                    'next_hop_ip' Ip address will be used. Default is None.
                vrf ('str',optional): Vrf name to be used with 'set vrf' or other vrf related actions.
                is_ipv6 ('bool',optional): (True | False) 'True' for ipv6 pbr configuration. Default is False.
                force ('bool', optional): Force the configuration. Default to False.

            Returns:
                None

            Raises:
                SubCommandFailure
                ValueError: If both 'verify-availability' and 'recursive' are enabled at the same time

        """
    ip_type = 'ipv6' if is_ipv6 else 'ip'
    vrf_cfg = f'vrf {vrf} ' if vrf else ''
    default_cfg = 'default ' if default_next_hop else ''
    force_cfg = ' force' if force else ''

    configs = [f"route-map {route_map_name} {rule_type} {seq_num}"]

    if verify_availability and recursive:
        raise ValueError("Both 'verify-availability' and 'recursive' cannot be enabled at the same time")
    
    if verify_availability:
        configs.append(f"set {ip_type} {default_cfg}{vrf_cfg}next-hop verify-availability {next_hop_ip} {set_seq_num} track {track}")
    elif recursive:
        configs.append(f"set {ip_type} next-hop recursive {vrf_cfg}{next_hop_ip}{force_cfg}")
    else:
        configs.append(f"set {ip_type} {default_cfg}{vrf_cfg}next-hop {next_hop_ip}")
        
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to add set actionat route-map {route_map_name} on device {device.name}. Error:\n{e}")
    
def unconfigure_pbr_route_map(device, route_map_name):
    """ Unconfigure route-map

        Args:
            device (`obj`): Device object
            route_map_name (`str`): Route-map to be configured on interface

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    configs = ["no route-map {pbr}".format(pbr=route_map_name)]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure route map {pbr} on device {dev}. Error:\n{error}"
            .format(
                pbr=route_map_name,
                dev=device.name,
                error=e,
            ))
