# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_traceroute_parsed_output(device, addr, vrf=None, proto=None, ingress=None, source=None,
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
    if vrf:
        kwargs.pop('vrf')
        kwargs['command'] = 'traceroute vrf {}'.format(vrf)
    try:
        output = device.traceroute(**kwargs)
    except SubCommandFailure as e:
        log.info("Could not find any traceroute information")
        return False

    command = kwargs.get('command', 'traceroute')
    try:
        parsed_ouput = device.parse(command, output=output)
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
                return int(label.split('/')[0])

    log.info(
        "Could not find any MPLS label to prefix {prefix}".format(
            prefix=prefix
        )
    )
    return None

def get_traceroute_ipv6(device, addr, source=None, dscp=None, numeric=None,
                        timeout=None, probe=None, minimum_ttl=None,
                        maximum_ttl=None, precedence=None):
    """ Get parsed output of traceroute command
        Args:
            device ('obj'): Device object
            addr ('str'): Destination address
            source ('str'): Source address or interface
            dscp ('int'): DSCP Value
            numeric ('str'): Numeric display
            timeout ('int'): Timeout in seconds
            probe ('int'): Probe count
            minimum_ttl ('int'): Minimum Time to Live
            maximum_ttl ('int'): Maximum Time to Live
            precedence ('str'): specify Precedence (Range: 0 to 7)
        Returns:
            Dictionary: Parsed output of traceroute ipv6 command
        Raises:
            None
    """
    cmd = f'traceroute ipv6 {addr}'
    if dscp:
        cmd = cmd + ' dscp '+dscp
    if numeric:
        cmd = cmd + ' numeric'
    if precedence:
        cmd = cmd + ' precedence '+str(precedence)
    if probe:
        cmd = cmd + ' probe '+str(probe)
    if source:
        cmd = cmd + ' source '+source
    if timeout:
        cmd = cmd + ' timeout '+str(timeout)
    if minimum_ttl and maximum_ttl:
        cmd = cmd + ' ttl '+str(minimum_ttl)+' '+str(maximum_ttl)
    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to execute {cmd} on device {device.name}. Error:\n{e}')

    try:
        parsed_ouput = device.parse(cmd, output=output)
    except SchemaEmptyParserError as e:
        log.info(f'Could find any traceroute ipv6 information for prefix {addr}')
        return None

    return parsed_ouput
