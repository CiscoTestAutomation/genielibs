"""Common verification functions for ip access lists"""

# Python
import logging

log = logging.getLogger(__name__)


def _normalize_acl_line(line):
    return ' '.join(line.split())


def verify_ip_access_list(device, name, acl_list):
    '''Verify "show ip access-lists {name}" output
        Args:
            device ('obj'): device object
            name ('str'): name of the access list
            acl_list ('list' or 'str'): expected acl or list of acls
        Returns:
            True/False
    '''
    if isinstance(acl_list, str):
        acl_list = [acl_list]
    output = device.execute(f'show ip access-lists {name}')
    output_lines = {
        _normalize_acl_line(line)
        for line in output.splitlines()
        if line.strip()
    }
    for acl in acl_list:
        expected_acl = _normalize_acl_line(acl)
        if expected_acl not in output_lines:
            log.error(f'Verify ip access list {name} failed, '
                      f'expect {acl} in output')
            return False
    else:
        return True
