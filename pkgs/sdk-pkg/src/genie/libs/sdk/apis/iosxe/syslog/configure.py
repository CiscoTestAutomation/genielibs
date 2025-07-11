# Steps
from pyats.aetest.steps import Steps

import re
import logging
from time import sleep
# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

log = logging.getLogger(__name__)
def configure_syslog_server(device, ip_address, transport=None, vrf_name=None):
    """ Configure Syslog servers

        Args:
            device ('obj'): Device to be configured
            ip_address ('str'): IP address of the syslog server
            transport ('str', optional): Transport protocol to be used (e.g., 'udp', 'tcp')
            vrf_name ('str', optional): VRF name to be used
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = f"logging host {ip_address}"
    if vrf_name:
        configs += f" vrf {vrf_name}"
    if transport:
        configs += f" transport {transport}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure syslog server with ip address {ip_address} on device {device.name}"
        )

def configure_logging_tls_profile(device, profile_name, tls_version, cipher, trustpoint):
    """ Configure logging TLS profile

        Args:
            device ('obj'): Device to be configured
            profile_name ('str'): Name of the TLS profile to be configured
            tls_version ('str'): TLS version to be used (e.g., '1.2', '1.3')
            cipher ('str'): Cipher suite for this TLS profile
            trustpoint ('str'): Trustpoint of the client
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = [f'logging tls-profile {profile_name}',
            f'client-id-trustpoint {trustpoint}',
            f'ciphersuite {cipher}'
            ]
     # Add tls-version configuration if provided
    if tls_version is not None:
        configs.append(f'tls-version {tls_version}')   
    try:
        device.configure(configs)
    except SubCommandFailure as err:
        log.error(err)
        raise SubCommandFailure(f"ERROR: Unable to configure on the device : {device.name}")

def configure_syslog_server_tls_profile(device, ip_address, profile_name, vrf_name=None):
    """ Configure Syslog server with TLS profile

        Args:
            device ('obj'): Device to be configured
            ip_address ('str'): IP address of the syslog server
            profile_name ('str'): TLS profile to be configured
            vrf_name ('str', optional): VRF name to be used
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if vrf_name is None:
        configs = f"logging host {ip_address} transport tls profile {profile_name}"
    else:
        configs = f"logging host {ip_address} vrf {vrf_name} transport tls profile {profile_name}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure syslog server with IP address {ip_address} on device {device.name}"
        )

def unconfigure_logging_tls_profile(device, profile_name):
    """ Unconfigure logging TLS profile

        Args:
            device ('obj'): Device to be unconfigured
            profile_name ('str'): Name of the TLS profile to be removed
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = [f'no logging tls-profile {profile_name}']
    try:
        device.configure(configs)
    except SubCommandFailure as err:
        log.error(err)
        raise SubCommandFailure(f"Failed to unconfigure profile {profile_name} device {device.name}")

def unconfigure_syslog_server_tls_profile(device, ip_address, profile_name):
    """ Unconfigure Syslog server with TLS profile

        Args:
            device ('obj'): Device to be unconfigured
            ip_address ('str'): IP address of the syslog server
            profile_name ('str'): TLS profile to be unconfigured
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if profile_name is not None:
        config = f"no logging host {ip_address} transport tls profile {profile_name}"
    else:   
        config = f"no logging host {ip_address}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure syslog server with ip address {ip_address} on device {device.name}"
        )

def change_cipher_from_tls_profile(device, profile_name, cipher):
    """ Change cipher in a TLS profile

        Args:
            device ('obj'): Device to be configured
            profile_name ('str'): Name of the TLS profile to be updated
            cipher ('str'): New cipher suite to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = [f'logging tls-profile {profile_name}',
               'no ciphersuite',
               f'ciphersuite {cipher}']
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to change cipher in TLS profile {profile_name} on device {device.name}"
        )

