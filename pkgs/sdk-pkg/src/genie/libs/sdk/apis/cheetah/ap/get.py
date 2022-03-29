# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)


def get_ap_mode(device):
    """Get ap mode 
    Args:
        device (obj): Device object
    Returns:
        ap mode in string 
        """
    try:
        capwap_client_rcb = device.parse('show capwap client rcb')
    except SchemaEmptyParserError as e:
        log.error(e)
        return ''

    return capwap_client_rcb.get('ap_mode', '')


def get_operation_state(device):
    """Get operation state 
    Args:
        device (obj): Device object
    Returns:
        operation state in string 
        """
    try:
        capwap_client_rcb = device.parse('show capwap client rcb')
    except SchemaEmptyParserError as e:
        log.error(e)
        return ''

    return capwap_client_rcb.get('operation_state', '')


def get_controller_name(device):
    """Get controller name
    Args:
        device (obj): Device object
    Returns:
        mwar name in string 
        """
    try:
        capwap_client_rcb = device.parse('show capwap client rcb')
    except SchemaEmptyParserError as e:
        log.error(e)
        return ''

    return capwap_client_rcb.get('mwar_name', '')


def get_ip_prefer_mode(device):
    """Get ip prefer mode 
    Args:
        device (obj): Device object
    Returns:
        ip prefer mode in string
        """
    try:
        capwap_client_rcb = device.parse('show capwap client rcb')
    except SchemaEmptyParserError as e:
        log.error(e)
        return ''

    return capwap_client_rcb.get('ip_prefer_mode', '')


def get_ip_address(device):
    """Get ip address of controller associated to AP
    Args:
        device (obj): Device object
    Returns:
        IP address
        """
    try:
        capwap_client_rcb = device.parse('show capwap client rcb')
    except SchemaEmptyParserError as e:
        log.error(e)
        return ''

    return capwap_client_rcb.get('mwar_ap_mgr_ip', '')