import re
import logging

log = logging.getLogger(__name__)


def get_mgmt_src_ip_addresses(device):
    """ Get the source IP addresses connected via SSH or telnet to the device.

    Returns:
        List of IP addresses or []
    """
    # tcp        0      0 1.1.1.161:22        1.1.1.26:60718      ESTABLISHED 24543/sshd: admin [
    show_tcp_output = device.execute('bash netstat -antp')
    mgmt_src_ip_addresses = re.findall(r':(?:22|23) +(\S+):\d+ +ESTAB', show_tcp_output)
    if not mgmt_src_ip_addresses:
        log.error('Unable to find management session, cannot determine management IP addresses')
        return []

    log.info('Device management source IP addresses: {}'.format(mgmt_src_ip_addresses))

    return mgmt_src_ip_addresses


def get_mgmt_ip_and_mgmt_src_ip_addresses(device):
    """ Get the management IP address and management source addresses.

    Returns:
        Tuple of mgmt_ip and list of IP address (mgmt_ip, [mgmt_src_addrs]) or None
    """
    tcp_output = device.execute('bash netstat -antp')

    # tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      32230/sshd
    # tcp        0      0 1.1.1.161:22        1.1.1.26:60718      ESTABLISHED 24543/sshd: admin [
    mgmt_addresses = re.findall(r'\w+ +(\S+):(?:22|23) +(\S+):\d+ +ESTAB', tcp_output)
    if mgmt_addresses:
        mgmt_ip = [m[0] for m in mgmt_addresses][0]
        mgmt_src_ip_addresses = set([m[1] for m in mgmt_addresses])
    else:
        log.error('Unable to find management session, cannot determine management IP addresses')
        return []

    log.info('Device management IP: {}'.format(mgmt_ip))
    log.info('Device management source IP addresses: {}'.format(mgmt_src_ip_addresses))

    return (mgmt_ip, mgmt_src_ip_addresses)
