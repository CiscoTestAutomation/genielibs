"""Common configure/unconfigure functions for IKE"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_ikev2_keyring(device,
                            keyring_name,
                            peer_name,
                            peer_ip=None,
                            peer_mask=None,
                            key=None,
                            required=False,
                            ppk_id=None,
                            ppk_key=None,
                            sks_client_config_block_name=None):
    """ Configures IKEV2 keyring or Preshared Key (PSK)
        Args:
            device (`obj`): Device object
            keyring_name ('str'): Name for the keyring
            peer_name ('str'): peer name
            peer_ip ('str',optional): peer ip addr
            peer_mask ('str',optional): peer nw mask
            key ('str',optional): preshared key
            required ('boolean',optional): Required option for PPK
            ppk_id ('str',optional): ppk id for manual ppk
            ppk_key ('str',optional): Post-quantum preshared key
            sks_client_config_block_name ('str',optional): SKS client config block name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IKEV2 Preshared Key"
    )

    configs = []
    configs.append("crypto ikev2 keyring {keyring_name}".format(keyring_name=keyring_name))
    configs.append("peer {peer_name}".format(peer_name=peer_name))
    
    if peer_ip is not None and peer_mask is not None:    
        configs.append("address {peer_ip} {peer_mask}".format(peer_ip=peer_ip,peer_mask=peer_mask))
    if key is not None:
        configs.append("pre-shared-key {key}".format(key=key))
    if ppk_key is not None:
        cmd = f'ppk manual id {ppk_id} key {ppk_key}'
        if required:
            cmd += ' required'
        configs.append(cmd)                
    if sks_client_config_block_name is not None:
        cmd = f"ppk dynamic {sks_client_config_block_name}"
        if required:
            cmd += ' required'
        configs.append(cmd)                
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 keyring,"
             "Error:\n{error}".format(error=e)
        )
        raise


