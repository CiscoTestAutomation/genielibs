"""Configure and Unconfigure macsec functions on device and interface"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)


def config_wan_macsec_on_interface(device, interface, destination_address,
        eth_type, speed=None, dot1q_clear=True):
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
        "eapol destination-address {dest_addr}".format(
            dest_addr=destination_address),
        "eapol eth-type {eth_type}".format(eth_type=eth_type)
    ]
    if dot1q_clear:
        config.append("macsec dot1q-in-clear 1")
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

def config_macsec_should_secure(device, interface):
    """ Configures macsec should secure on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure should secure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
            "Configure Should secure on interface"
            )
    try:
        device.configure([
            "interface {intf}".format(intf=interface),
            "macsec access-control should-secure"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure should secure on interface "
            "should secure interface {interface}, Error: {error}".format(
               interface=interface, error=e
            )
        )

def unconfig_macsec_should_secure(device, interface):
    """ Unconfigures macsec should secure on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to Unconfigure should secure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(
            "Unconfigure Should secure on interface"
            )
    try:
        device.configure([
            "interface {intf}".format(intf=interface),
            "no macsec access-control should-secure"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure should secure on interface "
            "should secure interface {interface}, Error: {error}".format(
               interface=interface, error=e
            )
        )

def config_macsec_keychain_on_device(device, keychain_name, key,
        crypt_algorithm, key_string, lifetime=None):
    """ Configures macsec key chain on device
        Args:
            device ('obj'): device to use
            keychain_name ('str'): keychain name to configure
            key_string ('str'): key string to configure
            lifetime ('list'): start and end timings
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
        configs = [
            "key chain {keychain_name} macsec".format(
                keychain_name=keychain_name),
            "key {key}".format(key=key),
            "cryptographic-algorithm {crypt_algorithm}".format(
                crypt_algorithm=crypt_algorithm),
            "key-string {key_string}".format(key_string=key_string)]

        if lifetime is not None:
            configs.append("lifetime local {start} {end}".format(
                start=lifetime[0], end=lifetime[1]))
        device.configure(configs)

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


def config_mka_keychain_on_interface(device, 
        interface, 
        key_string, 
        key_chain=None):
    """ Configures mka keychain on interface
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            key_string ('str'): master key chain to configure
            key_chain ('str'): fall back key chain to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        if key_chain is not None:
            log.info(
                "Configure mka keychain {key_string} fall back key chain {key_chain} on {intf}".format(
                   key_string=key_string, key_chain=key_chain, intf=interface))
            device.configure([
                "interface {intf}".format(intf=interface),
                "mka pre-shared-key key-chain {key_string} fallback-key-chain {key_chain}"
                .format(key_string=key_string, key_chain=key_chain)])
        else:
            log.info(
                "Configure mka keychain {key_string} on {intf}".format(
                 key_string=key_string, intf=interface))
            device.configure([
                "interface {intf}".format(intf=interface),
                "mka pre-shared-key key-chain {key_string}".format(key_string=key_string)])
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
               "Could not configure mka keychain and fallback keychain {key_string} {key_chain} "
               "on interface {interface}, Error: {error}".format(
               key_string=key_string, key_chain=key_chain, interface=interface, error=e)
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


def config_mka_policy_xpn(device, interface=None, cipher=None,
        sak_rekey_int=None, key_server_priority=None):
    """ Configures mka policy xpn on device or interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            cipher ('str'): Cipher suite value
            sak_rekey_int ('str'): Sak rekey interval
            key_server_priority ('str'): Key server priority

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    if interface is None:
        log.info("Configure mka policy xpn on device")
        configs = [
            "mka policy XPN",
            "macsec-cipher-suite {cipher}".format(cipher=cipher)]
        if sak_rekey_int:
            configs.append("sak-rekey interval {interval}".format(
                interval=sak_rekey_int))
        if key_server_priority:
            configs.append("key-server priority {key_pr}".format(
                key_pr=key_server_priority))
    else:
        log.info("Configure mka policy xpn on "
                "interface {interface}".format(interface=interface)
        )
        configs = [
            "interface {intf}".format(intf=interface),
            "mka policy XPN"]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mka policy xpn on device/interface, "
            "Error: {error}".format(error=e)
            )

