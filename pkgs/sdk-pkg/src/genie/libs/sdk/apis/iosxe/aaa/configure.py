# Python
import logging

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def configure_eap_method(device, server_config):

    """ configure EAP method

        Args:
            device ('obj'): Device object
            server_config ('dict'): Dict object
              dictionary contains following keys:
                key_name_compliance ('bool'): eap Key-name (attr 102)
                profile_word ('str'): specify a profile name (max 63 characters)
                description ('str'): provide a description for the EAP profile
                method ('str'): add an allowed method like gtc,fast,leap,md5,mschapv2,peap,tls
                fast_profile_word ('str'): specify the method profile (max 63 characters)
                pki_trustpoint ('str'): set the default pki trustpoint
                exit_eap_profiles ('bool'): exit EAP profiles configuration submode
        Returns:
            None
        Raises:
           Failed configuring EAP method
        Example:
            server_config = {
                     key_name_compliance = True,
                     profile_word = "word1",
                     description = "des1",
                     method = "grc",
                     fast_profile_word = "w1",
                     pki_trustpoint = "pki_word",
                     exit_eap_profiles = True,
                     
                    },
    """
    # initialize list variable
    config_commands = []

    # eap key-name compliance
    if server_config.get("key_name_compliance", False):
        config_commands.append("eap key-name compliance")

    # eap profile p1
    # description des1
    # method gtc
    # method fast profile s1
    # pki-trustpoint pki_word
    # exit
    if "profile_word" in server_config:
        config_commands.append("eap profile {0}".format(server_config["profile_word"]))
        if "description" in server_config:
            config_commands.append("description {0}".format(server_config["description"]))
        if "method" in server_config:
            if "fast_profile_word" not in server_config:
                config_commands.append("method {0}".format(server_config["method"]))
            elif "fast_profile_word" in server_config and server_config["method"] == 'fast':
                config_commands.append("method fast profile {0}".format(server_config["fast_profile_word"]))
        if "pki_trustpoint" in server_config:
            config_commands.append("pki-trustpoint {0}".format(server_config["pki_trustpoint"]))
        if server_config.get("exit_eap_profiles", False):
           config_commands.append("exit")
    try:
        device.configure(config_commands)
        return config_commands
    except SubCommandFailure:
        logger.error('Failed configuring EAP method')
        raise


def configure_tacacs_group(device, server_config):
    """ 
    Configure aaa tacacs server group
    Args:
        device ('obj'): Device object
        server_config('dict'): Dictionary of configurations for server
            dictionary contains following keys:
                server_group ('str'): Tacacs server group name
                server_name ('str'): Tacacs server name
                vrf('str'):  vrf name
                mgmt_intf('str'):  Management interface
                timeout('int'): <1-1000>  Wait time (default 5 seconds)
    Returns:
        configurations list
    Raises:
        SubCommandFailure
    Example:
        server_config = {
                    server_group = "sg1",
                    server_name = "sname1",
                    vrf = "vrf1",
                    mgmt_intf = "GigabitEthernet0/0",
                    timeout = 10,
                },
    """
    #initialize list variable
    config_list = []

    # aaa group server tacacs sg1
    if 'server_group' in server_config:
        config_list.append("aaa group server tacacs {}".format(server_config['server_group']))

    # server name sname1
    if 'server_name' in server_config:
        config_list.append("server name {}".format(server_config['server_name']))

    # ip vrf forwarding vrf1
    if 'vrf' in server_config:
        config_list.append("ip vrf forwarding {}".format(server_config['vrf']))

    # ip tacacs source-interface GigabitEthernet0/0
    if 'mgmt_intf' in server_config:
        config_list.append("ip tacacs source-interface {}".format(server_config['mgmt_intf']))

    # timeout 10
    if 'timeout' in server_config:
        config_list.append("timeout {}".format(server_config['timeout']))

    try:
        device.configure(config_list)
        return config_list
    except SubCommandFailure:
        logger.error('Failed configuring aaa tacacs server group')
        raise

