"""Common configure functions for snmp"""

import logging
import re
from unicon.core.errors import SubCommandFailure
from pyats.aetest.steps import Steps
from genie.conf.base import Interface

log = logging.getLogger(__name__)

def configure_snmp(device,community_string, access_type):
    """ Configures the snmp on device
        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
            access_type ('str') : type of Access
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring snmp on device {device}".format(device=device))

    try:
        device.configure("snmp-server community {community_string} {access_type}".format(
            community_string=community_string,access_type=access_type))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure snmp. Error:\n{error}".format(error=e))

def unconfigure_snmp(device,community_string):
    """ Unconfigures the snmp on device
        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring snmp on device {device}".format(device=device))

    try:
        device.configure("no snmp-server community {community_string}".format(community_string=community_string))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not unconfigure snmp. Error:\n{error}".format(error=e))

def configure_snmpv3_user(device, group_name, user_name, auth_password, priv_password,
                          auth_protocol='sha', priv_protocol='aes 128', access_type='priv',
                          acl_name=None):
    """
    snmp-server community is insecure and should not be used. SNMPv3 with authPriv security is recommended instead.
    Configures SNMPv3 group and user with authPriv security.

    Without an ACL, IOS-XE raises:
        INSECURE DYNAMIC WARNING - Module: SNMP,
        Reason: SNMP User without ACL,
        Remediation: Use SNMP User with AccessList

    To suppress this warning, pass acl_name (a standard ACL name/number that
    must already exist on the device).

        Example:
            snmp-server group SNMPV3_GROUP v3 priv
            snmp-server user SNMPV3_USER SNMPV3_GROUP v3 auth sha <auth_pass> priv aes 128 <priv_pass> access SNMP_ACL

        Args:
            device ('obj'): device to use
            group_name ('str'): SNMPv3 group name
            user_name ('str'): SNMPv3 user name
            auth_password ('str'): authentication password
            priv_password ('str'): privacy/encryption password
            auth_protocol ('str', optional): auth protocol (sha, default: 'sha')
            priv_protocol ('str', optional): privacy protocol (aes 128, default: 'aes 128')
            access_type ('str', optional): group access level (priv, default: 'priv')
            acl_name ('str', optional): Standard ACL name/number to restrict SNMP access.
                RECOMMENDED to avoid INSECURE DYNAMIC WARNING. Default: None.

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring SNMPv3 on device {device.name}")

    user_cmd = (f"snmp-server user {user_name} {group_name} v3 "
                f"auth {auth_protocol} {auth_password} "
                f"priv {priv_protocol} {priv_password}")
    if acl_name is not None:
        user_cmd += f" access {acl_name}"
    else:
        log.error(
            "INSECURE DYNAMIC WARNING - Module: SNMP, "
            "Command: snmp-server user %s %s v3 auth %s * priv %s *, "
            "Reason: SNMP User without ACL, "
            "Remediation: Use SNMP User with AccessList, "
            "Submode: configure, "
            "Parent CLI: Not Applicable",
            user_name, group_name, auth_protocol, priv_protocol
        )

    config = [
        f"snmp-server group {group_name} v3 {access_type}",
        user_cmd
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure SNMPv3. Error:\n{e}") from e

def unconfigure_snmpv3_user(device, group_name, user_name, access_type='priv'):
    """ Unconfigures the SNMPv3 group and user on device
        Args:
            device ('obj'): device to use
            group_name ('str'): SNMPv3 group name
            user_name ('str'): SNMPv3 user name
            access_type ('str', optional): group access level (priv, default: 'priv')
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring SNMPv3 on device {device.name}")

    config = [
        f"no snmp-server user {user_name} {group_name} v3",
        f"no snmp-server group {group_name} v3 {access_type}"
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfigure SNMPv3. Error:\n{e}") from e

def configure_snmp_server_view(device, mib_view, family_name, state = 'excluded'):
    """ Configures the snmp server view on device
        Args:
            device ('obj'): device to use
            mib_view ('str'): Name of the view
            family_name ('str'): MIB view family name
            state ('str'): mib family excluded|included
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring snmpserver view on device {device}")

    try:
        device.configure(f"snmp-server view {mib_view} {family_name} {state}")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure snmp server view. Error:\n{str(error)}"
        )

def unconfigure_snmp_server_view(device, mib_view, family_name, state = 'excluded'):
    """ Unconfigures the snmp server view on device
        Args:
            device ('obj'): device to use
            mib_view ('str'): Name of the view
            family_name ('str'): MIB view family name
            state ('str'): mib family excluded|included
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring snmp server view on device {device}")

    try:
        device.configure(f"no snmp-server view {mib_view} {family_name} {state}")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure snmp server view. Error:\n{str(error)}"
        )

