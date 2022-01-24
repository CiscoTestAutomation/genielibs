# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)


def get_wireless_management_trustpoint_name(device):
    """Get configured trustpoint
    Args:
        device (obj): Device object
    Returns:
        Trustpoint name (str) if success else empty string
        ""
    """
    try:
        output = device.parse('show wireless management trustpoint')
    except SchemaEmptyParserError:
        return ''
    return output.q.get_values('trustpoint_name', 0) or ''


def get_pki_trustpoint_state(device, trustpoint_name):
    """Get configured trustpoint
    Args:
        device (obj): Device object
        trustpoint_name (str): trustpoint name
    Returns:
        Trustpoint state (str) if success else empty string
    """
    try:
        pki_trustpoint_status = device.parse(
            'show crypto pki trustpoint {} status'.format(trustpoint_name))
        pki_trustpoint_state = pki_trustpoint_status['Trustpoints'][trustpoint_name]['state']
    except KeyError:
        return ""
    return pki_trustpoint_state