def configure_radius_group(device, server_config):
    """ 
    Configure aaa radius server group
    Args:
        device ('obj'): Device object
        server_config('dict'): Dictionary of configurations for server
            dictionary contains following keys:
                server_group ('str'): Radius server group name
                server_name ('str'): Radius server name
                vrf('str'):  vrf name
                mgmt_intf('str'):  Management interface
                retransmit('int'):  <1-100>  Number of retries for a transaction (default is 3)
                timeout('int'): <1-1000>  Wait time (default 5 seconds)
                ip_addr ('str'): ISE IP
                key('str'): Server key
    Returns:
        configurations list
    Raises:
        SubCommandFailure
    Example:
        server_config = {
                    server_group = "sg1",
                    server_name = "sname1",
                    vrf = "vrf1",
                    mgmt_intf = "GigabitEthernet0/0",
                    retransmit = 0,
                    timeout = 10,
                    ip_addr = "11.19.99.99",
                    key = "cisco123',
                },
    """
    #initialize list variable
    config_list = []

    # aaa group server radius sg1
    if 'server_group' in server_config:
        config_list.append("aaa group server radius {}".format(server_config['server_group']))

    # server name sname1
    if 'server_name' in server_config:
        config_list.append("server name {}".format(server_config['server_name']))

    # ip vrf forwarding vrf1
    if 'vrf' in server_config:
        config_list.append("ip vrf forwarding {}".format(server_config['vrf']))

    # ip radius source-interface GigabitEthernet0/0
    if 'mgmt_intf' in server_config:
        config_list.append("ip radius source-interface {}".format(server_config['mgmt_intf']))
    
    # radius server sname1
    if 'server_name' in server_config:
        config_list.append("radius server {}".format(server_config['server_name']))

    # address ipv4 11.19.99.99 auth-port 1812 acct-port 1813
    if 'ip_addr' in server_config:
       config_list.append("address ipv4 {} auth-port 1812 acct-port 1813".format(server_config['ip_addr']))

    # key cisco123
    if 'key' in server_config:
       config_list.append("key {}".format(server_config['key']))

    # retransmit 0
    if 'retransmit' in server_config:
        config_list.append("retransmit {}".format(server_config['retransmit']))

    # timeout 10
    if 'timeout' in server_config:
        config_list.append("timeout {}".format(server_config['timeout']))

    try:
        device.configure(config_list)
        return config_list
    except SubCommandFailure:
        logger.error('Failed configuring aaa radius server group')
        raise

def configure_coa(device, config_dict):
    """
    COA Configuration for dot1x and mab
    Args:
        device ('obj'): Device object
        config_dict ('dict'): Dictionary of interface configuration details
            dictionary contains following keys:
                auth_type(all, any, session-key) : all(Matches when all attributes match)
                                                    any(Matches when all sent attributes match)
                                                    session-key(Matches with session key attribute only)
                hostname(hostname/ipv4/ipv6) : Ip/ipv6 or hostname of the RADIUS client
                encryption_type(0,6,7): 0(UNENCRYPTED), 6(ENCRYPTED), 7(HIDDEN)
                server_key(str) : Specify a RADIUS client server-key
                ignore_retransmission(bool) : Drop packets using same radius id
                ignore_server-key(bool) : Ignore shared secret
                ignore_session-key(bool) : Ignore attr 151

    Returns:
        None

    Example: {
                'auth_type': 'all',
                'hostname': 'hostname',
                'encryption_type' : 0,
                'server_key' : 'secretkey',
                'ignore_retransmission': True,
                'ignore_server_key': True,
                'ignore_session_key': True
                }

    """
    config_list = ["aaa server radius dynamic-author"]

    '''
    auth-type <auth_type>
    '''
    if 'auth_type' in config_dict:
        config_list.append("auth-type {}".format(config_dict['auth_type']))

    '''
    client <hostname> server-key <server_key>
    client <hostname> server-key <encryption_type> <server_key>
    '''
    if 'hostname' in config_dict:
        if 'encryption_type' in config_dict:
            config_list.append("client {} server-key {} {}".
                               format(config_dict['hostname'], config_dict['encryption_type'],
                                      config_dict['server_key']))
        elif 'server_key' in config_dict:
            config_list.append("client {} server-key {}".format(config_dict['hostname'], config_dict['server_key']))

    # ignore retransmission
    # ignore server-key
    # ignore session-key
    if 'ignore_retransmission' in config_dict and config_dict['ignore_retransmission']:
        config_list.append("ignore retransmission")
    if 'ignore_server_key' in config_dict and config_dict['ignore_server_key']:
        config_list.append("ignore server-key")
    if 'ignore_session_key' in config_dict and config_dict['ignore_session_key']:
        config_list.append("ignore session-key")

    try:
        device.configure(config_list)
    except SubCommandFailure:
        logger.error('Failed configuring COA on device {}'.format(device))
        raise


