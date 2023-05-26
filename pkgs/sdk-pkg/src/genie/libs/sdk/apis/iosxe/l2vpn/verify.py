"""Common verification functions for l2vpn"""

# Python
import logging
import re
from prettytable import PrettyTable

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Common
from genie.libs.parser.utils.common import Common
from unicon.core.errors import SubCommandFailure

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


def verify_flood_suppress(device, evi):
    '''
    verify_flood_suppress
    Check the output of 'show l2vpn evpn evi {evi} detail | include Flood' to verify if flood suppress is enabled/disbled
    
    Args:
        device ('obj') : Device object
        evi ('int') : evi_id to check the flood suppress on the l2vpn evpn instance
    
    Returns:
        True
        False
    
    Raises:
        None
    '''

    log.info('Verify if the flood suppress is disabled')
    cmd = f'show l2vpn evpn evi {evi} detail | include Flood'

    try:
        sh_flood_suppress = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure('Could not execute CLI on {device}. Error: {error}'.format(device = device, error = e))

    is_disabled = re.search(r'AR\s+Flood\s+Suppress:\s+Disabled', sh_flood_suppress)
    is_detached = re.search(r'\s+Flood\s+Suppress:\s+Detached', sh_flood_suppress)

    if is_disabled and is_detached:
        log.info('The Flood Suppress is Disabled on the l2vpn evi {}'.format(evi))
        return True
    else:
        log.info('The Flood Suppress is not Disabled on the l2vpn evi {}'.format(evi))
        return False
