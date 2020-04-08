# Python
import logging
import re
from ipaddress import ip_address, ip_network


# pyATS
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout

from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_cef_repair_path_of_route(device, prefix, vrf="default", address_family="ipv4"):
    """ Get 'repair path' of route
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            vrf ('str'): VRF name
            address_family ('str'): Address family
        Return:
            tuple: (
                String: Repair path IP address,
                String: Repair path Interface
            )
        Raises:
            None
    """
    try:
        output = device.parse("show ip cef {prefix} detail".format(prefix=prefix))
    except SchemaEmptyParserError:
        log.info("Could not find cef repair path information")
        return None, None

    r1 = re.compile(
        r"attached\-nexthop\s+(?P<repair_next_hop_ip>\S+)\s+(?P<repair_next_hop_interface>\S+)"
    )

    prefixes_dict = (
        output["vrf"]
        .get(vrf, {})
        .get("address_family", {})
        .get(address_family, {})
        .get("prefix", {})
    )
    for prefix_address in prefixes_dict:
        if prefix in prefix_address:
            for hop in prefixes_dict[prefix_address].get("nexthop", {}):
                for out_interface in (
                    prefixes_dict[prefix_address]["nexthop"]
                    .get(hop, {})
                    .get("outgoing_interface", {})
                ):
                    repair_path = (
                        prefixes_dict[prefix_address]["nexthop"]
                        .get(hop, {})["outgoing_interface"][out_interface]
                        .get("repair", None)
                    )

                    if repair_path is None:
                        continue

                    result = r1.match(repair_path)
                    if result:
                        group = result.groupdict()
                        repair_next_hop_ip = group["repair_next_hop_ip"]
                        repair_next_hop_interface = group["repair_next_hop_interface"]

                        log.info(
                            "Found repair path to address {address} and interface {interface}".format(
                                address=repair_next_hop_ip,
                                interface=repair_next_hop_interface,
                            )
                        )
                        return repair_next_hop_ip, repair_next_hop_interface

    log.info("Could not find cef repair path information")
    return None, None


def get_cef_next_hop_ip_address(device, prefix, vrf=None, address_family=None):
    """ Get next hop ip address from Express Forwarding
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            vrf ('str'): VRF name
            address_family ('str'): Address family
        Returns:
            String: Next hop Ip address 
        Raises:
            None
    """

    try:
        output = device.parse("show ip cef {prefix} detail".format(prefix=prefix))
    except SchemaEmptyParserError as e:
        log.info(
            "Could not find any next hop information for prefix {prefix}".format(
                prefix=prefix
            )
        )
        return None

    vrf = vrf if vrf else "default"
    address_family = address_family if address_family else "ipv4"

    prefixes_dict = (
        output["vrf"]
        .get(vrf, {})
        .get("address_family", {})
        .get(address_family, {})
        .get("prefix", {})
    )
    for prefix_address in prefixes_dict:
        if prefix in prefix_address:
            for hop in prefixes_dict[prefix_address].get("nexthop", {}):
                log.info("Found next hop address {address}".format(address=hop))
                return hop

    log.info(
        "Could not find any next hop information for prefix {prefix}".format(
            prefix=prefix
        )
    )
    return None