def configure_enable_aes_encryption(device, master_key):
    """
        enables aes password encryption
        Args:
            device ('obj'): Device object
            master_key ('str'): Master key(New key with minimum length of 8 chars)
        Returns:
            None
        Raises:
            SubCommandError
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*New\s*key.*",
                action=f"sendline({master_key})",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r".*Confirm\s*key.*",
                action=f"sendline({master_key})",
                loop_continue=True,
                continue_timer=False,
            )
        ]
    )
    try:
        device.configure("key config-key password-encrypt", reply=dialog)
        device.configure("password encryption aes")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enables aes password encryption on device {device}.\nError:"
            " {e}".format(device=device.name, e=str(e))
        )


def configure_disable_aes_encryption(device):
    """
        removes aes password encryption
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandError
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Continue\s*with\s*master\s*key\s*deletion.*",
                action="sendline(yes)",
                loop_continue=True,
                continue_timer=False,
            )
        ]
    )
    try:
        device.configure("no key config-key password-encrypt", reply=dialog)
        device.configure("no password encryption aes")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove aes password encryption on {device}.\nError: {e}".format(
                device=device.name, e=str(e))
        )


def configure_radius_attribute_6(device):

    """
    Configure radius attribute 6 on-for-login-auth
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try: 
        device.configure([
            "radius-server attribute 6 on-for-login-auth"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure radius attribute 6 on-for-login-auth'
        )

def unconfigure_radius_attribute_6(device):

    """
    Unconfigure radius attribute 6 on-for-login-auth
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no radius-server attribute 6 on-for-login-auth"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure radius attribute 6 on-for-login-auth'
        )
        

def configure_any_radius_server(device, server_name, addr_type, address, authport, acctport, secret):

    """ Configure radius server on device
    Args:
        device (`obj`): Device object
        server_name (`str`): Radius server name
        addr_type (`str`): Address type v4 or v6
        address (`str`): ISE Ip
        authport (`int`): Auth port
        acctport (`int`): Acct port
        secret (`str`): ISE Secret key
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "radius server {server_name}".format(server_name=server_name),
            "address {addr_type} {address} auth-port {authport} acct-port {acctport}".\
                format(addr_type=addr_type,address=address,authport=authport,acctport=acctport),
            "key {secret}".format(secret=secret)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure radius server {server_name}'.format(server_name=server_name)
        )    

def unconfigure_any_radius_server(device, server_name):

    """ Unconfigure radius server on device
    Args:
        device (`obj`): Device object
        server_name (`str`): Radius server name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no radius server {server_name}".format(server_name=server_name)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure radius server {server_name}'.format(server_name=server_name)
        )            

def configure_radius_server_group(device, servergrp, rad_server):

    """ Configure aaa radius server group
    Args:
        device (`obj`): Device object
        servergrp (`str`): Radius Server Grp name
        rad_server (`str`): Radius Server
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "aaa group server radius {servergrp}".format(servergrp=servergrp),
            "server name {rad_server}".format(rad_server=rad_server)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure AAA radius server group {servergrp}'.format(servergrp=servergrp)
        )

def unconfigure_radius_server_group(device, servergrp):

    """ unconfigure aaa radius server group
    Args:
        device (`obj`): Device object
        servergrp (`str`): Radius Server Grp name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no aaa group server radius {servergrp}".format(servergrp=servergrp)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure AAA radius server group {servergrp}'.format(servergrp=servergrp)
        )   

