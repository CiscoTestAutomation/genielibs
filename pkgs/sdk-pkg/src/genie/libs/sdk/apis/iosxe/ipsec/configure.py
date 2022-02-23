"""Common configure/unconfigure functions for IPSEC"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def clear_crypto_sa_counters(device):
    """ Clear all the ipsec sa counters
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Clearing crypto sa counters"
    )

    try:
        device.execute(
            "clear crypto sa counters"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear crypto sa counters. Error:\n{error}".format(error=e)
        )


def configure_ipsec_transform_set(device,
                transform_set_name,
                transform_method,
                transform_auth=None,
                transform_bit=None,
                ecn=True,
                mode="tunnel",
                transport_require=False
                ):
    """ Configures ipsec transform set
        Args:
            device (`obj`): Device object
            transform_set_name ('str'): transform-set name
            transform_method ('str'): transform method e.g. esp-gcm, esp-md5-hmac
            transform_auth ('str'): Auth transform 
            transform_bit ('str'): transform bit keys
            esn ('boolean'): setting esn
            mode ('str'): Tunnel and transform mode
            transport_require('boolean'): enabling transport require

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IPSEC transform set"
    )

    configs = []
    if transform_auth is None and transform_bit is None:
        configs.append(f"crypto ipsec transform-set {transform_set_name} {transform_method}")
    
    if transform_auth is not None and transform_bit is None:
        configs.append(f"crypto ipsec transform-set {transform_set_name} {transform_auth} {transform_method}")
    
    if transform_auth is not None and transform_bit is not None:
        configs.append(f"crypto ipsec transform-set {transform_set_name} {transform_auth} {transform_method} {transform_bit}")

    if ecn is True:
        configs.append("esn")

    if mode == 'tunnel':
        configs.append(f"mode {mode}")
    else:
        if transport_require:
            configs.append("mode transport require")
        else:
            configs.append("mode transport")


    try:
        device.configure(configs, error_pattern = ["Proposal with ESP is missing cipher"])
    except SubCommandFailure as e:
        log.error("Failed to configure ipsec transform-set"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_crypto_transform_set(device, transform_name, cipher, ah='', mode='tunnel', esn=None, defaultMode=None):
    """ Configures Crypto IPsec
        Args:
            device ('obj')    : device to use
            transform_name ('str).  Transform set name
            cipher ('str). ESP header type (i.e  esp-aes, esp-gcm)
            ah ('str',optional) Authentication (i.e esp-sha-hmac) (Default '')
            mode ('str',optional) Tunnel mode (i.e transparent,tunnel) (Default tunnel)
            esn: ('str',optional) Boolean.
            default: ('str',optional). Set to defaults (options are 'esn' or 'mode')
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = []
    config_list.append("crypto ipsec transform-set {transform_name} {cipher} "
                       "{ah}".format(transform_name=transform_name,cipher=cipher,ah=ah))
    if esn:
        config_list.append("esn")
    config_list.append("mode {mode}".format(mode=mode))
    if defaultMode:
        config_list.append("default {defaultMode}".format(defaultMode=defaultMode))
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure Crypto IPsec Transform-set. Error:\n{e}'.format(e=e)
        )

def unconfigure_crypto_transform_set(device, transform_name):
    """ Configures switchport mode on interface
        Args:
            device ('obj')    : device to use
            transform_name ('str).  Transform set name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure([
            "no crypto ipsec transform-set {transform_name}".format(transform_name=transform_name),
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure Crypto IPsec Transform-set. Error:\n{e}'.format(e=e)
        )

def configure_ipsec_profile(device,
                            profile_name,
                            transform_set_name,
                            ikev2_profile_name,
                            isakmp_profile_name=None,
                            is_responder_only=False,
                            sa_dfbit_clear=False,
                            sa_dfbit_copy=False,
                            sa_dfbit_set=False,
                            ecn_discard=False,
                            ecn_propagate=False,
                            idle_time=None,
                            sa_granularity=False,
                            sa_life_days=None,
                            sa_life_kb_disable=False,
                            sa_life_kbytes=None,
                            sa_life_sec=None,
                            replay_disable=False,
                            replay_window=None,
                            sa_policy_limit=None,
                            mixed_mode=False,
                            pfs_group=None,
                            rr_distance=None,
                            rr_gateway=None,
                            rr_tag=None,
                            identity_name=None,
                            rr_route=None,
                            rr_static=False,
                            redundancy_name=None,
                            stateful=False
                            ):
    """ Configures ipsec transform set
        Args:
            device (`obj`): Device object
            profile_name ('str'): ipsec profile name
            transform_set_name ('str'): transform-set name
            ikev2_profile_name ('str'): ikev2 profile name
            isakmp_profile_name ('str'): isakmp profile name
            is_responder_only ('boolean'): Do not initiate SAs
            sa_dfbit_clear ('boolean'): Clear DF bit for encapsulated packets
            sa_dfbit_copy ('boolean'): Copy DF bit from inner for encapsulated packets
            sa_dfbit_set ('boolean'): Set DF bit for encapsulated packets
            ecn_discard ('boolean'): Discard the Explicit Congestion Notification
            ecn_propagate ('boolean'): Propagate the Explicit Congestion Notification
            idle_time ('int'): Automatically delete IPSec SAs after a given idle period
            sa_granularity ('boolean'): granularity to host level
            sa_life_days ('int'): Security association duration in days
            sa_life_kb_disable ('boolean'): Disable Volume-based Rekey
            sa_life_kbytes ('int'): Security association duration in kilobytes
            sa_life_sec ('int'): Security association duration in seconds
            replay_disable ('boolean'): SA replay disable
            replay_window ('int'): SA replay window size
            sa_policy_limit ('int'): Set security-policy limit
            mixed_mode ('boolean'): Enable mixed mode
            pfs_group ('int') : set PFS group
            rr_distance ('int') : Routing distance
            rr_gateway ('str') : Next hop IPv4/IPv6 address of the gateway
            rr_tag ('str') : Routing Tag ID
            identity_name ('str') : Identity name
            rr_route ('str') : IPv4 address overrides remote tunnel endpoint
            rr_static ('boolean') : Create routes based on static ACLs permanently
            redundancy_name ('str') : Redundancy group name
            stateful ('boolean') : enable stateful failover
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IPSEC profile"
    )

    configs = []
    configs.append(f"crypto ipsec profile {profile_name}")
    configs.append(f"set transform-set {transform_set_name}")
    configs.append(f"set ikev2-profile {ikev2_profile_name}")

    if isakmp_profile_name is not None:
        configs.append(f"set isakmp-profile {isakmp_profile_name}")

    if is_responder_only:
        configs.append("responder-only")

    if sa_dfbit_clear:
        configs.append("set security-association dfbit clear")

    if sa_dfbit_copy:
        configs.append("set security-association dfbit copy")

    if sa_dfbit_set:
        configs.append("set security-association dfbit set")

    if ecn_discard:
        configs.append("set security-association ecn discard")
    
    if ecn_propagate:
        configs.append("set security-association ecn propagate")
    
    if idle_time is not None:
        configs.append(f"set security-association idle-time {idle_time}")

    if sa_granularity:
        configs.append("set security-association level per-host")

    if sa_life_days is not None:
        configs.append(f"set security-association lifetime days {sa_life_days}")
    
    if sa_life_kbytes is not None:
        configs.append(f"set security-association lifetime kilobytes {sa_life_kbytes}")

    if sa_life_kb_disable:
        configs.append("set security-association lifetime kilobytes disable")

    if sa_life_sec is not None:
        configs.append(f"set security-association lifetime seconds {sa_life_sec}")

    if replay_disable:
        configs.append("set security-association replay disable")

    if replay_window:
        configs.append(f"set security-association replay window-size {replay_window}")

    if sa_policy_limit is not None:
        configs.append(f"set security-policy limit {sa_policy_limit}")

    if mixed_mode:
        configs.append("set mixed-mode")
    
    if pfs_group is not None:
        configs.append(f"set pfs {pfs_group}")
    
    if rr_distance is not None:
        configs.append(f"set reverse-route distance {rr_distance}")

    if rr_gateway is not None:
        configs.append(f"set reverse-route gateway {rr_gateway}")

    if rr_tag is not None:
        configs.append(f"set reverse-route tag {rr_tag}")

    if identity_name is not None:
        configs.append(f"set identity {identity_name}")

    if rr_route is not None:
        configs.append(f"reverse-route remote-peer {rr_route}")

    if rr_static:
        configs.append(f"reverse-route static")

    if redundancy_name is not None and stateful:
        configs.append(f"redundancy {redundancy_name} stateful")
    
    if redundancy_name is not None and stateful == False:
        configs.append(f"redundancy {redundancy_name}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ipsec profile,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_ipsec_profile(device, profile_name):
    """ Unconfigures ipsec profile
        Args:
            device (`obj`): Device object
            profile_name ('str'): ipsec profile name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring IPSEC profile"
    )

    configs = []
    configs.append("no crypto ipsec profile {profile_name}".format(profile_name=profile_name))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure ipsec profile,"
             "Error:\n{error}".format(error=e)
        )
        raise


def configure_ipsec_tunnel(device,
                            tunnel_intf,
                            tunnel_ip,
                            tunnel_mask,
                            tunnel_src_ip,
                            tunnel_mode,
                            tunnel_dst_ip,
                            ipsec_profile_name):
    """ Configures ipsec transform set
        Args:
            device (`obj`): Device object
            tunnel_intf ('str'): tunnel interface
            tunnel_ip ('str'): tunnel ip addr
            tunnel_mask ('str'): tunnel mask
            tunnel_src_ip ('str'): tunnel source IP
            tunnel_mode ('str'): ipv4 or ipv6
            tunnel_dst_ip ('str'): tunnel destination IP
            ipsec_profile_name ('str'): IPSEC profile name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IPSEC tunnel"
    )

    configs = []
    configs.append("interface {tunnel_intf}".format(tunnel_intf=tunnel_intf))
    configs.append("ip address {tunnel_ip} {tunnel_mask}".format(tunnel_ip=tunnel_ip,tunnel_mask=tunnel_mask))
    configs.append("tunnel source {tunnel_src_ip}".format(tunnel_src_ip=tunnel_src_ip))
    configs.append("tunnel destination {tunnel_dst_ip}".format(tunnel_dst_ip=tunnel_dst_ip))
    configs.append("tunnel mode ipsec {tunnel_mode}".format(tunnel_mode=tunnel_mode))
    configs.append("tunnel protection ipsec profile {ipsec_profile_name}".format(ipsec_profile_name=ipsec_profile_name))


    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ipsec tunnel,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_crypto_ikev2_keyring(device, keyring_name, peer_name=None, preshare_key=None, address='0.0.0.0', mask='0.0.0.0', type='ipv4'):
    """ Configure Cryto Ikev2 Keyring
    Args:
        device (`obj`): Device object
        keyring_name (`str`): Keyring name
        peer_name (`str`,optional): Peer name for the tunnel endpoint (Default None)
        preshare_key (`str`,optional): Share key between tunnel endpoints (Default None)
        address (`str`,optional): IPv4 or IPv6 address (i.e 1.1.1.1 or 1:1:1::1) (Default 0.0.0.0)
        mask (`str`,optional): IPv4 or IPv6 mask (i.e 0.0.0.0 or 128) (Default 0.0.0.0)
        type (`str`,optional): IP protocol (ipv4 or ipv6) (Default ipv4)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    config_list = []
    config_list.append('crypto ikev2 keyring {keyring_name}'.format(keyring_name=keyring_name))
    # Configure Peer Attributes
    if peer_name:
        config_list.append('peer {peer_name}'.format(peer_name=peer_name))
        if (type=='ipv4'):
            config_list.append('address {address} {mask}'.format(address=address,mask=mask))
        else:
            config_list.append('address {address}/{mask}'.format(address=address, mask=mask))
    if preshare_key:
        config_list.append('pre-shared-key {preshare_key}'.format(preshare_key=preshare_key))
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure Crypto Ikev2 Keyring. Error: {error}'.format(error=e)
        )

def unconfigure_crypto_ikev2_keyring(device,keyring):
    """ Unconfigure Crypto Ikev2 Keyring
    Args:
        device (`obj`): Device object
        keyring (`str`): Radius server name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no crypto ikev2 keyring {keyring}".format(keyring=keyring),
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Crypto keyring. Error: {error}".format(error=e)
        )