def configure_snmp_server_group(device,
                                group_name,
                                version,
                                auth_type,
                                mode = None,
                                acl_name = None,
                                view_name = None,
                                acl_type = None,
                                context_name = None,
                                match_type = None,
                                notify_name = None):
    """ Configures the snmp server group on device
        Args:
            device ('obj'): device to use
            group_name ('str'): name of the group
            version ('str'): v1,v2c,v3
            auth_type ('str'): auth, noauth, priv
            mode ('str'): write or read mode
            acl_name ('str'): name of the Standerd acl, acl list name, ipv6 named acl
            acl_type ('str'): specify IPv6 Named Access-List
            context_name ('str'): context name
            match_type ('str'): exact or prefix
            notify_name ('str'): notify view name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cli = f"snmp-server group {group_name} {version}"

    if auth_type is not None:
        cli = cli+' '+auth_type
    if match_type is not None:
        cli = cli+' match '+match_type
    if mode is not None and (mode == 'write'):
        cli = cli+' write '+view_name
    if mode is not None and (mode == 'read'):
        cli = cli+' read '+view_name
    if notify_name is not None:
        cli = cli+' notify '+notify_name
    if acl_name is not None:
        if acl_type is not None:
            cli = cli+' access ipv6 '+acl_name+' '+acl_name
        else:
            cli = cli+' access '+acl_name
    if context_name is not None:
        cli = cli+' context '+context_name

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure snmp server group. Error:\n{str(error)}"
        )

def unconfigure_snmp_server_group(device,
                                group_name,
                                version='v3',
                                auth_type='priv',
                                mode = None,
                                acl_name = None,
                                view_name = None,
                                acl_type = None,
                                context_name = None,
                                match_type = None,
                                notify_name = None):
    """ Unconfigures the snmp server group on device
    Example:
        unconfigure_snmp_server_group(
            device=device,
            group_name='snmpgroup1'
        )
        --> no snmp-server group snmpgroup1 v3 priv

        unconfigure_snmp_server_group(
            device=device,
            group_name='snmpgroup1',
            version='v3',
            auth_type='priv',
            mode='read',
            view_name='myview',
            acl_name='SNMP-ACL'
        )
        --> no snmp-server group snmpgroup1 v3 priv read myview access SNMP-ACL

        Args:
            device ('obj'): device to use
            group_name ('str'): name of the group
            version ('str'): v3 (v1 and v2c are insecure and not recommended)
            auth_type ('str'): priv (noauth is insecure and not recommended)
            mode ('str'): write or read mode
            acl_name ('str'): name of the Standard acl, acl list name, ipv6 named acl
            view_name ('str'): view name for read/write mode
            acl_type ('str'): specify IPv6 Named Access-List
            context_name ('str'): context name
            match_type ('str'): exact or prefix
            notify_name ('str'): notify view name
        Returns:
            None
        Raises:
            ValueError: If input parameters contain invalid characters
            SubCommandFailure
    """
    # Input validation - prevent command injection via newlines or special chars
    safe_pattern = re.compile(r'^[\w\-\.]+$')

    for param_name, param_value in [('group_name', group_name),
                                     ('version', version)]:
        if not safe_pattern.match(param_value):
            raise ValueError(f"Invalid characters in {param_name}: must be alphanumeric, hyphen, underscore, or dot")

    if auth_type is not None and auth_type != '' and not safe_pattern.match(auth_type):
        raise ValueError("Invalid characters in auth_type")
    if acl_name is not None and not safe_pattern.match(acl_name):
        raise ValueError("Invalid characters in acl_name")
    if view_name is not None and not safe_pattern.match(view_name):
        raise ValueError("Invalid characters in view_name")
    if context_name is not None and not safe_pattern.match(context_name):
        raise ValueError("Invalid characters in context_name")
    if notify_name is not None and not safe_pattern.match(notify_name):
        raise ValueError("Invalid characters in notify_name")
    if match_type is not None and match_type not in ('exact', 'prefix'):
        raise ValueError("match_type must be 'exact' or 'prefix'")

    # Warn about insecure SNMP versions
    if version in ('v1', 'v2c'):
        log.warning("SNMPv1/v2c is insecure. Use v3 with auth and priv per Cisco hardening guidelines.")

    # Warn about weak auth types
    if auth_type is not None and auth_type.lower() == 'noauth':
        log.warning("noauth provides no authentication. Use 'priv' or 'auth' per Cisco hardening guidelines.")

    cli = f"no snmp-server group {group_name} {version}"

    if auth_type is not None:
        cli = cli+' '+auth_type
    if match_type is not None:
        cli = cli+' match '+match_type
    if mode is not None and (mode == 'write'):
        cli = cli+' write '+view_name
    if mode is not None and (mode == 'read'):
        cli = cli+' read '+view_name
    if notify_name is not None:
        cli = cli+' notify '+notify_name
    if acl_name is not None:
        if acl_type is not None:
            cli = cli+' access ipv6 '+acl_name+' '+acl_name
        else:
            cli = cli+' access '+acl_name
    if context_name is not None:
        cli = cli+' context '+context_name

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure snmp server group. Error:\n{str(error)}"
        )

def configure_snmp_server_trap(device, intf=None, host_name=None, trap_type=None, version='v3',
                               user_name=None, config_type=None, engine_id=None):
    """ Configures the snmp traps or informs on device
    
    Example:
        configure_snmp_server_trap(
            device=device,
            intf='GigabitEthernet0/0',
            host_name='10.1.1.1',
            trap_type='traps',
            version='v3',
            user_name='snmpuser1',
            config_type='config'
        )
        
        snmp-server trap-source GigabitEthernet0/0
        snmp-server enable traps
        snmp-server host 10.1.1.1 traps version v3 priv snmpuser1 config
        
        snmp-server engineID remote 10.1.1.1 <engine_id>
        
        snmp-server enable traps traps
        
        snmp-server enable traps


        Args:
            device ('obj'): device to use
            intf ('str',optional): trap source interface
            host_name ('str',optional): hostname/ip address of snmp-server
            trap_type ('str',optional): traps or informs
            version ('str',optional): v3 recommended (v1 and v2c are insecure)
            user_name ('str',optional): Name of the user
            config_type ('str',optional): snmp trap type i.e config,link up down
            engine_id ('str',optional): remote engine id
        Returns:
            None
        Raises:
            ValueError: If input parameters contain invalid characters
            SubCommandFailure
    """
    # Input validation - prevent command injection via newlines or special
    # chars. trap_type is validated separately below because it is
    # dual-purpose:
    #   - With the host form it is the literal 'traps'/'informs' token.
    #   - Used alone it is the 'snmp-server enable traps <category>' name,
    #     which can legitimately contain spaces (e.g. 'snmp linkdown').
    safe_pattern = re.compile(r'^[\w\-\.:\/]+$')
    # Category names may contain spaces but must not contain newlines or
    # shell/CLI metacharacters. fullmatch rejects a trailing newline that
    # '$' would otherwise allow.
    category_pattern = re.compile(r'[\w\-\.:\/ ]+')

    for param_name, param_value in [
            ('intf', intf), ('host_name', host_name),
            ('version', version), ('user_name', user_name),
            ('config_type', config_type), ('engine_id', engine_id)]:
        if param_value is not None and not safe_pattern.match(param_value):
            raise ValueError(
                f"Invalid characters in {param_name}: must be "
                "alphanumeric, hyphen, underscore, dot, colon, or slash")

    # trap_type may be a delivery token or a category name with spaces, but
    # must never contain unsafe characters before it is interpolated.
    if trap_type is not None and not category_pattern.fullmatch(trap_type):
        raise ValueError(
            "Invalid characters in trap_type: must be alphanumeric, "
            "hyphen, underscore, dot, colon, slash, or space")

    # Validate trap_type as delivery mechanism only when used with host config
    if intf and host_name and trap_type and version and user_name and \
            config_type:
        if trap_type not in ('traps', 'informs'):
            raise ValueError(
                "trap_type must be 'traps' or 'informs' when "
                "configuring a trap host")

    # Warn about insecure SNMP versions
    if version is not None and version in ('v1', 'v2c'):
        log.warning(
            "SNMPv1/v2c is insecure for trap hosts. Use v3 with priv "
            "per Cisco hardening guidelines.")

    if intf and host_name and trap_type and version and user_name and \
            config_type:
        cli = [
            f"snmp-server trap-source {intf}",
            "snmp-server enable traps",
            f"snmp-server host {host_name} {trap_type} version {version} "
            f"priv {user_name} {config_type}"]
        if trap_type == 'informs':
            cli.append(f"snmp-server engineID remote {host_name} {engine_id}")
    elif trap_type:
        cli = [f"snmp-server enable traps {trap_type}"]
    else:
        cli = ["snmp-server enable traps"]

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not configure trap/inform config \
                on snmp-server. Error:\n{str(error)}")

def unconfigure_snmp_server_trap(device, intf=None, host_name=None, trap_type=None, version='v3',
                               user_name=None, config_type=None, engine_id=None):
    """ Unconfigures the snmp traps or informs on device
    Example:
        unconfigure_snmp_server_trap(
            device=device,
            intf='GigabitEthernet0/0',
            host_name='10.1.1.1',
            trap_type='traps',
            version='v3',
            user_name='snmpuser1',
            config_type='config'
        )
        --> no snmp-server trap-source GigabitEthernet0/0
            no snmp-server enable traps
            no snmp-server host 10.1.1.1 traps version v3 priv snmpuser1 config

        unconfigure_snmp_server_trap(
            device=device,
            trap_type='traps'
        )
        --> no snmp-server enable traps traps

        unconfigure_snmp_server_trap(device=device)
        --> no snmp-server enable traps

        Args:
            device ('obj'): device to use
            intf ('str',optional): trap source interface
            host_name ('str',optional): hostname/ip address of snmp-server
            trap_type ('str',optional): traps or informs
            version ('str',optional): v3 recommended (v1 and v2c are insecure)
            user_name ('str',optional): Name of the user
            config_type ('str',optional): snmp trap type i.e config,link up down
            engine_id ('str',optional): remote engine id
        Returns:
            None
        Raises:
            ValueError: If input parameters contain invalid characters
            SubCommandFailure
    """
    # Input validation - prevent command injection via newlines or special
    # chars. trap_type is validated separately below because it is
    # dual-purpose:
    #   - With the host form it is the literal 'traps'/'informs' token.
    #   - Used alone it is the 'snmp-server enable traps <category>' name,
    #     which can legitimately contain spaces (e.g. 'snmp linkdown').
    safe_pattern = re.compile(r'^[\w\-\.:\/]+$')
    # Category names may contain spaces but must not contain newlines or
    # shell/CLI metacharacters. fullmatch rejects a trailing newline that
    # '$' would otherwise allow.
    category_pattern = re.compile(r'[\w\-\.:\/ ]+')

    for param_name, param_value in [
            ('intf', intf), ('host_name', host_name),
            ('version', version), ('user_name', user_name),
            ('config_type', config_type), ('engine_id', engine_id)]:
        if param_value is not None and not safe_pattern.match(param_value):
            raise ValueError(
                f"Invalid characters in {param_name}: must be "
                "alphanumeric, hyphen, underscore, dot, colon, or slash")

    # trap_type may be a delivery token or a category name with spaces, but
    # must never contain unsafe characters before it is interpolated.
    if trap_type is not None and not category_pattern.fullmatch(trap_type):
        raise ValueError(
            "Invalid characters in trap_type: must be alphanumeric, "
            "hyphen, underscore, dot, colon, slash, or space")

    # Validate trap_type as delivery mechanism only when used with host config
    if intf and host_name and trap_type and version and user_name and \
            config_type:
        if trap_type not in ('traps', 'informs'):
            raise ValueError(
                "trap_type must be 'traps' or 'informs' when "
                "configuring a trap host")

    # Warn about insecure SNMP versions
    if version is not None and version in ('v1', 'v2c'):
        log.warning(
            "SNMPv1/v2c is insecure for trap hosts. Use v3 with priv "
            "per Cisco hardening guidelines.")

    if intf and host_name and trap_type and version and user_name and \
            config_type:
        cli = [
            f"no snmp-server trap-source {intf}",
            "no snmp-server enable traps",
            f"no snmp-server host {host_name} {trap_type} version {version} "
            f"priv {user_name} {config_type}"]
        if trap_type == 'informs':
            cli.append(
                f"no snmp-server engineID remote {host_name} {engine_id}")
    elif trap_type:
        cli = [f"no snmp-server enable traps {trap_type}"]
    else:
        cli = ["no snmp-server enable traps"]

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not unconfigure trap/inform config \
                on snmp-server. Error:\n{str(error)}")

def configure_snmp_server_user(device,
                               user_name,
                               group_name,
                               version,
                               auth_type = None,
                               auth_algorithm = None,
                               auth_password = None,
                               priv_method = None,
                               aes_algorithm = None,
                               aes_password = None,
                               des_algorithm = None,
                               des_password = None,
                               priv_password = None,
                               acl_type = None,
                               acl_name = None):
    """ Configure the snmp user on device
        Args:
            device ('obj'): device to use
            user_name ('str'): Name of the user
            group_name ('str'): Group to which the user belongs
            version ('str'): v1,v2c,v3
            auth ('str'): authentication parameters for the user
            auth_type ('str'): md5, sha
            auth_algorithm ('str'): 256,192,128
            auth_password ('str'): authentication password for user
            priv_method ('str'): 3des,aes,des
            aes_algorithm ('str'): 128,192,256
            aes_password ('str'): privacy password for user
            des_algorithm ('str'): 128,192,256
            des_password ('str'): privacy password for user
            priv_password ('str'): privacy password for user
            acl_name ('str'): name of the Standerd acl, acl list name, ipv6 named acl
            acl_type ('str'): specify IPv6 Named Access-List
        Returns:
            str: CLI output from the device after applying the configuration
        Raises:
            SubCommandFailure
    """

    cli = f"snmp-server user {user_name} {group_name} {version}"

    if auth_type and auth_password:
        cli += f" auth {auth_type}"
        if auth_algorithm:
            cli += f" {auth_algorithm}"
        cli += f" {auth_password}"

    if priv_method  is not None:
        if(priv_method == 'aes'):
            if aes_algorithm is not None and aes_password is not None:
                cli = f"{cli} priv {priv_method} {aes_algorithm} {aes_password}"
        elif(priv_method in ['des', '3des']):
            if des_algorithm is not None and des_password is not None:
                cli = f"{cli} priv {priv_method} {des_algorithm} {des_password}"

    if acl_name is not None:
        if (acl_type == 'ipv6'):
            cli = cli+' access ipv6 '+acl_name+' '+acl_name
        else:
            cli = cli+' access'+acl_name

    try:
        return device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure snmp user. Error:\n{error}"
        )


def unconfigure_snmp_server_user(device,
                               user_name,
                               group_name,
                               version = 'v3',
                               auth_type = 'sha',
                               auth_algorithm = '128',
                               auth_password = None,
                               priv_method = 'aes',
                               aes_algorithm = None,
                               aes_password = None,
                               priv_password = None,
                               acl_type = None,
                               acl_name = None):
    """ Unconfigures the snmp user on device
    Example :
        unconfigure_snmp_server_user(
        device=device,
        user_name='snmpuser1',
        group_name='snmpgroup1',
        auth_password='AuthPass123',
        aes_algorithm='128',
        aes_password='PrivPass456'
        )
        --> no snmp-server user snmpuser1 snmpgroup1 v3 auth sha 128 AuthPass123 priv aes 128 PrivPass456
        
        unconfigure_snmp_server_user(
        device=device,
        user_name='snmpuser1',
        group_name='snmpgroup1',
        auth_password='AuthPass123',
        aes_algorithm='128',
        aes_password='PrivPass456',
        acl_type='ipv6',
        acl_name='SNMPv6-ACL'
        )
        --> no snmp-server user snmpuser1 snmpgroup1 v3 auth sha 128 AuthPass123 priv aes 128 PrivPass456 access ipv6 SNMPv6-ACL SNMPv6-ACL
        
        Args:
            device ('obj'): device to use
            user_name ('str'): Name of the user
            group_name ('str'): Group to which the user belongs
            version ('str'): v3 (v1 and v2c are insecure and not recommended)
            auth ('str'): authentication parameters for the user
            auth_type ('str'): sha (md5 is deprecated)
            auth_algorithm ('str'): 256,192,128
            auth_password ('str'): authentication password for user
            priv_method ('str'): aes (des and 3des are deprecated)
            aes_algorithm ('str'): 128,192,256
            aes_password ('str'): privacy password for user
            priv_password ('str'): privacy password for user
            acl_name ('str'): name of the Standerd acl, acl list name, ipv6 named acl
            acl_type ('str'): specify IPv6 Named Access-List
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    # Input validation - prevent command injection via newlines or special chars
    safe_pattern = re.compile(r'^[\w\-\.]+$')

    for param_name, param_value in [('user_name', user_name),
                                     ('group_name', group_name),
                                     ('version', version)]:
        if not safe_pattern.match(param_value):
            raise ValueError(f"Invalid characters in {param_name}: must be alphanumeric, hyphen, underscore, or dot")
    # Validate acl_name if provided
    if acl_name is not None and not safe_pattern.match(acl_name):
        raise ValueError("Invalid characters in acl_name: must be alphanumeric, hyphen, underscore, or dot")

    # Validate passwords don't contain newlines (command injection vector)
    for param_name, param_value in [('auth_password', auth_password),
                                     ('aes_password', aes_password)]:
        if param_value and '\n' in param_value:
            raise ValueError(f"{param_name} must not contain newline characters")

    # Warn about insecure SNMP versions
    if version in ('v1', 'v2c'):
        log.warning(f"SNMPv1/v2c is insecure. Use v3 with auth and priv for secure communication.")

    # Warn about weak authentication algorithms
    if auth_type is not None and auth_type.lower() == 'md5':
        log.warning("MD5 authentication is deprecated. Use SHA or SHA-256+ per Cisco hardening guidelines.")

    # Warn about weak encryption methods
    if priv_method is not None and priv_method.lower() in ('des', '3des'):
        log.warning(f"{priv_method} encryption is deprecated. Use AES-128 or higher per Cisco hardening guidelines.")

    cli = f"no snmp-server user {user_name} {group_name} {version}"

    if auth_type is not None and version == 'v3':
        if not auth_algorithm or not auth_password:
            raise ValueError("auth_algorithm and auth_password are required when auth_type is specified")
        if not safe_pattern.match(auth_type):
            raise ValueError("Invalid characters in auth_type")
        cli = cli+' auth '+auth_type+' '+auth_algorithm+' '+auth_password

    if priv_method is not None and version == 'v3':
        if priv_method == 'aes':
            if not aes_algorithm or not aes_password:
                raise ValueError("aes_algorithm and aes_password are required when priv_method is 'aes'")
            cli = cli+' priv '+priv_method+' '+aes_algorithm+' '+aes_password

    if acl_name is not None:
        if acl_type == 'ipv6':
            cli = cli+' access ipv6 '+acl_name+' '+acl_name
        else:
            cli = cli+' access '+acl_name

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure snmp user. Error:\n{error}"
        )

