'''IOSXE execute functions for call-home'''

# Python
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def configure_call_home_http_proxy(device, proxy_server, port):
    """ Configures call-home http-proxy
        Example : http-proxy test port 1
        Args:
            device ('obj'): device to use
            proxy_server ('str'): http proxy server (eg. test)
            port ('int'): proxy server port number (Range: 1-65535)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home http-proxy on {device.name}')
    config = [
        'call-home',
        f'http-proxy {proxy_server} port {port}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home http-proxy on device {device.name}. Error:\n{e}')

def configure_call_home_mail_server(device, server, priority, secure=None):
    """ Configures call-home mail-server
        Example : mail-server test priority 1 secure tls
        Args:
            device ('obj'): device to use
            server ('str'): hostname or IPv4/IPv6 address of the email server
            priority ('int'): mail server priority (Range: 1-100)
            secure ('str'): secure settings for mail server (eg. tls)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home mail-server on {device.name}')
    config = [
        'call-home',
        f'mail-server {server} priority {priority} secure {secure}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home mail-server on device {device.name}. Error:\n{e}')

def configure_call_home_phone_number(device, phone_number):
    """ Configures call-home phone-number
        Example : phone-number +123456789012
        Args:
            device ('obj'): device to use
            phone_number ('str'): phone number (start with '+', length: 12-17)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home phone-number on {device.name}')
    config = [
        'call-home',
        f'phone-number {phone_number}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home phone-number on device {device.name}. Error:\n{e}')

def configure_call_home_rate_limit(device, rate_limit):
    """ Configures call-home rate-limit
        Example : rate-limit 1
        Args:
            device ('obj'): device to use
            rate_limit ('int'): message rate-limit threshold per minute (Range: 1-60)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home rate-limit on {device.name}')
    config = [
        'call-home',
        f'rate-limit {rate_limit}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home rate-limit on device {device.name}. Error:\n{e}')

def configure_call_home_aaa_authorization(device, username=None):
    """ Configures call-home aaa-authorization
        Example : aaa-authorization username test
        Args:
            device ('obj'): device to use
            username ('str'): name of the user
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home aaa-authorization on {device.name}')
    config = ['call-home']
    if username:
        config.append(f'aaa-authorization username {username}')
    else:
        config.append('aaa-authorization')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home aaa-authorization on device {device.name}. Error:\n{e}')

def configure_call_home_alert_group(device, group):
    """ Configures call-home alert-group
        Example : alert-group inventory
        Args:
            device ('obj'): device to use
            group ('str'): alert-group name
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home alert-group {group} on {device.name}')
    config = [
        'call-home',
        f'alert-group {group}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home alert-group on device {device.name}. Error:\n{e}')

def configure_call_home_alert_group_config_snapshot(device, add_command_type='', cli=''):
    """ Configures call-home alert-group-config snapshot
        Example : alert-group-config snapshot
        Args:
            device ('obj'): device to use
            add_command_type ('str'): type of CLI command to be added (eg. default, no)
            cli ('str'): cli command (1-127) characters. If includes spaces,
                        enclose the entry in quotes ("")
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home alert-group-config snapshot on {device.name}')
    config = [
        'call-home',
        'alert-group-config snapshot'
    ]
    if not add_command_type and not cli:
        config.append(f'exit')
    elif add_command_type:
        config.append(f'{add_command_type} add-command {cli}')
    else:
        config.append(f'add-command {cli}')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home alert-group-config snapshot on device {device.name}. Error:\n{e}')

def configure_call_home_contact_email_addr(device, email):
    """ Configures call-home contact_email_addr
        Example : contact-email-addr test@test.com
        Args:
            device ('obj'): device to use
            email ('str'): contact person's email address
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home contact-email-addr on {device.name}')
    config = [
        'call-home',
        f'contact-email-addr {email}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home contact-email-addr on device {device.name}. Error:\n{e}')

def configure_call_home_contract_id(device, id):
    """ Configures call-home contract-id
        Example : contract-id test123
        Args:
            device ('obj'): device to use
            id ('str'): alphanumeric contract identification
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home contract-id on {device.name}')
    config = [
        'call-home',
        f'contract-id {id}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home contract-id on device {device.name}. Error:\n{e}')

def configure_call_home_copy_profile(device, source_profile, target_profile):
    """ Configures call-home copy profile
        Example : copy profile test_source test_target
        Args:
            device ('obj'): device to use
            source_profile ('str'): source profile name
            target_profile ('str'): target profile name
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home copy profile on {device.name}')
    config = [
        'call-home',
        f'copy profile {source_profile} {target_profile}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home copy profile on device {device.name}. Error:\n{e}')