def configure_logging_discrimnator(device, filter_name, filter_field, filter_value, filter_type):
    """ Configure logging tls profile

        Args:
            device ('obj') : Device to be configured server
            filter_name ('str'): logging discrimnator to be configured
            filter_field ('str'): field based on which the discrimnator 
                                 to be configured eg: msg_body, mnemonics, facility, severity
            filter_value ('str'): value to be filtered eg: CONFIG_I
            filter_type ('str'): drops or includes
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    configs = [f'logging discriminator {filter_name} {filter_field} {filter_type} {filter_value}']
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure logging discriminator {filter_name} on device {device.name}"
        )
        

def unconfigure_logging_discrimnator(device, filter_name):
    """ Configure logging tls profile

        Args:
            device ('obj') : Device to be configured server
            filter_name ('str'): logging discrimnator to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = [f'no logging discriminator {filter_name}']
    try:
        device.configure(configs)
    except Exception as err:
        log.error(f"ERROR: Unable to configure on the device : {device} Error:{err}")
        raise SubCommandFailure(
            f"Failed to unconfigure logging discriminator {filter_name} on device {device.name}"
        )

def apply_logging_discrimnator(device, filter_name, ip_address, transport, profile_name, vrf_name=None):
    """ Configure logging discrimnator on syslog server

        Args:
            device ('obj') : Device to be configured server
            filter_name ('str'): logging discrimnator to be configured
            ip_address ('str'): ip address of host to be configured
            transport ('str'): transport to be configured
            profile_name('str'): name of the tls profile for logging host
            vrf_name('str'): vrf_name through which logging host can be reached from device
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = f"logging host {ip_address}"
    if vrf_name is not None:
        configs += f" vrf {vrf_name}"
    if transport is not None:
        configs += f" transport {transport} profile {profile_name}" 
    configs += f" discriminator {filter_name}"

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure syslog server with ip address {ip_address} on device {device.name}"
            
        )
    
def unapply_logging_discrimnator(device, ip_address, transport, filter_name, vrf_name=None):
    """ Unconfigure logging discriminator on syslog server

        Args:
            device ('obj'): Device to be configured
            ip_address ('str'): IP address of the syslog server
            transport ('str'): Transport protocol to be unconfigured (e.g., 'udp', 'tcp')
            filter_name ('str'): Name of the logging discriminator to be unapplied
            vrf_name ('str', optional): VRF name to be used
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = f"no logging host {ip_address}"
    if vrf_name is not None:
        configs += f" vrf {vrf_name}"
    if transport is not None:
        configs += f" transport {transport}" 
    configs += f" discriminator {filter_name}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure syslog server with IP address {ip_address} on device {device.name}"
        )
    

def configure_pki_import_cert(device, trustpoint, pem_import_cert):
    """ Configure pki import certificate 
    Args:
        device ('obj') : Device to be configured server 
        trustpoint ('str'): trustpoint to be configured 
        pem_import_cert ('str'): certificate to be imported
    Returns:
        True on success
    Raises:     
        SubCommandFailure
        """
            # --- Custom handler to send cert line-by-line ---
    def send_certificate_lines(spawn, context, session):
        pem_cert = pem_import_cert
        if not pem_cert:
            raise ValueError("pem_import_cert not found in context")

        cert_lines = pem_cert.strip().splitlines()
        for line in cert_lines:
            spawn.sendline(line)
        spawn.sendline('quit')

    try:
        log.debug("Configuring crypto pki import")
        dialog = Dialog([
            Statement(pattern=r'.*Source filename \[.*?\]\?\s*$',
                        action='sendline()',
                        loop_continue=True,
                        continue_timer=False),
                
            Statement(pattern=r'.*End with a blank line or the word "quit" on a line by itself\r?\n',
                        action=send_certificate_lines,
                        loop_continue=True,
                        continue_timer=False),
            Statement(pattern=r'.*% Do you really want to replace them.*?$',
                        action='sendline(y)',
                        loop_continue=True,
                        continue_timer=False)
        ])
        import_config = f"crypto pki import {trustpoint} certificate"
        error_patterns = ["% PEM files import failed.",
                "% Please delete it or use a different label.",
                "% Trustpoint {trustpoint} is in use."]
        device.configure(import_config, reply=dialog,
                    error_pattern=error_patterns, 
                    context={'pem_import_cert': pem_import_cert})
        log.debug("client certificate imported successfully")
        return True
    except Exception as e: 
        log.info("importing client certificate failed")
        log.error(e)
        raise SubCommandFailure(
            "Failed to import client certificate"
        )
