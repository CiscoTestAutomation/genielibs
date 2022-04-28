"""Common configure functions for fips"""

# Python
import logging

from unicon.eal.dialogs import Statement, Dialog    

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_fips_authorization_key(device, value):
    """ Config fips authorization-key
    Args:
        device('obj'): Device object
        value('str'): fips authorization-key value
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring  
    """

    dialog = Dialog ([
        Statement(
            pattern = r"A valid FIPS key is installed, do you want to overwrite\? \? \(yes/\[no\]\):",
            action = "sendline(yes)",
            args = None,
            loop_continue = True,
            continue_timer = False),
    ])

    try:
        device.configure(
            "fips authorization-key {value}".format(value=value), reply=dialog
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            'unable to configure fips authorization-key'
        )            

def unconfigure_fips_authorization_key(device):
    """ UnConfigure fips authorization-key
    Args:
        device('obj'): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfiguring  
    """
    try:
        device.configure([
            "no fips authorization-key"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"unable to unconfigure fips authorization-key \n{e}"
        )   
