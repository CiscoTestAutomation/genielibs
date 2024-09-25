"""Common configure/unconfigure functions for IPSEC"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)

def configure_sks_client(device,
                         sks_client_config_block_name,
                         ip_mode,
                         server_ip_address,
                         server_port_number,
                         psk_identity,
                         password_string):
    """ Configures SKS client
        Args:
            device (`obj`): Device object
            sks_client_config_block_name ('str'): Name of the SKS-Client config block.
            ip_mode ('str'): ip mode (ipv4/ipv6)
            server_IP_address ('str'): Server ipv4/ipv6 address
            server_port_number ('str'): Port configuration
            psk_identity ('str'): Key identity
            password ('str'): Unencrypted password
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring sks client"
    )

    configs = []
    configs.append(f"crypto skip-client {sks_client_config_block_name}")
    configs.append(f"server {ip_mode} {server_ip_address} port {server_port_number}")
    configs.append(f"psk id {psk_identity} key 0 {password_string}")


    try:
        device.configure(configs, error_pattern = ["Proposal with ESP is missing cipher"])
    except SubCommandFailure as e:
        log.error("Failed to configure sks cient"
             "Error:\n{error}".format(error=e)
        )
        raise e

def unconfigure_sks_client(device,
                           sks_client_config_block_name):
    """ Configures SKS client
        Args:
            device (`obj`): Device object
            sks_client_config_block_name ('str'): Name of the SKS-Client config block.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring sks client"
    )

    configs = []
    configs.append(f"no crypto skip-client {sks_client_config_block_name}")

    try:
        device.configure(configs, error_pattern = ["Proposal with ESP is missing cipher"])
    except SubCommandFailure as e:
        log.error("Failed to configure sks cient"
             "Error:\n{error}".format(error=e)
        )
        raise e




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

    if transform_auth is None and transform_bit is not None:
        configs.append(f"crypto ipsec transform-set {transform_set_name} {transform_method} {transform_bit}")

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
                            ikev2_profile_name=None,
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
                            stateful=False,
                            rr_enable=None
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
            rr_enable ('str') : Create routes based on ACLs permanently            
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
    if ikev2_profile_name:
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

    if rr_enable:
        configs.append(f"reverse-route")

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
                            ipsec_profile_name,
                            v6_overlay=False,
                            vrf=None,
                            tunnel_vrf=None,
                            tunnel_ipv6=None,
                            desc=None,
                            tunnel_mode_protocol='ipsec',
                            pmtud=False):
    """ Configures ipsec tunnel interface
        Args:
            device (`obj`): Device object
            tunnel_intf ('str'): tunnel interface
            tunnel_ip ('str'): tunnel ip addr
            tunnel_mask ('str'): tunnel mask
            tunnel_src_ip ('str'): tunnel source IP
            tunnel_mode ('str'): ipv4 or ipv6 or dual-overlay
            tunnel_dst_ip ('str'): tunnel destination IP
            ipsec_profile_name ('str'): IPSEC profile name
            v6-overlay ('boolean', optional): True if v6-over-ipv4. Default is False
            vrf ('str',optional): overlay or ivrf of the tunnel, default is None
            tunnel_vrf ('str',optional): underlay or fvrf name, default is None
            tunnel_ipv6 ('str'): tunnel ipv6 addr with mask eg.) A::1/128
            desc ('str'): description on tunnel interface
            tunnel_mode_protocol ('str'): tunnel mode protocol. Defaults to ipsec 
            pmtud ('bool'): Path MTU Discovery. Defaults to False

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring IPSEC tunnel"
    )

    configs = []
    configs.append(f"interface {tunnel_intf}")
    if desc:
        configs.append(f"description {desc}")
    if vrf:
        configs.append("vrf forwarding {vrf}".format(vrf=vrf))
    configs.append(f"ip address {tunnel_ip} {tunnel_mask}")
    if tunnel_ipv6:
        configs.append(f"ipv6 address {tunnel_ipv6}")
    configs.append(f"tunnel mode {tunnel_mode_protocol} {tunnel_mode}")
    configs.append(f"tunnel source {tunnel_src_ip}")
    configs.append(f"tunnel destination {tunnel_dst_ip}")
    if tunnel_vrf:
        configs.append(f"tunnel vrf {tunnel_vrf}")
    configs.append(f"tunnel protection ipsec profile {ipsec_profile_name}")
    if v6_overlay:
        configs.append(f"tunnel mode ipsec {tunnel_mode} v6-overlay")
    if pmtud:
        configs.append("tunnel path-mtu-discovery")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ipsec tunnel, Error:\n{e}"
        )

