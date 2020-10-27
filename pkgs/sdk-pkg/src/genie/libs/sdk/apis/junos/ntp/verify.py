import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_ntp_mode(device,
                   expected_mode,
                   expected_peer=None,
                   max_time=30,
                   check_interval=10,):
    """ Verify a peer has expected ntp mode

        Args:
            device (`obj`): Device object
            expected_mode (`str`): Expected mode
            expected_peer (`str`): Expected peer IP
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show ntp associations')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example output
        # 'peer': {
        #     Any(): {
        #         'local_mode': {
        #             Any(): {
        #                 'remote': str,
        #                 'mode': str,

        if expected_peer:
            return expected_peer in output.q.contains_key_value('mode', expected_mode).get_values('peer')
        elif expected_mode in output.q.get_values('mode'):
            return True

        timeout.sleep()
    return False