def configure_ikev2_profile(device,
                            profile_name,
                            remote_addr,
                            remote_auth,
                            local_auth,
                            keyring,
                            dpd_hello_time,
                            dpd_retry_time,
                            dpd_query):
    """ Configures IKEV2 keyring or Preshared Key (PSK)
        Args:
            device (`obj`): Device object
            profile_name ('str'): ikev2 profile name
            remote_addr ('str'): peer/remote ip address
            remote_auth ('str'): remote authentication method
            local_auth ('str'): local authentication method
            keyring ('str'): ikev2 keyring name
            dpd_hello_time ('int'): DPD R-U-THERE interval
            dpd_retry_time ('int'): DPD Retry Interval
            dpd_query ('str'): DPD queires on-demand or periodic
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IKEV2 Profile"
    )

    configs = []
    configs.append("crypto ikev2 profile {profile_name}".format(profile_name=profile_name))
    configs.append("match identity remote address {remote_addr}".format(remote_addr=remote_addr))
    configs.append("authentication remote {remote_auth}".format(remote_auth=remote_auth))
    configs.append("authentication local {local_auth}".format(local_auth=local_auth))
    configs.append("keyring local {keyring}".format(keyring=keyring))
    configs.append("dpd {dpd_hello_time} {dpd_retry_time} {dpd_query}".format(dpd_hello_time=dpd_hello_time,dpd_retry_time=dpd_retry_time,dpd_query=dpd_query))

    

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 profile,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_ikev2_proposal(device,
                            proposal_name,
                            encr_algos,
                            dh_group,
                            integrity_algos=None,
                            prf_algos=None
                        ):
    """ Configures IKEV2 Proposal
        Args:
            device (`obj`): Device object
            proposal_name ('str'): ikev2 proposal name
            encr_algos ('str'): encryption algorithms
            integrity_algos ('str'): integrity or authentication algorithms
            dh_group ('str'): Diffie Hellman group
            prf_algos ('str'): Psuedo random number function
        Returns:
            True/False
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IKEV2 Proposal"
    )

    configs = []
    configs.append(f"crypto ikev2 proposal {proposal_name}")
    configs.append(f"encryption {encr_algos}")
    if not re.search(r"aes\-gcm\-.*", encr_algos):
        configs.append(f"integrity {integrity_algos}")
    configs.append(f"group {dh_group}")
    if prf_algos is not None:
        configs.append(f"prf {prf_algos}")
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 proposal,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_ikev2_policy(device,
                        policy_name,
                        proposal_name,
                        local_address=None,
                        fvrf=None
                        ):
    """ Configures IKEV2 Policy
        Args:
            device (`obj`): Device object
            policy_name ('str'): ikev2 policy name
            proposal_name ('str'): ikev2 profile name
            local_address ('str'): local device address
            fvrf ('str'): fvrf name
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IKEV2 Policy"
    )

    configs = []
    configs.append(f"crypto ikev2 policy {policy_name}")
    if local_address is not None:
        configs.append(f"match address local {local_address}")
    
    if fvrf is not None:
        configs.append(f"match fvrf {fvrf}")
    configs.append(f"proposal {proposal_name}")
    try:
        device.configure(configs, error_pattern=[f"% fvrf {fvrf} not configured",
                                f"% No Proposal exists with the specified name {proposal_name}"])
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 policy,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_ikev2_authorization_policy(device,
                            policy_name,
                            set_interface=False,
                            interface=None,
                            ipv4_acl=None,
                            ipv6_acl=None,
                            local_prefix=None,
                            local_netmask=None,
                            local_ipv6_prefix=None,
                            local_ipv6_netmask=None,
                            remote_prefix=None,
                            remote_netmask=None,
                            remote_ipv6_prefix=None,
                            remote_ipv6_netmask=None,
                            dhcp_giaddr=None,
                            dhcp_server=None,
                            dhcp_timeout=None,
                            pool_name=None,
                            ipsec_flow_limit=None,
                            primary_dns=None,
                            secondary_dns=None,
                            aaa_attribute=None,
                            net_mask=None,
                            pfs=False,
                            ipv6_dns=None,
                            ipv6_pool=None,
                            ipv6_prefix_len=None,
                            lifetime=None,
                            config_url=None,
                            config_version=None,
                            backup_gateway=None,
                            default_domain=None,
                            split_dns=None):
    """ Configures IKEV2 authorization policy
        Args:
            device (`obj`): Device object
            policy_name ('str'): ikev2 authorization policy name
            set_interface ('boolean'): knob to configure "route set interface"
            interface ('str'): configuring interface in "route set interface"
            ipv4_acl ('str'): configuring ipv4 acl in "route set access-list"
            ipv6_acl ('str'): configuring ipv6 acl in "route set access-list"
            local_prefix ('str'): setting local prefix
            local_netmask ('str'): setting mask for local prefix
            local_ipv6_prefix ('str'): setting local ipv6 prefix
            local_ipv6_netmask ('str'): setting local ipv6 netmask
            remote_prefix ('str'): setting remote prefix
            remote_netmask ('str'): setting mask for remote prefix
            remote_ipv6_prefix ('str'): setting remote ipv6 prefix
            remote_ipv6_netmask ('str'): setting remote ipv6 netmask
            dhcp_giaddr ('str'): configuring dhcp giaddr address
            dhcp_server ('str'): configuring dhcp server address
            dhcp_timeout ('int'): configuring dhcp timeout(4-30)
            pool_name ('str'): dhcp pool name
            ipsec_flow_limit ('str'): configuring ipsec flow limit
            primary_dns ('str'): Primary DNS server IP
            secondary_dns ('str'): Secondary DNS server IP
            aaa_attribute ('str'): AAA attribute for connections
            net_mask ('str'): subnet mask
            pfs ('boolean'): Enabling Prefect forward secrecy
            ipv6_dns ('str'): Configuring ipv6 DNS address
            ipv6_pool ('str'): Configuring ipv6 pool name
            ipv6_prefix_len ('int') : configuring ipv6 prefix length
            lifetime ('int') : configuring session lifetime
            config_url ('str'): Configuring http url for fetching configuration
            config_version ('int'): Configuring configuration version
            backup_gateway ('str'): Configuring backup gateway
            default_domain ('str'): Configuring default domain name
            split_dns ('str') : Configuring split dns domain name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IKEV2 Authorization"
    )

    configs = []
    configs.append(f"crypto ikev2 authorization policy {policy_name}")

    if set_interface == True and interface is None:
        configs.append("route set interface")
    if set_interface == True and interface is not None:
        configs.append(f"route set interface {interface}")
    
    if ipv4_acl is not None:
        configs.append(f"route set access-list {ipv4_acl}")

    if ipv6_acl is not None:
        configs.append(f"route set access-list ipv6 {ipv6_acl}")

    if local_prefix is not None and local_netmask is not None:
        configs.append(f"route set local ipv4 {local_prefix} {local_netmask}")
    
    if local_ipv6_prefix is not None and local_ipv6_netmask is not None:
        configs.append(f"route set local ipv6 {local_ipv6_prefix}/{local_ipv6_netmask}")
    
    if remote_prefix is not None and remote_netmask is not None:
        configs.append(f"route set local ipv4 {remote_prefix} {remote_netmask}")
    
    if remote_ipv6_prefix is not None and remote_ipv6_netmask is not None:
        configs.append(f"route set local ipv6 {remote_ipv6_prefix}/{remote_ipv6_netmask}")

    if dhcp_giaddr is not None:
        configs.append(f"dhcp giaddr {dhcp_giaddr}")

    if dhcp_server is not None:
        configs.append(f"dhcp server {dhcp_server}")

    if dhcp_timeout is not None:
        configs.append(f"dhcp timeout {dhcp_timeout}")

    if pool_name is not None:
        configs.append(f"pool {pool_name}")

    if ipsec_flow_limit is not None:
        configs.append(f"ipsec flow-limit {ipsec_flow_limit}")

    if primary_dns is not None and secondary_dns is None:
        configs.append(f"dns {primary_dns}")
    
    if primary_dns is not None and secondary_dns is not None:
        configs.append(f"dns {primary_dns} {secondary_dns}")
    
    if aaa_attribute is not None:
        configs.append(f"aaa attribute list {aaa_attribute}")

    if net_mask is not None:
        configs.append(f"netmask {net_mask}")

    if pfs == True:
        configs.append("pfs")
    
    if ipv6_dns is not None:
        configs.append(f"ipv6 dns {ipv6_dns}")
    
    if ipv6_pool is not None:
        configs.append(f"ipv6 pool {ipv6_pool}")

    if ipv6_prefix_len is not None:
        configs.append(f"ipv6 prefix {ipv6_prefix_len}")
    
    if lifetime is not None:
        configs.append(f"session-lifetime {lifetime}")
    
    if config_url is not None:
        configs.append(f"configuration url {config_url}")

    if config_version is not None:
        configs.append(f"configuration version {config_version}")

    if backup_gateway is not None:
        configs.append(f"backup-gateway {backup_gateway}")

    if default_domain is not None:
        configs.append(f"def-domain {default_domain}")

    if split_dns is not None:
        configs.append(f"split-dns {split_dns}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 authorization policy,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_ikev2_profile_advanced(device,
                        profile_name,
                        remote_auth=None,
                        local_auth=None,
                        keyring_aaa=None,
                        keyring_local=None,
                        dpd_interval=None,
                        dpd_retry=None,
                        dpd_query=None,
                        auth_method=None,
                        aaa_list=None,
                        override=False,
                        auth_type=None,
                        cached=False,
                        anyconnect_prof_name=None,
                        auth_eap_method=None,
                        auth_uname=None,
                        auth_pwd_type=None,
                        auth_password=None,
                        double_auth=False,
                        eap_query=False,
                        eap_timeout=None,
                        conf_exch_accept=False,
                        conf_set_accept=False,
                        conf_set_send=False,
                        id_local=False,
                        id_local_addr=None,
                        id_local_dn=False,
                        id_local_email=None,
                        id_local_fqdn=None,
                        id_local_key_id=None,
                        initial_contact=False,
                        ivrf=None,
                        lifetime=None,
                        match_address=None,
                        match_cert_map=None,
                        match_fvrf=None,
                        id_remote=False,
                        id_remote_addr=None,
                        id_remote_any=False,
                        id_remote_email=None,
                        id_remote_email_domain=None,
                        id_remote_fqdn=None,
                        id_remote_fqdn_domain=None,
                        id_remote_key_id=None,
                        nat_encap=False,
                        nat_keepalive=None,
                        trustpoint=None,
                        trustpoint_verify=False,
                        trustpoint_sign=False,
                        ppk_dynamic=None,
                        ppk_manual=None,
                        reconnect_timer=None,
                        ikev2_redirect=False,
                        shutdown=False,
                        vt_number=None,
                        vt_mode_auto=False,
                        dynamic_enabled=False
                        ):
    """ Configures IKEV2 keyring or Preshared Key (PSK)
        Args:
            device (`obj`): Device object
            profile_name ('str') : ikev2 profile name
            remote_auth ('str') : Remote authentication method
            local_auth ('str') : Local authentication method
            keyring_aaa ('str') : Keyring name for AAA
            keyring_local ('str') : Local keyring name
            dpd_interval ('int') : DPD interval
            dpd_retry ('int') : DPD retry times
            dpd_query ('str') : DPD query type
            auth_method ('str') : AAA Authentication method
            aaa_list ('str') : AAA list name
            override ('str') : Override user authorization with group authorization 
            auth_type ('str') : Authorization type, User or Group
            cached ('boolean') : Caching User authorization True/False
            anyconnect_prof_name ('str') : AnyConnect Profile Name
            auth_eap_method ('str') : local EAP authentication method
            auth_uname ('str') : username of local/Remote EAP and PSK authentication
            auth_pwd_type('int') : Encryption type of password of Local/Remote authentication
            auth_password('str') : Password for Local/Remote EAP and PSK authentication
            double_auth ('Boolean') : Double authentication
            eap_query ('Boolean') : EAP authentication EAP query identity
            eap_timeout ('str') : EAP authentication timeout timer
            conf_exch_accept ('Boolean') : Configuration Exchange accept True/False
            conf_set_accept ('Boolean') : Configuration set accept True/False
            conf_set_send ('Boolean') : Configuration set send True/False
            id_local ('Boolean') : knob for local identity 
            id_local_addr ('str') : Identity local IP address 
            id_local_dn ('str') : Identity local distingushed name
            id_local_email ('str') : Identity local email id
            id_local_fqdn ('str') : Identity local Fully Qualified Domain name
            id_local_key_id ('str') : Identity local key id
            initial_contact ('Boolean') : Initial contact enable True/False
            ivrf ('str') : IVRF name
            lifetime ('int') : lifetime in seconds
            match_address ('str') : Match remote peer IP address
            match_cert_map ('str') : Match remote incoming certificate parameters using cert map
            match_fvrf ('str') : Match remote fvrf 
            id_remote ('Boolean') : Knob for remote identity
            id_remote_addr ('str') : Identity remote IP address 
            id_remote_any ('Boolean') : Match remote identity any
            id_remote_email ('str') : Match remote identity email 
            id_remote_email_domain ('str') : Match remote identity email domain
            id_remote_fqdn ('str') : Match remote identity Fully Qualified domain name
            id_remote_fqdn_domain ('str') : Match remote identity FQDN domain name
            id_remote_key_id ('str') : Match remote key id
            nat_encap ('Boolean') : NAT encapsulation force
            nat_keepalive ('int') : NAT keepalive interval 
            trustpoint ('str') : PKI trustpoint name
            trustpoint_verify ('boolean') : Trustpoint to verify True/False
            trustpoint_sign ('boolean') : Trustpoint to sign True/False
            ppk_dynamic ('str') : PPK config dynamic label
            ppk_manual ('str') : PPK config manual label
            reconnect_timer ('int') : AnyConnect Reconnect timer 
            ikev2_redirect ('Boolean') : IKEv2 Redirect enable True/False
            shutdown ('Boolean') : Shutdown ikev2 profile
            vt_number ('int') : Vurtual Template number
            vt_mode_auto ('Boolean') : Auto mode enable True/False
            dynamic_enabled ('Boolean') : Dynamic authentication method
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IKEV2 Profile"
    )

    configs = []
    configs.append(f"crypto ikev2 profile {profile_name}")
    
    if auth_method is not None and aaa_list is not None:
        configs.append(f"aaa accounting {auth_method} {aaa_list}")
    
    if auth_method == "anyconnect-eap" or auth_method == "eap" and aaa_list is not None:
        configs.append(f"aaa authentication {auth_method} {aaa_list}")
    
    if auth_type is not None and aaa_list is not None and auth_method is not None:
        configs.append(f"aaa authorization {auth_type} {auth_method} list {aaa_list}")
    
    if auth_type == "group" and override is True and aaa_list is not None and auth_method is not None:
        configs.append(f"aaa authorization group override {auth_method} list {aaa_list}")
    
    if auth_type == "user" and cached is True and auth_method != "cert" :
        configs.append(f"aaa authorization user {auth_method} cached")

    if anyconnect_prof_name is not None:
        configs.append(f"anyconnect profile {anyconnect_prof_name}")

    if local_auth == "rsa-sig" or local_auth == "ecdsa-sig":
        configs.append(f"authentication local {local_auth}")
    
    if local_auth == "eap" and auth_eap_method is not None and auth_uname is None and \
        auth_pwd_type is not None and auth_password is not None:
        configs.append(f"authentication local eap {auth_eap_method} password {auth_pwd_type} {auth_password}") 
    
    if local_auth == "eap" and auth_eap_method is not None and auth_uname is not None and \
        auth_pwd_type is not None and auth_password is not None:
        configs.append(f"authentication local eap {auth_eap_method} username {auth_uname} password {auth_pwd_type} {auth_password}")
        
    if local_auth == "eap" and auth_eap_method is not None and auth_uname is None and \
        auth_pwd_type is None and auth_password is not None:
        configs.append(f"authentication local eap {auth_eap_method} password {auth_password}") 

    if local_auth == "eap" and auth_eap_method is not None and auth_uname is not None and \
        auth_pwd_type is None and auth_password is not None:
        configs.append(f"authentication local eap {auth_eap_method} username {auth_uname} password {auth_password}")

    if local_auth == "pre-share" and auth_pwd_type is not None and auth_password is not None:
        configs.append(f"authentication local pre-share key {auth_pwd_type} {auth_password}") 
            
    if local_auth == "pre-share" and auth_pwd_type is None and auth_password is not None:
        configs.append(f"authentication local pre-share key {auth_password}") 

    if remote_auth == "rsa-sig" or remote_auth == "ecdsa-sig":
        configs.append(f"authentication remote {remote_auth}")

    if (local_auth == "rsa-sig" or local_auth == "ecdsa-sig") and remote_auth == "anyconnect-eap":
        if double_auth:
            configs.append(f"authentication remote {remote_auth} aggregate cert-request")
        else:
            configs.append(f"authentication remote {remote_auth} aggregate")
    
    
    if (local_auth == "rsa-sig" or local_auth == "ecdsa-sig") and remote_auth == "eap" and \
        eap_query == False and eap_timeout is not None:
        configs.append(f"authentication remote {remote_auth}")
    
    if (local_auth == "rsa-sig" or local_auth == "ecdsa-sig") and remote_auth == "eap" and eap_query:
        configs.append(f"authentication remote eap query-identity")

    if (local_auth == "rsa-sig" or local_auth == "ecdsa-sig") and remote_auth == "eap" and eap_timeout is not None:
        configs.append(f"authentication remote eap timeout {eap_timeout}")
    
    if remote_auth == "pre-share" and auth_pwd_type is not None and auth_password is not None:
        configs.append(f"authentication remote pre-share key {auth_pwd_type} {auth_password}") 
    
    if remote_auth == "pre-share" and auth_pwd_type is  None and auth_password is not None:
        configs.append(f"authentication remote pre-share key {auth_password}")
        
    
    if conf_exch_accept:
        configs.append(f"config-exchange request")

    if conf_set_accept:
        configs.append(f"config-exchange set accept")
    
    if conf_set_send:
        configs.append(f"config-exchange set send")

    if dpd_interval is not None and dpd_retry is not None and dpd_query is not None:
        configs.append(f"dpd {dpd_interval} {dpd_retry} {dpd_query}")
    
    if id_local:
        if id_local_addr is not None:
            configs.append(f"identity local address {id_local_addr}")
        
        if id_local_dn:
            configs.append(f"identity local dn")

        if id_local_email is not None:
            configs.append(f"identity local email {id_local_email}")
        
        if id_local_fqdn is not None:
            configs.append(f"identity local fqdn {id_local_fqdn}")
        
        if id_local_key_id is not None:
            configs.append(f"identity local key-id {id_local_key_id}")
        
    if initial_contact:
        configs.append(f"initial-contact force")
    
    if ivrf is not None:
        configs.append(f"ivrf {ivrf}")

    if keyring_aaa is not None:
        configs.append(f"keyring aaa {keyring_aaa}")

    if keyring_local is not None:
        configs.append(f"keyring local {keyring_local}")

    if lifetime is not None:
        configs.append(f"lifetime {lifetime}")
    
    if match_address is not None:
        configs.append(f"match address local {match_address}")

    if match_cert_map is not None:
        configs.append(f"match certificate {match_cert_map}")
    
    if match_fvrf is not None:
        configs.append(f"match fvrf {match_fvrf}")

    if id_remote:
        if id_remote_addr is not None:
            configs.append(f"match identity remote address {id_remote_addr}")
        
        if id_remote_any:
            configs.append(f"match identity remote any")

        if id_remote_email is not None:
            configs.append(f"match identity remote email {id_remote_email}")
        
        if id_remote_email_domain is not None:
            configs.append(f"match identity remote email domain {id_remote_email_domain}")
        
        if id_remote_fqdn is not None:
            configs.append(f"match identity remote fqdn {id_remote_fqdn}")

        if id_remote_fqdn_domain is not None:
            configs.append(f"match identity remote fqdn domain {id_remote_fqdn_domain}")
        
        if id_remote_key_id is not None:
            configs.append(f"match identity remite key-id {id_remote_key_id}")
    
    if local_auth is None and remote_auth is None and id_local == False and \
        id_remote == False and dynamic_enabled == True:
        configs.append(f"dynamic")

    if nat_encap:
        configs.append(f"nat force-encap")
    
    if nat_keepalive is not None:
        configs.append(f"nat keepalive {nat_keepalive}")
    if trustpoint is not None and trustpoint_verify is False and trustpoint_sign is False:
        configs.append(f"pki trustpoint {trustpoint}")
        
    if trustpoint is not None and trustpoint_verify:
        configs.append(f"pki trustpoint {trustpoint} verify")

    if trustpoint is not None and trustpoint_sign:
        configs.append(f"pki trustpoint {trustpoint} sign")

    if ppk_dynamic is not None:
        configs.append(f"ppk dynamic {ppk_dynamic}")

    if ppk_manual is not None:
        configs.append(f"ppk manual {ppk_dynamic}")
    
    if reconnect_timer is not None:
        configs.append(f"reconnect timeout {reconnect_timer}")

    if ikev2_redirect:
        configs.append(f"redirect gateway auth")
    
    if shutdown:
        configs.append(f"shutdown")
    
    if vt_number is not None and ivrf is None:
        configs.append(f"virtual-template {vt_number}")
    
    if vt_number is not None and ivrf is None and vt_mode_auto:
        configs.append(f"virtual-template {vt_number} mode auto")
    
    errors = [f"% vrf {ivrf} not configured",
    f"% Invalid keyring {keyring_local}",
    f"% No such trustpoint {trustpoint}",
    "Reconnect can not be configured if either Keyring, PSK  authentication or PSK authorization enabled in profile.",
    r" \! \(IKEv2 Cluster load-balancer is not enabled\)"
    ]
    try:
        device.configure(configs, error_pattern = errors)
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 profile,"
             "Error:\n{error}".format(error=e)
        )

def configure_ikev2_dpd(device,
                        interval=10,
                        retry=2,
                        dpd_query="on-demand"
                        ):
    """ Configures IKEV2 DPD
        Args:
            device (`obj`): Device object
            interval ('int', optional): dpd interval, default is 10
            retry ('int', optional): dpd retry, default is 2
            dpd_query ('str'): dpd query, default is on-demand
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring IKEV2 DPD"
    )

    configs = []
    configs.append(f"crypto ikev2 dpd {interval} {retry} {dpd_query}")
   
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 DPD,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_ikev2_fragmentation(device,
                        mtu
                        ):
    """ Configures IKEV2 Fragmentation
        Args:
            device (`obj`): Device object
            mtu ('int'): IKEv2 MTU 
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring IKEV2 Fragmentation"
    )

    configs = []
    configs.append(f"crypto ikev2 fragmentation mtu {mtu}")
   
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 fragmentation,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_ikev2_cac(device,
                        in_nego=0,
                        sa=0
                        ):
    """ Configures IKEV2 CAC
        Args:
            device (`obj`): Device object
            in_nego ('int', optional): Maximum IKEv2 in negotiation sa, default is 0
            sa ('int',optional): Maximum IKEv2 sa, default is 0
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring IKEV2 CAC"
    )

    configs = []
    if in_nego:
        configs.append(f"crypto ikev2 limit max-in-negotation-sa {in_nego}")
   
    if sa:
        configs.append(f"crypto ikev2 limit max-sa {sa}")
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 CAC,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_isakmp_key(device,
                         key,
                         key_type=None,
                         ipv4_address=None,
                         sub_mask=None,
                         host_name=None,
                         ipv6_prefix=None,
                         no_xauth=False):
    """ Configures ISAKMP key 
        Args:
            device (`obj`): Device object
            key_type ('int',optional): type of key that will follow
            key ('str', optional): preshared key
            ipv4_address ('str',optional): IPv4 address associated with the keyring
            sub_mask ('str',optional): subnet mask associated with the keyring
            host_name ('str',optional): hostname associated with the keyring
            ipv6_prefix ('str',optional): IPv6 address associated with the keyring
            no_xauth ('bool',optional): This option specifies if no_xauth needs to be configured or not
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring ISAKMP Key"
    )

    configs = []

    if no_xauth is False:
        if ipv4_address is not None:
            configs.append(f"crypto isakmp key {key_type} {key} address {ipv4_address} {sub_mask}")
        elif host_name is not None:
            configs.append(f"crypto isakmp key {key_type} {key} hostname {host_name}")
        elif ipv6_prefix is not None:
            configs.append(f"crypto isakmp key {key_type} {key} address ipv6 {ipv6_prefix}")
    else:
        if ipv4_address is not None:
            configs.append(f"crypto isakmp key {key_type} {key} address {ipv4_address} {sub_mask} no-xauth")
        elif host_name is not None:
            configs.append(f"crypto isakmp key {key_type} {key} hostname {host_name} no-xauth")
        elif ipv6_prefix is not None:
            configs.append(f"crypto isakmp key {key_type} {key} address ipv6 {ipv6_prefix} no-xauth")

    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure isakmp key,"
             "Error:\n{error}".format(error=e)
        )
        raise


def configure_isakmp_policy(device,
                            policy_number,
                            auth_type=None,
                            encr_algos=None,
                            dh_group=None,
                            hash=None,
                            default=None,
                            lifetime=None
                        ):
    """ Configures ISAKMP Policy
        Args:
            device (`obj`): Device object
            policy_number ('str'): isakmp policy number
            auth_type ('str', optional): autehntication type to be used
            default ('str', optional): set a command to its defaults
            encr_algos ('str', optional): encryption algorithms
            dh_group ('str', optional): Diffie Hellman group
            hash ('str', optional): hash algorithm for protection suite
            lifetime ('str', optional): lifetime for ISAKMP security association
        Returns:
            True/False
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring ISAKMP POLICY"
    )

    configs = []
    configs.append(f"crypto isakmp policy {policy_number}")
    if auth_type is not None:
        configs.append(f"authentication {auth_type}")
    if default is not None:
        configs.append(f"default {default}")
    if encr_algos is not None:
        configs.append(f"encryption {encr_algos}")
    if dh_group is not None:
        configs.append(f"group {dh_group}")
    if hash is not None:
        configs.append(f"hash {hash}")
    if lifetime is not None:
        configs.append(f"lifetime {lifetime}")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure isakmp policy,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_crypto_logging_ikev2(device):
    """ Configure IKEv2 Logging
        Args:
            device (`obj`): Device object
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Configure IKEv2 Logging")

    try:
        device.configure(["crypto logging ikev2"])
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure crypto logging ikev2. Error: {e}')

def unconfigure_crypto_logging_ikev2(device):
    """ Unconfigure IKEv2 Logging
        Args:
            device (`obj`): Device object
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure IKEv2 Logging")
    
    try:
        device.configure(["no crypto logging ikev2"])
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure crypto logging ikev2. Error: {e}')

