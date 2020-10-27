import logging
import operator

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_snmp_target(device,
                       expected_target,
                       max_time=30,
                       check_interval=10,):
    """ Verify snmp target

        Args:
            device (`obj`): Device object
            expected_target (`str`): Expected target IP
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
            output = device.parse('show configuration snmp')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example output
        # "configuration": {
        #             "snmp": {
        #                "trap-group": {
        #                                 "targets": [
        #                                     {
        #                                         "name": "125.53.99.32"
        #                                     },

        targets = output.q.get_values('targets')
        if [target for target in targets if target.get('name', None) == expected_target]:
            return True

        timeout.sleep()
    return False

def verify_snmp_statistics(device,
                       expected_output_counter,
                       max_time=30,
                       check_interval=10,
                       invert=False):
    """ Verify snmp statistics

        Args:
            device (`obj`): Device object
            expected_output_counter (`str`): Expected output counter
            max_time (`int`): Max time, default: 60 seconds
            check_interval (`int`): Check interval, default: 10 seconds
            invert('bool'): True if negative scenario to verify
        Returns:
            result (`bool`): Verified result
        Raises:
            N/A
    """

    op = operator.contains
    if invert:
        op = lambda data, check: operator.not_(operator.contains(data, check))

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse('show snmp statistics')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example output
        # "snmp-statistics": {
        #     "snmp-output-statistics": {
        #         "traps": "0"

        traps = Dq(output).contains('snmp-output-statistics').get_values('traps')
        if traps and op(traps, expected_output_counter):
            return True

        timeout.sleep()
    return False
