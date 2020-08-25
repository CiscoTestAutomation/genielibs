"""Common get info functions for MPLS"""

# Python
import re
import logging
import copy
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

# unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def get_mpls_out_label(device, name, session_type="Transit"):
    """ Get out label information from mpls

    Args:
        device (obj): device object
        name (str): lsp name
        session_type (str): Which session to look into. Defaults to "Transit"

    Returns:
        str or None: mpls out label
    """

    try:
        out = device.parse("show mpls lsp name {name} detail".format(name=name))
    except SchemaEmptyParserError:
        return None
    
    for session in out.q.get_values('rsvp-session-data'):
        if session.get('session-type') == session_type:
            session_data = session.get('rsvp-session')
            return session_data.get('label-out')
    
    return None

def get_mpls_record_routes(device, name, purge_self=True):
    """ Get mpls record routes

    Args:
        device (obj): device object
        name (str): mpls name to check
        purge_self (bool, optional): Purge <self> from record routes? Defaults to True.
        
    Returns:
        str or None: mpls out label
    """

    try:
        out = device.parse('show mpls lsp name {name} detail'.format(
            name=name
        ))
    except SchemaEmptyParserError:
        return None

    routes_ = out.q.get_values('record-route-element') or None
    if not routes_:
        return None

    if purge_self:
        routes_ = [r['address'] for r in routes_ if r['address'] != '<self>']
    else:
        routes_ = [r['address'] for r in routes_]

    return routes_