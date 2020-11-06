'''Common get info functions for ping'''
import logging

# Genie
from genie.utils import Dq
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_ping_message(
    device, 
    interface,
    address,
    source,
    size,
    count,
    ):
    """ Get ntp peer information

        Args:
            device (`obj`): Device object
            interface (`str`): Given interface for the output
            address (`str`): Interface used in command
            source (`str`): Interface used in command
            size (`int`): Size value used in command
            count (`int`): Count value used in command
        Returns:
            result (`str`): message
        Raises:
            N/A
    """
    
    try:
        output = device.parse('\
            ping {address} source {source} size {size} do-not-fragment count {count}'.format(
                address=address,
                source=source,
                size=size,
                count=count,
            ))
    except SchemaEmptyParserError as e:
        raise Exception("Failed to parse output with error.") from e

    # Example output
    # {
    #     'ping': 
    #         {'address': '1.1.1.1',
    #             'data-bytes': 1400,
    #             'result': [
    #                 {'bytes': 1408,
    #                 'from': '1.1.1.1',
    #                 'message': 'expected message',
    # ...

    rout=output.q.contains(f'message|{interface}',regex=True).reconstruct()

    # {'ping': {'address': '1.1.1.1',
    #   'result': [{'message': '...', 'from': 'interface'},
    #              ...
    result_list = Dq(rout).get_values('result')

    message = result_list[0]['message']

    return message