def unconfigure_isakmp_policy(device,
                        policy_number
                        ):
    """ Unconfigures ISAKMP POLICY
        Args:
            device (`obj`): Device object
            policy_number ('str'): isakmp policy number
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring ISAKMP policy"
    )

    configs = []
    configs.append(f"no crypto isakmp policy {policy_number}")
   
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure isakmp policy,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_isakmp_key(device,
                        key,
                        key_type=None,
                        ipv4_address=None,
                        sub_mask=None,
                        host_name=None,
                        ipv6_prefix=None,
                        no_xauth=False):
    """ Unconfigures ISAKMP key 
        Args:
            device (`obj`): Device object
            key_type ('int', optional): type of key that will follow
            key ('str'): preshared key
            ipv4_address ('str',optional): IPv4 address associated with the keyring
            sub_mask ('str',optional): subnet mask associated with the keyring
            host_name ('str',optional): hostname associated with the keyring
            ipv6_prefix ('str',optional): IPv6 address associated with the keyring
            no_xauth ('str',optional): This option specifies if no_xauth needs to be configured or not
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring ISAKMP Key"
    )

    configs = []
    if no_xauth is False:
        if ipv4_address is not None:
            configs.append(f"no crypto isakmp key {key_type} {key} address {ipv4_address} {sub_mask}")
        elif host_name is not None:
            configs.append(f"no crypto isakmp key {key_type} {key} hostname {host_name}")
        elif ipv6_prefix is not None:
            configs.append(f"no crypto isakmp key {key_type} {key} address ipv6 {ipv6_prefix}")
    else:
        if ipv4_address is not None:
            configs.append(f"no crypto isakmp key {key_type} {key} address {ipv4_address} {sub_mask} no-xauth")
        elif host_name is not None:
            configs.append(f"no crypto isakmp key {key_type} {key} hostname {host_name} no-xauth")
        elif ipv6_prefix is not None:
            configs.append(f"no crypto isakmp key {key_type} {key} address ipv6 {ipv6_prefix} no-xauth")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure isakmp key,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_ikev2_proposal(device,
                        proposal_name
                        ):
    """ Unconfigures IKEV2 Policy
        Args:
            device (`obj`): Device object
            proposal_name ('str'): ikev2 proposal name
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring IKEV2 proposal"
    )

    configs = []
    configs.append(f"no crypto ikev2 proposal {proposal_name}")
   
    try:
        device.configure(configs, error_pattern=[r'% Cannot remove as proposal is in use\.'])
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 policy,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_ikev2_policy(device,
                        policy_name
                        ):
    """ Unconfigures IKEV2 Policy
        Args:
            device (`obj`): Device object
            policy_name ('str'): ikev2 policy name
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring IKEV2 Policy"
    )

    configs = []
    configs.append(f"no crypto ikev2 policy {policy_name}")
   
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ikev2 policy,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_ikev2_dpd(device,
                        interval,
                        retry,
                        dpd_query
                        ):
    """ Unconfigure IKEV2 DPD
        Args:
            device (`obj`): Device object
            interval ('int'): Determine in what interval Dead Peer Detection should happen
            retry ('int'): Number of time DPD should retry before making the peer dead 
            dpd_query ('str'): Determine whether query is on-demand or periodic
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring IKEV2 DPD"
    )

    configs = []
    configs.append(f"no crypto ikev2 dpd {interval} {retry} {dpd_query}")
   
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure ikev2 DPD,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_ikev2_fragmentation(device,
                        mtu
                        ):
    """ Unonfigure IKEV2 Fragmentation
        Args:
            device (`obj`): Device object
            mtu ('int'): IKEv2 MTU Fragmentation
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring IKEV2 Fragmentation"
    )

    configs = []
    configs.append(f"no crypto ikev2 fragmentation mtu {mtu}")
   
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure ikev2 fragmentation,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_ikev2_cac(device,
                        in_nego,
                        sa=0
                        ):
    """ Unonfigure IKEV2 CAC
        Args:
            device (`obj`): Device object
            in_nego ('int'): Maximum IKEv2 in negotiation sa
            sa ('int',optional): Maximum IKEv2 sa, default is 0
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring IKEV2 CAC"
    )

    configs = []
    if in_nego:
        configs.append(f"no crypto ikev2 limit max-in-negotation-sa {in_nego}")
   
    if sa:
        configs.append(f"no crypto ikev2 limit max-sa {sa}")
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure ikev2 CAC,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_ikev2_authorization_policy(device,
                    policy_name
                    ):
    """ Unonfigure IKEV2 Authorization policy
        Args:
            device (`obj`): Device object
            policy_name ('str'): IKEv2 authorization policy
        Returns:
            NA
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring IKEV2 Authorization Policy"
    )

    configs = []
    configs.append(f"no crypto ikev2 authorization policy {policy_name}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure ikev2 authorization policy,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_ikev2_keyring(device,keyring_name):
    """ Unconfigure IKEV2 keyring
        Args:
            device (`obj`): Device object
            keyring_name ('str'): Name for the keyring

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "unConfiguring IKEV2 keyring"
    )

    configs = []
    configs.append("no crypto ikev2 keyring {keyring_name}".format(keyring_name=keyring_name))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to  unconfigure ikev2 keyring "
            "on device {dev}. Error:\n{error}".format(
                dev=device,
                error=e,
            )
        )
        
def unconfigure_ikev2_profile(device,profile_name):
    """ unconfigure IKEV2 profile
        Args:
            device (`obj`): Device object
            profile_name ('str'): ikev2 profile name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "unconfiguring IKEV2 Profile"
    )

    configs = []
    configs.append("no crypto ikev2 profile {profile_name}".format(profile_name=profile_name))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to  unconfigure ikev2 Profile "
            "on device {dev}. Error:\n{error}".format(
                dev=device,
                error=e,
            )
        )