def configure_crypto_ikev2_keyring(device, keyring_name, peer_name=None, preshare_key=None, address='0.0.0.0', mask='0.0.0.0', type='ipv4'):
    """ Configure Crypto Ikev2 Keyring
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
                                    keyring=None, address=None, mask='', protocol='ipv4',
                                    dpd_interval=None, dpd_retry='2', dpd_type='periodic',
                                    fvrf=None, lifetime=None, local_interface=None):

    """ Configure Ikev2 Profile with pre-share option
        Args:
            device ('obj')    : device to use
            profile_name ('str)  Ikev2 Profile Name
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
            fvrf ('str',optional) FVRF name (Default None)
            lifetime ('str',optional) lifetime in secs (Default is None)
            local_interface ('str', optional) interface name  (Default is None)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    #initialize list variable
    config_list = []
    config_list.append("crypto ikev2 profile {profile_name}".format(profile_name=profile_name))
    if fvrf:
        config_list.append("match fvrf {fvrf}".format(fvrf=fvrf))
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
    if lifetime:
        config_list.append("lifetime {lifetime}".format(lifetime=lifetime))
    if local_interface:
        config_list.append("match address local interface {local_interface}".format(local_interface=local_interface))

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

def configure_crypto_ikev2_proposal(device, proposal_name,
                                    encryption_name=None,
                                    integrity_name=None,
                                    group_number=None):
    """ Configure Cryto Ikev2 proposal
    Args:
        device (`obj`): Device object
        proposal_name (`str`): proposal name
        encryption_name (`str`,optional): name of encryption (Default None)
        integrity_name (`str`,optional): name of integrity (Default None)
        group_number (`str`,optional): group number (Default None)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    config_list = []
    config_list.append(f'crypto ikev2 proposal {proposal_name}')
    # Configure Peer Attributes
    if encryption_name:
        config_list.append(f'encryption {encryption_name}')
    if integrity_name:
        config_list.append(f'integrity {integrity_name}')
    if group_number:
        config_list.append(f'group {group_number}')
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure Crypto Ikev2 Keyring. Error: {e}'
        )

def unconfigure_crypto_ikev2_proposal(device, proposal_name):
    """ Unconfigure Crypto Ikev2 proposal
    Args:
        device (`obj`): Device object
        proposal_name (`str`): proposal name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            f"no crypto ikev2 proposal {proposal_name}"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure Crypto proposal. Error: {e}"
        )

def configure_crypto_ipsec_nat_transparency(device):
    """ Configure crypto ipsec nat-transparency udp-encapsulation
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    config = 'crypto ipsec nat-transparency udp-encapsulation'

    # Configure Peer Attributes
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure crypto ipsec nat-transparency udp-encapsulation. Error: {e}'
        )

def unconfigure_crypto_ipsec_nat_transparency(device):
    """ Configure no crypto ipsec nat-transparency udp-encapsulation
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    unconfig = 'no crypto ipsec nat-transparency udp-encapsulation'

    # Configure Peer Attributes
    try:
        device.configure(unconfig)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure crypto ipsec nat-transparency udp-encapsulation. Error: {e}'
        )

