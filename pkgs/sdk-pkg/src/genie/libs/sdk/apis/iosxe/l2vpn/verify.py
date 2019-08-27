"""Common verification functions for l2vpn"""

# Python
import logging
import copy
from prettytable import PrettyTable


# import Steps
from pyats.aetest.steps import Steps

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.parser.utils.common import Common

# Common
from genie.libs.parser.utils.common import Common

log = logging.getLogger(__name__)


def verify_l2vpn_storm_control_configuration(
    device, interface, service_instance_id, storm_control
):
    """ Verify storm-control configuration is applied

        Args:
            device ('obj'): device object
            interface ('str'): interface name
            service_instance_id:('int'): service instance id
            storm_control('list'): list of storm control configurations
                ex.)
                        [
                            {
                                'traffic_flow': 'unicast',
                                'name': 'cir',
                                'val': 8000
                            },
                            {
                                'traffic_flow': 'broadcast',
                                'name': 'cir',
                                'val': 8000
                            },
                            {
                                'traffic_flow': 'multicast',
                                'name': 'cir',
                                'val': 8000
                            }
                        ]
        Returns:
            None
        Raises:
            None
    """
    try:
        out = device.parse(
            "show ethernet service instance id "
            "{} interface {} detail".format(
                service_instance_id, Common.convert_intf_name(interface)
            )
        )
    except SchemaEmptyParserError:
        return False

    x = PrettyTable()
    x.field_names = [
        "Traffic flow",
        "Configuration expected",
        "Configuration found",
    ]
    config_found = True
    for sc in storm_control:

        sc_traffic_flow = sc.get("traffic_flow", "")
        sc_name = sc.get("name", "")
        sc_val = sc.get("val", "")

        row_val = [sc_traffic_flow.title()]
        row_val.append(
            "{}".format(
                "storm-control {} {} {}".format(
                    sc_traffic_flow, sc_name, sc_val
                )
            )
        )

        try:
            val = out["service_instance"][service_instance_id]["interfaces"][
                interface
            ]["micro_block_type"]["Storm-Control"][
                "storm_control_{}_cir".format(sc_traffic_flow)
            ]
            if sc_val != int(val):
                config_found = False
                row_val.append(
                    "{}".format(
                        "storm-control {} {} {}".format(
                            sc_traffic_flow, sc_name, int(val)
                        )
                    )
                )
            else:
                row_val.append(
                    "{}".format(
                        "storm-control {} {} {}".format(
                            sc_traffic_flow, sc_name, sc_val
                        )
                    )
                )

        except KeyError as e:
            row_val.append(
                "Configuration not found for {}:".format(sc_traffic_flow)
            )
            log.error(
                "Key: '{}' is not found from the command output".format(str(e))
            )
            config_found = False
        x.add_row(row_val)

    log.info(x)
    return config_found


def is_l2vpn_storm_control_packet_count_increased(
    intial_discard_packets, current_discard_packets
):
    """ Verify packet count has increased
        
            Args:
                intial_discard_packets ('dict'): previous dictionary of packet counts for flow groups
                    ex.) 
                        {
                            'broadcast': 234234,
                            'unicast': 123123
                        }
                current_discard_packets ('dict'): current dictionary of packet counts for flow groups
                    ex.) 
                        {
                            'broadcast': 234534,
                            'unicast': 123523
                        }
            Returns:
                True
                False
            Raises:
                None
        """

    result = True
    for k, v in current_discard_packets.items():
        log.info(
            "Getting current StormControl Discard packet"
            " count for {}".format(k)
        )

        key = k.lower().replace(" ", "_")
        val = intial_discard_packets.get(k, 0)

        if v <= val:
            result = False
            log.info("Packet count has not increased")
        else:
            log.info(
                "Packet count for {}: \n"
                "    Initial: {}\n"
                "    Current: {}".format(k.title().replace("_", " "), val, v)
            )
    return result
