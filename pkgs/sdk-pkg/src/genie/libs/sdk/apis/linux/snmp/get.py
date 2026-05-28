# Python
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def get_snmp_snmpwalk(
    device, community, ip_address, oid, version="2c", option=None, timeout=60
):
    """ Get snmpwalk output from SNMP device
        Args:
            device (`obj`): SNMP device
            community (`str`): Community name
            ip_address (`str`): IP address
            oid (`str`): Oid code
            version (`str`, optional): SNMP version. Default is "2c"
            option (`str`): Optional command. Default is None
            timeout (`int`): Optional timeout value. Default is 60 seconds.
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

    return device.execute(cmd, timeout=timeout)

def get_snmpv3_snmpwalk(
    device, user_name, ip_address, oid, auth_password, priv_password,
    auth_protocol='SHA', priv_protocol='AES', security_level='authPriv',
    option=None, timeout=60
):
    """ Get snmpwalk output from SNMP device using SNMPv3 authPriv
    
    SHA auth + AES-128 encryption
        Example command:
            snmpwalk -v 3 -l authPriv -u SNMPV3_USER -a SHA -A AuthPass123 -x AES -X PrivPass123 <mgmt_address> 1.3.6.1.2.1.1.1
        Args:
            device (`obj`): SNMP device
            user_name (`str`): SNMPv3 username
            ip_address (`str`): IP address
            oid (`str`): Oid code
            auth_password (`str`): Authentication password
            priv_password (`str`): Privacy/encryption password
            auth_protocol (`str`): Auth protocol (SHA, default: 'SHA')
            priv_protocol (`str`): Privacy protocol (AES, default: 'AES')
            security_level (`str`): Security level (authPriv, default: 'authPriv')
            option (`str`): Optional command
            timeout (`int`): Optional timeout value. Default is 60 seconds.
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            None
    """
    cmd = (
        f"snmpwalk -v 3 -l {security_level} -u {user_name} "
        f"-a {auth_protocol} -A {auth_password} "
        f"-x {priv_protocol} -X {priv_password} "
        f"{ip_address} {oid}"
    )
    if option:
        cmd = f"{cmd} {option}"

    return device.execute(cmd, timeout=timeout)


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


def get_snmpv3_snmpget(
    device, user_name, ip_address, oid, auth_password, priv_password,
    auth_protocol='SHA', priv_protocol='AES', security_level='authPriv',
    option=None
):
    """ Get snmpget output from SNMP device using SNMPv3 authPriv
        SHA auth + AES-128 encryption
        Example command:
            snmpget -v 3 -l authPriv -u SNMPV3_USER -a SHA -A AuthPass123 -x AES -X PrivPass123 <ip> <oid>

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
            option (`str`): Optional command
        Returns:
            out (`str`): Executed output of SNMP command
        Raises:
            SubCommandFailure
    """
    cmd = (
        f"snmpget -v 3 -l {security_level} -u {user_name} "
        f"-a {auth_protocol} -A {auth_password} "
        f"-x {priv_protocol} -X {priv_password} "
        f"{ip_address} {oid}"
    )
    if option:
        cmd += f" {option}"

    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to get snmpv3 get output from the device. Error:\n{e}") from e


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

def get_snmp_snmpwalk_version3(device, ip_address, oid, version="3", username=None, passprs=None, passphrase=None, var=None, 
        security=None, security_level=None, security_method=None, algorithm=None, private_passphrase=None, option=None):
    """ Get snmpwalk version 3 output from SNMP device
        Args:
            device (`obj`): SNMP device
            ip_address (`str`): IP address
            oid (`str`): Oid code
            username (`str`): username
            passprs ('str'): SNMP passphrase type
            passphrase (`str`): SNMP passphrase
            var ('str'): var type
            security ('str'): security type
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
    cmd = f"snmpwalk -v {version}"
    if username:
        cmd += f" -u {username}"
    if passphrase:
        cmd += f" {passprs} {passphrase}"
    if var:
        if security_level:
            cmd += f" {var} {security_level}"
    if security:
        if security_method:
            cmd += f" {security} {security_method}"

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


def get_snmp_snmpwalk_sysname(device, ip_address, oid, username, passphrase, 
                              security_level,security_method, dir=None, 
                              algorithm=None, private_passphrase=None, 
                              version="3", option=None):
    """ Get snmpwalk version 3 sysname output from SNMP device
        Args:
            device (`obj`): SNMP device
            ip_address (`str`): IP address of hostname specified
            oid (`str`): Oid includes given OID in the search range
            username (`str`): security username 
            passphrase (`str`): authentication protocol pass phrase
            security_level (`str`): set security level 
            dir('str',Optional): change path to given directory path. Defaults to None
            security_method (`str`): authentication protocol to set 
            algorithm (`str`,Optional): privacy protocol .Defaults to None
            private_passphrase (`str`,Optional) : privacy protocol pass phrase. Defaults to None
            version (`str`): specifies SNMP version to use
            option (`str`,Optional): Optional command. Defaults to None
        Returns:
            (`str`): Executed output of SNMP command
        Raises:
            SubCommandFailure
    """

    cmd = f"snmpwalk -v{version} -u {username} -A {passphrase} -l {security_level} -a {security_method}"

    if algorithm:
        cmd += f" -x {algorithm}"
    if private_passphrase:
        cmd += f" -X {private_passphrase}"

    cmd += f" {ip_address} {oid}"
    if option:
        cmd += f" {option}"

    if dir:
        f"cd {dir}"
    
    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to get snmp walk output from the device. Error:\n{e}")
