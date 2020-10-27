"""Common get info functions for LDP"""

# Python
import re
import logging
import datetime


# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError



log = logging.getLogger(__name__)


def get_ldp_database_session(
    device,
    interface=None,
    expected_interface=None,
    label_type='input',
    local_label=None,
):
    """Verifies ldp session exists

    Args:
        device (obj): device object
        interface (str): Interface to use in show command
        expected_interface (str): Expected interface
        label_type (str): Database label. Defaults to input
        local_label (str): Database local label. Defaults to None

    Returns:
        ldp_label ('str'): Will return one value
    """

    if label_type.lower() == 'input':
        label_type = 0
    elif label_type.lower() == 'output':
        label_type = 1

    out = None
    try:
        out = device.parse(
            "show ldp database session {interface}".format(interface=interface))
    except SchemaEmptyParserError:
        return

    ldp_database = Dq(out).get_values('ldp-database', label_type)
    if ldp_database:
        
        for ldp in ldp_database.get('ldp-binding', []):
            if ldp.get('ldp-prefix').split('/')[0] != expected_interface:
                return
            return(ldp.get('ldp-label'))


    return None


def get_ldp_database_session_label(device, address, expected_ldp_prefix,
    expected_ldp_database_type='Input label database'):
    """ Gets ldp prefix

    Args:
        device (obj): Device object
        address (str): IP address
        expected_ldp_prefix (str): Expected LDP prefix value
        expected_ldp_database_type (str): Expected LDP database type. Default is 'Input label database'
    
    Returns:
        (str): database session label
    """
    # Dictionary
    #  "ldp-database-information": {
    #         "ldp-database": [
    #             {
    #                 "ldp-binding": [
    #                     {
    #                         "ldp-label": "3",
    #                         "ldp-prefix": "10.34.2.250/32"
    try:
        out = device.parse('show ldp database session {address}'.format(
            address=address
        ))
    except SchemaEmptyParserError:
        return None

    for database in out.q.get_values('ldp-database'):
        ldp_database_type = database.get('ldp-database-type')
        if ldp_database_type != expected_ldp_database_type:
            continue
        for binding in database.get('ldp-binding', []):
            ldp_label = binding.get('ldp-label')
            ldp_prefix = binding.get('ldp-prefix')
            if ldp_prefix.startswith(expected_ldp_prefix):
                return ldp_label
    
    return None

def get_ldp_session_state_count(device, expected_session_state='Operational', max_time=60, check_interval=10):
    """ Get show ldp session count

    Args:
        device (obj): Device object
        expected_session_state (str): Expected session state. Defaults to 'Operational'.
        max_time (int, optional): Maximum timeout time. Defaults to 60 seconds.
        check_interval (int, optional): Check interval. Defaults to 10 seconds.
    """
    try:
        out = device.parse('show ldp session')
    except SchemaEmptyParserError:
        return None

    state_count = out.q.contains_key_value('ldp-session-state', 
        expected_session_state).count()

    return state_count