"""Common get info functions for mpls"""

# Python
import re
import logging

# pyats
from pyats.utils.objects import find, R

# Genie
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.libs.parser.utils.common import Common
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Utils
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config_section_dict,
)

log = logging.getLogger(__name__)


def get_mpls_outgoing_label(device, label):
    """ Get mpls outgoing label 
        using 'show mpls forwarding-table labels {label}'

        Args:
            device ('obj'): Device object
            label ('str'): Local label
        Returns:
            out_label ('str'): Outgoing label
    """
    cmd = 'show mpls forwarding-table labels {label}'.format(label=label)
    try:
        out = device.parse(cmd)
    except Exception as e:
        log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
        return None

    reqs = R(['vrf','(.*)','local_label','(?P<local_label>.*)',
              'outgoing_label_or_vc','(?P<outgoing_label>.*)','(.*)'])
    found = find([out], reqs, filter_=False, all_keys=True)

    if found:
        return found[0][1][-1]
    else:
        return None


def get_mpls_label_stack(device, label=None, prefix=None):
    """ Get mpls Label Stack
        using 'show mpls forwarding-table labels {label} detail'

        Args:
            device ('obj'): Device object
            label ('str'): Local label
            prefix ('str'): Prefix value
        Returns:
            stack ('list'): Label stack
    """
    stack = []
    if label:
        cmd = 'show mpls forwarding-table labels {label} detail'.format(label=label)
    elif prefix:
        cmd = 'show mpls forwarding-table {prefix} detail'.format(prefix=prefix)
    else:
        cmd = 'show mpls forwarding-table detail'
    try:
        out = device.parse(cmd)
    except Exception as e:
        log.error("Failed to parse '{cmd}': {e}".format(cmd=cmd, e=e))
        return stack

    reqs = R(['vrf','(.*)','local_label','(?P<local_label>.*)',
              'outgoing_label_or_vc','(?P<outgoing_label>.*)',
              'prefix_or_tunnel_id','(.*)','outgoing_interface','(.*)',
              'label_stack','(?P<label_stack>.*)'])
    found = find([out], reqs, filter_=False, all_keys=True)

    if found:
        stack = found[0][0].split()

    return [int(label) for label in stack]


def get_interface_interfaces_ldp_enabled(device, vrf=""):
    """ Get interfaces which have ldp configured from 'show mpls interfaces details'

        Args:
            device ('str'): Device str
            vrf ('str'): Vrf name
        Returns:
            interface list
        Raises:
            None
    """
    try:
        out = device.parse("show mpls interfaces detail")
    except SchemaEmptyParserError:
        return []

    vrf = vrf if vrf else "default"

    try:
        keys = out["vrf"][vrf]["interfaces"].keys()
    except KeyError:
        return []

    return [Common.convert_intf_name(intf) for intf in keys]


def get_mpls_interface_ldp_configured(device):
    """ Get interfaces which have ldp configured from 'show run'

        Args:
            device ('obj'): Device object
        Returns:
            interface address
    """
    interfaces = []
    intf_dict = get_running_config_section_dict(
        device, "interface"
    )

    p = re.compile(r"^interface +(?P<name>[\S\s]+)$")
    for intf, data_dict in intf_dict.items():
        if "mpls label protocol ldp" in data_dict:
            m = p.match(intf)
            interfaces.append(m.groupdict()["name"])
    return interfaces


def get_mpls_ldp_session_count(device):
    """ Get mpls ldp seesion count

        Args:
            device(`str`): Device str
        Returns:
            int: session count
        Raises:
            None
    """
    log.info("Getting LDP neighbor count")
    ldp_session_count = 0

    try:
        output_ldp = device.parse("show mpls ldp neighbor")
    except SchemaEmptyParserError as e:
        return ldp_session_count

    for vrf in output_ldp["vrf"]:
        ldp_session_count += len(output_ldp["vrf"][vrf]["peers"].keys())

    log.info("LDP neighbor count is {}".format(ldp_session_count))

    return ldp_session_count


def get_mpls_ldp_peer_state(device, interface):
    """ Gets the ldp peer state under specified interface

        Args:
            device ('obj'): device to run on
            interface ('str'): interface to search under
        Returns:
            ldp peer state ('str')
        Raises:
            None
    """
    try:
        out = device.parse("show mpls ldp neighbor")
    except SchemaEmptyParserError:
        return None

    if out and "vrf" in out:
        for vrf in out["vrf"]:
            for peer in out["vrf"][vrf].get("peers", {}):
                for index in out["vrf"][vrf]["peers"][peer].get(
                    "label_space_id", {}
                ):

                    state = out["vrf"][vrf]["peers"][peer]["label_space_id"][
                        index
                    ].get("state", None)

                    if "ldp_discovery_sources" in out["vrf"][vrf]["peers"][
                        peer
                    ]["label_space_id"][index] and interface in out["vrf"][
                        vrf
                    ][
                        "peers"
                    ][
                        peer
                    ][
                        "label_space_id"
                    ][
                        index
                    ][
                        "ldp_discovery_sources"
                    ].get(
                        "interface", None
                    ):
                        return state


def get_mpls_forwarding_table(device):
    """ Gets all fields from the mpls forwarding table

        Args:
            device (`obj`): Device object

        Returns:
            The whole table ('dict')

        Raises:
            N/A
    """

    try:
        out = device.parse('show mpls forwarding-table')
    except SchemaEmptyParserError:
        log.info("Device output is empty.")
        return {}

    return out


def get_mpls_forwarding_table_key_value_pairs(device, ip):
    """ Gets all key:value pairs from the mpls forwarding table

        Args:
            device (`obj`): Device object
            ip (`str`): IP address

        Returns:
            result (`bool`): Verified result

        Raises:
            N/A
    """

    try:
        out = device.parse('show mpls forwarding-table {}'.format(ip))
    except SchemaEmptyParserError:
        log.info("Device output is empty.")
        return {}

    reqs = R(['vrf', '(.*)',
            'local_label', '(?P<local_label>.*)',
            'outgoing_label_or_vc', '(?P<outgoing_label>.*)',
            'prefix_or_tunnel_id', '(?P<prefix>.*)',
            'outgoing_interface', '(?P<interface>.*)',
            'next_hop', '(?P<next_hop>.*)'])
    found = find([out], reqs, filter_=False, all_keys=True)

    if found:
        return GroupKeys.group_keys(
            reqs=reqs.args, ret_num={}, source=found, all_keys=True)

    return {}