def configure_call_home_customer_id(device, id):
    """ Configures call-home customer-id
        Example : customer-id test123
        Args:
            device ('obj'): device to use
            id ('str'): alphanumeric customer identification
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home customer-id on {device.name}')
    config = [
        'call-home',
        f'customer-id {id}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home customer-id on device {device.name}. Error:\n{e}')

def configure_call_home_rename_profile(device, source, target):
    """ Configures call-home rename profile
        Example : rename profile test_abc test_123
        Args:
            device ('obj'): device to use
            source ('str'): source profile name
            target ('str'): target profile name
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home rename profile on {device.name}')
    config = [
        'call-home',
        f'rename profile {source} {target}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home rename profile on device {device.name}. Error:\n{e}')

def configure_call_home_site_id(device, site_id):
    """ Configures call-home site-id
        Example : site-id test_site
        Args:
            device ('obj'): device to use
            site_id ('str'): alphanumeric site identification
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home site-id on {device.name}')
    config = [
        'call-home',
        f'site-id {site_id}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home site-id on device {device.name}. Error:\n{e}')

def configure_call_home_source_ip_address(device, ip):
    """ Configures call-home source-ip-address
        Example : source-ip-address 1.1.1.1
        Args:
            device ('obj'): device to use
            ip ('str'): IPv4/IPv6 source IP address
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home source-ip-address on {device.name}')
    config = [
        'call-home',
        f'source-ip-address {ip}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home source-ip-address on device {device.name}. Error:\n{e}')

def configure_call_home_data_privacy(device, level=None):
    """ Configures call-home data-privacy
        Example : data-privacy level high
        Args:
            device ('obj'): device to use
            level ('str'): data-privacy level (eg. high or normal)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home data_privacy on {device.name}')
    config = ['call-home']
    if level is None:
        config.append(f'data-privacy hostname')
    else:
        config.append(f'data-privacy level {level}')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home data-privacy on device {device.name}. Error:\n{e}')

def configure_call_home_http_resolve_hostname_ipv4_first(device):
    """ Configures call-home http resolve-hostname ipv4-first
        Example : http resolve-hostname ipv4-first
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """ 
    log.info(f'Configuring call-home http resolve-hostname on {device.name}')
    config = [
        'call-home',
        'http resolve-hostname ipv4-first'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure http resolve-hostname on device {device.name}. Error:\n{e}')

def configure_call_home_http_secure_server_identity_check(device):
    """ Configures call-home secure server-identity-check
        Example : http secure server-identity-check
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """ 
    log.info(f'Configuring call-home http secure server-identity-check on {device.name}')
    config = [
        'call-home',
        'http secure server-identity-check'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure http secure on device {device.name}. Error:\n{e}')

def unconfigure_call_home_sub_cli(device, sub_cli):
    """ Unconfigures call-home sub cli
        Example : no rate-limit
        Args:
            device ('obj'): device to use
            sub_cli ('str'): sub-cli to unconfigure (eg. rate-limit)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Unconfiguring call-home {sub_cli} on {device.name}')
    config = [
        'call-home',
        f'no {sub_cli}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure call-home {sub_cli} on device {device.name}. Error:\n{e}')

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

