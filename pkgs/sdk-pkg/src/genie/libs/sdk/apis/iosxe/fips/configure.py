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

def configure_crypto_map_entry(device,ctag,sentry,peerip=None,ptag=None,ike=None,ipacl=None,ipsec=None,pfs=None):
    """  configure crypto map entry
    Args:
        device('obj'): Device object
        ctag('str'): Crypto map tag
        sentry('str'):  Sequence to insert into crypto map entry
        peerip('str',optional): IP/IPv6 address of peer or Hostname of peer 
        ptag('str',optional): Transform set tag name
        ike('str',optional):  Name the ikev2 profile
        ipacl('str',optional): IP access-list number or extended or ACL name
        ipsec('str',optional): IPSEC w/ISAKMP/ IPSEC w/manual keying
        pfs('str',optional): Perfect Forward Secrecy group
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
    if pfs:
        cmd.append(f"set pfs {pfs}")
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
    
def unconfigure_crypto_map_xauthmap(device):
    """ Unconfigure crypto map xauthmap
    Args:
        device('obj'): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfiguring  
    """
    try:
        device.configure([
            "no crypto map xauthmap"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"unable to unconfigure crypto map xauthmap \n{e}"
        )  
    
def unconfigure_crypto_map_entry(device,ctag,sentry):
    """ Unconfigure crypto map entry
    Args:
        device('obj'): Device object
        ctag('str'): Crypto map tag
        sentry('str'):  Sequence to insert into crypto map entry
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfiguring  
    """
    try:
        device.configure([
            f"no crypto map {ctag} {sentry}"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"unable to unconfigure crypto map entry \n{e}"
        )

def unconfigure_crypto_map(device, ctag, dtag=None, dynamic=False, ipv6=False):
    """
    Unconfigure crypto map for both IPv4 and IPv6 with dynamic support for IPv4 only.
    Args:
        device (obj): Device connection object (pyATS/unicon object) used to send commands.
        ctag (str): Crypto map tag/name to unconfigure.
        dtag (str, optional): Dynamic crypto map tag/name to unconfigure (IPv4 only).
        dynamic (bool, optional): Whether to unconfigure dynamic crypto map (IPv4 only). Defaults to False.
        ipv6 (bool, optional): Whether to unconfigure IPv6 crypto map. Defaults to False (IPv4).
    Returns:
        None
    Raises:
        ValueError: If required parameters are missing or invalid combinations.
        SubCommandFailure: If unable to unconfigure the crypto map.
    """
    if dynamic and not dtag:
        raise ValueError("dtag parameter is required when dynamic=True")
    if dynamic and ipv6:
        raise ValueError("Dynamic crypto maps are not supported for IPv6")
    cmd = []
    try:
        if dynamic and not ipv6:
            cmd.append(f"no crypto map {ctag}")
            cmd.append(f"no crypto dynamic-map {dtag}")        
        elif not dynamic and ipv6:
            cmd.append(f"no crypto map ipv6 {ctag}")
        else:
            cmd.append(f"no crypto map {ctag}")
        device.configure(cmd)
    except SubCommandFailure as e:
        map_type = "IPv6" if ipv6 else "IPv4"
        dynamic_type = "dynamic" if dynamic else "static"
        raise SubCommandFailure(
            f"Unable to unconfigure {map_type} {dynamic_type} crypto map {ctag}. Error:\n{e}"
        )



def configure_dynamic_cmap(
                            device, 
                            ctag, 
                            ptag, 
                            dtag, 
                            sentry, 
                            ike=None, 
                            sa_life_days=None, 
                            sa_life_kb_disable=False, 
                            sa_life_kbytes=None, 
                            sa_life_sec=None, 
                            ipacl=None, 
                            pfs=None
                        ):  
    """
    Configure dynamic crypto map with Perfect Forward Secrecy support.
    Args:
        device (obj): Device connection object (pyATS/unicon object) used to send commands.
        ctag (str): Crypto map tag/name.
        ptag (str): Transform set name for encryption/authentication.
        dtag (str): Dynamic crypto map tag/name.
        sentry (str): Sequence number to insert into crypto map entry.
        ike (str, optional): IKEv2 profile name.
        sa_life_days (int, optional): Security association duration in days.
        sa_life_kb_disable (bool, optional): Disable Volume-based Rekey.
        sa_life_kbytes (int, optional): Security association duration in kilobytes.
        sa_life_sec (int, optional): Security association duration in seconds.
        ipacl (str, optional): IP access-list number, extended ACL, or ACL name.
        pfs (str, optional): Perfect Forward Secrecy group (e.g., 'group2', 'group5', 'group14').
    Returns:
        None
    Raises:
        ValueError: If required parameters are missing.
        SubCommandFailure: If unable to configure the dynamic crypto map.
    """
    cmd = []
    cmd.append(f"crypto dynamic-map {dtag} {sentry}")
    cmd.append(f"set transform-set {ptag}")
    if ike:
        cmd.append(f"set ikev2-profile {ike}")
    if pfs:
        cmd.append(f"set pfs {pfs}")
    if ipacl:
        cmd.append(f"match address {ipacl}")
    if sa_life_days is not None:
        cmd.append(f"set security-association lifetime days {sa_life_days}")
    if sa_life_kbytes is not None:
        cmd.append(f"set security-association lifetime kilobytes {sa_life_kbytes}")
    if sa_life_kb_disable:
        cmd.append("set security-association lifetime kilobytes disable")
    if sa_life_sec is not None:
        cmd.append(f"set security-association lifetime seconds {sa_life_sec}")
    cmd.append(f"crypto map {ctag} {sentry} ipsec-isakmp dynamic {dtag}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Unable to configure dynamic crypto map. Error:\n{e}"
        )