def clear_crypto_session(device,
                active=False,
                ikev2=False,
                fvrf=None,
                timeout=30):
    """ Clear crypto session
        Args:
            device (`obj`): Device object
            active('boolean', optional): clear active session, default is False
            ikev2('boolean', optional): Clear ikev2 based sessions, default is False
            fvrf('str', optional): Front door VRF name, default is None
            timeout('int', optional): timeout for exec command execution, default is 30
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Clearing crypto session"
    )
    cmd = f"clear crypto session"
    if active:
        cmd += " active"

    if ikev2:
        cmd += " ikev2"

    if fvrf is not None:
        cmd += f" fvrf {fvrf}"

    try:    
        device.execute(cmd, 
            error_pattern=[f' No VRF named {fvrf} exists',r'% Invalid input detected at \'\^\' marker\.'], 
            timeout=timeout)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear crypto session on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def clear_crypto_call_admission_stats(device):
    """ clear crypto call admission stats
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Clearing crypto ikev1 statistics"
    )

    try:
        device.execute(
            "clear crypto call admission statistics"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear crypto call admission stats. Error:\n{error}".format(error=e)
        )

def disable_crypto_engine_compliance(device):
    """ Disable CSDL
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Disabling CSDL. write mem and reload device is required ")

    try:
        device.configure(["crypto engine compliance shield disable"])
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not disable. Error: {e}')

def unconfigure_ppk_on_keyring(device,
                            keyring_name,
                            peer_name,
                            peer_ip=None,
                            peer_mask=None,
                            key=None,
                            required=True,
                            ppk_id=None,
                            ppk_key=None,
                            sks_client_config_block_name=None):
    """ unconfigures IKEV2 keyring or Preshared Key (PSK)
        Args:
            device (`obj`): Device object
            keyring_name ('str'): Name for the keyring
            peer_name ('str'): peer name
            peer_ip ('str',optional): peer ip addr
            peer_mask ('str',optional): peer nw mask
            key ('str',optional): preshared key
            required ('boolean',optional): Required option for PPK
            ppk_id ('str',optional): ppk id for manual ppk
            ppk_key ('str',optional): Post-quantum preshared key
            sks_client_config_block_name ('str',optional): SKS client config block name
        Returns:
            None
        Raises:
            SubCommandFailure
    """


    log.info(
        "unconfiguring ppk Key"
    )

    configs = []
    configs.append("crypto ikev2 keyring {keyring_name}".format(keyring_name=keyring_name))
    configs.append("peer {peer_name}".format(peer_name=peer_name))
    if peer_ip is not None and peer_mask is not None:
        configs.append("no address {peer_ip} {peer_mask}".format(peer_ip=peer_ip,peer_mask=peer_mask))
    if key is not None:
        configs.append("no pre-shared-key {key}".format(key=key))
    if ppk_key is not None:
        cmd = f'no ppk manual id {ppk_id} key {ppk_key}'
        if required:
            cmd += ' required'
        configs.append(cmd)
    if sks_client_config_block_name is not None:
        cmd = f"no ppk dynamic {sks_client_config_block_name}"
        if required:
            cmd += ' required'
        configs.append(cmd)
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to  unconfigure ikev2 keyring "
            "on device {dev}. Error:\n{error}".format(
                dev=device,
                error=e,
            )
        )

def configure_modify_ikev2_profile(device,
                            profile_name,
                            remote_addr = None,
                            local_add = None,
                            remote_auth = None,
                            local_auth = None,
                            keyring_type = None,
                            keyring_name = None,
                            lifetime = None):

    """ Configures IKEV2 keyring or Preshared Key (PSK)
        Args:
            device (`obj`): Device object
            profile_name ('str'): ikev2 profile name
            remote_addr ('str'): peer/remote ip address
            remote_auth ('str'): remote authentication method
            local_auth ('str'): local authentication method
            keyring ('str'): ikev2 keyring name
            dpd_hello_time ('int'): DPD R-U-THERE interval
            dpd_retry_time ('int'): DPD Retry Interval
            dpd_query ('str'): DPD queires on-demand or periodic
            lifetime ('int') Optional : configuring session lifetime
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.info(
        "Configuring IKEV2 Profile"
    )

    configs = [f"crypto ikev2 profile {profile_name}"]    
    configs.append(f"crypto ikev2 profile {profile_name}")
    if remote_addr is not None:
        configs.append(f"match identity remote {remote_addr}")
    if local_add is not None:
        configs.append(f"identity local {local_add}")
    if remote_auth is not None:
        configs.append(f"authentication remote {remote_auth}")
    if local_auth is not None:
        configs.append(f"authentication local {local_auth}")
    if keyring_type in ('ppk', 'local'):
        configs.append(f"keyring {keyring_type} {keyring_name}")        
    if lifetime is not None:
        configs.append(f"lifetime {lifetime}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ikev2 params under profile "
            "on device {dev}. Error:\n{error}".format(
                dev=device,
                error=e,
            )
        )

