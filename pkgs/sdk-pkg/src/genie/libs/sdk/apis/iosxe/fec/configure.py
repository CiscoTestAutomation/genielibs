"""Common configure functions for fec"""

# Python
import logging
# Unicon
from unicon.core.errors import SubCommandFailure
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def configure_fec_on_interface(device, interface, fec_type):
    '''
    configure fec on interface
    Args: 
        device ('obj'):  device to use
        interface('str'): interface to configure
        fec_type : Enable fec type with avilable options on device like Auto/clause_value/Off
    Returns:
        None
    '''
    try:
        device.configure([
            f"interface {interface}",
            f"fec {fec_type}"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
        "Could not configure fec on interface. Error:\n{error}".format(
        error=e
        )
        )
    
def unconfigure_fec_on_interface(device, interface):
    '''
    Unconfigure fec on interace
    Args:
        device ('obj'):  device to use
        interface('str'): interface to configure
    Returns:
        None
    '''
    try:
        device.configure([
            f"interface {interface}",
            f"no fec"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
        "Could not unconfigure fec on interface. Error:\n{error}".format(
        error=e
        )
        )