def configure_call_home_street_address(device, address):
    """ Configures call-home street-address
        Example : street-address 123abcStreet
        Args:
            device ('obj'): device to use
            address ('str'): street address, city, state, and zip code. If includes
                            spaces, enclose the entry in quotes ("")
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f'Configuring call-home street-address on {device.name}')
    config = [
        'call-home',
        f'street-address {address}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home street-address on device {device.name}. Error:\n{e}')

def configure_call_home_syslog_throttling(device):
    """ Configures call-home syslog-throttling 
        Example : syslog-throttling
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f'Configuring call-home syslog-throttling on {device.name}')
    config = [
        'call-home',
        'syslog-throttling'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home syslog-throttling on device {device.name}. Error:\n{e}')

def configure_call_home_vrf(device, vrf_name):
    """ Configures call-home vrf
        Example : vrf vrf1
        Args:
            device ('obj'): device to use
            vrf_name ('str'): VRF instance name
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f'Configuring call-home vrf on {device.name}')
    config = [
        'call-home',
        f'vrf {vrf_name}'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure call-home vrf on device {device.name}. Error:\n{e}')

def configure_call_home_profile_active(device, profile):
    """ Configures call home profile active
        Args:
            device ('obj'): device to use
            profile ('str'): call home profile
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "call-home",
        f"profile {profile}",
        "active"
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configurecall home profile active on device {device.name}. Error:\n{e}")

def unconfigure_call_home_profile_active(device, profile):
    """ Unconfigures call home profile active
        Args:
            device ('obj'): device to use
            profile ('str'): call home profile
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "call-home",
        f"profile {profile}",
        "no active"
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigurecall home profile active on device {device.name}. Error:\n{e}")

def configure_call_home_profile_anonymous_reporting_only(device, profile):
    """ Configures call home profile anonymous-reporting-only
        Args:
            device ('obj'): device to use
            profile ('str'): call home profile
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "call-home",
        f"profile {profile}",
        "anonymous-reporting-only"
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configurecall home profile anonymous-reporting-only on device {device.name}. Error:\n{e}")

def configure_call_home_profile_subscribe_to_alert_group(device, profile, group):
    """ Configures call home profile active
        Args:
            device ('obj'): device to use
            profile ('str'): call home profile
            group ('str): alert group 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "call-home",
        f"profile {profile}",
        f"subscribe-to-alert-group {group}"
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configurecall home profile active on device {device.name}. Error:\n{e}")

def configure_call_home_profile_destination_address(device, profile, address, address_url):
    """ Configures call home profile destination address
        Args:
            device ('obj'): device to use
            profile ('str'): call home profile
            address ('str'): address to profile email or http
            address_url ('int'): address url 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "call-home",
        f"profile {profile}",
        f"destination address {address} {address_url}"
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configurecall home profile destination address on device {device.name}. Error:\n{e}")

def configure_call_home_profile_destination_message_size_limit(device, profile, msg_size):
    """ Configures call home profile destination message size limit 
        Args:
            device ('obj'): device to use
            profile ('str'): call home profile
            msg_size ('int'): maximum call-home message size <50-3145728>
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "call-home",
        f"profile {profile}",
        f"destination message-size-limit {msg_size}"
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configurecall home profile destination message size limit on device {device.name}. Error:\n{e}")

def configure_call_home_profile_destination_preferred_msg_format(device, profile, msg_format):
    """ Configures call home profile destination preferred-msg-format
        Args:
            device ('obj'): device to use
            profile ('str'): call home profile
            msg_format ('str'): message format (long-term, short-term, xml)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "call-home",
        f"profile {profile}",
        f"destination preferred-msg-format {msg_format}"
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configurecall home profile destination preferred-msg-format on device {device.name}. Error:\n{e}")

def configure_call_home_profile_destination_transport_method(device, profile, address):
    """ Configures call home profile destination address transport-method
        Args:
            device ('obj'): device to use
            profile ('str'): call home profile
            address ('str'): address to profile email or http
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        "call-home",
        f"profile {profile}",
        f"destination transport-method {address}"
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configurecall home profile destination transport-method on device {device.name}. Error:\n{e}")

def unconfigure_call_home_profile(device, profile):
    """ Unconfigures call home profile destination
        Args:
            device ('obj'): device to use
            profile ('str'): call home profile
    """
    cmd = [
        "call-home",
        f"no profile {profile}",
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigurecall home profile on device {device.name}. Error:\n{e}")

def configure_service_call_home(device):
    """ Configures service call home 
        Args:
            device ('obj'): device to use
    """
    cmd = "service call-home"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure service call home on device {device.name}. Error:\n{e}")

def unconfigure_service_call_home(device):
    """ Unconfigures serbice call home 
        Args:
            device ('obj'): device to use
    """
    cmd = "no service call-home"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure service call home on device {device.name}. Error:\n{e}")

def configure_call_home_profile_reporting(device, profile, reporting):
    """ Configures call home reporting
        Args:
            device ('obj'): device to use
    """
    cmd = [
        "call-home",
        f"profile {profile}",
        f"reporting {reporting}"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure call home reporting on device {device.name}. Error:\n{e}")


def configure_call_home_profile(device, dest_add, profile_name="CiscoTAC-1"):
    """ Configure call home profile
        Args:
            device ('obj'): device to use
            dest_add ('str'): destination address 
            profile_name ('str', optional): call home profile name, default is CiscoTAC-1
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure call home profile
    """

    cmd = ["call-home", "no http secure server-identity-check", f"profile {profile_name}", "active", 
           "destination transport-method http", f"destination address http {dest_add}", 
           "reporting smart-licensing-data"]

    log.info("Creating call home profile")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure call home profile. Error\n{e}")