def unconfigure_modify_ikev2_profile(device,
                            profile_name,
                            remote_addr = None,
                            local_add = None,
                            remote_auth = None,
                            local_auth = None,
                            keyring_type = None,
                            keyring_name = None,
                            lifetime = None):
    """ Unconfigures IKEV2 keyring or Preshared Key (PSK)
        Args:
            device (`obj`): Device object
            profile_name ('str'): ikev2 profile name
            remote_addr ('str'): peer/remote ip address
            remote_auth ('str'): remote authentication method
            local_auth ('str'): local authentication method
            keyring ('str'): ikev2 keyring name
            lifetime ('int') : configuring session lifetime
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "unconfiguring IKEV2 Profile parameters"
    )

    configs = [f"crypto ikev2 profile {profile_name}"]    
    if remote_addr is not None:
        configs.append(f"no match identity remote {remote_addr}")
    if local_add is not None:
        configs.append(f"no identity local {local_add}")
    if remote_auth is not None:
        configs.append(f"no authentication remote {remote_auth}")
    if local_auth is not None:
        configs.append(f"no authentication local {local_auth}")
    if keyring_type in ('ppk', 'local'):
        configs.append(f"no keyring {keyring_type} {keyring_name}")        
    if lifetime is not None:
        configs.append(f"no lifetime {lifetime}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ikev2 params under profile "
            "on device {dev}. Error:\n{error}".format(
                dev=device,
                error=e,
            )
        )

