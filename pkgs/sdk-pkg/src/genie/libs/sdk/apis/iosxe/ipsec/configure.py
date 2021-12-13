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


def configure_ipsec_transform_set(device,transform_set_name,transform_method):
    """ Configures ipsec transform set
        Args:
            device (`obj`): Device object
            transform_set_name ('str'): transform-set name
            transform_method ('str'): transform method e.g. esp-gcm, esp-md5-hmac
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IPSEC transform set"
    )

    configs = []
    configs.append("crypto ipsec transform-set {transform_set_name} {transform_method}".format(transform_set_name=transform_set_name,transform_method=transform_method))
    configs.append("esn")
    configs.append("mode tunnel")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ipsec transform-set,"
             "Error:\n{error}".format(error=e)
        )
        raise

def configure_ipsec_profile(device,
                            profile_name,
                            transform_set_name,
                            ikev2_profile_name):
    """ Configures ipsec transform set
        Args:
            device (`obj`): Device object
            profile_name ('str'): ipsec profile name
            transform_set_name ('str'): transform-set name
            ikev2_profile_name ('str'): ikev2 profile name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring IPSEC profile"
    )

    configs = []
    configs.append("crypto ipsec profile {profile_name}".format(profile_name=profile_name))
    configs.append("set transform-set {transform_set_name}".format(transform_set_name=transform_set_name))
    configs.append("set ikev2-profile {ikev2_profile_name}".format(ikev2_profile_name=ikev2_profile_name))


    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure ipsec profile,"
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