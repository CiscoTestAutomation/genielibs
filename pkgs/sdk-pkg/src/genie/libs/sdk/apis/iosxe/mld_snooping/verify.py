"""Common verify functions for MLD snooping"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def _dict_compare(expect, actual):
    """Recursively compare expected values against actual values.
        Args:
            expect('dict'): expected key-value pairs
            actual('dict'): actual key-value pairs
        Returns:
            True if every expected entry matches actual, else False
    """
    for k in expect:
        if k in actual:
            if isinstance(expect[k], dict) and isinstance(actual[k], dict):
                if not _dict_compare(expect[k], actual[k]):
                    return False
            elif isinstance(expect[k], list) and isinstance(actual[k], list):
                for element in expect[k]:
                    if element not in actual[k]:
                        return False
            elif expect[k] != actual[k]:
                log.debug(f"{k} mismatch: expected {expect[k]}, "
                          f"actual {actual[k]}")
                return False
        else:
            log.debug(f"{k} does not exist, expect {expect[k]}")
            return False
    return True


def verify_mld_snooping(
        device, vlan, verify_scope='vlan', mld_snooping=None,
        mldv2_snooping=None, mld_admin_state=None, mld_oper_state=None,
        listener_message_suppression=None, robustness_variable=None,
        check_hop_count=None, last_listener_query_count=None,
        last_listener_query_interval=None, mld_immediate_leave=None,
        **kwargs):
    """
    Verifies if all the given parameters are correct for mld snooping
    Args:
        device('obj'): Device object
        vlan('str'): vlan
        verify_scope('str'): verify scope, global or vlan
        mld_snooping('str'): MLD snooping global status,
                             Enabled/Disabled
        mldv2_snooping('str'): MLDv2 snooping global status,
                               Enabled/Disabled
        mld_admin_state('str'): MLD snooping admin state,
                                Enabled/Disabled
        mld_oper_state('str'): MLD snooping oper state,
                               Enabled/Disabled
        listener_message_suppression('str'): Listener message
                                             suppression,
                                             Enabled/Disabled
        robustness_variable('str'): Robustness variable value
        check_hop_count('str'): check hop count, Yes/No
        mld_immediate_leave('str'): mld immediate leave,
                                    Enabled/Disabled
        last_listener_query_count('int'): last listener query count
        last_listener_query_interval('int'): last listener query
                                             interval
        kwargs: Additional key-value pairs to verify
    Returns:
        True/False
    Raises:
        None
    """

    kwargs.update({
        k: v for k, v in {
            'mld': mld_snooping,
            'mldv2': mldv2_snooping,
            'admin_state': mld_admin_state,
            'oper_state': mld_oper_state,
            'suppression': listener_message_suppression,
            'check_hop_count': check_hop_count,
            'mld_leave': mld_immediate_leave,
            'robustness': robustness_variable,
            'query_count': last_listener_query_count,
            'query_interval': last_listener_query_interval,
        }.items()
        if v is not None
    })
    entry = device.api.get_mld_snooping(vlan=vlan)
    if verify_scope == 'vlan':
        entry = entry.get('vlan', {}).get(str(vlan), {})
    log.debug('Verify the mld snooping configuration.\n'
              f'Expected values: {kwargs}\n'
              f'Actual values: {entry}')
    if entry:
        return _dict_compare(kwargs, entry)
    return False


def verify_mld_snooping_address_count(
        device, min_count, max_count=None, max_time=4, check_interval=2):
    """
    Verify the ip mld snooping address count
    Args:
        device('obj'): device object
        max_count('int'): expected maximum group count
        min_count('int'): expected minimum group count
        max_time('int'): maximum time to wait for verification
        check_interval('int'): interval between checks
    Returns:
        True/False
    Raises:
        None
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = device.api.get_mld_snooping_address_count()
        act_group_count = out.get(
            'total_number_of_groups', {}).get('mld_groups_count', 0)
        check_result = True
        if min_count is not None and act_group_count < min_count:
            check_result = False
        elif max_count is not None and act_group_count > max_count:
            check_result = False
        if check_result:
            log.debug(
                f'Group count {act_group_count} is within the '
                f'expected range [{min_count}, {max_count}]')
            return True
        timeout.sleep()
    return False


def verify_ipv6_mld_snooping_address_summary(
        device, vlan, address, snoop_type=None, version=None, port=None,
        source_address=None, max_time=6, check_interval=2, **kwargs):
    """
    Verifies if all the given parameters are correct for snooping group
    Args:
        device('obj'): Device object
        vlan('str'): vlan
        address('str'): group IP address
        snoop_type('str'): snooping type
        version('str'): protocol version
        port('str'): mld snooping port list
        source_address('str'): source ip address
        max_time('int'): maximum time to wait for verification
        check_interval('int'): interval between checks
        **kwargs: additional parameters to verify
    Returns:
        True/False
    Raises:
        None
    """

    kwargs.update({
        k: v for k, v in {
            'type': snoop_type,
            'version': version,
            'port_list': port,
            'source_ip': source_address,
        }.items()
        if v is not None
    })
    timeout = Timeout(max_time, check_interval)
    out = {}
    while timeout.iterate():
        out = device.api.get_ipv6_mld_snooping_address_summary(
            vlan=vlan, group=address)
        if out:
            entry = out.get('vlan', {}).get(str(vlan), {}).get(
                'group', {}).get(str(address), {})
            if _dict_compare(kwargs, entry):
                log.debug(
                    'MLD snooping group entry verified PASSED. '
                    f'Expected: {kwargs}, actual: {entry}')
                return True
        timeout.sleep()
    return False