def configure_aaa_new_model(device):

    """ configure aaa new-model
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "aaa new-model"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure AAA new-model'
        )

def configure_aaa_default_dot1x_methods(device,server_grp,group_type='group',group_type2=None,server_grp2=None):
    """ configure aaa default dot1x methods
        Args:
            device (`obj`): Device object
            server_grp (`str`): Radius Server Grp name
            group_type ('str'): Group type. Options are 'group','cache','local'
            server_grp2 (`str`, optional): 2nd Radius Server Grp name. i.e aaa cache feature (Default is None)
            group_type2 ('str', optional): 2nd Group type. Options are 'group','cache','local' (Default is None)
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring
        Examples:
            configure_aaa_default_dot1x_methods(switch1,'testRadiusGrp')
            configure_aaa_default_dot1x_methods(switch1,'radiusGroup',group_type='cache',
                group_type2='group',server_grp2='radiusGroup')
    """
    if group_type2 is None:
        group_type2 = ""
    if server_grp2 is None:
        server_grp2 = ""

    try:
        device.configure([
            "aaa authentication dot1x default {group_type} {server_grp} {group_type2} {server_grp2}".format(
                group_type=group_type,server_grp=server_grp,group_type2=group_type2,server_grp2=server_grp2),
            "aaa authorization network default {group_type} {server_grp} {group_type2} {server_grp2}".format(
                group_type=group_type,server_grp=server_grp,group_type2=group_type2,server_grp2=server_grp2),
            "aaa accounting dot1x default start-stop group {server_grp}".format(server_grp=server_grp),
            "aaa accounting network default start-stop group {server_grp}".format(server_grp=server_grp)
            ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure AAA dot1x default method {server_grp}'.format(server_grp=server_grp)
        )

def unconfigure_aaa_default_dot1x_methods(device):

    """ configure aaa default dot1x methods
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no aaa authentication dot1x default",
            "no aaa authorization network default",
            "no aaa accounting dot1x default",
            "no aaa accounting network default"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure AAA dot1x default method'
        )            

def configure_aaa_login_method_none(device,servergrp):

    """ This configure will enable login method none that is applicable for line and vty
    from getting locked for password 
    Args:
        device (`obj`): Device object
        servergrp (`str`): Radius Server Grp name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "aaa authentication login {servergrp} none".format(servergrp=servergrp),
            "line con 0",
            "login authentication {servergrp}".format(servergrp=servergrp),
            "line vty 0 4",
            "login authentication {servergrp}".format(servergrp=servergrp),
            "line vty 5 15",
            "login authentication {servergrp}".format(servergrp=servergrp)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure AAA login  method none {servergrp}'.format(servergrp=servergrp)
        )

def unconfigure_aaa_login_method_none(device,servergrp):

    """ This configure will enable login method none that is applicable for line and vty
        from getting locked for password 
    Args:
        device (`obj`): Device object
        servergrp (`str`): Radius Server Grp name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "line con 0",
            "no login authentication {servergrp}".format(servergrp=servergrp),
            "line vty 0 4",
            "no login authentication {servergrp}".format(servergrp=servergrp),
            "line vty 5 15",
            "no login authentication {servergrp}".format(servergrp=servergrp),
            "no aaa authentication login {servergrp} none".format(servergrp=servergrp)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure AAA login  method none {servergrp}'.format(servergrp=servergrp)
    )

def configure_wired_radius_attribute_44(device):

    """ To configure radius attribute 44 for wired
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "radius-server attribute 44 extend-with-addr"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure wired radius attribute 44'
        )


def unconfigure_wired_radius_attribute_44(device):

    """ To unconfigure radius attribute 44 for wired
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no radius-server attribute 44 extend-with-addr"
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure wired radius attribute 44'
        )

def configure_radius_interface(device, interface):

    """ Configure Radius Interface
    Args:
        device ('obj'): device to use
        interface('str'): Interface to be configured
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring Radius Interface
    """
    try:
        device.configure(["ip radius source-interface {interface}".format(interface=interface)])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not Configure Radius Interface"
        )


def unconfigure_radius_interface(device, interface):

    """ Configure Radius Interface
    Args:
        device ('obj'): device to use
        interface('str'): Interface to be configured
    Returns:
        None
    Raises:
        SubCommandFailure: Failed configuring Radius Interface
    """
    try:
        device.configure(["no ip radius source-interface {interface}".format(interface=interface)])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not Configure Radius Interface"
        )


