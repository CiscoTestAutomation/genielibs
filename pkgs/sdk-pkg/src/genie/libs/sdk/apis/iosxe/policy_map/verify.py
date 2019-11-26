"""Common verify functions for policy-map"""

# Python
import re
import logging
from prettytable import PrettyTable

# Genie
from genie.utils.timeout import Timeout

# POLICY-MAP
from genie.libs.sdk.apis.iosxe.policy_map.get import (
    get_policy_map_configurational_policy_map,
    get_policy_map_operational_policy_map_on_interface,
    get_policy_map_class_maps,
)

log = logging.getLogger(__name__)


def verify_policy_map_policy_map_configurational_operational_policy_map(
    device, configurational_out, interface
):
    """Verify configured policy map and operational state match

        Args:
            device (`obj`): Device object
            configurational_out (`Dict`): Configurational status
            interface (`str`): Interface name

        Returns:
            result(`bool`): Verify result
            table(`obj`): Table result
    """
    table = PrettyTable()
    table.field_names = ["Parameter name", "Configurational", "Operational"]
    table.align["Parameter name"] = "l"
    failed = False

    operational_out = get_policy_map_operational_policy_map_on_interface(
        device, interface
    )
    if not operational_out:
        failed = True
        return failed, table
    for direction in configurational_out:
        verify_policy_map_row_added(table, "direction", direction)
        for policy_map in configurational_out[direction]["policy_map"]:
            verify_policy_map_row_added(table, "    policy_map", policy_map)
            configurational_container = configurational_out[direction][
                "policy_map"
            ][policy_map]["class"]
            operational_container = operational_out[interface][
                "service_policy"
            ][direction]["policy_name"][policy_map]["class_map"]
            verify_policy_map_policy_map_configuration_policy_map_with_operational(
                configurational_container, operational_container, table
            )
            if (
                "child_policy_name"
                in configurational_out[direction]["policy_map"][policy_map]
            ):
                for child_policy_name in configurational_out[direction][
                    "policy_map"
                ][policy_map]["child_policy_name"]:
                    verify_policy_map_row_added(
                        table, "        child_policy_map", child_policy_name
                    )
                    child_configurational_container = configurational_out[
                        direction
                    ]["policy_map"][policy_map]["child_policy_name"][
                        child_policy_name
                    ][
                        "class"
                    ]
                    child_operational_container = operational_out[interface][
                        "service_policy"
                    ][direction]["policy_name"][policy_map][
                        "child_policy_name"
                    ][
                        child_policy_name
                    ][
                        "class_map"
                    ]
                    verify_policy_map_policy_map_configuration_policy_map_with_operational(
                        child_configurational_container,
                        child_operational_container,
                        table,
                        spaces="    ",
                    )

    return failed, table


def verify_policy_map_values(
    table, parameter_name, config_key, oper_key, spaces
):
    """Verify running configuration values to operational one and add Table row

        Args:
            table (`obj`): Table object
            parameter_name (`str`): Parameter name
            config_key (`str`): Configuration key to check
            oper_key (`str`): Operational key to check

        Returns:
            True
            False
    """
    if not oper_key:
        log.warn(
            "Operational configuration key {oper_key} is not found".format(
                oper_key=oper_key
            )
        )
        return False

    # display in table
    table.add_row(
        [
            "            {}{}".format(spaces, parameter_name),
            config_key,
            oper_key,
        ]
    )
    if str(config_key) != str(oper_key):
        log.warn(
            "{parameter_name} in running "
            "configuration equals {conf} which is not equal to the opeartional one {oper}".format(
                parameter_name=parameter_name, conf=config_key, oper=oper_key
            )
        )
        return False
    return True


def verify_policy_map_row_added(table, parameter_name, parameter_value):
    """Add row to Table

        Args:
            table (`obj`): Table object
            parameter_name (`str`): Parameter name
            parameter_value (`str`): Parameter value

        Returns:
            True
            False
    """
    try:
        table.add_row(
            [
                "{parameter_name}: {parameter_value}".format(
                    parameter_name=parameter_name,
                    parameter_value=parameter_value,
                ),
                "",
                "",
            ]
        )
        table.add_row(
            [
                "***********************************************",
                "*************************",
                "*************************",
            ]
        )
    except Exception:
        return False
    return True


