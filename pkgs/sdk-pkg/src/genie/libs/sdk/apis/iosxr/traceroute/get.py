# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# iosxe traceroute
from genie.libs.parser.iosxr.traceroute import Traceroute

log = logging.getLogger(__name__)


def get_traceroute_parsed_output(device, addr, proto=None, ingress=None, source=None,
                                 dscp=None, numeric=None, timeout=None, probe=None,
                                 minimum_ttl=None, maximum_ttl=None, port=None, style=None):
    """ Get parsed output of traceroute command
        Args:
            device ('obj'): Device object
            addr ('str'): Destination address
            proto ('str'): Protocol(ip/ipv6)
            ingress ('str'): Ingress traceroute
            source ('str'): Source address or interface
            dscp ('int'): DSCP Value
            numeric ('str'): Numeric display
            timeout ('int'): Timeout in seconds
            probe ('int'): Probe count
            minimum_ttl ('int'): Minimum Time to Live
            maximum_ttl ('int'): Maximum Time to Live
            port ('int'): Port Number
            style ('str'): Loose, Strict, Record, Timestamp, Verbose

        Returns:
            Dictionary: Parsed output of traceroute command
        Raises:
            None
    """
    # kwargs is used to pass args that aren't "None" to traceroute()
    kwargs = {k: v for k, v in locals().items() if v}
    kwargs.pop('device')

    try:
        output = device.traceroute(**kwargs)
    except SubCommandFailure as e:
        log.info("Could not find any traceroute information")
        return False

    parser_obj = Traceroute(device=device)
    try:
        parsed_ouput = parser_obj.parse(output=output)
    except SchemaEmptyParserError as e:
        log.info(
            "Could find any traceroute information for prefix {address}".format(
                address=addr
            )
        )
        return None

    return parsed_ouput

def get_traceroute_mpls_label_to_prefix(device, prefix, timeout=None):
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

    parsed_output = get_traceroute_parsed_output(device=device, addr=prefix, timeout=timeout)

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
                .get("label")
            )
            if label:
                log.info("Found label {label}".format(label=label))
                return int(label)

    log.info(
        "Could not find any MPLS label to prefix {prefix}".format(
            prefix=prefix
        )
    )
    return None