def configure_ipsec_fragmentation(device,
                after_encr=False,
                before_encr=False):
    """ Configure IPSec Fragmentation
        Args:
            device ('obj')    : device to use
            after_encr ('boolean', optional) :  Perform fragmentation of large packets after IPSec
                    encapsulation, default is False
            before_encr ('boolean', optional) : Perform fragmentation of large packets before IPSec
                    encapsulation, default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring IPSec fragmentation"
    )
    config_list = []
    if after_encr:
        config_list.append("crypto ipsec fragmentation after-encryption")

    if before_encr:
        config_list.append("crypto ipsec fragmentation before-encryption")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure Crypto IPsec Fragmentation. Error: {error}'.format(error=e)
        )

def configure_ipsec_df_bit(device,
                clear=False,
                copy=False,
                set=False):
    """ Configure IPSec DF bit
        Args:
            device ('obj')    : device to use
            clear ('boolean', optional) :  Clear DF bit for encapsulated packets, default is False
            copy ('boolean', optional) :  Copy DF bit from inner for encapsulated packets, default is False
            set ('boolean', optional) : Set DF bit for encapsulated packets, default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring IPSec df bit"
    )
    config_list = []
    if clear:
        config_list.append("crypto ipsec df-bit clear")

    if copy:
        config_list.append("crypto ipsec df-bit copy")

    if set:
        config_list.append("crypto ipsec df-bit set")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure Crypto IPsec DF bit. Error: {error}'.format(error=e)
        )

def configure_ipsec_sa_global(device,
                            ecn_discard=False,
                            ecn_propagate=False,
                            idle_time=None,
                            sa_life_days=False,
                            sa_life_kb_disable=False,
                            sa_life_kbytes=None,
                            sa_life_sec=False,
                            replay_disable=False,
                            replay_window=None,
                            multi_sn=False
                            ):
    """ Configures IPSec SA global parameters
        Args:
            device ('obj'): device to use
            ecn_discard ('boolean', optional): Discard the Explicit Congestion Notification, default is False
            ecn_propagate ('boolean', optional): Propagate the Explicit Congestion Notification, default is False
            idle_time ('int', optional): Automatically delete IPSec SAs after a given idle period, default is None
            sa_life_days ('boolean', optional): Security association duration in days, default is False
            sa_life_kb_disable ('boolean', optional): Disable Volume-based Rekey, default is False
            sa_life_kbytes ('int', optional): Security association duration in kilobytes, default is None
            sa_life_sec ('boolean', optional): Security association duration in seconds, default is False
            replay_disable ('boolean', optional): SA replay disable, default is False
            replay_window ('int', optional): SA replay window size, default is None
            multi_sn ('boolean', optional): Enable multiple sequence number per IPSec SA, default is False

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring IPSec security association parameters"
    )

    configs = []

    if ecn_discard:
        configs.append("crypto ipsec security-association ecn discard")

    if ecn_propagate:
        configs.append("crypto ipsec security-association ecn propagate")

    if idle_time is not None:
        configs.append(f"crypto ipsec security-association idle-time {idle_time}")

    if sa_life_days:
        configs.append(f"crypto ipsec security-association lifetime days 1")

    if sa_life_kbytes is not None:
        configs.append(f"crypto ipsec security-association lifetime kilobytes {sa_life_kbytes}")

    if sa_life_kb_disable:
        configs.append("crypto ipsec security-association lifetime kilobytes disable")

    if sa_life_sec:
        configs.append(f"crypto ipsec security-association lifetime seconds 86400")

    if replay_disable:
        configs.append("crypto ipsec security-association replay disable")

    if replay_window:
        configs.append(f"crypto ipsec security-association replay window-size {replay_window}")

    if multi_sn:
        configs.append("crypto ipsec security-association multi-sn")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ipsec security association parameters globally,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_ipsec_fragmentation(device,
                no_after_encr=False,
                no_before_encr=False):
    """ Configure IPSec Fragmentation
        Args:
            device ('obj')    : device to use
            no_after_encr ('boolean', optional) :  Perform fragmentation of large packets after IPSec
                    encapsulation, default is False
            no_before_encr ('boolean', optional) : Perform fragmentation of large packets before IPSec
                    encapsulation, default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring IPSec fragmentation"
    )
    config_list = []
    if no_after_encr:
        config_list.append("no crypto ipsec fragmentation after-encryption")

    if no_before_encr:
        config_list.append("no crypto ipsec fragmentation before-encryption")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure Crypto IPsec Fragmentation. Error: {error}'.format(error=e)
        )

