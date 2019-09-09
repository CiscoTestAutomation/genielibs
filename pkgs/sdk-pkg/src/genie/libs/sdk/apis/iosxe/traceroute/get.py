# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# iosxe traceroute
from genie.libs.parser.iosxe.traceroute import Traceroute

log = logging.getLogger(__name__)


def get_traceroute_parsed_output(device, prefix):
    """ Get parsed output of traceroute command
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
        Returns:
            Dictionary: Parsed output of traceroute command
        Raises:
            None
    """

    try:
        output = device.traceroute(addr=prefix)
    except SubCommandFailure as e:
        log.info("Could not find any traceroute information")
        return False

    parser_obj = Traceroute(device=device)
    try:
        parsed_ouput = parser_obj.parse(output=output)
    except SchemaEmptyParserError as e:
        log.info(
            "Could find any traceroute information for prefix {address}".format(
                address=prefix
            )
        )
        return None

    return parsed_ouput

def get_traceroute_mpls_label_to_prefix(device, prefix):
    """ Get traceroute label to prefix address
        Args:
            device ('obj'): Device object
            prefix ('str'): Prefix address
        Returns:
            int: Traceroute label
        Raises:
            None
    """

    log.info(
        "Getting label from traceroute to prefix {prefix}".format(
            prefix=prefix
        )
    )

    parsed_output = get_traceroute_parsed_output(device=device, prefix=prefix)

    if not parsed_output:
        return None

    for index_hop in (
        parsed_output["traceroute"].get(prefix, {}).get("hops", {})
    ):
        for index_path in (
            parsed_output["traceroute"][prefix]["hops"]
            .get(index_hop, {})
            .get("paths", {})
        ):
            label = (
                parsed_output["traceroute"][prefix]["hops"][index_hop]["paths"]
                .get(index_path, {})
                .get("label_info", {})
                .get("MPLS", {})
                .get("label", {})
            )
            log.info("Found label {label}".format(label=label))
            return int(label)

    log.info(
        "Could not find any MPLS label to prefix {prefix}".format(
            prefix=prefix
        )
    )
    return None