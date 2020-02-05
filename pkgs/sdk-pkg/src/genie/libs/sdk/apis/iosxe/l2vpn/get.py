"""Common get info functions for bgp"""

# Python
import os
import logging
import re
import time

# pyATS
from pyats.easypy import runtime
from genie.utils.config import Config
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.parser.utils.common import Common

log = logging.getLogger(__name__)


def get_l2vpn_interface_under_service_instance(device, service_instance_id):
    """ Gets interface under service instance 'service_instance_id' using command
        'show ethernet service instance'

        Args:
            device ('obj'): Device object
            service_instance_id ('int'): service instance id
    
        Returns:
            interface
            None
        Raises:
            None

    """
    interfaces = None
    try:
        out = device.parse("show ethernet service instance")
    except SchemaEmptyParserError as e:
        return interfaces
    try:
        interfaces = list(
            out["service_instance"][service_instance_id]["interfaces"]
        )
    except KeyError as e:
        return interfaces

    return interfaces


def get_l2vpn_storm_control_discard_packet_count(
    device, service_instance_id, interface
):
    """Get current storm control discard packet count
        
            Args:
                device ('Obj'): Device object
                service_instance_id ('int'): L2VPN service instance id
                interface ('str'): Interface name

            Returns:
                None

            Raises:
                None
                
        """

    packets_counts = {}

    try:
        out = device.parse(
            "show ethernet service instance id {} interface {} stats".format(
                service_instance_id, Common.convert_intf_name(interface)
            )
        )
    except SchemaEmptyParserError:
        return packets_counts

    try:
        packets_counts = out["service_instance"][service_instance_id][
            "storm_control_discard_pkts"
        ]
    except KeyError as e:
        return packets_counts

    for k, v in packets_counts.items():
        val = v.get("default", 0)
        log.info(
            "{} discard pkts: {}".format(k.title().replace("_", " "), val)
        )
        key = k.lower().replace(" ", "_")
        packets_counts[key] = val

    return packets_counts
