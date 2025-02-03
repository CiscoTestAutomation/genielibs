"""Common configure/unconfigure functions for GKM"""

# Python
from email.policy import default
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def configure_gikev2_profile_under_gkm_group(device,
                        group_name,
                        server_local=True,
                        gikev2_profile=None):
    """ Configures Crypto gikev2 profile under Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            server_local ('bool', optional): Configure server local.  Default is False
            gikev2_profile ('str'): Gikev2 profile name.
        Returns: None
        Raises:
            SubCommandFailure
    """

    log.info(
        "Configuring CRYPTO gkev2 profile under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if server_local:
        configs.append("server local")
        if gikev2_profile is not None:
            configs.append(f"gikev2 {gikev2_profile}")

    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure gikev2 profile under crypto gkm group,"
             "Error:\n{error}")
        raise

def configure_client_protocol_under_gkm_group(device,
                        group_name,
                        client_protocol,
                        profile_name):
    """ Configures Crypto client protocol under Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            client_protocol ('bool'): Gikev2/gdoi
            profile_name ('str'): Gikev2/gdoi profile name.
        Returns: None
        Raises:
            SubCommandFailure
    """

    log.info(
        "Configuring crypto gkm client protocol under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if client_protocol is not None:
        configs.append(f"client protocol {client_protocol} {profile_name}")

    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure client protocol under crypto gkm group,"
             "Error:\n{error}")
        raise

def configure_gkm_group_identity_number(device,
                        group_name,
                        ident_num=None):
    """ Configures Crypto Gdoi Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            ident_num ('str', optional): Identity number of  gkm group
        Returns: None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring identity number under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if ident_num is not None :
        configs.append(f"identity number {ident_num}")

    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure identity number under crypto gkm group,"
             "Error:\n{error}")
        raise

def configure_rekey_under_gkm_group(device,
                        group_name,
                        server_local=True,
                        rekey_algo=None,
                        rekey_sighash=None,
                        rekey_lifetime_sec=None,
                        rekey_retransmit=None,
                        rekey_retransmit_number=None,
                        rekey_auth_key=None,
                        rekey_transport_unicast=False):
    """ Configures Crypto Gdoi Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            server_local ('bool', optional): Configure server local.  Default is False
            rekey_algo ('str', optional): Configure rekey algorithm
            rekey_sighash ('str', optional): Configure rekey hash
            rekey_lifetime_sec ('str', optional): Configure rekey lifetime in seconds
            rekey_retransmit ('str', optional): Configure rekey retransmit periodic
            rekey_retransmit_number ('str', optional): Configure rekey retransmit number
            rekey_auth_key ('str', optional): Configure authentication key
            rekey_transport_unicast ('bool', optional): Configure rekey transport as unicast. Default is False
        Returns: None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring CRYPTO rekey params under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if server_local:
        configs.append("server local")
        if rekey_algo is not None :
            configs.append(f"rekey algorithm {rekey_algo}")
        if rekey_sighash is not None:
            configs.append(f"rekey sig-hash algorithm {rekey_sighash}")
        if rekey_lifetime_sec is not None :
            configs.append(f"rekey lifetime seconds {rekey_lifetime_sec}")
        if rekey_retransmit is not None and rekey_retransmit_number is not None :
            configs.append(f"rekey retransmit {rekey_retransmit} number {rekey_retransmit_number}")
        if rekey_retransmit is not None and rekey_retransmit_number is None :
            configs.append(f"rekey retransmit {rekey_retransmit} periodic")
        if rekey_auth_key is not None :
            configs.append(f"rekey authentication mypubkey rsa {rekey_auth_key}")
        if rekey_transport_unicast:
            configs.append("rekey transport unicast")

    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure rekey params under crypto gkm group,"
             "Error:\n{error}")
        raise
