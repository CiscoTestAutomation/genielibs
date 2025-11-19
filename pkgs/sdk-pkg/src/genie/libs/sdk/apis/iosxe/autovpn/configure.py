import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_crypto_ikev2_profile_autovpn(device, 
                                         profile_name=None,
                                         match_application=None,
                                         match_identity_remote_any=False,
                                         auth_remote=None,
                                         auth_local=None,
                                         nat_force_encap=False,
                                         virtual_template=None,
                                         policy_name=None,
                                         proposal_name=None):
    """ Configure crypto ikev2 profile for autovpn and optionally ikev2 policy
    Args:
        device (`obj`): Device object
        profile_name (`str`, optional): name of ikev2 profile (Default None)
        match_application ('str', optional): Application to match (e.g., 'autovpn')
        match_identity_remote_any (`bool`, optional): Match any remote identity
        auth_remote (`str`, optional): Remote authentication method (e.g., 'pre-share')
        auth_local (`str`, optional): Local authentication method (e.g., 'pre-share')
        nat_force_encap (`bool`, optional): Force NAT encapsulation
        virtual_template (`int`, optional): Virtual template number
        policy_name (`str`, optional): name of ikev2 policy to configure
        proposal_name (`str`, optional): name of ikev2 proposal for policy
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    config_list = []
    
    # Configure IKEv2 Policy if provided
    if policy_name:
        config_list.append('crypto ikev2 policy {policy_name}'.format(policy_name=policy_name))
        
        if match_application:
            config_list.append("match app {match_application}".format(match_application=match_application))
        
        if proposal_name:
            config_list.append('proposal {proposal_name}'.format(proposal_name=proposal_name))
    
    # Configure IKEv2 Profile only if profile_name is provided
    if profile_name:
        config_list.append('crypto ikev2 profile {profile_name}'.format(profile_name=profile_name))
        
        if match_application:
            config_list.append("match application {match_application}".format(match_application=match_application))
        
        if match_identity_remote_any:
            config_list.append("match identity remote any")
        
        if auth_remote:
            config_list.append("authentication remote {auth_remote}".format(auth_remote=auth_remote))
        
        if auth_local:
            config_list.append("authentication local {auth_local}".format(auth_local=auth_local))
        
        if nat_force_encap:
            config_list.append("nat force-encap")
        
        if virtual_template:
            config_list.append("virtual-template {virtual_template}".format(virtual_template=virtual_template))
    
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure Crypto IKEv2 Profile/Policy. Error: {error}'.format(error=e)
        )


def configure_virtual_template_for_autovpn(device, 
                                         vt_number,
                                         ipsec_profile_name,
                                         ip_address=None,
                                         tunnel_mode="ipsec ipv4"):
    """ Configure Virtual-Template interface for AutoVPN
    Args:
        device (`obj`): Device object
        vt_number (`int`): Virtual template number
        ipsec_profile_name (`str`): IPsec profile name for tunnel protection
        ip_address (`str`, optional): IP address for the interface (default: no ip address)
        tunnel_mode (`str`, optional): Tunnel mode (default: "ipsec ipv4")
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    log.info(f"Configuring Virtual-Template{vt_number} for AutoVPN")
    
    config_list = []
    config_list.append(f'interface Virtual-Template{vt_number} type tunnel')
    
    if ip_address:
        config_list.append(f'ip address {ip_address}')
    else:
        config_list.append('no ip address')
    
    config_list.append(f'tunnel mode {tunnel_mode}')
    config_list.append(f'tunnel protection ipsec profile {ipsec_profile_name}')
    
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure Virtual-Template{vt_number} for AutoVPN. Error: {e}'.format(error=e)
        )