def clear_aaa_cache(device, server_grp, profile='all'):
    """ Clear AAA Cache
        Args:
            device (`obj`): Device object
            server_grp (`str`): Radius Server Grp name
            profile ('str',optional): Profile name to clear. Default 'all.'
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring
        Examples:
            switch1.api.clear_aaa_cache('radiusGroup')
    """
    try:
        device.execute('clear aaa cache group {server_grp} {profile}'.format(
            server_grp=server_grp,
            profile=profile))
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to execute clear aaa cache"
        )


def configure_username(device, username, pwd, encryption=0):
    """ Configure a user with a password
        Args:
            device (`obj`): Device object
            username (`str`): User name
            pwd ('str'): Password for the user
            encryption ('int',optional): Encryption level (Default 0 for cleartext)
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring
        Examples:
            dut1.api.configure_username(username='testUser',pwd='secretPwd')
            -->username testUser password 0 secretPwd
    """
    try:
        # Update str with password encryption level
        if encryption:
            pwd = '{encryption} {pwd}'.format(encryption=encryption,pwd=pwd)
        device.configure('username {username} password {pwd}'.format(username=username,pwd=pwd))
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure user {username}".format(username=username)
        )


def unconfigure_username(device, username):
    """ Configure a user with a password
        Args:
            device (`obj`): Device object
            username (`str`): User name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring
        Examples:
            dut1.api.unconfigure_username(username='testUser')
    """
    try:
        device.configure('no username {username}'.format(username=username))
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to unconfigure user {username}".format(username=username)
        )


def configure_radius_automate_tester(device, server_name, username, idle_time=None):
    """ configure Radius Automate Tester. It polls the radius to make sure it is alive.
    Args:
        device (`obj`): Device object
        server_name ('str'): Radius server name
        username ('str'): Identity Username to query radius server
        idle_time ('int',optional): Radius polling interval in min.
                                  Default: None. Device will add idle time depending on IOS version
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    if idle_time is None:
        optCfg = ""
    else:
        optCfg = "idle-time {idle_time}".format(idle_time=str(idle_time))
    try:
        device.configure([
            "radius server {server_name}".format(server_name=server_name),
            "automate-tester username {username} {optCfg}".format(username=username,optCfg=optCfg)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure radius automate tester"
        )

def unconfigure_radius_automate_tester(device, server_name, username):
    """ Unconfigure Radius Automate Tester.
    Args:
        device (`obj`): Device object
        server_name ('str'): Radius server name
        username ('str'): Identity Username to query radius server
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "radius server {server_name}".format(server_name=server_name),
            "no automate-tester username {username}".format(username=username)
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure Radius automate tester"
        )

def configure_radius_interface_vrf(device, interface, vrf):

    """ Configure Radius Interface via vrf
    Args:
        device ('obj'): device to use
        interface('str'): Interface to be configured
        vrf('str'): VRF name

    Returns:
        None

    Raises:
        SubCommandFailure: Failed configuring Radius Interface via vrf

    """

    try:
        device.configure(["ip radius source-interface {interface} vrf {vrf}".format(interface=interface, vrf=vrf)])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not Configure Radius Interface via vrf"
        )

def unconfigure_radius_interface_vrf(device, interface, vrf):

    """ Unconfigure Radius Interface via vrf
    Args:
        device ('obj'): device to use
        interface('str'): Interface to be configured
        vrf('str'): VRF name

    Returns:
        None

    Raises:
        SubCommandFailure: Failed unconfiguring Radius Interface via vrf

    """

    try:
        device.configure(["no ip radius source-interface {interface} vrf {vrf}".format(interface=interface, vrf=vrf)])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not Unconfigure Radius Interface via vrf"
        )