def unconfigure_ipsec_df_bit(device,
                no_clear=False,
                no_copy=False,
                no_set=False):
    """ Configure IPSec DF bit
        Args:
            device ('obj')    : device to use
            no_clear ('boolean', optional) :  Clear DF bit for encapsulated packets, default is False
            no_copy ('boolean', optional) :  Copy DF bit from inner for encapsulated packets, default is False
            no_set ('boolean', optional) : Set DF bit for encapsulated packets, default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring IPSec df bit"
    )
    config_list = []
    if no_clear:
        config_list.append("no crypto ipsec df-bit clear")

    if no_copy:
        config_list.append("no crypto ipsec df-bit copy")

    if no_set:
        config_list.append("no crypto ipsec df-bit set")

    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure Crypto IPsec DF bit. Error: {error}'.format(error=e)
        )

def unconfigure_ipsec_sa_global(device,
                            no_ecn=False,
                            no_idle_time=False,
                            no_sa_life_days=False,
                            no_sa_life_kbytes=False,
                            no_sa_life_sec=False,
                            no_replay_disable=False,
                            no_replay_window=False,
                            no_multi_sn=False
                            ):
    """ Configures IPSec SA global parameters
        Args:
            device ('obj'): device to use
            no_ecn('boolean', optional): Discard the Explicit Congestion Notification, default is False
            no_idle_time ('boolean', optional): Automatically delete IPSec SAs after a given idle period, default is False
            no_sa_life_days ('boolean', optional): Security association duration in days, default is False
            no_sa_life_kbytes ('boolean', optional): Security association duration in kilobytes, default is False
            no_sa_life_sec ('boolean', optional): Security association duration in seconds, default is False
            no_replay_disable ('boolean', optional): SA replay disable, default is False
            no_replay_window ('boolean', optional): SA replay window size, default is False
            no_multi_sn ('boolean', optional): Enable multiple sequence number per IPSec SA, default is False

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring IPSec security association parameters"
    )

    configs = []

    if no_ecn:
        configs.append("no crypto ipsec security-association ecn")


    if no_idle_time:
        configs.append("no crypto ipsec security-association idle-time")

    if no_sa_life_days:
        configs.append("no crypto ipsec security-association lifetime days")

    if no_sa_life_kbytes:
        configs.append("no crypto ipsec security-association lifetime kilobytes")

    if no_sa_life_sec:
        configs.append("no crypto ipsec security-association lifetime seconds")

    if no_replay_disable:
        configs.append("no crypto ipsec security-association replay disable")

    if no_replay_window:
        configs.append("no crypto ipsec security-association replay window-size")

    if no_multi_sn:
        configs.append("no crypto ipsec security-association multi-sn")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure ipsec security association parameters globally,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_crypto_ikev2_policy(device, policy_name, proposal_name, fvrf=None):
    """ Configure crypto ikev2 policy ikev2policy
    Args:
        device (`obj`): Device object
        policy_name (`str`): name of ikev2 policy
        proposal_name (`str`): name of ikev2 proposal
        fvrf ('str',optional) FVRF name (Default None)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    config_list = []
    config_list.append('crypto ikev2 policy {policy_name}'.format(policy_name=policy_name))
    # Configure Peer Attributes
    if proposal_name:
        config_list.append('proposal {proposal_name}'.format(proposal_name=proposal_name))
    if fvrf:
        config_list.append("match fvrf {fvrf}".format(fvrf=fvrf))
    try:
        device.configure(config_list)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure Crypto Ikev2 Keyring. Error: {error}'.format(error=e)
        )

def unconfigure_crypto_ikev2_policy(device,policy_name):
    """ Unconfigure Crypto Ikev2 proposal
    Args:
        device (`obj`): Device object
        policy_name (`str`): name of ikev2 policy name
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    try:
        device.configure([
            "no crypto ikev2 policy {policy_name}".format(policy_name=policy_name),
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Crypto proposal. Error: {error}".format(error=e)
        )

def configure_tunnel_with_ipsec(
    device,
    tunnel_intf,
    overlay='ipv4',
    tunnel_ip=None,
    tunnel_mask=None,
    tunnel_src_ip=None,
    tunnel_dst_ip=None,
    keepalive_timer=None,
    ip_mtu=None,
    tunnel_ipv6=None,
    tunnel_maskv6=None,
    tunnel_mode='ipsec',
    tunnel_protection='ipsec',
    ipsec_profile_name=None,
    vrf=None,
    tunnel_vrf=None,
    v6_overlay=None
):
    """ Configure ipsec on Tunnel interface
        Args:
            device (`obj`): Device object
            tunnel_intf (`str`): Interface to get address
            overlay (`str`): Tunnel is eitehr IPv4 or Ipv6 or dual-overlay default value is ipv4
            tunnel_ip (`str`,optional): IPv4 addressed to be configured on interface
            tunnel_mask (`str`,optional): IPv4 Mask address to be used in configuration
            tunnel_src_ip (`str`): tunnel source address
            tunnel_dst_ip (`str`): tunnel destination address
            keepalive_timer ('int',optional): tunnel keepalive timer,default value is 10
            ip_mtu ('str',optional): tunnel mtu, default value is None
            tunnel_ipv6 (`str`,optional): IPv6 address with subnet mask,default value is None
            tunnel_maskv6 ('str',optional): IPv6 mask (Default None)
            tunnel_mode ('str',optional): Tunnel mode. Default is gre
            tunnel_protection ('str',optional): Protection type (i.e ipsec,dike)
            ipsec_profile_name ('str',optional): Tunnel protection profile name
            vrf ('str',optional): client vrf for  the tunnel
            tunnel_vrf ('str',optional): wan vrf for  the tunnel
            v6_overlay:('boolean', optional): True if v6-over-ipv4. Default is False

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("interface {intf}".format(intf=tunnel_intf))
    #configure vrf (vrf to be configured before ip)
    if vrf:
        configs.append("vrf forwarding {vrf}".format(vrf=vrf))
    if tunnel_ip:
        configs.append("ip address {ip} {mask}".format(ip=tunnel_ip,mask=tunnel_mask))
    if tunnel_ipv6:
        if tunnel_maskv6:
            configs.append("ipv6 enable")
            configs.append("ipv6 address {ipv6}/{v6_mask}".format(ipv6=tunnel_ipv6, v6_mask=tunnel_maskv6))
        else:
            configs.append("ipv6 enable")
            configs.append("ipv6 address {ipv6}".format(ipv6=tunnel_ipv6))

    if tunnel_mode == 'gre':
        if overlay == 'ipv6':
            configs.append("tunnel mode {mode} ipv6".format(mode=tunnel_mode))
        else:
            configs.append("tunnel mode {mode} ip".format(mode=tunnel_mode))
    else:
        configs.append("tunnel mode {mode} {over}".format(mode=tunnel_mode, over=overlay))
    configs.append("tunnel source {ip}".format(ip=tunnel_src_ip))
    configs.append("tunnel destination {ip}".format(ip=tunnel_dst_ip))
    if keepalive_timer:
        configs.append("keepalive {timer}".format(timer=keepalive_timer))
    if ip_mtu:
        configs.append("ip mtu {mtu}".format(mtu=ip_mtu))
    if tunnel_vrf:
        configs.append("tunnel vrf {vrf}".format(vrf=tunnel_vrf))
    if tunnel_protection:
        configs.append("tunnel protection {tunnel_protection} profile {profile}".
                       format(tunnel_protection=tunnel_protection,profile=ipsec_profile_name))
    if v6_overlay:
        configs.append("tunnel mode ipsec {tunnel_mode} v6-overlay".format(tunnel_mode=tunnel_mode))
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure Tunnel interface "
            "{interface} on device {dev}. Error:\n{error}".format(
                interface=tunnel_intf,
                dev=device.name,
                error=e,
            )
        )

def clear_crypto_ikev2_stats(device):
    """ Clear crypto ikev2 stats
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Clearing crypto ikev2 stats"
    )

    try:
        device.execute(
            "clear crypto ikev2 stats"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear crypto ikev2 stats. Error:\n{error}".format(error=e)
        )

