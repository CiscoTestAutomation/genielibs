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


def get_ap_state(device, ap_name):
    """Get configured ap state
    Args:
        device (obj): Device object
        ap_name (str): accesspoint name
    Returns:
        ap state (str) if success else empty string
    Raises:
        N/A        
    """
    ap_state = ""
    try:
        ap_summary = device.parse('show ap summary')
        if ap_summary.get('ap_name').get(ap_name):
            ap_state = ap_summary.get('ap_name').get(ap_name).get('state')
    except (SchemaEmptyParserError) as e:
        log.error("Failed to parse 'show ap summary': {e}".format(e=e))
        return ""
    return ap_state


def get_ap_country(device, ap_name):
    """Get configured ap country
    Args:
        device (obj): Device object
        ap_name (str): accesspoint name
    Returns:
        ap country (str) if success else empty string
    Raises:
        N/A        
    """
    ap_country = ""
    try:
        ap_summary = device.parse('show ap summary')
        if ap_summary.get('ap_name').get(ap_name):
            ap_country = ap_summary.get('ap_name').get(ap_name).get('country')

    except (SchemaEmptyParserError) as e:
        log.error("Failed to parse 'show ap summary': {e}".format(e=e))
        return ""
    return ap_country


def get_ap_mode(device, ap_name):
    """Get configured ap mode
    Args:
        device (obj): Device object
        ap_name (str): accesspoint name
    Returns:
        ap mode (str) if success else empty string
    Raises:
        N/A        
    """
    ap_mode = ""
    try:
        ap_config_general = device.parse('show ap name {} config general'.format(ap_name))
        if ap_config_general.get('ap_name').get(ap_name):
            ap_mode = ap_config_general.get('ap_name').get(ap_name).get('ap_mode')
    except (SchemaEmptyParserError) as e:
        log.error("Failed to parse 'show ap name config general': {e}".format(e=e))
        return ""
    return ap_mode

