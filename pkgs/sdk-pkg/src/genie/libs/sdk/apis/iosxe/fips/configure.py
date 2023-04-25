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

def configure_crypto_isakmp_policy(device,priority,encrtype,hashtype,authtype,diffietype,ltime):
    """ configure crypto isakmp policy
    Args:
        device('obj'): Device object
        priority('str'): Priority of protection suite
        encrtype('str'):  encryption Set hash algorithm for protection suite
        hashtype('str'): Set hash algorithm for protection suite
        authtype('str'): Set authentication method for protection suite
        diffietype('str'): Set the Diffie-Hellman group
        ltime('str'): Set lifetime value for ISAKMP security association
    Return:
        None
    Raise:
        SubCommandFailure: configure crypto isakmp policy
    """
    cmd = [
            f"crypto isakmp policy {priority}",
            f"encryption {encrtype}",
            f"hash {hashtype}",
            f"authentication {authtype}",
            f"group {diffietype}",
            f"lifetime {ltime}"
        ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"unable to configure crypto isakmp policy. Error:\n{e}"
        )   

def configure_crypto_map_entry(device,ctag,sentry,peerip=None,ptag=None,ike=None,ipacl=None,ipsec=None):
    """  configure crypto map entry
    Args:
        device('obj'): Device object
        ctag('str'): Crypto map tag
        sentry('str'):  Sequence to insert into crypto map entry
        ipsec('str',optional): IPSEC w/ISAKMP/ IPSEC w/manual keying
        peer('str',optional): IP/IPv6 address of peer or Hostanme of peer 
        ike('str',optional):  Name the ikev2 profile.
        ipacl('str',optional): IP access-list number or extended or ACL name
    Return:
        None
    Raise:
        SubCommandFailure: configure crypto map entry
    """
    cmd=[f"crypto map {ctag} {sentry} {ipsec}"]
    if peerip:
        cmd.append(f"set peer {peerip}")
    if ptag:
        cmd.append(f"set transform-set {ptag}")
    if ike:
        cmd.append(f"set ikev2-profile {ike}")
    if ipacl:
        cmd.append(f"match address {ipacl}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Unable to configure crypto map entry. Error:\n{e}"
        )