def verify_policy_map_policy_map_configuration(device, interfaces):
    """ Verify policy map configuration

        Args:
            device (`obj`): Device object
            interfaces (`List`): List of interfaces

        Returns:
            True
            False
    """
    log.info("Verify configured policy map and operational state match")

    policy_out = get_policy_map_configurational_policy_map(device, interfaces)

    if policy_out:
        # Checking for all fields inside 'show policy-map <policy_map>'
        verify_out, table = verify_policy_map_policy_map_configurational_operational_policy_map(
            device, policy_out, interfaces[0]
        )

        if verify_out:
            log.error(
                "Configurational state is not equal to the opeartional one"
            )
            return False

        log.info(table)
        return True
    else:
        log.error(
            "Couldn't retrieve the policy-map running configuration or "
            "no service-policy configuration found"
        )

    return False


def verify_policy_map_packet_count_match(
    flows_dict, class_map_out_packets_dict
):
    """ Compare the packets' count for the provided traffic flows

        Args:
            flows_dict (`dict`): Dictionary of traffic flows
            class_map_out_packets_dict (`dict`): Dictionary of retrieved traffic flows packets count

        Returns:
            True
            False
    """

    failures = []
    counted_traffic_flow_list = []
    for traffic_flow in flows_dict:
        if traffic_flow in class_map_out_packets_dict.keys():
            counted_traffic_flow_list.append(traffic_flow)
            if (
                flows_dict[traffic_flow]
                == class_map_out_packets_dict[traffic_flow]
            ):
                log.info(
                    "Class-map '{class_map}' packets count '{class_map_out_packets}' matches "
                    "the expected count '{expected_count}'".format(
                        class_map=traffic_flow,
                        class_map_out_packets=class_map_out_packets_dict[
                            traffic_flow
                        ],
                        expected_count=flows_dict[traffic_flow],
                    )
                )
            else:
                failures.append(
                    "Class-map '{class_map}' packets count '{class_map_out_packets}' doesn't "
                    "match the expected count '{expected_count}'".format(
                        class_map=traffic_flow,
                        class_map_out_packets=class_map_out_packets_dict[
                            traffic_flow
                        ],
                        expected_count=flows_dict[traffic_flow],
                    )
                )
        else:
            # Traffic flow name is not found, need to search in ip match precedence
            get_traffic_flow_num = " ".join(
                filter(str.isdigit, traffic_flow)
            ).split(" ")[0]
            for class_map in class_map_out_packets_dict:
                if class_map != "class-default" and get_traffic_flow_num in " ".join(
                    filter(str.isdigit, class_map)
                ).split(
                    " "
                ):
                    # Case of multiple traffic streams
                    combined_traffic_flows_list = []
                    sum_flows = 0
                    for num in " ".join(filter(str.isdigit, class_map)).split(
                        " "
                    ):
                        new_name = "IPP{}".format(num)
                        combined_traffic_flows_list.append(new_name)
                        counted_traffic_flow_list.append(new_name)
                        sum_flows += flows_dict[new_name]

                    if class_map_out_packets_dict[class_map] != sum_flows:
                        # Failure: 'IPP67' count is not equal to the sum of 'IPP6' & 'IPP7'
                        failures.append(
                            "Sum of packets count for IPP '{combined_traffic_flows_list}' is '{sum_pkts}' "
                            "doesn't match the packet count of class-map '{class_map}' '{expected_count}'".format(
                                combined_traffic_flows_list=combined_traffic_flows_list,
                                sum_pkts=sum_flows,
                                class_map=class_map,
                                expected_count=class_map_out_packets_dict[
                                    class_map
                                ],
                            )
                        )
                    else:
                        log.info(
                            "Sum of packets count for IPP '{combined_traffic_flows_list}' is '{sum_pkts}' "
                            "match the packet count of class-map '{class_map}' '{expected_count}'".format(
                                combined_traffic_flows_list=combined_traffic_flows_list,
                                sum_pkts=sum_flows,
                                class_map=class_map,
                                expected_count=class_map_out_packets_dict[
                                    class_map
                                ],
                            )
                        )

    rest_of_traffic_flows_in_class_default = set(flows_dict) - set(
        counted_traffic_flow_list
    )
    sum_of_the_rest = 0
    for item in rest_of_traffic_flows_in_class_default:
        sum_of_the_rest += flows_dict[item]

    if rest_of_traffic_flows_in_class_default:
        if sum_of_the_rest > class_map_out_packets_dict["class-default"]:
            # Failure: Sum of remaining traffic flows is higher than the class-default packets
            failures.append(
                "Sum of packets count for '{flow_tracking_list}' is '{sum_of_the_rest}' is greater than "
                "the packet count of class-map 'class-default' '{expected_count}'".format(
                    flow_tracking_list=rest_of_traffic_flows_in_class_default,
                    sum_of_the_rest=sum_of_the_rest,
                    expected_count=class_map_out_packets_dict["class-default"],
                )
            )
        else:
            log.info(
                "Sum of packets count for '{flow_tracking_list}' is '{sum_of_the_rest}' less than "
                "or equal the packet count of class-map 'class-default' '{expected_count}'".format(
                    flow_tracking_list=rest_of_traffic_flows_in_class_default,
                    sum_of_the_rest=sum_of_the_rest,
                    expected_count=class_map_out_packets_dict["class-default"],
                )
            )

    if failures:
        log.error("\n".join(set(failures)))
    else:
        return True

    return False