def get_cef_internal_repair_next_hop_ip_address(device, prefix, vrf=None, address_family=None):
    """ Get internal next hop ip address from Express Forwarding
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            vrf ('str'): VRF name
            address_family ('str'): Address family
        Returns:
            String: Next hop Ip address
        Raises:
            None
    """

    try:
        if vrf:
            output = device.parse(
                "show ip cef vrf {vrf} {prefix} internal".format(vrf=vrf, prefix=prefix))
        else:
            output = device.parse("show ip cef {prefix} internal".format(prefix=prefix))
    except SchemaEmptyParserError as e:
        log.info(
            "Could not find any repair next hop information for prefix {prefix}".format(
                prefix=prefix
            )
        )
        return None

    vrf = vrf if vrf else "default"
    address_family = address_family if address_family else "ipv4"

    prefixes_dict = (
        output["vrf"]
        .get(vrf, {})
        .get("address_family", {})
        .get(address_family, {})
        .get("prefix", {})
    )
    for prefix_address in prefixes_dict:
        if ip_address(prefix) in ip_network(prefix_address):

            output_chain_dict = prefixes_dict[prefix_address].get('output_chain',{})
            # {'frr': {
            #         'primary': {
            #             'info': '0x80007F2B146ED518',
            #             'primary': {
            #                 'tag_adj': {
            #                     'GigabitEthernet0/1/6': {
            #                         'addr': '10.19.198.25',
            #                         'addr_info': '7F2B21B245A8',
            #                     },},},
            #             'repair': {
            #                 'tag_adj': {
            #                     'GigabitEthernet0/1/7': {
            #                         'addr': '10.19.198.29',
            #                         'addr_info': '7F2B21B24148',
            #                     },},},},},
            #     'label': ['[63300|68544](elc)-(local:25)'],}
            tag_adj_dict = output_chain_dict.get('frr', {}).get('primary', {}).get(
                'repair', {}).get('tag_adj', {})

            if not tag_adj_dict:
                # {'label': ['262', 'implicit-null'],
                #     'tag_midchain': {
                #         'Tunnel65537': {
                #             'frr': {
                #                 'primary': {
                #                     'info': '0x80007F4F894B79F0',
                #                     'primary': {
                #                         'tag_adj': {
                #                             'GigabitEthernet0/1/6': {
                #                                 'addr': '10.169.196.213',
                #                                 'addr_info': '7F4F881C1898',
                #                             },},},
                #                     'repair': {
                #                         'label': ['16061'],
                #                         'tag_adj': {
                #                             'GigabitEthernet0/1/7': {
                #                                 'addr': '10.169.196.217',
                #                                 'addr_info': '7F4F881C1CF8',
                #                             },},},},},
                #             'label': ['[16073|16073]', '[90|90]', '[95|95]', '[90|90]'],
                #             'tag_midchain_info': '7F4F881C0718',
                #         },},}
                for intf in output_chain_dict.get('tag_midchain', {}):
                    tag_adj_dict = output_chain_dict['tag_midchain'][intf].get('frr', {}).get(
                        'primary', {}).get('repair', {}).get('tag_adj', {})

            if not tag_adj_dict:
                # {'label': ['[11111|1622222073]-(local:26)'], 'frr': {
                #     'primary': {'info': '0xaaaaaaaaa', 'primary': {'tag_adj': {
                #         'GigabitEthernet0/1/6': {'addr': '10.69.111.111',
                #                                  'addr_info': 'AAAAAAAAAA'}}},
                #                                  'repair': {
                #         'tag_midchain': {
                #             'MPLS-SR-Tunnel1': {'tag_midchain_info': 'AAAAAAAAAA',
                #                                 'label': ['98'], 'tag_adj': {
                #                     'GigabitEthernet0/1/7': {'addr': '111.1111.111.111',
                #                                              'addr_info':
                #                                              'AAAAAAAAAA'}}}}}}}}
                for intf in output_chain_dict.get('frr', {}).get('primary', {}).get(
                        'repair', {}).get('tag_midchain', {}):
                    tag_adj_dict = output_chain_dict.get('frr', {}).get('primary', {}).get(
                        'repair', {}).get('tag_midchain', {})[intf].get('tag_adj', {})

            for intf in tag_adj_dict:
                address = tag_adj_dict[intf].get('addr')
                if address:
                    log.info(
                        "Found repair next hop address {address}".format(address=address))
                    return address

    log.info(
        "Could not find any repair next hop information for prefix {prefix}".format(
            prefix=prefix
        )
    )
    return None