def config_mka_policy(device, 
        global_level=None, 
        interface=None, 
        cipher=None, 
        send_secure_announcements=None,
        sak_rekey_int=None, 
        key_server_priority=None, 
        sak_rekey_on_live_peer_loss=None, 
        conf_offset=None, 
        policy_name=None, 
        delay_protection= None):
    """ Configures user defined mka policy on device or interface
        Args:
            device ('obj'): device to use
            global_level ('bool'): Enable policy globally
            Policy name ('str'): policy name to configure 
            interface ('str'): interface to configure
            cipher ('str'): Cipher suite value
            sak_rekey_int ('str'): Sak rekey interval
            key_server_priority ('str'): Key server priority
            conf_offset ('str'): confidentiality offset
            send_secure_announcements ('bool'): Enable/disable send secure announcements  
            delay_protection ('bool'): Enable/disable delay_protection
            sak_rekey_on_live_peer_loss ('bool'): Enable/disable sak rekey on live peer loss
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if global_level:
        log.info("Configure user defined mka policy on device and interface")
        configs = [
            "mka policy {policy_name}".format(policy_name=policy_name)]
        if cipher:
            configs.append(
               "macsec-cipher-suite {cipher}".format(cipher=cipher))
        if sak_rekey_int:
            configs.append("sak-rekey interval {interval}".format(
                interval=sak_rekey_int))
        if key_server_priority:
            configs.append("key-server priority {key_pr}".format(
                key_pr=key_server_priority))
        if conf_offset:
            configs.append("confidentiality-offset {conf_off}".format(
                conf_off=conf_offset))
        if send_secure_announcements:
            configs.append("send-secure-announcements")
        if sak_rekey_on_live_peer_loss:
            configs.append("sak-rekey on-live-peer-loss")
        if delay_protection:
            configs.append("delay-protection")
        if interface:
            configs.append("interface {intf}".format(intf=interface))
            configs.append("mka policy {policy_name}".format(policy_name=policy_name))

    else:
        if interface:
            log.info("Configure user defined mka policy on "
                    "interface {interface}".format(interface=interface))
            configs = [
                "interface {intf}".format(intf=interface),
                "mka policy {policy_name}".format(policy_name=policy_name)]
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure user defined mka policy on device/interface, "
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

def unconfig_mka_policy(device, 
        interface=None, 
        policy_name=None, 
        global_level=None):
    """ Unconfigures mka policy on interface/device 
        Args:
            device ('obj'): device to use
            interface ('str'): interface to unconfigure
            global_level ('bool'): device level to unconfigure
            policy_name ('str'): Policy name to Unconfigure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        if interface is not None:
            log.info("Unconfigure user defined mka policy on interface")
            configs = [
            "interface {intf}".format(intf=interface),
            "no mka policy {policy_name}".format(policy_name=policy_name)]
            device.configure(configs)

        if global_level is not None:
            log.info("Unconfigure mka policy on device")
            configs = [
            "no mka policy {policy_name}".format(policy_name=policy_name)]
            device.configure(configs)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mka policy on interface/device, "
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

def configure_mka_policy_delay_protection(device, policy_name, interface, cipher):
    """ Configures mka policy with delay protection on device and interface

        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be configured
            interface ('str'): interface to configure
            cipher ('str'): Cipher suite to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Configure mka policy with delay protection on device")
    configs = [
            "mka policy {policy_name}".format(policy_name=policy_name),
            "delay-protection",
            "macsec-cipher-suite {cipher}".format(cipher=cipher)]
    log.info("Configure mka policy {policy_name} on "
                "interface {interface}".format(policy_name=policy_name, interface=interface)
        )
    configs.extend(["interface {intf}".format(intf=interface),
            "mka policy {policy_name}".format(policy_name=policy_name)])
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mka policy with delay protection on device/interface, "
            "Error: {error}".format(error=e)
            )


def unconfigure_mka_policy_delay_protection(device, policy_name, interface):
    """ Unconfigures mka policy with delay protection on device and interface

        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be unconfigured
            interface ('str'): interface to unconfigure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Unconfigure mka policy {policy_name} on "
                "interface {interface}".format(policy_name=policy_name, interface=interface)
        )
    configs = [
            "interface {intf}".format(intf=interface),
            "no mka policy {policy_name}".format(policy_name=policy_name)]

    log.info("Unconfigure mka policy with delay protection on device")
    
    configs.append("no mka policy {policy_name}".format(policy_name=policy_name))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mka policy with delay protection on device/interface, "
            "Error: {error}".format(error=e)
            )