def configure_ikev2_profile_pre_share(device, profile_name, auth_local='pre-share', auth_remote='pre-share',
                                    keyring=None, address=None,mask='', protocol='ipv4',
                                    dpd_interval=None, dpd_retry='2', dpd_type='periodic'):
    """ Configure Ikev2 Profile with pre-share option
        Args:
            device ('obj')    : device to use
            profile_name ('str).  Ikev2 Profile Name
            auth_local ('str,optional). Authentication local (Default is pre-share)
            auth_remote ('str',optional) Authentication (i.e esp-sha-hmac) (Default is pre-share)
            keyring ('str',optional) Ikev2 Keyring name (needs to be pre-configured) (Default is None)
            address ('str',optional) Matching address (i.e 100.0.0.2) (Default is None)
            mask ('str',optional)  Address Mask (i.e 255.255.255.255 or 64) (Default is '')
                Optional for IPv4, mandatory for IPv6
            protocol ('str',optional) Protocol being used on address (Default is ipv4)
            dpd_interval ('str',optional) DPD interval (Default None)
            dpd_retry ('str',optional) DPD Retries (Default 2)
            dpd_type ('str',optional) DPD type (ie periodic or on-demand) (Default periodic)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = []
    config_list.append("crypto ikev2 profile {profile_name}".format(profile_name=profile_name))
    if address:
        if protocol == 'ipv4':
                config_list.append("match identity remote address {address} {mask}".format(address=address, mask=mask))
        else:
            # IPv6 Match Address
            config_list.append("match identity remote address {address}/{mask}".format(address=address,mask=mask))
    if auth_local:
        config_list.append("authentication local {auth_local}".format(auth_local=auth_local))
    if auth_remote:
        config_list.append("authentication remote {auth_remote}".format(auth_remote=auth_remote))
    if keyring:
        config_list.append("keyring local {keyring}".format(keyring=keyring))
    if dpd_interval:
        config_list.append("dpd {interval} {retry} {type}".format(interval=dpd_interval,
                                                                  retry=dpd_retry, type=dpd_type))

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure Crypto IPsec Profile. Error: {error}'.format(error=e)
        )

def unconfigure_ikev2_profile_pre_share(device, profile_name):
    """ Unconfigure ikev2 Profile
        Args:
            device ('obj')    : device to use
            profile_name ('str).  Ikev2 Profile Name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = []
    config_list.append("no crypto ikev2 profile {profile_name}".format(profile_name=profile_name))

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure Crypto IPsec Profile. Error: {error}'.format(error=e)
        )