def configure_ipsec_under_gkm_group(device,
                        group_name,
                        server_local=True,
                        sa_ipsec_seq=None,
                        sa_ipsec_profile=None,
                        sa_ipsec_match_ipv4=None,
                        sa_ipsec_match_ipv6=None,
                        sa_ipsec_replay=False,
                        sa_ipsec_replay_time=None,
                        sa_ipsec_tag=False):
    """ Configures Crypto Gdoi Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            server_local ('bool', optional): Configure server local.  Default is False
            sa_ipsec_seq ('str',optional): Configure sa ipsec sequence number
            sa_ipsec_profile ('str', optional): configure ipsec profile on gkm group
            sa_ipsec_match_ipv4 ('str', optional): Set ipv4 match address
            sa_ipsec_match_ipv6 ('str', optional): Set ipv6 match address
            sa_ipsec_replay ('bool', optional): Set to True if sa replay needs to configured. Default is False
            sa_ipsec_replay_time ('str', optional): Set replay time window size
            sa_ipsec_tag ('bool', optional): Set tag. Default is False
        Returns: None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring CRYPTO ipsec params under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if server_local:
        configs.append("server local")
        if sa_ipsec_seq is not None:
            configs.append(f"sa ipsec {sa_ipsec_seq}")
            if sa_ipsec_profile is not None:
                configs.append(f"profile {sa_ipsec_profile}")
            if sa_ipsec_match_ipv4 is not None:
                configs.append(f"match address ipv4 {sa_ipsec_match_ipv4}")
            if sa_ipsec_match_ipv6 is not None:
                configs.append(f"match address ipv6 {sa_ipsec_match_ipv6}")
            if sa_ipsec_replay:
                if sa_ipsec_replay_time is not None :
                    configs.append(f"replay time window-size {sa_ipsec_replay_time}")
            elif sa_ipsec_replay is False:
                configs.append("no replay")
            if sa_ipsec_tag:
                configs.append("tag cts sgt")
            elif sa_ipsec_tag is False :
                configs.append("no tag")
    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure ipsec params under crypto gkm group,"
             "Error:\n{error}")
        raise
def configure_server_redundancy_under_gkm_group(device,
                        group_name,
                        server_local=False,
                        server_local_redundancy=False,
                        server_local_redundancy_local_prior=None,
                        server_local_redundancy_peer_addr=None):
    """ Configures Crypto Gdoi Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            server_local_redundancy ('bool', optional): Set redundancy in local server. Default is False
            server_local_redundancy ('bool', optional): Set redundancy in local server. Default is False
            server_local_redundancy_local_prior ('str', optional): set local priority value for redundancy
            server_local_redundancy_peer_addr ('str', optional): set peer address value for redundancy
        Returns: None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring redundancy server under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if server_local:
        configs.append("server local")
        if server_local_redundancy:
            configs.append("redundancy")
            if server_local_redundancy_local_prior is not None :
                configs.append(f"local priority {server_local_redundancy_local_prior}")
            if server_local_redundancy_peer_addr is not None :
                configs.append(f"peer address ipv4 {server_local_redundancy_peer_addr}")

    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure gikev2 profile under crypto gkm group,"
             "Error:\n{error}")
        raise

def configure_protocol_version_optimize_cli_under_gkm_group(device,
                        group_name,
                        server_local=True,
                        server_local_redundancy=True,
                        protocol_version_optimize=True):
    """ Configures Crypto Gdoi Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            server_local ('bool', optional): Configure server local.  Default is False
            server_local_redundancy ('bool', optional): Set redundancy in local server. Default is False
            protocol_version_optimize ('str', optional): set protocol version optimize
        Returns: None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring protocol version optimize cli under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if server_local:
        configs.append("server local")
        if server_local_redundancy:
            configs.append("redundancy")
            if protocol_version_optimize:
                configs.append(f"protocol version optimize")

    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure protocol version optimize command under crypto gkm group,"
             "Error:\n{error}")
        raise

def configure_ip_for_server_local_under_gkm_group(device,
                        group_name,
                        server_local=True,
                        ipv4_address=None):
    """ Configures Crypto Gdoi Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            server_local ('bool', optional): Configure server local.  Default is False
            ipv4_address ('str'): ipv4 address

        Returns: None

        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring ipv4 address for server local under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if server_local:
        configs.append("server local")
        if ipv4_address is not None:
            configs.append(f"address ipv4 {ipv4_address}")

    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure ipv4 address for server local under crypto gkm group,"
             "Error:\n{error}")
        raise

def configure_ipv4_server_under_gkm_group(device,
                        group_name,
                        server_ipv4_address=None,
                        server_ipv4_sec_address=None):
    """ Configures Crypto Gdoi Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            server_ipv4_address ('str', optional): Set ipv4 server address
            server_ipv4_sec_address ('str', optional): Set ipv4 secondary server address
        Returns: None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring CRYPTO gkm profile under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if server_ipv4_address is not None:
        configs.append(f"server address ipv4 {server_ipv4_address}")
    if server_ipv4_sec_address is not None:
        configs.append(f"server address ipv4 {server_ipv4_sec_address}")

    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure primary/secondary ipv4 severs under gkm group,"
             "Error:\n{error}")
        raise
def configure_pfs_enable_or_disable_under_gkm_group(device,
                        group_name,
                        server_local=True,
                        pfs=False):
    """ Configures Crypto Gdoi Gkm group
        Args:
            device ('obj'): Device object
            group_name ('str'): gkm group name
            server_local ('bool', optional): Configure server local.  Default is False
            pfs ('str', optional): Enable/Disable the PFS feature on Key Server
        Returns: None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring pfs command enable or disable under gkm group"
    )
    configs = [f"crypto gkm group {group_name}"]
    if server_local:
        configs.append("server local")
        if pfs:
            configs.append(f"pfs")
        elif pfs is False:
            configs.append(f"no pfs")

    try:
        device.configure(configs)
    except SubCommandFailure as error:
        log.error(f"Failed to configure pfs enable or disable under gkm group,"
             "Error:\n{error}")
        raise