def configure_common_criteria_policy(device, 
                                     policy_name, 
                                     char_changes=None,
                                     copy=None, 
                                     lifetime=None, 
                                     lower_case=1, 
                                     upper_case=1,
                                     max_len=None, 
                                     min_len=3, 
                                     no_value=None, 
                                     num_count=1,
                                     special_case=None):
    
    """ Configure aaa common criteria policy
    Args:
        device (`obj`):                 Device object
        policy_name (`str`):            Policy name
        char_changes (`str`, optional): Number of change characters between old and new passwords
        copy (`str`, optional):         Copy from policy
        lifetime (`dict`, optional):    lifetime configuration
        lower_case (`str`, optional):   Number of lower-case characters
        upper_case (`str`, optional):   Number of upper-case characters
        max_len (`str`, optional):      Specify the maximum length of the password
        min_len (`str`, optional):      Specify the minimum length of the password
        no_value (`dict`, optional):    value to unconfigure
        num_count (`str`, optional):    Number of numeric characters
        special_case (`str`, optional): Number of special characters

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """

    configs = ["aaa common-criteria policy {pol}".format(pol=policy_name)]
    if char_changes:
        configs.append("char-changes {char}".format(char=char_changes))
    if copy:
        configs.append("copy {copy_pol}".format(copy_pol=copy))
    if lifetime:
       for key in lifetime:
           configs.append("lifetime {attr} {val}".format(attr=key, val=lifetime[key])) 
    if int(lower_case) > 1:
        configs.append("lower-case {low}".format(low=lower_case))
    if int(upper_case) > 1:
        configs.append("upper-case {up}".format(up=upper_case))
    if max_len:
        configs.append("max-length {maxl}".format(maxl=max_len))
    if int(min_len) > 3:
        configs.append("min-length {minl}".format(minl=min_len))
    if no_value:
        if 'lifetime' in no_value:
            configs.append("no lifetime {val1} {val2}".format(
                val1=no_value["lifetime"][0],
                val2=no_value["lifetime"][1]))
        else:
            for key in no_value:
                configs.append("no {attr} {val}".format(attr=key,
                    val=no_value[key]))
    if int(num_count) > 1:
        configs.append("numeric-count {num}".format(num=num_count))
    if special_case:
        configs.append("special-case {spcl}".format(spcl=special_case))

    try:
        device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure aaa common criteria policy {pol} "
            "Error: {error}".format(pol=policy_name, error=e
            )
        )

def unconfigure_common_criteria_policy(device, 
                                       policy_name):
    
    """ Unconfigure aaa common criteria policy
    Args:
        device (`obj`):      Device object
        policy_name (`str`): Policy name

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """

    try:
        out = device.configure("no aaa common-criteria policy {pol}".format(
                               pol=policy_name))
        if '% Policy {pol} cannot be deleted'.format(pol=policy_name) in out:
            raise SubCommandFailure(out)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure aaa common criteria policy {pol} "
            "Error: {error}".format(pol=policy_name, error=e
            )
        )

def configure_enable_policy_password(device, 
                                     password, 
                                     policy_name=None, 
                                     password_type=None):
    
    """ Configure enable password with policy
    Args:
        device (`obj`):                  Device object
        password (`str`):                Password
        policy_name (`str`, optional):   Policy name
        password_type ('str', optional): Password type
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
      
    if policy_name:
        config = "enable common-criteria-policy {pol} password {ptype} {pwd}".format(
                            pol=policy_name, ptype=password_type, pwd=password)
    else:
        config = "enable password {pwd}".format(pwd=password)

    try:
        out = device.configure(config)
        if '% Password' in out:
            raise SubCommandFailure(out)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure enable password with policy {pwd} "
            "Error: {error}".format(pwd=password, error=e
            )
        )
        
def unconfigure_enable_policy_password(device, 
                                       password, 
                                       policy_name=None, 
                                       password_type=None):
    
    """ Unconfigure enable password with policy
    Args:
        device (`obj`):                   Device object
        password (`str`):                 Password
        policy (`str`, optional):         Policy name
        password_type ('str', optional) : Password type

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """

    if policy_name:
        config = "no enable common-criteria-policy {pol} password {ptype} {pwd}".format(
                            pol=policy_name, ptype=password_type, pwd=password)
    else:
        config = "no enable password {pwd}".format(pwd=password)

    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure enable password with policy {pwd} "
            "Error: {error}".format(pwd=password, error=e
            )
        )

def configure_service_password_encryption(device):

    """ Configures service password encryption
    Args:
        device ('obj'): device to use

    Returns:
        None

    Raises:
        SubCommandFailure: Failed configuring service password encryption 

    """

    try:
        device.configure("service password-encryption")
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure service password encryption"
        )

def unconfigure_service_password_encryption(device):

    """ Unconfigures service password encryption
    Args:
        device ('obj'): device to use

    Returns:
        None

    Raises:
        SubCommandFailure: Failed unconfiguring service password encryption 

    """

    try:
        device.configure("no service password-encryption")
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure service password encryption"
        )