# def configure_snmp_host_version(device,host_name,vrf_id,version_id,community_string, udp_port = 0):
def configure_snmp_host_version(device,host_name,vrf_id,version_id='v3',community_string=None, udp_port = 0):
    """ Configures the snmp-server host with vrf and version on device
    Example:
        configure_snmp_host_version(device=device, host_name='172.21.226.240', vrf_id='Mgmt-vrf', community_string='snmpuser1')
        --> snmp-server host 172.21.226.240 vrf Mgmt-vrf version v3 snmpuser1

        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
            host_name ('str'): Host name
            vrf_id ('str') : vrf(Mgmt-vrf) is special connection,usually we have it in mgmt-interface for management port.
            version_id('str') : Snmp Version (v3 recommended, v1/v2c are insecure)
            udp_port('int', optional) :  udp_port should be passed when enabling traps. The value can also be checked in snmp.server.
        Returns:
            None
        Raises:
            ValueError: If input parameters contain invalid characters
            SubCommandFailure
    """
    safe_pattern = re.compile(r'^[\w\-\.:\/]+$')

    for param_name, param_value in [('host_name', host_name), ('vrf_id', vrf_id),
                                     ('version_id', version_id)]:
        if not safe_pattern.match(param_value):
            raise ValueError(f"Invalid characters in {param_name}")

    if '\n' in community_string:
        raise ValueError("community_string must not contain newline characters")

    # Warn about insecure SNMP versions
    if version_id in ('1', '2c', 'v1', 'v2c'):
        log.warning("SNMPv1/v2c is insecure. Use v3 per Cisco hardening guidelines.")

    log.debug("Configuring snmp host version on device {device}".format(device=device))

    if  udp_port == 0:
        cmd = f"snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string}"
    else:
        cmd = f"snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string} udp-port {udp_port}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure snmp host version. Error:\n{error}".format(error=e))


