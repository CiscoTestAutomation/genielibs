'''IOSXE execute functions for platform-licensing'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def configure_license_smart_transport_cslu(device):
    """ Configures the license transport type to cslu
        Example : license smart transport cslu

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring transport type to cslu on {device.name}')
    config = f'license smart transport cslu'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure transport type to cslu on device {device.name}. Error:\n{e}')

def unconfigure_license_smart_transport(device):
    """ Unconfigures the license transport type
        Example : no license smart transport

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring transport type on {device.name}')
    config = f'no license smart transport'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure transport type on device {device.name}. Error:\n{e}')

def configure_license_smart_url_cslu(device, url):
    """ Configures the url for cslu transport mode
        Example : license smart url cslu http://192.168.0.1:8182/cslu/v1/pi

            device ('obj'): device to use
            url ('str'): the Smart Transport URL (eg. http://192.168.0.1:8182/cslu/v1/pi)

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring license smart url cslu on {device.name}')
    config = f'license smart url cslu {url}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure license smart url cslu on device {device.name}. Error:\n{e}')

def unconfigure_license_smart_url_cslu(device):
    """ Unconfigures the license smart url cslu
        Example : no license smart url cslu

            device ('obj'): device to use

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring license smart url cslu on {device.name}')
    config = f'no license smart url cslu'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure license smart url cslu on device {device.name}. Error:\n{e}')

def configure_line_console(device, line_number):
    """ Configures line console on a line
        Example : line console 0

            device ('obj'): device to use
            line_number ('int'): First Line number (Eg. 0)

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring line console on line {line_number} on {device.name}')
    config = f'line console {line_number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure line console on {line_number} on device {device.name}. Error:\n{e}')

def configure_ip_domain_timeout(device, time):
    """ Configures the IP domain timeout
        Example : ip domain timeout 2000

        Args:
            device ('obj'): device to use
            time ('int'): Timeout value in seconds (Range 1-3600)

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring ip domain timeout {time} on {device.name}')
    config = f'ip domain timeout {time}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure ip domain timeout {time} on device {device.name}. Error:\n{e}')

def unconfigure_ip_domain_timeout(device):
    """ Unconfigures the IP domain timeout
        Example : no ip domain timeout

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring ip domain timeout on {device.name}')
    config = f'no ip domain timeout'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure ip domain timeout on device {device.name}. Error:\n{e}')

def unconfigure_ip_http_server(device):
    """ Unconfigures ip http server
        Example : no ip http server

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring ip http server on {device.name}')
    config = 'no ip http server'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure ip http server on device {device.name}. Error:\n{e}')

def configure_ip_http_authentication_local(device):
    """ Configures ip http authentication local
        Example : ip http authentication local

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring ip http authentication local on {device.name}')
    config = 'ip http authentication local'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure ip http authentication local on device {device.name}. Error:\n{e}')

def unconfigure_ip_http_authentication_local(device):
    """ Unconfigures ip http authentication local
        Example : no ip http authentication local

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring http authentication local on {device.name}')
    config = 'no ip http authentication local'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure http authentication local on device {device.name}. Error:\n{e}')

def configure_ip_http_secure_server(device):
    """ Configures ip http secure-server
        Example : ip http secure-server

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring http secure-server on {device.name}')
    config = 'ip http secure-server'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure http secure-server on device {device.name}. Error:\n{e}')

def unconfigure_ip_http_secure_server(device):
    """ Unconfigures ip http secure-server
        Example : no ip http secure-server

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring http secure-server on {device.name}')
    config = 'no ip http secure-server'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure http secure-server on device {device.name}. Error:\n{e}')

def unconfigure_call_home(device):
    """ Unconfigures call-home
        Example : no call-home

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring call-home on {device.name}')
    config = 'no call-home'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure call-home on device {device.name}. Error:\n{e}')

def configure_license_smart_usage_interval(device, interval):
    """ Configures license smart usage interval
        Example : license smart usage interval 1

        Args:
            device ('obj'): device to use
            interval ('int'): Reporting interval in days (Range: 1-3650)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring license smart usage interval on {device.name}')
    config = f'license smart usage interval {interval}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure license smart usage interval. Error:\n{e}')

def unconfigure_http_client_source_interface(device):
    """ Unconfigures ip http client source-interface
        Example : no ip http client source-interface

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring http client source-interface on {device.name}')
    config = 'no ip http client source-interface'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure http client source-interface on device {device.name}. Error:\n{e}')

def unconfigure_ip_domain_name(device, name, vrf=None):
    """ Unconfigures ip domain name
        Example : no ip domain name cisco.com

        Args:
            device ('obj'): device to use
            name ('str'): domain name (eg. cisco.com)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring ip domain name {name} on {device.name}')
    if vrf is None:
        config = f'no ip domain name {name}'
    else:
        config = f'no ip domain name vrf {name}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure ip domain name {name} on device {device.name}. Error:\n{e}')

def configure_platform(device, license):
    """ Configures platform with a license
        Example : platform hsec-license-release

        Args:
            device ('obj'): device to use
            license ('str'): license name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f'Configuring platform {license} on {device.name}')
    config = f'platform {license}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure platform {license} on device {device.name}. Error:\n{e}')

def configure_license_smart(device, license):
    """ Configures license smart with a license
        Example : license smart transport smart

        Args:
            device ('obj'): device to use
            license ('str): license name

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f'Configuring license smart {license} on {device.name}')
    config = f'license smart {license}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to license smart {license} on device {device.name}. Error:\n{e}')