def configure_crypto_map(device, tagname, sequence, ip_address, access_list_num, tag):
    """ configure crypto map
    Args:
        device (`obj`): Device object
        tagname (`str`): Crypto map tag
        sequence (`str`): Sequence to insert into crypto map entry
        ip_address (`str`): IP address of peer
        access_list_num (`str`): IP access-list number
        tag (`str`: Proposal tag
        
    Return:
        None
    Raise:
        SubCommandFailure: Failed to configure crypto map
    """
    try:
        device.configure([
            "crypto map {tagname} {sequence} ipsec-isakmp".format(tagname=tagname, sequence=sequence),
            "set peer {ip_address}".format(ip_address=ip_address),
            "match address {access_list_num}".format(access_list_num=access_list_num),
            "set transform-set {tag}".format(tag=tag)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure crypto map. Error: {error}".format(error=e)
        )


def configure_generate_self_certificate(
    device,
    label='self-cert',
    modulus=2048,
    ca_server='self-cert',
    subject_name='cn=self-cert.cisco.com',
    revocation_check='none',
):
    """ Configure generate self certificate
    Args:
        device (`obj`): Device object
        label (`str`, optional): RSA keypair label. defaults to 'self-cert'
        ca_server (`str`, optional): size of the key modulus. defaults to 2048
        subject_name ('str', optional): subject name. Defaults to 'cn=self-cert.cisco.com'
        revocation_check ('str, optional): revocation check. Defaults to 'none'
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """

    dialog = Dialog([
        Statement(
            pattern=
            r'.*Include the router serial number in the subject name\? \[yes/no\].*',
            action='sendline(no)',
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(
            pattern=
            r'.*Include an IP address in the subject name\? \[no\].*',
            action='sendline(no)',
            loop_continue=True,
            continue_timer=False,
        ),
        Statement(
            pattern=
            r'.*Generate Self Signed Router Certificate\? \[yes/no\].*',
            action='sendline(yes)',
            loop_continue=True,
            continue_timer=False,
        ),
    ])

    configs = [
        f'crypto key generate rsa general-keys label {label} modulus {modulus}',
        f'crypto pki trustpoint {ca_server}',
        'enrollment selfsigned',
        f'subject-name {subject_name}',
        f'revocation-check {revocation_check}',
        f'rsakeypair {label}',
        f'crypto pki enroll {ca_server}'
    ]

    try:
        device.configure(command=configs, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not generate self certificate. Error: {error}'.format(
                error=e)) from e
def unconfigure_ospfv3_authentication_null(device, interface):
    '''
    Unconfigure ospfv3 authentication null
        Args:
            device (`obj`): Device object
            inteface ('str'): interface with ospfv3 authenticaiton null.
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    log.info(
        "Unconfiguring ospfv3 authentication null"
    )
    configs = []
    configs.append("interface {intf}".format(intf=interface))
    configs.append('no ospfv3 authentication null')

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove ospfv3 authentication null. Error:\n{error}".format(error=e)
        )


def configure_interface_tunnel_mode_ipsec(device, interface):
    """ Configures Interface tunnel mode ipsec
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"interface {interface}", "tunnel mode ipsec ipv4"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure Interface tunnel mode ipsec. Error: {e}')


def unconfigure_interface_tunnel_mode_ipsec(device, interface):
    """ Unconfigures Interface tunnel mode ipsec
        Args:
            device ('obj')    : device to use
            interface ('str') : interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"interface {interface}", "no tunnel mode ipsec ipv4"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure Interface tunnel mode ipsec. Error: {e}')

def configure_ipsec_ike_sa_strength_enforcement(device):
    """ Configure IPsec IKE SA strength enforcement
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure IPsec IKE SA strength enforcement")

    try:
        device.configure(["crypto ipsec ike sa-strength-enforcement"])
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure IPsec IKE SA strength enforcement. Error: {e}')
    
def unconfigure_ipsec_ike_sa_strength_enforcement(device):
    """ Unconfigure IPsec IKE SA strength enforcement
        Args:
            device ('obj')    : device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure IPsec IKE SA strength enforcement")

    try:
        device.configure(["no crypto ipsec ike sa-strength-enforcement"])
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure IPsec IKE SA strength enforcement. Error: {e}')