def get_cef_internal_primary_next_hop_ip_address(device, prefix, vrf=None, address_family=None):
    """ Get internal next hop ip address from Express Forwarding
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            vrf ('str'): VRF name
            address_family ('str'): Address family
        Returns:
            String: Next hop Ip address
        Raises:
            None
    """

    try:
        if vrf:
            output = device.parse("show ip cef vrf {vrf} {prefix} internal".format(vrf=vrf, prefix=prefix))
        else:
            output = device.parse("show ip cef {prefix} internal".format(prefix=prefix))
    except SchemaEmptyParserError as e:
        log.info(
            "Could not find any primary next hop information for prefix {prefix}".format(
                prefix=prefix
            )
        )
        return None

    vrf = vrf if vrf else "default"
    address_family = address_family if address_family else "ipv4"

    prefixes_dict = (
        output["vrf"]
        .get(vrf, {})
        .get("address_family", {})
        .get(address_family, {})
        .get("prefix", {})
    )
    for prefix_address in prefixes_dict:
        if ip_address(prefix) in ip_network(prefix_address):

            output_chain_dict = prefixes_dict[prefix_address].get('output_chain',{})
            # {'frr': {
            #         'primary': {
            #             'info': '0x80007F2B146ED518',
            #             'primary': {
            #                 'tag_adj': {
            #                     'GigabitEthernet0/1/6': {
            #                         'addr': '10.19.198.25',
            #                         'addr_info': '7F2B21B245A8',
            #                     },},},
            #             'repair': {
            #                 'tag_adj': {
            #                     'GigabitEthernet0/1/7': {
            #                         'addr': '10.19.198.29',
            #                         'addr_info': '7F2B21B24148',
            #                     },},},},},
            #     'label': ['[63300|68544](elc)-(local:25)'],}
            tag_adj_dict = output_chain_dict.get('frr', {}).get('primary', {}).get(
                'primary', {}).get('tag_adj', {})

            if not tag_adj_dict:
                # {'label': ['262', 'implicit-null'],
                #     'tag_midchain': {
                #         'Tunnel65537': {
                #             'frr': {
                #                 'primary': {
                #                     'info': '0x80007F4F894B79F0',
                #                     'primary': {
                #                         'tag_adj': {
                #                             'GigabitEthernet0/1/6': {
                #                                 'addr': '10.169.196.213',
                #                                 'addr_info': '7F4F881C1898',
                #                             },},},
                #                     'repair': {
                #                         'label': ['16061'],
                #                         'tag_adj': {
                #                             'GigabitEthernet0/1/7': {
                #                                 'addr': '10.169.196.217',
                #                                 'addr_info': '7F4F881C1CF8',
                #                             },},},},},
                #             'label': ['[16073|16073]', '[90|90]', '[95|95]', '[90|90]'],
                #             'tag_midchain_info': '7F4F881C0718',
                #         },},}
                for intf in output_chain_dict.get('tag_midchain', {}):
                    tag_adj_dict = output_chain_dict['tag_midchain'][intf].get('frr', {}).get(
                        'primary', {}).get('primary', {}).get('tag_adj', {})

            if not tag_adj_dict:
                # {'label': ['[11111|1622222073]-(local:26)'], 'frr': {
                #     'primary': {'info': '0xaaaaaaaaa', 'primary': {'tag_adj': {
                #         'GigabitEthernet0/1/6': {'addr': '10.69.111.111',
                #                                  'addr_info': 'AAAAAAAAAA'}}},
                #                                  'repair': {
                #         'tag_midchain': {
                #             'MPLS-SR-Tunnel1': {'tag_midchain_info': 'AAAAAAAAAA',
                #                                 'label': ['98'], 'tag_adj': {
                #                     'GigabitEthernet0/1/7': {'addr': '111.1111.111.111',
                #                                              'addr_info':
                #                                              'AAAAAAAAAA'}}}}}}}}
                for intf in output_chain_dict.get('frr', {}).get('primary', {}).get(
                        'primary', {}).get('tag_midchain', {}):
                    tag_adj_dict = output_chain_dict.get('frr', {}).get('primary', {}).get(
                        'primary', {}).get('tag_midchain', {})[intf].get('tag_adj', {})

            if not tag_adj_dict:
                # 'output_chain': {
                #     'label': ['362', 'implicit-null'],
                #     'tag_midchain': {
                #         'Tunnel65536': {
                #             'label': ['16063', '16051'],
                #             'tag_midchain_info': '7F9C9D301840',
                #         },
                #     },
                #     'tag_adj': {
                #             'GigabitEthernet0/1/7': {
                #                 'addr': '10.19.198.29',
                #                 'addr_info': '7F9C9D304A90',
                #             },
                #         },
                # },
                tag_adj_dict = output_chain_dict.get('tag_adj', {})

            for intf in tag_adj_dict:
                address = tag_adj_dict[intf].get('addr')
                if address:
                    log.info(
                        "Found primary next hop address {address}".format(address=address))
                    return address

    log.info(
        "Could not find any primary next hop information for prefix {prefix}".format(
            prefix=prefix
        )
    )
    return None