def unconfigure_snmp_host_version(device,host_name,vrf_id,version_id='v3',community_string=None,udp_port = 0):
    """ Unconfigures the snmp-server host with vrf and version on device
    Example:
        unconfigure_snmp_host_version(device=device, host_name='172.21.226.240', vrf_id='Mgmt-vrf', version_id='v3', community_string='snmpuser1')
        --> no snmp-server host 172.21.226.240 vrf Mgmt-vrf version v3 snmpuser1

        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
            host_name ('str'): Host name
            vrf_id ('str') : vrf(Mgmt-vrf) is special connection,usually we have it in mgmt-interface for management port.
            version_id('str') : Snmp Version
            udp_port('int', optional) :  udp_port should be passed when enabling traps. The value can also be checked in snmp.server.
        Returns:
            None
        Raises:
            ValueError: If input parameters contain invalid characters
            SubCommandFailure
    """
    safe_pattern = re.compile(r'^[\w\-\.:\/]+$')

    for param_name, param_value in [('host_name', host_name), ('vrf_id', vrf_id),
                                     ('version_id', version_id)]:
        if not safe_pattern.match(param_value):
            raise ValueError(f"Invalid characters in {param_name}")

    if '\n' in community_string:
        raise ValueError("community_string must not contain newline characters")

    # Warn about insecure SNMP versions
    if version_id in ('1', '2c', 'v1', 'v2c'):
        log.warning("SNMPv1/v2c is insecure. Use v3 per Cisco hardening guidelines.")

    log.debug("Unconfiguring snmp host version on device {device}".format(device=device))

    if  udp_port == 0:
        cmd = f"no snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string}"
    else:
        cmd = f"no snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string} udp-port {udp_port}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not unconfigure snmp host version. Error:\n{error}".format(error=e))