def configure_mka_policy(device, policy_name, interface, cipher):
    """ Configures mka policy on device and interface

        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be configured
            interface ('str'): interface to configure
            cipher ('str'): Cipher suite to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Configure mka policy on device")
    configs = [
            "mka policy {policy_name}".format(policy_name=policy_name),
            "macsec-cipher-suite {cipher}".format(cipher=cipher)]
    log.info("Configure mka policy {policy_name} on "
                "interface {interface}".format(policy_name=policy_name, interface=interface)
        )
    configs.extend(["interface {intf}".format(intf=interface),
            "mka policy {policy_name}".format(policy_name=policy_name)])
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mka policy on device/interface, "
            "Error: {error}".format(error=e)
            )


def unconfigure_mka_policy(device, policy_name, interface):
    """ Unconfigures mka policy on device and interface

        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be unconfigured
            interface ('str'): interface to unconfigure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info("Unconfigure mka policy {policy_name} on "
                "interface {interface}".format(policy_name=policy_name, interface=interface)
        )
    configs = [
            "interface {intf}".format(intf=interface),
            "no mka policy {policy_name}".format(policy_name=policy_name)]

    log.info("Unconfigure mka policy with on device")

    configs.append("no mka policy {policy_name}".format(policy_name=policy_name))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mka policy with on device/interface, "
            "Error: {error}".format(error=e)
            )

def unconfigure_mka_keychain_on_interface(device, interface, key_string, key_chain=None):
    """ Unconfigures mka keychain on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
            key_string ('str'): key string to configure
            key_chain ('str'): fall back key chain to unconfigure

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        if key_chain is not None:
            log.info(
                "Unconfigure mka keychain {key_string} fall back key chain {key_chain} on {intf}".format(
                key_string=key_string, key_chain=key_chain, intf=interface))
            device.configure([
                "interface {intf}".format(intf=interface),
                "no mka pre-shared-key key-chain {key_string} fallback-key-chain {key_chain}".
                 format(key_string=key_string, key_chain=key_chain)])
        else:
            log.info(
                "Unconfigure mka keychain {key_string} on {intf}".format(
                 key_string=key_string, intf=interface))
            device.configure([
                "interface {intf}".format(intf=interface),
                "no mka pre-shared-key key-chain {key_string}".format(key_string=key_string)])
                
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mka keychain {key_string} "
            "on interface {interface}, Error: {error}".format(
                key_string=key_string, interface=interface, error=e
            )
        )


def unconfigure_pki_trustpoint(device, label_name):
    """ Unconfigures Trustpoint related config on device

        Args:
            device ('obj'): device to use
            label_name ('str'): Label name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure Trustpoint on device")

    dialog = Dialog([
    Statement(pattern=r'.*\% Removing an enrolled trustpoint will destroy all certificates\n'
    r'received from the related Certificate Authority\.\n'

    r'Are you sure you want to do this\? \[yes\/no\]\:',
                        action='sendline(y)',
                        loop_continue=True,
                        continue_timer=False)
    ])

    try:
       device.configure("no crypto pki trustpoint {label_name}".format(label_name=label_name), reply=dialog)    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure Trustpoint related config from device "
            "Error: {error}".format(error=e)
            )

def configure_mka_macsec(device,
        interface,
        keychain_name,
        policy_name
        ):
    """ Configures MKA and MACSec interface

        Args:
            device ('obj'): device to use
            interface ('str'): Interface name
            keychain_name ('str'): Key Chain name
            policy_name ('str'): MKA policy name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug("Configure MKA and MACSec on interface")
    configs = []
    configs.append(f"interface {interface}")
    configs.append(f"mka pre-shared-key key-chain {keychain_name}")
    configs.append(f"mka policy {policy_name}")
    configs.append("macsec")

    errors = [f"% MKA policy \"{policy_name}\" has not been configured.",
    f"% Either the Key-Chain \"{keychain_name}\" is not defined or there is no valid key in the key-chain\\."
    ]

    try:
        device.configure(configs, error_pattern = errors)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure MACSec on interface"
            "Error: {error}".format(error=e)
            )


def unconfigure_mka_macsec(device,
        interface,
        keychain_name,
        policy_name
        ):
    """ Unonfigures MKA and MACSec interface

        Args:
            device ('obj'): device to use
            interface ('str'): Interface name
            keychain_name ('str'): Key Chain name
            policy_name ('str'): MKA policy name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigure MKA and MACSec on interface")
    configs = []
    configs.append(f"interface {interface}")
    configs.append("no macsec")
    configs.append(f"no mka policy {policy_name}")
    configs.append(f"no mka pre-shared-key key-chain {keychain_name}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure MACSec on interface"
            "Error: {error}".format(error=e)
            )
        

