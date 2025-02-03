"""Common configure/unconfigure functions for GDOI"""

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

def configure_gdoi_group(device,
                         group_name,
                         ipv6_group=False,
                         ident_num=None,
                         server_ipv4_address=None,
                         server_local=False,
                         rekey_algo=None,
                         rekey_lifetime_sec=None,
                         rekey_retransmit=None,
                         rekey_retransmit_number=None,
                         rekey_auth_key=None,
                         rekey_transport_unicast=False,
                         sa_ipsec_seq=None,
                         sa_ipsec_profile=None,
                         sa_ipsec_match_ipv4=None,
                         sa_ipsec_match_ipv6=None,
                         sa_ipsec_replay=False,
                         sa_ipsec_replay_time=None,
                         sa_ipsec_tag=False,
                         server_local_addr=None,
                         server_local_redundancy=False,
                         server_local_redundancy_local_prior=None,
                         server_local_redundancy_peer_addr=None,
                         server_local_identifier=False,
                         server_local_identifier_range=None,
                         server_local_identifier_val=None,
                         gikev2_profile=None,
                         rekey_address_acl=None,
                         gikev2_client=None,
                         pfs=None):

    """ Configures Crypto Gdoi Group
        Args:
            device (`obj`): Device object
            group_name ('str'): gdoi group name
            ident_num ('str', optional): Identity number of  gdoi group
            server_ipv4_address ('str', optional): Set ipv4 server address
            server_local ('bool', optional): Configure server local.  Default is False
            rekey_algo ('str', optional): Configure rekey algorithm
            rekey_lifetime_sec ('str', optional): Configure rekey lifetime in seconds
            rekey_retransmit ('str', optional): Configure rekey retransmit periodic
            rekey_retransmit_number ('str', optional): Configure rekey retransmit number
            rekey_auth_key ('str', optional): Configure authentication key
            rekey_transport_unicast ('bool', optional): Configure rekey transport as unicast. Default is False
            sa_ipsec_seq ('str',optional): Configure sa ipsec sequence number
            sa_ipsec_profile ('str', optional): configure ipsec profile on gdoi group
            sa_ipsec_match_ipv4 ('str', optional): Set ipv4 match address
            sa_ipsec_match_ipv6 ('str', optional): Set ipv6 match address
            sa_ipsec_replay ('bool', optional): Set to True if sa replay needs to configured. Default is False
            sa_ipsec_replay_time ('str', optional): Set replay time window size
            sa_ipsec_tag ('bool', optional): Set tag. Default is False
            server_local_addr ('str', optional): Set server local address
            server_local_redundancy ('bool', optional): Set redundancy in local server. Default is False
            server_local_redundancy_local_prior ('str', optional): set local priority value for redundancy
            server_local_redundancy_peer_addr ('str', optional): set peer address value for redundancy
            server_local_identifier ('bool', optional): Configure identifier. Default is False
            server_local_identifier_range ('str', optional): set server local identifier range
            server_local_identifier_val ('str', optional): set server local identifier value
            gikev2_profile ('str', optional): Set gikev2 profile
            rekey_address_acl ('str', optional): Set rekey ipv4 address
            gikev2_client ('str', optional): Set gikev2 profile for GM
            pfs ('bool', optional): Set to True to enable PFS
        Returns:
			True/False
        Raises:
            SubCommandFailure
    """


    log.info(
        "Configuring CRYPTO GDOI GROUP"
    )


    configs = []

    if not ipv6_group:
        configs.append(f"crypto gdoi group {group_name}")
    else:
        configs.append(f"crypto gdoi group ipv6 {group_name}")
    if ident_num is not None :
        configs.append(f"identity number {ident_num}")
    if server_ipv4_address is not None:
        configs.append(f"server address ipv4 {server_ipv4_address}")
    if gikev2_client is not None:
        configs.append(f"client protocol gikev2 {gikev2_client}")
    if server_local:
        configs.append("server local")
        if rekey_algo is not None :
            configs.append(f"rekey algorithm {rekey_algo}")
        if rekey_lifetime_sec is not None :
            configs.append(f"rekey lifetime seconds {rekey_lifetime_sec}")
        if rekey_address_acl is not None:
            configs.append(f"rekey address ipv4 {rekey_address_acl}")
        if rekey_retransmit is not None and rekey_retransmit_number is not None :
            configs.append(f"rekey retransmit {rekey_retransmit} number {rekey_retransmit_number}")
        if rekey_retransmit is not None and rekey_retransmit_number is None :
            configs.append(f"rekey retransmit {rekey_retransmit} periodic")
        if rekey_auth_key is not None :
            configs.append(f"rekey authentication mypubkey rsa {rekey_auth_key}")
        if rekey_transport_unicast:
            configs.append("rekey transport unicast")
        if pfs is True:
            configs.append("pfs")
        if gikev2_profile is not None:
            configs.append(f"gikev2 {gikev2_profile}")
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
        if server_local_addr is not None :
            configs.append(f"address ipv4 {server_local_addr}")
        if server_local_redundancy:
            configs.append("redundancy")
            if server_local_redundancy_local_prior is not None :
                configs.append(f"local priority {server_local_redundancy_local_prior}")
            if server_local_redundancy_peer_addr is not None :
                configs.append(f"peer address ipv4 {server_local_redundancy_peer_addr}")
        if server_local_identifier:
            configs.append("identifier")
            if server_local_identifier_val is not None :
                configs.append(f"value {server_local_identifier_val}")
            elif server_local_identifier_range is not None :
                configs.append(f"range {server_local_identifier_range}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure crypto gdoi group,"
             "Error:\n{error}".format(error=e)
        )
        raise