def get_cef_registred_label_to_prefix(
    device,
    prefix,
    vrf="default",
    address_family="ipv4",
    interface=None,
    nexthop_address=None,
    output=None,
):
    """ Get registered label to prefix in CEF
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            output ('dict'): Optional. Parsed output from command 'show ip cef {prefix} detail'
            vrf ('str'): Optional. VRF name. Default: 'default'
            address_family ('str'): Optional. Family name. Default: 'ipv4'
            interface ('str'): Optional. Interface name
            nexthop_address ('str'): Optional. Nexthop address
        Returns:
            int: Registered label
        Raises:
            ValueError: Found more than on registered label
    """

    log.info("Getting registered label to prefix {prefix} in CEF".format(prefix=prefix))

    if not output:
        try:
            if vrf and vrf != "default":
                output = device.parse(
                    "show ip cef vrf {vrf} {prefix} detail".format(
                        vrf=vrf, prefix=prefix
                    )
                )
            else:
                output = device.parse(
                    "show ip cef {prefix} detail".format(prefix=prefix)
                )
        except SchemaEmptyParserError:
            log.info(
                "Could not find ant registered label for prefix {prefix}".format(
                    prefix=prefix
                )
            )
            return None

    prefixes_dict = (
        output["vrf"]
        .get(vrf, {})
        .get("address_family", {})
        .get(address_family, {})
        .get("prefix", {})
    )

    label = []

    for pfx in prefixes_dict:
        if prefix in pfx:
            if interface and nexthop_address:
                label = (
                    prefixes_dict[pfx]
                    .get("nexthop", {})
                    .get(nexthop_address, {})
                    .get("outgoing_interface", {})
                    .get(interface, {})
                    .get("outgoing_label", [])
                )
            elif nexthop_address:
                for interface in (
                    prefixes_dict[pfx]
                    .get("nexthop", {})
                    .get(nexthop_address, {})
                    .get("outgoing_interface", {})
                ):
                    label = prefixes_dict[interface].get("outgoing_label", [])

            elif interface:
                for hop in prefixes_dict[pfx].get("nexthop", {}):
                    label = (
                        prefixes_dict[pfx]["nexthop"][hop]
                        .get("outgoing_interface", {})
                        .get(interface, {})
                        .get("outgoing_label", [])
                    )
            else:
                for hop in prefixes_dict[pfx].get("nexthop", {}):
                    for interface in prefixes_dict[pfx]["nexthop"][hop].get(
                        "outgoing_interface", {}
                    ):
                        label = (
                            prefixes_dict[pfx]["nexthop"][hop]
                            .get("outgoing_interface", {})[interface]
                            .get("outgoing_label", [])
                        )

    if not label:
        log.info(
            "Could not find ant registered label for prefix {prefix}".format(
                prefix=prefix
            )
        )
    elif len(label) > 1:
        raise ValueError(
            "Command has returned more than one label. The following "
            "labels have been returned:\n{areas}".format(areas="\n".join(label))
        )
    else:
        label = int(label[0])
        log.info("Found label {label}".format(label=label))

    return label



def get_cef_internal_primary_interface(device, prefix, vrf=None, max_time=60, check_interval=15):
    """ Get cef internal output primary interface

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF to check
            prefix (`str`): Prefix to check
            max_time (`int`): Maximum time to keep checking
            check_interval (`int`): How long to wait between checks

        Raises:
            N/A

        Returns:
            interface name/None
    """
    if vrf:
        cmd = 'show ip cef vrf {vrf} {prefix} internal'.format(vrf=vrf, prefix=prefix)
    else:
        cmd = 'show ip cef vrf {prefix} internal'.format(prefix=prefix)

    vrf = vrf if vrf else "default"

    reqs = R(
        [
            "vrf",
            "(?P<vrf>{vrf})".format(vrf=vrf),
            "address_family",
            "(?P<address_family>.*)",
            "prefix",
            "(?P<prefix>.*)",
            "output_chain",
            "tag_midchain",
            "(?P<tag_midchain>.*)",
            "frr",
            "primary",
            "primary",
            "tag_adj",
            "(?P<interface>.*)",
        ]
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            log.info("Parser output is empty")
            timeout.sleep()
            continue

        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            for interface in found[0][0]:
                return interface

        timeout.sleep()

    log.error("Failed to get primary interface")
    return None


def get_cef_internal_repair_interface(device, prefix, vrf=None, max_time=60, check_interval=15):
    """ Get cef internal output repair interface

        Args:
            device (`obj`): Device object
            vrf (`str`): VRF to check
            prefix (`str`): Prefix to check
            max_time (`int`): Maximum time to keep checking
            check_interval (`int`): How long to wait between checks

        Raises:
            N/A

        Returns:
            interface name/None
    """
    if vrf:
        cmd = 'show ip cef vrf {vrf} {prefix} internal'.format(vrf=vrf, prefix=prefix)
    else:
        cmd = 'show ip cef vrf {prefix} internal'.format(prefix=prefix)

    vrf = vrf if vrf else "default"

    reqs = R(
        [
            "vrf",
            "(?P<vrf>{vrf})".format(vrf=vrf),
            "address_family",
            "(?P<address_family>.*)",
            "prefix",
            "(?P<prefix>.*)",
            "output_chain",
            "tag_midchain",
            "(?P<tag_midchain>.*)",
            "frr",
            "primary",
            "repair",
            "tag_adj",
            "(?P<interface>.*)",
        ]
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            log.info("Parser output is empty")
            timeout.sleep()
            continue

        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            for interface in found[0][0]:
                return interface

        timeout.sleep()

    log.error("Failed to get repair interface")
    return None