def configure_disable_sci_dot1q_clear(device,
        interface,
        disable_sci=True,
        dot1q_in_clear=False,
        tag_number=1
        ):
    """ Configures MACSec with disable-sci and dot1q-in-clear

        Args:
            device ('obj'): device to use
            interface ('str'): Interface name
            disable_sci ('boolean', 'Optional'): 
                disable sci for MACsec, default is True
            dot1q_in_clear ('boolean', 'Optional' ): 
                Configure dot1q-in-clear on interface, default is False
            tag_number('int', 'Optional'):
                Specify the dot1q tag number(1 or 2), default is 1

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug("Configures MACSec with disable-sci and/or dot1q-in-clear")
    configs = []
    configs.append(f"interface {interface}")
    if disable_sci:
        configs.append("macsec disable-sci")
    
    if dot1q_in_clear:
        configs.append(f"macsec dot1q-in-clear {tag_number}")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure MACSec with disable-sci and/or dot1q-in-clear"
            "Error: {error}".format(error=e)
            )


def unconfigure_disable_sci_dot1q_clear(device,
        interface,
        no_disable_sci=True,
        no_dot1q_in_clear=True
        ):
    """ Unconfigures MACSec with disable-sci and dot1q-in-clear

        Args:
            device ('obj'): device to use
            interface ('str'): Interface name
            no_disable_sci ('boolean', 'Optional'): 
                remove disable sci for MACsec, default is True
            dot1q_in_clear ('boolean', 'Optional' ): 
                unconfigure dot1q-in-clear on interface, default is True

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug("Configures MACSec with disable-sci and/or dot1q-in-clear")
    configs = []
    configs.append(f"interface {interface}")
    if no_disable_sci:
        configs.append("no macsec disable-sci")
    
    if no_dot1q_in_clear:
        configs.append("no macsec dot1q-in-clear")

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure MACSec with disable-sci and/or dot1q-in-clear"
            "Error: {error}".format(error=e)
            )

def configure_pki_trustpoint(device, key_type=None, label_name=None,
    modulus_size=None, enrollment_type=None, subject_line=None, revocation_check=None,
    storage_type=None):
    """ Configures Trustpoint related config on device

        Args:
            device ('obj'): device to use
            key_type ('str', Optional): Key type to be generated. Defaults to None
            label_name ('str', Optional): Label name. Defaults to None
            modulus_size ('str', Optional): Modulus size to be configured. Defaults to None
            enrollment_type ('str', Optional): Enrollment type to be configured. Defaults to None
            subject_line ('str', Optional): Subject Line to be configured. Defaults to None
            revocation_check ('str', Optional): Revocation check to be configured. Defaults to None
            storage_type ('str', Optional): Storage type to be configured. Defaults to None

       Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.debug("Configure Trustpoint on device")
    try:
        configs = []
        if key_type and label_name and modulus_size:
            configs.append(f"crypto key generate {key_type} label {label_name} modulus {modulus_size}")
        if label_name:
            configs.append(f"crypto pki trustpoint {label_name}")
        if enrollment_type:
            configs.append(f"enrollment {enrollment_type}")
        if subject_line:
            configs.append(f"subject-name {subject_line}")
        if revocation_check:
            configs.append(f"revocation-check {revocation_check}")
        if key_type and label_name and modulus_size:
            configs.append(f"rsakeypair {label_name}")
        if storage_type:
            configs.append(f"storage {storage_type}")
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Trustpoint related config on device "
            "Error: {error}".format(error=e)
            )        