def configure_debug_snmp_packets(device):
    """ enable snmp debugs on device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring snmp debugs on device {device}")

    try:
        device.execute("debug snmp packets")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure debugs on device. Error:\n{error}"
        )

def unconfigure_debug_snmp_packets(device):
    """ enable snmp debugs on device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring snmp debugs on device {device}")

    try:
        device.execute("undebug snmp packets")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure debugs on device. Error:\n{error}"
        )

def configure_snmp_server_enable_traps_power_ethernet_group(device, number, ip, snmp_v, name=None, rw='ro'):
    """ Configure snmp-server enable traps power-ethernet group
    Example:
        configure_snmp_server_enable_traps_power_ethernet_group(
            device=device, number='1', ip='10.1.1.1', snmp_v='snmpuser1', name='myCommunity', rw='ro'
        )

        Args:
            device ('obj'): Device object
            number ('str'): The group number
            ip ('str') : ip address
            snmp_v ('str'): snmpv1/v2c community string or snmpv3 user name
            name ('str'): snmp community string
            rw ('str'): ro (read-only) or rw (read-write)

        Returns:
                None
        Raises:
                ValueError: If input parameters contain invalid characters
                SubCommandFailure
    """
    safe_pattern = re.compile(r'^[\w\-\.:\/]+$')

    for param_name, param_value in [('number', number), ('ip', ip), ('snmp_v', snmp_v)]:
        if not safe_pattern.match(param_value):
            raise ValueError(f"Invalid characters in {param_name}")
    if name is not None and not safe_pattern.match(name):
        raise ValueError("Invalid characters in name")
    if rw not in ('ro', 'rw'):
        raise ValueError("rw must be 'ro' or 'rw'")

    # Warn about read-write community
    if rw == 'rw':
        log.warning("Read-write community strings grant full control. Use 'ro' unless write access is required per Cisco hardening guidelines.")

    config = [
        f'snmp-server enable traps power-ethernet group {number}',
        f'snmp-server host {ip} {snmp_v}',
        'snmp-server enable traps power-ethernet police',
        f'snmp-server community {name} {rw}',
        'snmp-server manager'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure snmp-server enable traps power-ethernet group on the device. Error:\n{e}")

def configure_snmp_server_manager(device):
    """
        Configures the snmp-server manager
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring snmp manager on {device}")
    try:
        device.configure("snmp-server manager")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure snmp-server manager . Error:\n{e}")

def unconfigure_snmp_server_manager(device):
    """
        Unconfigures the snmp-server manager
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring snmp manager on {device}")
    try:
        device.configure("no snmp-server manager")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not un configure snmp-server manager . Error:\n{e}")


def configure_logging_snmp_trap(device, sev_type):
    """
        Configures the snmp-trap logging
        Args:
            device ('obj'): device to use
            sev_type('sev_type): trap-sev or trap_type
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring logging snmp-trap on {device}")
    try:
        device.configure(f"logging snmp-trap {sev_type}")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure logging snmp-trap . Error:\n{e}")


def unconfigure_logging_snmp_trap(device, sev_type):
    """
        Configures the snmp-trap logging
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring logging snmp-trap on {device}")
    try:
        device.configure(f"no logging snmp-trap {sev_type}")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure logging snmp-trap . Error:\n{e}")


def unconfigure_snmp_server_engineid(device):
    """
        Unconfigures the snmp server engineID
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring snmp server engineID on {device}")
    try:
        device.configure("no snmp-server engineID local")

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not un configure snmp server engineID . Error:\n{e}")


def enable_ietf_standard_snmp_link_traps(device):
    """
        Enable ietf standard snmp link traps
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Enable ietf standard snmp link traps {device}")
    try:
        device.configure("snmp-server trap link ietf")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not enable ietf standard snmp link traps . Error:\n{e}")


def disable_ietf_standard_snmp_link_traps(device):
    """
        Disable ietf standard snmp link traps
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Disable ietf standard snmp link traps on {device}")
    try:
        device.configure(f"no snmp-server trap link ietf")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not disable ietf standard snmp link traps . Error:\n{e}")

def configure_snmp_server_host_trap(device, host_name=None, trap_type=None, community_string='myComm'):
    """ Configures the snmp traps or informs on device
    Example:
        configure_snmp_server_host_trap(device=device, host_name='10.1.1.1', trap_type='entity', community_string='myComm')
        --> snmp-server host 10.1.1.1 traps myComm entity
        Args:
            device ('obj'): device to use
            host_name ('str', optional): WORD     IP/IPV6 address of SNMP notification host
            trap_type ('str', optional): entity Allow SNMP entity traps
            community_string ('str', optional): Community string (avoid 'public' per Cisco hardening)
        Returns:
            None
        Raises:
            ValueError: If input parameters contain invalid characters
            SubCommandFailure
    """
    safe_pattern = re.compile(r'^[\w\-\.:\/]+$')

    if host_name is not None and not safe_pattern.match(host_name):
        raise ValueError("Invalid characters in host_name")
    if trap_type is not None and not safe_pattern.match(trap_type):
        raise ValueError("Invalid characters in trap_type")
    if community_string is not None and '\n' in community_string:
        raise ValueError("community_string must not contain newline characters")

    # Warn about community string
    if community_string == 'public':
        log.warning("Using 'public' community string is insecure. Use a unique string per Cisco hardening guidelines.")

    try:
        device.configure(f"snmp-server host {host_name} traps {community_string} {trap_type}")
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not configure host on snmp-server. Error:\n{str(error)}")

def unconfigure_snmp_server_enable_traps_power_ethernet_group(device, action_type_1, action_type_2, group_number):

    """unconfigure snmp server enable traps power ethernet group
       Args:
            device ('obj'): device object
            action_type_1 ('str'): logging or traps
            action_type_2 ('str'): group or police
            group_number ('int') : The group number (1-9)

       Return:
            None
       Raises:
            SubCommandFailure
    """
    config = [
        f'no snmp-server enable {action_type_1} power-ethernet {action_type_2} {group_number}'
    ]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure snmp server enable traps power ethernet group on {device.name}\n{e}'
        )


def configure_object_list_schema_transfer_for_bulkstat(device, type_, object_name=None, schema_name=None, transfer_name=None,
                                                       oid_value_list=None, poll_interval=None, snmp_interface=None,
                                                       format_=None, transfer_interval=None,
                                                       buffer_size=None, primary_url=None, enable=None, logging_on=None):
    """ Configure object list, schema and transfer for bulkstat
        Args:
            device ('obj'): device to use
            type_('str'): object-list  Configure an Object List
                          schema       Configure Schema definition
                          transfer     Configure Transfer Parameters
            object_name('str', optional): WORD  Name of object list, default value is None
            schema_name('str', optional): WORD  Name of the schema, default value is None
            transfer_name('str', optional): WORD  Name of bulk transfer, default value is None
            oid_value_list:('list', optional): WORD  Object name or OID list, default value is None
            poll_interval('int', optional): Periodicity for the polling of objects in this schema in
                                  Minutes. (Default value is 5 Mins), default value is None
            snmp_interface('str', optional): Specify instance as ifDescr, default value is None
            format_('str', optional): An ASCII format containing schema definitions, default value is None
            transfer_interval('int', optional): Periodicity for the transfer of bulk data in Minutes, default value is None
            buffer_size('int', optional): Bulkstat data file maximum size(Default size is 2048 bytes), default value is None
            primary_url('str', optional): WORD  URL of primary destination, default value is None
            enable('str', optional): Start Data Collection for this Configuration, default value is None
            logging_on('str', optional): Modify message logging facilities, default value is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """


    if type_ == "object-list":
        cli = [f"snmp mib bulkstat {type_} {object_name}"]
        for oid_value in oid_value_list:
            cli.append(f"add {oid_value}")

    elif type_ == "schema":
        cli =[f"snmp mib bulkstat {type_} {schema_name}",
        f"object-list {object_name}",
        f"poll-interval {poll_interval}",
        f"instance wild interface {snmp_interface}"]

    elif type_ == "transfer":
        cli =[f"snmp mib bulkstat {type_} {transfer_name}",
        f"schema {schema_name}",
        f"format {format_}",
        f"transfer-interval {transfer_interval}",
        f"buffer-size {buffer_size}",
        f"url primary {primary_url}",
        f"{enable}",
        f"{logging_on}"]
    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not  configure Object list Schema Transfer for Bulkstat. Error:\n{error}"
        )


def _build_snmp_server_host_command(
    host_ip, version=None, community_string=None, unconfigure=False
):
    """Build ``snmp-server host`` CLI for supported calling patterns.
        Args:
            host_ip ('str'): IP address of the SNMP notification host
            version ('str', optional): SNMP version. If community_string is
                omitted, this value is treated as the community string for
                backward compatibility.
            community_string ('str', optional): Community string
            unconfigure ('bool', optional): When True, prefix the command with
                ``no``
        Returns:
            str: Formatted ``snmp-server host`` command
        Raises:
            ValueError: If input parameters contain invalid characters
    """
    safe_pattern = re.compile(r'^[\w\-\.:\/]+$')

    if not safe_pattern.match(str(host_ip)):
        raise ValueError("Invalid characters in host_ip")

    if community_string is None:
        community_string = version
        version = None

    command = ["snmp-server", "host", str(host_ip)]

    if version is not None:
        if not safe_pattern.match(str(version)):
            raise ValueError("Invalid characters in version")
        command.append(str(version).strip())

    if community_string is not None:
        if '\n' in str(community_string):
            raise ValueError("community_string must not contain newline characters")
        command.append(str(community_string).strip())

    if unconfigure:
        command.insert(0, "no")

    return " ".join(command)


def configure_snmp_server_host(device, host_ip, version='v3', community_string=None):
    """ Configures the snmp-server host on device
    Example:
        configure_snmp_server_host(device=device, host_ip='10.1.1.1', version='v3', community_string='snmpuser1')
        --> snmp-server host 10.1.1.1 v3 snmpuser1

        Args:
            device ('obj'): device to use
            host_ip ('str'): IP address of the SNMP notification host
            version ('str', optional): SNMP version. If community_string is
                omitted, this value is treated as the community string for
                backward compatibility.
            community_string ('str', optional): Community string
        Returns:
            None
        Raises:
            ValueError: If input parameters contain invalid characters
            SubCommandFailure
    """
    # Warn about community-string based access (insecure)
    if community_string is not None and version in (None, '2c', '1', 'v1', 'v2c'):
        log.warning("Community-string based SNMP (v1/v2c) is insecure. Use SNMPv3 per Cisco hardening guidelines.")

    try:
        device.configure(
            _build_snmp_server_host_command(
                host_ip=host_ip,
                version=version,
                community_string=community_string,
            )
        )
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not configure host on snmp-server. Error:\n{str(error)}")


def unconfigure_snmp_server_host(device, host_ip, version=None, community_string=None):
    """ Unconfigures the snmp-server host
        Args:
            device ('obj'): device to use
            host_ip ('str'): IP address of the SNMP notification host
            version ('str', optional): SNMP version. If community_string is
                omitted, this value is treated as the community string for
                backward compatibility.
            community_string ('str', optional): Community string
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            _build_snmp_server_host_command(
                host_ip=host_ip,
                version=version,
                community_string=community_string,
                unconfigure=True,
            )
        )
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not unconfigure SNMP server host. Error:\n{str(error)}")
