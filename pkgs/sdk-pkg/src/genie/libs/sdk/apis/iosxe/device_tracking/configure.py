
"""Common configure functions for device tracking policy"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_device_tracking_policy(
    device,
    client_policy_name,
    server_policy_name,
    protocol,
    ):
    
    """ Configure device tracking Policy
        Args:
            device ('obj'): device to use
            client_policy_name ('str'): name of the policy to be configured on client side
            server_policy_name ('str'): name of the policy to be configured on server side
            protocol ('str'): protocol to be configured (arp,dhcp4,dhcp6,ndp,udp)

        Returns:
            None
            
        Raises:
            SubCommandFailure: Failed configuring device tracking policy
    """

    log.debug('Configuring device tracking Policy of client_policy_name={client_policy_name}on' 
              'client side,server_policy_name={server_policy_name} on server side'.
              format(client_policy_name=client_policy_name,
              server_policy_name=server_policy_name))

    if protocol == 'arp':
        cmd = \
            ['device-tracking policy {client_policy_name}'.format(client_policy_name=client_policy_name),
             'security-level glean', 'tracking enable',
             'device-tracking policy {server_policy_name}'.format(server_policy_name=server_policy_name),
             'trusted-port']
        try:
            device.configure(cmd)
        except SubCommandFailure:

            log.warning('Could not configure device tracking Policy {client_policy_name} and'
                        '{server_policy_name}'.format(client_policy_name=client_policy_name,
                        server_policy_name=server_policy_name),exc_info=True)
            raise

    if protocol == 'dhcp6':
        cmd = [
            'device-tracking policy {client_policy_name}'.format(client_policy_name=client_policy_name),
            'device-role node',
            'protocol dhcp6',
            'protocol ndp',
            'device-tracking policy {server_policy_name}'.format(server_policy_name=server_policy_name),
            'device-role node',
            'protocol dhcp6',
            'protocol ndp',
            ]
        try:
            device.configure(cmd)
        except SubCommandFailure:

            log.warning('Could not configure device tracking Policy {client_policy_name} and'
                        '{server_policy_name}'.format(client_policy_name=client_policy_name,
                        server_policy_name=server_policy_name), exc_info=True)
            raise

    if protocol == 'dhcp6_trust':
        cmd = [
            'device-tracking policy {client_policy_name}'.format(client_policy_name=client_policy_name),
            'device-role node',
            'protocol dhcp6',
            'protocol ndp',
            'trusted-port',
            'device-tracking policy {server_policy_name}'.format(server_policy_name=server_policy_name),
            'device-role node',
            'protocol dhcp6',
            'protocol ndp',
            'trusted-port',
            ]
        try:
            device.configure(cmd)
        except SubCommandFailure:
            log.warning('Could not configure device tracking Policy {client_policy_name} and'
                        '{server_policy_name}'.format(client_policy_name=client_policy_name,
                        server_policy_name=server_policy_name), exc_info=True)
            raise
    else:

        log.debug('Invalid protocol')

def configure_device_policy_tracking(device, policy_name, tracking=True):
    """Configure device policy tracking 
    Args:
        device (`obj`): Device object
        policy_name('str'): policy name
        tracking('boolean',optional): Flag to configure tracking enable (Default True)
    Return:
        None
    Raise:
        SubCommandFailure
    """
    cmd = [f'device-tracking policy {policy_name}']
    if tracking:
        cmd.append("tracking enable")
    else:
        cmd.append("tracking disable")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure device policy tracking on {device}. Error:\n{e}"
        )

def configure_source_tracking_on_interface(device, interface, value):
    """Configure source tracking on interface
    Args:
        device (`obj`): Device object
        interface ('str'): interface name
        value ('str'): provide the values details
    Return:
        None
    Raise:
        SubCommandFailure
    """
    cmd = [
        f'interface {interface}',
        f'ip verify source {value}'
          ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure source tracking on {interface}. Error:\n{e}"
        )