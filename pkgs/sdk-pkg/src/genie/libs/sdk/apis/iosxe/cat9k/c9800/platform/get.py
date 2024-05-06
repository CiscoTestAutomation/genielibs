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
        if ap_summary.get("ap_name"):
            if ap_summary.get('ap_name').get(ap_name):
                ap_state = ap_summary.get('ap_name').get(ap_name).get('state')
    except SchemaEmptyParserError as e:
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
        if ap_summary.get("ap_name"):
            if ap_summary.get('ap_name').get(ap_name):
                ap_country = ap_summary.get('ap_name').get(ap_name).get('country')

    except SchemaEmptyParserError as e:
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
    except SchemaEmptyParserError as e:
        log.error("Failed to parse 'show ap name config general': {e}".format(e=e))
        return ""
    return ap_mode


def get_installation_mode(device):
    """Get installation mode
    Args:
        device (obj): Device object
    Returns:
        installation mode (str) if success else empty string
    Raises:
        N/A        
    """
    installation_mode = ""
    try:
        show_version = device.parse('show version')
        if show_version.get('version'):
            installation_mode = show_version.get('version', {}).get('installation_mode')
    except SchemaEmptyParserError as e:
        log.error("Failed to get installation mode from 'show version': Error: {e}".format(e=str(e)))
        return ""
    return installation_mode


def get_ap_model(device, ap_name):
    """Get configured ap model 
    Args:
        device (obj): Device object
        ap_name (str): accesspoint name
    Returns:
        ap model (str) if success else empty string
    Raises:
        N/A        
    """
    ap_model = ""
    try:
        ap_summary = device.parse('show ap summary')
        if ap_summary.get("ap_name"):
            if ap_summary.get('ap_name').get(ap_name):
                ap_model = ap_summary.get('ap_name').get(ap_name).get('ap_model')

    except SchemaEmptyParserError as e:
        log.error("Failed to get ap model from 'show ap summary': Error: {e}".format(e=str(e)))
        return ""
    return ap_model


def get_tx_power(device, ap_name):
    """Get configured tx power 
    Args:
        device (obj): Device object
        ap_name (str): access point name 
    Returns:
        tx power (str) if success else empty string
    Raises:
        N/A        
    """
    tx_power = ""
    try:
        radio_summary = device.parse('show ap dot11 5ghz summary')
        if radio_summary.get('ap_name').get(ap_name):
            tx_power = radio_summary.get('ap_name').get(ap_name).get('tx_pwr')

    except SchemaEmptyParserError as e:
        log.error("Failed to get tx power from 'show ap dot11 5ghz summary': Error: {e}".format(e=str(e)))
        return ""
    return tx_power


def get_unused_channel(device):
    """Get configured un used clannel list 
    Args:
        device (obj): Device object
    Returns:
        unused_channel_lst (list) if success else empty string
    Raises:
        N/A        
    """
    unused_channel_lst = ""
    try:
        channel_summary = device.parse('show ap dot11 5ghz channel')
        if channel_summary.get('channel_assignment'):
            unused_channel_lst = channel_summary.get('channel_assignment').get('unused_channel_list')

    except SchemaEmptyParserError as e:
        log.error("Failed to get unused channel list from 'show ap dot11 5ghz channel': Error: {e}".format(e=str(e)))
        return ""
    unused_channel_lst = unused_channel_lst.split(",")
    return unused_channel_lst


def get_assignment_mode(device):
    """Get configured assignment mode 
    Args:
        device (obj): Device object
    Returns:
        assignment_mode (str) if success else empty string
    Raises:
        N/A
    """
    assignment_mode = ""
    try:
        channel_summary = device.parse('show ap dot11 5ghz channel')
        if channel_summary.get('channel_assignment'):
            assignment_mode = channel_summary.get('channel_assignment').get('chan_assn_mode')

    except SchemaEmptyParserError as e:
        log.error("Failed to get assignment mode from 'show ap dot11 5ghz channel': Error: {e}".format(e=str(e)))
        return ""
    return assignment_mode
