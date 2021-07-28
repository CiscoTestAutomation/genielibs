"""Configure macsec functions on device and interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def config_wan_macsec_on_interface(device, interface, destination_address, eth_type, speed=None):
    """ Configures WAN Macsec on interface 

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            speed ('str'): Operation speed
            destination_address ('str'): eapol destination-address
            eth_type ('str'): eapol eth-type

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
            "Configure WAN Macsec on {intf}".format(
                intf=interface)
            )

    config = [
        "interface {intf}".format(intf=interface),
        "macsec dot1q-in-clear 1",
        "eapol destination-address {dest_addr}".format(
            dest_addr=destination_address),
        "eapol eth-type {eth_type}".format(eth_type=eth_type)
    ]

    if speed:
        config.append("speed {speed}".format(speed=speed))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure WAN Macsec on interface {interface}, "
            "Error: {error}".format(interface=interface, error=e
            )
        )

def config_macsec_replay_protection_window_size(device, interface, window_size):
    """ Configures macsec replay-protection window-size on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            window_size ('str'): window size

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
            "Configure macsec replay-protection with window-size {win_size} "
            "on {intf}".format(win_size=window_size, intf=interface)
            )
    try:
        device.configure([
            "interface {intf}".format(intf=interface),
            "macsec replay-protection window-size {win_size}".format(
                win_size=window_size)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure macsec replay-protection with window-size "
            "{win_size} interface {interface}, Error: {error}".format(
                win_size=window_size, interface=interface, error=e
            )
        )

def config_macsec_keychain_on_device(device, keychain_name, key, crypt_algorithm, key_string):
    """ Configures macsec key chain on device

        Args:
            device ('obj'): device to use
            keychain_name ('str'): keychain name to configure
            key_string ('str'): key string to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
            "Configure macsec key chain {keychain_name} on device".format(
                keychain_name=keychain_name)
            )
    try:
        device.configure([
            "key chain {keychain_name} macsec".format(
                keychain_name=keychain_name),
            "key {key}".format(key=key),
            "cryptographic-algorithm {crypt_algorithm}".format(
                crypt_algorithm=crypt_algorithm),
            "key-string {key_string}".format(key_string=key_string)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure macsec key chain {keychain_name} on "
            "device {device}, Error: {error}".format(
                keychain_name=keychain_name, device=device.name, error=e)
        )

def unconfig_macsec_keychain_on_device(device, keychain_name):
    """ Unconfigures macsec key chain on device

        Args:
            device ('obj'): device to use
            keychain_name ('str'): keychain name to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
            "Unconfigure macsec key chain {keychain_name} on device".format(
                keychain_name=keychain_name)
            )
    try:
        device.configure(
            "no key chain {keychain_name} macsec".format(
                keychain_name=keychain_name)
            )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure macsec key chain {keychain_name} on "
            "device {device}, Error: {error}".format(
                keychain_name=keychain_name, device=device.name, error=e)
        )


def config_mka_keychain_on_interface(device, interface, key_string):
    """ Configures mka keychain on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            key_string ('str'): key string to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
            "Configure mka keychain {key_string} on {intf}".format(
                key_string=key_string, intf=interface)
            )
    try:
        device.configure([
            "interface {intf}".format(intf=interface),
            "mka pre-shared-key key-chain {key_string}".format(key_string=key_string)])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mka keychain {key_string} "
            "on interface {interface}, Error: {error}".format(
                key_string=key_string, interface=interface, error=e
            )
        )


def config_macsec_network_link_on_interface(device, interface):
    """ Configures macsec network-link on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
            "configure macsec network-link on {intf}".format(
                 intf=interface)
            )
    try:
        device.configure([
            "interface {intf}".format(intf=interface),
            "macsec network-link"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure macsec network-link on "
            "interface {interface}, Error: {error}".format(
                interface=interface, error=e
            )
        )


def unconfig_macsec_network_link_on_interface(device, interface):
    """ Un configures macsec network-link on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
            "Unconfigure macsec network-link on {intf}".format(
                 intf=interface)
            )
    try:
        device.configure([
            "interface {intf}".format(intf=interface),
            "no macsec network-link"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure macsec network-link on "
            "interface {interface}, Error: {error}".format(
                interface=interface, error=e
            )
        )


def config_mka_policy_xpn(device,cipher=None,interface=None):
    """ Configures mka policy xpn on device or interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        if interface is None:
            log.info("Configure mka policy xpn on device")
            device.configure([
                "mka policy XPN",
                "macsec-cipher-suite {cipher}".format(cipher=cipher)])
        else:
            log.info("Configure mka policy xpn on "
                    "interface {interface}".format(interface=interface)
            )

            device.configure([
                "interface {intf}".format(intf=interface),
                "mka policy XPN"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mka policy xpn on device/interface, "
            "Error: {error}".format(error=e)
            )

def unconfig_mka_policy_xpn(device):
    """ Unconfigures mka policy xpn on device

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        log.info("Unconfigure mka policy xpn on device")
        device.configure("no mka policy XPN")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mka policy xpn on device, "
            "Error: {error}".format(error=e)
            )

def clear_macsec_counters(device,interfaces):
    """ Clears macsec counters on device

        Args:
            device ('obj'): device to use
            interfaces ('list'): List of interfaces

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        log.info(
                "Clears macsec counters on device {device} "
                "for interfaces {interfaces}".format(
                device=device.name,interfaces=interfaces)
                )
        for intf in interfaces:
            device.execute("clear macsec counters int {intf}".format(intf=intf))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear macsec counters on device {device}, "
            "Error: {error}".format(device=device.name, error=e)
            )
