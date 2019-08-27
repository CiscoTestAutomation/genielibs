"""Common get info functions for routing"""

# Python
import os
import logging
import re

from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_bridge_domain_bridge_domain_mac_count(device, timeout_parse=500):
    """ Get bridge domain mac count

        Args:
            device(`obj`): Device object 
            timeout_parse ('int'): Timeout in seconds for command device.parse('show bridge-domain')
        Returns:
            integer: mac count
        Raises:
            None
    """
    mac_count = 0

    log.info("Getting MAC count")
    device.execute.timeout = timeout_parse
    try:
        output_bd = device.parse("show bridge-domain")
    except SchemaEmptyParserError as e:
        return mac_count

    device.execute.timeout = 60

    for bd in output_bd.get("bridge_domain", []):
        for intf in (
            output_bd["bridge_domain"].get(bd, {}).get("mac_table", [])
        ):
            mac_count += len(
                output_bd["bridge_domain"][bd]
                .get("mac_table", {})
                .get(intf, {})
                .get("mac_address", {})
                .keys()
            )

    log.info("MAC count is {}".format(mac_count))

    return mac_count


def get_bridge_domain_bridge_domain_interfaces(device, bridge_domain_id):
    """ Get list of interfaces using bridge-domain id

        Args:
            bridge_domain_id('int'): bridge-domain id to get interfaces
            device ('obj'): Device object

        Returns:
            list of interfaces
        Raises:
            None
    """
    out = {}
    interfaces = []

    try:
        out = device.parse(
            "show bridge-domain {bridge_domain_id}".format(
                bridge_domain_id=bridge_domain_id
            )
        )

    except SchemaEmptyParserError as e:
        return interfaces

    try:
        interfaces = out["bridge_domain"][bridge_domain_id][
            "split-horizon_group"
        ]["0"]["interfaces"]

    except KeyError as e:
        pass

    return interfaces
