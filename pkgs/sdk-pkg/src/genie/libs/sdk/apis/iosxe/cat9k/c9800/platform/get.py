# Python
import logging
import re

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Logger
log = logging.getLogger(__name__)


_RADIO_MAC_RE = re.compile(r"^[0-9a-f]{12}$")


def normalize_ap_radio_mac(value):
    """Normalize a dotted, colon-separated, or hyphen-separated radio MAC.

    Args:
        value (str): AP radio MAC in a supported textual format.

    Returns:
        str: Normalized dotted lowercase radio MAC.

    Raises:
        ValueError: If ``value`` is not a valid radio MAC.
    """
    compact = re.sub(r"[.:-]", "", str(value or "").strip()).lower()
    if not _RADIO_MAC_RE.fullmatch(compact):
        raise ValueError("Invalid AP radio MAC: {!r}".format(value))
    return "{}.{}.{}".format(compact[0:4], compact[4:8], compact[8:12])


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


def get_ap_registration_evidence(device, radio_mac=None, ap_name=None):
    """Collect structured WLC evidence for one AP.

    Args:
        device (obj): C9800 WLC device.
        radio_mac (str, optional): AP radio MAC used as the stable identity.
        ap_name (str, optional): Expected AP name used as a fallback and
            consistency check.

    Returns:
        dict or None: Evidence containing AP name, radio MAC, state, join
            status, uptime presence, and a ``pending`` or ``confirmed``
            status. Returns ``None`` when the AP cannot be matched or the
            summary parser returns no data.

    Raises:
        ValueError: If ``radio_mac`` is not a valid MAC address.
    """
    expected_radio_mac = (
        normalize_ap_radio_mac(radio_mac) if radio_mac else None)
    try:
        ap_summary = device.parse('show ap summary')
    except SchemaEmptyParserError:
        return None
    ap_entries = ap_summary.get('ap_name', {}) or {}
    matched = None

    for summary_name, summary in ap_entries.items():
        summary_radio_mac = summary.get('radio_mac')
        if not summary_radio_mac:
            continue
        if (expected_radio_mac and summary_radio_mac and normalize_ap_radio_mac(
                summary_radio_mac) == expected_radio_mac):
            matched = (summary_name, summary)
            break
        if not expected_radio_mac and ap_name == summary_name:
            matched = (summary_name, summary)
            break

    if matched is None:
        return None

    actual_name, summary = matched
    learned_radio_mac = summary.get('radio_mac')
    if not learned_radio_mac:
        return None
    learned_radio_mac = normalize_ap_radio_mac(learned_radio_mac)
    evidence = {
        'ap_name': actual_name,
        'radio_mac': learned_radio_mac,
        'state': summary.get('state'),
        'ap_ip_address': summary.get('ap_ip_address'),
    }
    if ap_name and actual_name != ap_name:
        # AP names may be assigned or changed during onboarding.  Keep the
        # discrepancy as evidence, but let the radio MAC remain authoritative.
        evidence['name_mismatch'] = True

    try:
        join_summary = device.parse('show wireless stats ap join summary')
    except SchemaEmptyParserError:
        join_summary = {}
    join_entries = join_summary.get('base_mac', {}) or {}
    join_entry = None
    for join_radio_mac, entry in join_entries.items():
        if (entry.get('ap_name') == actual_name or
                (expected_radio_mac and
                 normalize_ap_radio_mac(join_radio_mac) == expected_radio_mac)):
            join_entry = entry
            break
    if join_entry is not None:
        evidence['join_status'] = join_entry.get('status')
        evidence['failure_phase'] = join_entry.get('failure_phase')
        evidence['disconnect_reason'] = join_entry.get('disconnect_reason')

    uptime_output = device.execute('show ap uptime')
    uptime_text = re.sub(r'[.:-]', '', str(uptime_output or '')).lower()
    uptime_present = learned_radio_mac.replace('.', '') in uptime_text
    evidence['uptime_present'] = uptime_present

    state_registered = str(summary.get('state', '')).lower() == 'registered'
    join_confirmed = (
        join_entry is not None and
        str(join_entry.get('status', '')).lower() == 'joined'
    )
    # Require independent WLC summary, join, and uptime evidence so a stale
    # single-source record cannot confirm registration.
    evidence['status'] = (
        'confirmed' if state_registered and join_confirmed and uptime_present
        else 'pending')
    return evidence


def get_ap_registration_diagnostics(device, radio_mac=None):
    """Collect bounded raw registration diagnostics for an unresolved AP.

    Args:
        device (obj): WLC device.
        radio_mac (str, optional): Learned AP radio MAC.

    Returns:
        dict: Bounded join and uptime diagnostics.

    Raises:
        ValueError: If ``radio_mac`` is provided in an invalid format.
    """
    normalized = normalize_ap_radio_mac(radio_mac) if radio_mac else None

    def bounded(value):
        value = str(value or '')
        value = re.sub(
            r'(?im)(password|secret|token)\s*[:=]\s*\S+',
            r'\1: <redacted>',
            value,
        )
        return value[-8192:]

    return {
        'join_detailed': bounded(device.execute(
            'show wireless stats ap mac {} join detailed'.format(normalized)
            if normalized else 'show wireless stats ap join summary')),
        'uptime': bounded(device.execute('show ap uptime')),
    }


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
