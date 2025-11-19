""" Common get info function for flow """

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_flows_src_dst_address_pairs(device, flow_monitor):
    """ Gets flows under flow_monitor and returns source and destination address pairs

        Args:
            device ('obj'): Device to use
            flow_monitor ('str'): Flow monitor name

        Raises:
            N/A

        Returns:
            [('source_address', 'destination_address'), ...]
    """
    log.info('Getting all source and destination address pairs under flow monitor {name}'
             .format(name=flow_monitor))

    try:
        output = device.parse('show flow monitor {name} cache format table'
                              .format(name=flow_monitor))
    except SchemaEmptyParserError:
        return []

    pairs = []

    # All hardcoded keys are mandatory in the parser
    for src in output.get('ipv4_src_addr', {}):
        for dst in output['ipv4_src_addr'][src]['ipv4_dst_addr']:
            pairs.append((src, dst))

    return pairs


def get_show_flow_monitor_cache_format_table_output(device, monitor_name, timeout=120):
    """ Find the lines which are match from show command.
        Args:
            device (`obj`): Device object
            monitor_name (`str`): Flow monitor name
            timeout (`int`): Timeout value for command execution , default is 120 seconds
        Returns:
            output('str') : Output returned
        Raises:
            SubCommandFailure: Failed to get cache format table output
    """
    command = f"show flow monitor {monitor_name} cache format table"
    output = ""
    try:
        output= device.execute(command, timeout=timeout)
        if output == "":
            log.error('No match found')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not get cache format table output. Error:\n{e}')

    return output