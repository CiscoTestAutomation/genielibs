"""Common get info functions for span"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.metaparser.util.exceptions import InvalidCommandError

log = logging.getLogger(__name__)


def get_span_session_info(device, session_id):
    """ Get span session info from device

        Args:
            device ('obj'): Device object
            session_id ('str'): ID of span session
        Returns:
            Dict with span session info, or None on failure.
    """
    try:
        return device.parse(f'show monitor session {session_id}')
    except (SchemaEmptyParserError, InvalidCommandError) as e:
        log.debug(
            f"Could not get device span session {session_id}: {e}")
        return None


def get_span_session_running_config(device):
    """ Get span session info from show running-config

        Args:
            device ('obj'): Device object
        Returns:
            List of span session cfg info dicts.

            Format example:
                [
                    {
                        'id': '1',
                        'role': 'source',
                        'intf': 'Gi0/1/4',
                        'direction': 'rx'
                    },
                    {
                        'id': '1',
                        'role': 'destination',
                        'intf': 'Gi0/1/5',
                        'direction': None
                    }
                ]
    """
    res = device.api.get_running_config_section('monitor')
    # monitor session 1 source interface Gi0/1/0
    pattern = re.compile(r"""
        ^\s*monitor\s+session\s+
        (?P<id>\d+)\s+
        (?P<role>\w+)\s+
        interface\s+
        (?P<intf>\S+)
        (?:\s+(?P<direction>\w+))?
    """, re.VERBOSE)

    session_cfg_dict_list = []
    if res:
        for line in res:
            # monitor session 1 source interface Gi0/1/0
            m = pattern.match(line)
            if m:
                cfg = m.groupdict()
                if (cfg.get('direction') is None
                        and cfg.get('role') == 'source'):
                    cfg['direction'] = 'both'
                session_cfg_dict_list.append(cfg)
    return session_cfg_dict_list
