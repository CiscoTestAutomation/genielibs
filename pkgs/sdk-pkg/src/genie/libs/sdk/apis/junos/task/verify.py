"""Common verification functions for task"""

# Python
import logging
from netaddr import IPAddress
import re
import operator

# pyATS
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils import Dq

log = logging.getLogger(__name__)


def verify_task_replication(device,
                            expected_state,
                            expected_re_mode,
                            expected_protocols=None,
                            expected_protocols_sync_status=None,
                            output=None,
                            max_time=60,
                            check_interval=15):
    """ Verifies task replication info

        Args:
            device (`obj`): device to use
            expected_state (`str`): expected state of stateful replication to verify
            expected_re_mode (`str`): expected re mode to verify
            expected_protcols (`list`, Optional): specify protocols to check
                                                  Default to None
            expected_protcols_sync_status (`list`, Optional): specify protocol sync status which corresponding to expected_protocols
                                                              Default to None
            output (`str`, optional): output of show task replication
                                      Default to None
            max_time (`int`): Maximum time to keep checking
                              Default to 60 secs
            check_interval (`int`): How often to check
                                    Default to 15 secs

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            if output:
                out = device.parse('show task replication', output=output)
            else:
                out = device.parse('show task replication')
        except SchemaEmptyParserError:
            log.info('Parser is empty')
            timeout.sleep()
            continue

        # example of out
        # {
        #   "task-replication-state": {
        #     "task-gres-state": "Enabled",
        #     "task-protocol-replication-name": [
        #       "OSPF"
        #     ],
        #     "task-protocol-replication-state": [
        #       "Complete"
        #     ],
        #     "task-re-mode": "Master"
        #   }
        # }
        state = out.q.get_values('task-gres-state', 0)
        re_mode = out.q.get_values('task-re-mode', 0)
        protocol_name = out.q.get_values('task-protocol-replication-name')
        protocol_state = out.q.get_values('task-protocol-replication-state')

        name_state_status = {name: state for name, state in zip(protocol_name, protocol_state)}

        if state and re_mode:
            if state == expected_state and re_mode == expected_re_mode:

                if expected_protocols and expected_protocols_sync_status:
                    for protocol in expected_protocols:
                        if name_state_status.get(protocol) in expected_protocols_sync_status:
                            return True

                elif expected_protocols:
                    for protocol in expected_protocols:
                        if protocol in protocol_name:
                            return True

                elif expected_protocols_sync_status:
                    for state in expected_protocols_sync_status:
                        if state in protocol_state:
                            return True

                else:
                    return True

        timeout.sleep()

    return False
