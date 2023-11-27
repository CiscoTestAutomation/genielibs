
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
    
def configure_device_tracking_logging(device, logging_type='drop'):
    """Configure device tracking logging
    Args:
        device (obj): Device object.
        logging_type (str): Type of logging to configure ex:'packet','theft',or'resolution-veto' (default is 'drop')
    Returns:
        None
    Raises:
        SubCommandFailure
        ValueError: If an invalid logging_type is provided.
    """
    if logging_type=="packet":
        config = f"device-tracking logging {logging_type} drop"
    else:
        config = f"device-tracking logging {logging_type}"

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to configure device tracking logging on {device.name}\n{e}')
    
def unconfigure_device_tracking_logging(device, logging_type='drop'):
    """unconfigure device tracking logging
    Args:
        device (obj): Device object.
        logging_type (str): Type of logging to configure ex:'packet','theft',or'resolution-veto' (default is 'drop')
    Returns:
        None
    Raises:
        SubCommandFailure
        ValueError: If an invalid logging_type is provided.
    """
    if logging_type=="packet":
        config = f"no device-tracking logging {logging_type} drop"
    else:
        config = f"no device-tracking logging {logging_type}"

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to unconfigure device tracking logging on {device.name}\n{e}')