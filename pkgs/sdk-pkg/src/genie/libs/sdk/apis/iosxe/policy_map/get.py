"""Common get info functions for interface"""

# Python
import os
import logging
import re

# Genie
from genie.metaparser.util import merge_dict

# pyATS
from genie.metaparser.util.exceptions import (
    SchemaEmptyParserError,
    SchemaUnsupportedKeyError,
)

# Interface
from genie.libs.sdk.apis.iosxe.interface.get import (
    get_interface_running_config,
)

log = logging.getLogger(__name__)


def get_policy_map_running_policy_map(device, policy_map):
    """ Get running policy-map configuration

        Args:
            device (`obj`): Device object
            policy_map (`str`): Policy map name

        Returns:
            None

        Raises:
            SchemaUnsupportedKeyError
    """

    try:
        out = device.parse("show run policy-map {}".format(policy_map))
    except SchemaUnsupportedKeyError as e:
        # Need to catch if there is unexpected configuration
        log.error(
            "Unexpected configuration found under "
            "{policy_map}: {e}".format(policy_map=policy_map, e=e)
        )
        return None
    except SchemaEmptyParserError:
        return None
    except Exception as e:
        log.error(
            "Failed to parse show run policy-map {}, Error: {}".format(
                policy_map, str(e)
            )
        )
        return None
    return out


def get_policy_map_configurational_policy_map(device, interfaces):
    """ Get policy-map running configuration

        Args:
            device (`obj`): Device object
            interfaces (`list`): List of interfaces

        Returns:
            policy-map configurational dictionary
    """

    out = {}
    policy_out = {}
    for interface in interfaces:
        out[interface] = get_interface_running_config(device, interface)

    service_policies = []

    for item in out[interface]:
        if interface in item:
            for service_policy_item in out[interface][item]:
                if "service-policy" in service_policy_item:
                    service_policies.append(service_policy_item[21:].strip())

    for service_policy in service_policies:
        if "in" in service_policy:
            direction = "input"
        else:
            direction = "output"
        output = get_policy_map_running_policy_map(device, service_policy)
        if not output:
            continue
        policy_out.setdefault(direction, {})
        policy_out[direction] = output
        for class_name in policy_out[direction]["policy_map"][service_policy][
            "class"
        ]:
            for item in policy_out[direction]["policy_map"][service_policy][
                "class"
            ][class_name]:
                if "service_policy" in item:
                    nested = policy_out[direction]["policy_map"][
                        service_policy
                    ]["class"][class_name][item]
                    nested_policy_out = get_policy_map_running_policy_map(
                        device, nested
                    )
                    if not nested_policy_out:
                        continue
                    new_nested_policy_out = {}
                    new_nested_policy_out.setdefault(
                        "policy_map", {}
                    ).setdefault(service_policy, {}).setdefault(
                        "child_policy_name", {}
                    )
                    new_nested_policy_out["policy_map"][service_policy][
                        "child_policy_name"
                    ] = nested_policy_out["policy_map"]
                    merge_dict(policy_out[direction], new_nested_policy_out)

    return policy_out


def get_policy_map_operational_policy_map_on_interface(device, interface):
    """ Get operational policy-map on an interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name

        Returns:
            Device output parsed dictionary
    """
    try:
        out = device.parse("show policy-map interface {}".format(interface))
    except SchemaEmptyParserError as e:
        log.error(
            "Failed to parse show policy-map interface {}".format(interface)
        )
        return None

    return out


