# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def get_snmp_snmpwalk(
    device, community, ip_address, oid, version="2c", option=None
):
    """ Get snmpwalk output from SNMP device
        Args:
            device (`obj`): SNMP device
            community (`str`): Community name
            ip_address (`str`): IP address
            oid (`str`): Oid code
            version (`str`, optional): SNMP version. Default is "2c"
            option (`str`): Optional command. Default is None
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            None
    """
    if option:
        cmd = "snmpwalk -v {version} -c {community} {ip_address} {oid} {option}".format(
            version=version,
            community=community,
            ip_address=ip_address,
            oid=oid,
            option=option,
        )
    else:
        cmd = "snmpwalk -v {version} -c {community} {ip_address} {oid}".format(
            version=version,
            community=community,
            ip_address=ip_address,
            oid=oid,
        )

    return device.execute(cmd)


def get_snmp_snmpget(device, community, ip_address, oid, version="2c", option=None):
    """ Get snmpget output from SNMP device

        Args:
            device (`obj`): SNMP device
            community (`str`): Community name
            ip_address (`str`): IP address
            oid (`str`): Oid code
            version (`str`): SNMP version
            option (`str`): Optional command
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            SubCommandFailure
    """
    cmd = f"snmpget -v {version} -c {community} {ip_address} {oid}"
    if option:
        cmd += f" {option}"

    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to get snmp get output from the device. Error:\n{e}")


def get_snmp_snmpgetnext(device, community, ip_address, oid, version="2c", option=None):
    """ Get snmpgetnext output from SNMP device

        Args:
            device (`obj`): SNMP device
            community (`str`): Community name
            ip_address (`str`): IP address
            oid (`str`): Oid code
            version (`str`): SNMP version
            option (`str`): Optional command
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            SubCommandFailure
    """
    cmd = f"snmpgetnext -v {version} -c {community} {ip_address} {oid}"
    if option:
        cmd += f" {option}"

    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to get snmp getnext output from the device. Error:\n{e}")


def get_snmp_snmpwalk_v3(device, ip_address, oid, username, passphrase, security_level,
security_method, algorithm=None, private_passphrase=None, version="3", option=None):
    """ Get snmpwalk version 3 output from SNMP device

        Args:
            device (`obj`): SNMP device
            ip_address (`str`): IP address
            oid (`str`): Oid code
            username (`str`): username
            passphrase (`str`): SNMP passphrase
            security_level (`str`): security level
            security_method (`str`): security method
            algorithm (`str`): algorithm
            private_passphrase (`str`) : private passphrase
            version (`str`): SNMP version
            option (`str`): Optional command
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            SubCommandFailure
    """
    cmd = f"snmpget -v {version} -u {username} -A {passphrase} -l {security_level} -a {security_method}"
    if algorithm:
        cmd += f" -x {algorithm}"
    if private_passphrase:
        cmd += f" -X {private_passphrase}"
    
    cmd += f" {ip_address} {oid}"
    if option:
        cmd += f" {option}"

    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to get snmp walk output from the device. Error:\n{e}")