def unconfigure_gdoi_group(device,
                         group_name,
                         ipv6_group=False):

    """ Configures Crypto Gdoi Group
        Args:
            device (`obj`): Device object
            group_name ('str'): gdoi group name
            ipv6_group ('boolean', optional): indicator of ipv6 group. Default value is False
        Returns:
                        True/False
        Raises:
            SubCommandFailure
    """
    dialog = Dialog([
                Statement(pattern=r'.*Do you want to continue.*',
                    action=f'sendline(yes)',
                    loop_continue=True,
                    continue_timer=False)
    ])

    log.info(
        "Unconfiguring crypto gdoi group"
    )

    configs = []

    if not ipv6_group:
        configs.append(f"no crypto gdoi group {group_name}")
    else:
        configs.append(f"no crypto gdoi group ipv6 {group_name}")

    try:
        device.configure(configs, reply=dialog, timeout=30)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure crypto gdoi group,"
             "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_gdoi_group_on_gm(device,
                                 group_name,
                                 ipv6_group=False):
    """ unconfigures Crypto gdoi group
        Args:
            device (`obj`): Device object
            group_name ('str'): Crypto gdoi group name
            ipv6_group ('bool',optional): unconfigure IPv6 crypto gdoi group

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring CRYPTO gdoi group on GM "
    )

    configs = []

    if not ipv6_group:
        configs.append(f"no crypto gdoi group {group_name}")
    else:
        configs.append(f"no crypto gdoi group ipv6 {group_name}")
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure gdoi group,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_crypto_map_for_gdoi(device,
                                  map_name,
                                  seq,
                                  group=None,
                                  description=None,
                                  ipv6=False):
    """ Configures Crypto Map for gdoi
        Args:
            device (`obj`): Device object
            map_name ('str'): Crypto Map name
            seq ('str'):  Sequence to insert into crypto map entry
            group ('str',optional): Set the san group parameters
            description ('str',optional): Description of the crypto map statement policy
            ipv6 ('bool',optional): Configure IPv6 crypto map

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring CRYPTO map"
    )

    configs = []
    if ipv6 is False:
        configs.append(f"crypto map {map_name} {seq}  gdoi")
    else:
        configs.append(f"crypto map ipv6 {map_name} {seq} gdoi")
    if group is not None:
        configs.append(f"set group {group}")
    if description is not None:
        configs.append(f"description {description}")

    try:
        errors = [f"% group {group} doesn't yet exist.",
                  f"Group {group} is an IPv6 group and Crypto map is for IPv4."
                  "Please set an IPv4 group."]
        device.configure(configs ,error_pattern = errors)
    except SubCommandFailure as e:
        log.error("Failed to configure crypto map,"
                  "Error:\n{error}".format(error=e)
        )
        raise

def unconfigure_crypto_map_for_gdoi(device,
                                    map_name,
                                    seq,
                                    ipv6=False):
    """ UnConfigure crypto map
        Args:
            device (`obj`): Device object
            map_name ('int'): type of key that will follow
            seq ('str'): Sequence Number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Unconfiguring crypto map"
    )

    configs = []
    if ipv6 is False:
        configs.append(f"no crypto map {map_name} {seq} gdoi")
    else:
        configs.append(f"no crypto map ipv6 {map_name} {seq} gdoi")

    try:
        errors = [f"% Crypto-map {map_name} is in use by interface(s): Gi3"]
        device.configure(configs ,error_pattern = errors)
    except SubCommandFailure as e:
        log.error("Failed to un configure crypto map on gdoi,"
                  "Error:\n{error}".format(error=e))
        raise
