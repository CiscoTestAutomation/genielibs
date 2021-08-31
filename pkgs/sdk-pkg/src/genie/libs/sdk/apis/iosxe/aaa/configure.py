# Python
import logging

# Unicon
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