def get_policy_map_policy_map_packet_count(
    device, interface, direction="output"
):
    """ Get policy-map packet count

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            direction ('str'): input/output pkt direction

        Returns:
            class_map_out_packets: Packet count

        Raises:
            KeyError
    """

    class_map_dict = {}

    out = get_policy_map_operational_policy_map_on_interface(device, interface)

    if not out:
        return class_map_dict

    for policy_name_out in (
        out.get(interface)
        .get("service_policy")
        .get(direction)
        .get("policy_name")
    ):
        for child_policy_name_out in out[interface]["service_policy"][
            direction
        ]["policy_name"][policy_name_out]["child_policy_name"]:
            for class_map in out[interface]["service_policy"][direction][
                "policy_name"
            ][policy_name_out]["child_policy_name"][child_policy_name_out][
                "class_map"
            ]:
                try:
                    class_map_dict[class_map] = out[interface][
                        "service_policy"
                    ][direction]["policy_name"][policy_name_out][
                        "child_policy_name"
                    ][
                        child_policy_name_out
                    ][
                        "class_map"
                    ][
                        class_map
                    ][
                        "packets"
                    ]
                except KeyError:
                    return None

    return class_map_dict


def get_policy_map_policy_map_ip_precedence(
    device, interface, direction="input"
):
    """ Gets policy-map ip precedence per stream

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            direction ('str'): input/output pkt direction

        Returns:
            stream ip precedece ('dict')
    """

    out = get_policy_map_operational_policy_map_on_interface(device, interface)

    ipp_dict = {}

    if not out:
        return ipp_dict

    for policy_name_out in (
        out.get(interface)
        .get("service_policy")
        .get(direction)
        .get("policy_name")
    ):
        if (
            "child_policy_name"
            in out[interface]["service_policy"][direction]["policy_name"][
                policy_name_out
            ]
        ):
            for child_policy_name_out in out[interface]["service_policy"][
                direction
            ]["policy_name"][policy_name_out]["child_policy_name"]:
                for class_map in out[interface]["service_policy"][direction][
                    "policy_name"
                ][policy_name_out]["child_policy_name"][child_policy_name_out][
                    "class_map"
                ]:
                    if (
                        "qos_set"
                        in out[interface]["service_policy"][direction][
                            "policy_name"
                        ][policy_name_out]["child_policy_name"][
                            child_policy_name_out
                        ][
                            "class_map"
                        ][
                            class_map
                        ]
                    ):
                        precedence = out[interface]["service_policy"][
                            direction
                        ]["policy_name"][policy_name_out]["child_policy_name"][
                            child_policy_name_out
                        ][
                            "class_map"
                        ][
                            class_map
                        ][
                            "qos_set"
                        ].get(
                            "ip precedence"
                        )
                        if precedence:
                            ipp_dict[class_map] = next(iter(precedence))
        else:
            for class_map in out[interface]["service_policy"][direction][
                "policy_name"
            ][policy_name_out]["class_map"]:
                if (
                    "qos_set"
                    in out[interface]["service_policy"][direction][
                        "policy_name"
                    ][policy_name_out]["class_map"][class_map]
                ):
                    precedence = out[interface]["service_policy"][direction][
                        "policy_name"
                    ][policy_name_out]["class_map"][class_map]["qos_set"].get(
                        "ip precedence"
                    )
                    if precedence:
                        ipp_dict[class_map] = next(iter(precedence))
    return ipp_dict


def get_policy_map_class_maps(device, policy_map, control_plane_policy):
    """ Get class map dictionary

        Args:
            device (`obj`): Device object
            control_plane_policy (`str`): Control policy name
            policy_map ('str'): policy map name
        Returns:
            class map dictionary
    """
    try:
        out = device.parse("show policy-map {}".format(policy_map))
    except SchemaEmptyParserError as e:
        return {}
    try:
        class_maps = out["Control Plane"]["service_policy"]["input"][
            "policy_name"
        ][control_plane_policy]["class_map"]
    except KeyError as e:
        return {}

    return class_maps

def get_policy_map_interface_queue_output(
    device,
    interface):

    """ Gets the policy-map type queueing interface output
        Args:
            device (`obj`): Device object
            interface ('str'): Device interface
        Returns:
            output
    """
    try:
        output=device.parse("show policy-map type queueing interface {interface} output".format(interface=interface))
    except SchemaEmptyParserError as e:
        log.error('Could not get policy map queue stats')
        return None
    
    return output

