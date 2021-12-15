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
                            peer_ip,
                            peer_mask,
                            key):
    """ Configures IKEV2 keyring or Preshared Key (PSK)
        Args:
            device (`obj`): Device object
            keyring_name ('str'): Name for the keyring
            peer_name ('str'): peer name
            peer_ip ('str'): peer ip addr
            peer_mask ('str'): peer nw mask
            key ('str'): preshared key
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
    configs.append("address {peer_ip} {peer_mask}".format(peer_ip=peer_ip,peer_mask=peer_mask))
    configs.append("pre-shared-key {key}".format(key=key))
    

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