def verify_policy_map_policy_map_configuration_policy_map_with_operational(
    configurational_container, operational_container, table, spaces=None
):
    """ Compare configuration policy map with operational 

        Args:
            configurational_container (`dict`): Dictionary of configurational container
            operational_container (`dict`): Dictionary of operational container
            table (`obj`): Table object
            spaces ('str'): Spaces in table field

        Returns:
            True
            False
    """
    failed = False
    for config_class in configurational_container:
        verify_policy_map_row_added(
            table, "        {}class".format(spaces), config_class
        )
        for parameter_name in configurational_container[config_class]:
            # Search for the configurational keys under the operational status
            if "service_policy" in parameter_name:
                continue
            if parameter_name == "qos_set":
                for sub_parameter in configurational_container[config_class][
                    "qos_set"
                ]:
                    config_key = configurational_container[config_class][
                        parameter_name
                    ][sub_parameter]
                    for sub_parameter_value in operational_container[
                        config_class
                    ]["qos_set"][sub_parameter]:
                        oper_key = sub_parameter_value
                        if not verify_policy_map_values(
                            table, sub_parameter, config_key, oper_key, spaces
                        ):
                            failed = True
            elif parameter_name == "police":
                for sub_parameter in configurational_container[config_class][
                    "police"
                ]:
                    config_key = configurational_container[config_class][
                        parameter_name
                    ][sub_parameter]
                    sub_parameter_value = operational_container[config_class][
                        "police"
                    ][sub_parameter]
                    oper_key = sub_parameter_value
                    if (
                        type(sub_parameter_value) is dict
                        and config_key in sub_parameter_value["actions"]
                    ):
                        for action in sub_parameter_value["actions"]:
                            table.add_row(
                                [
                                    "            {}{}".format(
                                        spaces, sub_parameter
                                    ),
                                    config_key,
                                    action,
                                ]
                            )
                        continue
                    if not verify_policy_map_values(
                        table, sub_parameter, config_key, oper_key, spaces
                    ):
                        failed = True
            else:
                config_key = configurational_container[config_class][
                    parameter_name
                ]
                oper_key = operational_container[config_class][parameter_name]
                if not verify_policy_map_values(
                    table, parameter_name, config_key, oper_key, spaces
                ):
                    failed = True
        table.add_row(
            [
                "***********************************************",
                "*************************",
                "*************************",
            ]
        )

    return False if failed else True


def verify_policy_map_packets_counting_up(
    device,
    packet_classes,
    control_plane_policy,
    policy_map,
    max_time=15,
    check_interval=5,
):
    """Verify packets are counting up

        Args:
            device (`obj`): Device object
            packet_classes (`Dict`): list of packet classes
                ex.)
                    packet_classes: ['BGP_Class', 'OSPF_Class', 'LDP_Class']

            control_plane_policy (`str`): Control policy name
            policy_map ('str'): policy map name
            max_time (int): Maximum wait time for the trigger,
                            in second. Default: 15
            check_interval (int): Wait time between iterations when looping is needed,
                            in second. Default: 5
        Returns:
            True
            False
    """
    timeout = Timeout(max_time, check_interval)
    result = True
    while timeout.iterate():
        result = True
        class_maps = get_policy_map_class_maps(
            device, policy_map, control_plane_policy
        )

        if class_maps and packet_classes:
            for packet_class in packet_classes:
                packets_count = class_maps.get(packet_class, {}).get("packets", 0)
                log.info(
                    "Verifying if packets are counting up for {}".format(
                        packet_class
                    )
                )
                if packets_count == 0:
                    result = False
                    log.error(
                        "{} packets are not counting up".format(packet_class)
                    )

            if result:
                return True
        else:
            result = False
        timeout.sleep()
    return result