def configure_crypto_autovpn_vpn_registry(device,
                                           autovpn_cfg,
                                           server_addr1,
                                           server_port1,
                                           server_addr2=None,
                                           server_port2=None,
                                           local=None,
                                           remotes=None):
    """Configure crypto autovpn on device
    
    Args:
        device (obj): Device object
        autovpn_cfg (str): AutoVPN configuration name
        server_addr1 (str): Primary server IPv4 address
        server_port1 (int): Primary server port (9350-9381)
        server_addr2 (str, optional): Secondary server IPv4 address
        server_port2 (int, optional): Secondary server port (9350-9381)
        local (dict, optional): Local peer configuration with keys:
            - device_num (int): 4-byte decimal peer number
            - device_id (str): 16-byte hex value
            - is_hub (bool): True for hub, False for spoke
            - multi_uplink_tunnels (bool): Enable multi-uplink tunnels
            - load_balance (bool): Enable load balancing
            - uplink0_name (str): First uplink interface name
            - uplink1_name (str, optional): Second uplink interface name
        remotes (list, optional): List of remote peer configurations (max 10), each dict with keys:
            - device_num (int): 4-byte decimal peer number
            - device_id (str): 16-byte hex value
            - is_hub (bool): True for hub, False for spoke
            - peer_psk (str): Pre-shared key
            - multi_uplink_tunnels (bool): Enable multi-uplink tunnels
    
    Returns:
        bool: True if configuration was successful, False otherwise
    
    Raises:
        SubCommandFailure: Failed to configure crypto autovpn (only for critical failures)
    
    Example:
        local_peer = {
            'device_num': 21219,
            'device_id': '0x21219',
            'is_hub': True,
            'multi_uplink_tunnels': True,
            'load_balance': True,
            'uplink0_name': 'GigabitEthernet2'
        }
        remote_peer = {
            'device_num': 20217,
            'device_id': '0x20217',
            'is_hub': False,
            'multi_uplink_tunnels': True,
            'peer_psk': '<peer_psk>'
        }
        configure_crypto_autovpn_vpn_registry(
            device=device,
            autovpn_cfg='autovpn1',
            server_addr1='10.126.208.110',
            server_port1=9350,
            server_addr2='10.126.208.110',
            server_port2=9351,
            local=local_peer,
            remotes=[remote_peer]
        )
        
        This generates the following configuration:
        crypto autovpn autovpn1
         vpn-registry server ipv4 10.126.208.110 9350 10.126.208.110 9351
         local 21219 0x21219 true true true GigabitEthernet2
         remote 20217 0x20217 false true <peer_psk>
         exit
    """
    
    if remotes is None:
        remotes = []
    
    config_cmds = []
    
    config_cmds.append(f"crypto autovpn {autovpn_cfg}")
    
    vpn_registry_parts = ["vpn-registry", "server", "ipv4", server_addr1, str(server_port1)]
    if server_addr2 and server_port2:
        vpn_registry_parts.extend([server_addr2, str(server_port2)])
    config_cmds.append(" ".join(vpn_registry_parts))
    
    if local:
        local_parts = ["local", str(local['device_num']), local['device_id'], str(local['is_hub']).lower()]
        
        if 'multi_uplink_tunnels' in local:
            local_parts.append(str(local['multi_uplink_tunnels']).lower())
            
            if 'load_balance' in local:
                local_parts.append(str(local['load_balance']).lower())
                
                if 'uplink0_name' in local:
                    local_parts.append(local['uplink0_name'])
                    
                    if 'uplink1_name' in local and local['uplink1_name'] is not None:
                        local_parts.append(local['uplink1_name'])
        
        config_cmds.append(" ".join(local_parts))
    
    for remote in remotes[:10]: 
        remote_parts = ["remote", str(remote['device_num']), remote['device_id'], str(remote['is_hub']).lower()]
        
        if 'multi_uplink_tunnels' in remote:
            remote_parts.append(str(remote['multi_uplink_tunnels']).lower())
        
        if 'peer_psk' in remote:
            remote_parts.append(remote['peer_psk'])
        
        config_cmds.append(" ".join(remote_parts))
    
    config_cmds.append("exit")
    
    try:
        device.configure(config_cmds)
        return True
        
    except SubCommandFailure as e:
        return False
    except Exception as e:
        raise SubCommandFailure(f"Failed to configure crypto autovpn {autovpn_cfg}") from e
        
def unconfigure_autovpn(device, autovpn_name):
    """ Unconfigure AutoVPN on device
    Args:
        device (`obj`): Device object
        autovpn_name (`str`): AutoVPN instance name to remove
    Return:
        None
    Raise:
        SubCommandFailure: Failed unconfiguring AutoVPN
    """
    log.info(f"Unconfiguring AutoVPN {autovpn_name}")
    
    try:
        device.configure(f'no crypto autovpn {autovpn_name}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not unconfigure AutoVPN {autovpn_name}. Error: {e}'
        )
