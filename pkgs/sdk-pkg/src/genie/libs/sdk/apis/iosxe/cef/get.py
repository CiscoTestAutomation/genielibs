# Python
import logging
import re

# Genie
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
            "Could not find any next hop informatin for prefix {prefix}".format(
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
        "Could not find any next hop informatin for prefix {prefix}".format(
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
    """ Get registred label to prefix in CEF
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
            output ('dict'): Optional. Parsed output from command 'show ip cef {prefix} detail'
            vrf ('str'): Optional. VRF name. Default: 'default'
            address_family ('str'): Optional. Family name. Default: 'ipv4'
            interface ('str'): Optional. Interface name
            nexthop_address ('str'): Optional. Nexthop address
        Returns:
            int: Registred label
        Raises:
            ValueError: Found more than on registred label
    """

    log.info("Getting registred label to prefix {prefix} in CEF".format(prefix=prefix))

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
                "Could not find ant registred label for prefix {prefix}".format(
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
            "Could not find ant registred label for prefix {prefix}".format(
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
