"""Common configure functions for snmp"""

import logging
from unicon.core.errors import SubCommandFailure
from pyats.aetest.steps import Steps
from genie.conf.base import Interface

log = logging.getLogger(__name__)


def set_snmp_snmpset(
    device, community, ip_address, oid, version="2c", string= None, option=None
):
    """ Snmpset command
        Args:
            device (`obj`): SNMP device
            community (`str`): Community name
            ip_address (`str`): IP address
            oid (`str`): Oid code
            version (`str`): SNMP version
            string (`str`): string command
            option (`str`): Optional command
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            SubCommandFailure
    """
    cmd = f"snmpset -v {version} -c {community} {ip_address} {oid}"
    if string:
        cmd += f" s {string}"
    if option:
        cmd += f" {option}"
    try:

        return device.execute(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure snmp set on the device. Error:\n{e}")


def set_snmpv3_snmpset(
    device, user_name, ip_address, oid, auth_password, priv_password,
    auth_protocol='SHA', priv_protocol='AES', security_level='authPriv',
    string=None, option=None
):
    """ SNMPv3 snmpset command with authPriv security

        Example command:
            snmpset -v 3 -l authPriv -u SNMPV3_USER -a SHA -A AuthPass123 -x AES -X PrivPass123 <ip> <oid>
            snmpset -v 3 -l authPriv -u SNMPV3_USER -a SHA -A AuthPass123 -x AES -X PrivPass123 <mgmt_address> 1.3.6.1.2.1.1.4.0 s admin@cisco.com
            
            Setting an integer value via option
            set_snmp_snmpset(..., oid='1.3.6.1.2.1.1.4.0', string=None, option='i 2')
             → snmpset ... 1.3.6.1.2.1.1.4.0 i 2   (sets integer value 2)

            Setting an IP address via option  
            set_snmp_snmpset(..., oid='...', string=None, option='a 192.168.1.1')
             → snmpset ... <oid> a 192.168.1.1   (sets IP address)

        Args:
            device (`obj`): SNMP device
            user_name (`str`): SNMPv3 username
            ip_address (`str`): IP address
            oid (`str`): Oid code
            auth_password (`str`): Authentication password
            priv_password (`str`): Privacy/encryption password
            auth_protocol (`str`): Auth protocol (default: 'SHA')
            priv_protocol (`str`): Privacy protocol (default: 'AES')
            security_level (`str`): Security level (default: 'authPriv')
            string (`str`): string command
            option (`str`): Optional command
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            SubCommandFailure
    """
    cmd = (
        f"snmpset -v 3 -l {security_level} -u {user_name} "
        f"-a {auth_protocol} -A {auth_password} "
        f"-x {priv_protocol} -X {priv_password} "
        f"{ip_address} {oid}"
    )
    if string:
        cmd += f" s {string}"
    if option:
        cmd += f" {option}"
    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure snmpv3 set on the device. Error:\n{e}") from e
