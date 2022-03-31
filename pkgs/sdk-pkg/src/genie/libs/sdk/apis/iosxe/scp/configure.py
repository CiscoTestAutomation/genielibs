"""Common configure/unconfigure functions for SCP"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_scp_local_auth(
        device,
        username,
        password,
        scp_server_enable=True                    
        ):
    """ Configures SCP parameters
        Args:
            device (`obj`): Device object
            username ('str'): username of the device
            password ('str'): password for the device
            scp_server_enable ('boolean', 'Optional'): 
                Enabling SCP server, default is True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring SCP parameters"
    )


    configs = ['aaa new-model',
            'aaa authentication login default local',
            'aaa authorization exec default local',
            'line vty 0 4',
            'transport input ssh'
        ]
    if username and password:
        configs.append(f"username {username} password {password}")
    if scp_server_enable:
        configs.append(f"ip scp server enable")
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to configure scp parameters,"
             "Error:\n{error}".format(error=e)
        )
        raise


def unconfigure_scp_local_auth(
        device,
        username,
        password,
        scp_server_disable=True                    
        ):
    """ unonfigures SCP parameters
        Args:
            device (`obj`): Device object
            username ('str'): username of the device
            password ('str'): password for the device
            scp_server_disable ('boolean', 'Optional'): 
                Disabling SCP server, default is True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring SCP parameters"
    )


    configs = ['aaa new-model',
            'no aaa authentication login default local',
            'no aaa authorization exec default local',
            'line vty 0 4',
            'transport input none'
        ]
    if username and password:
        configs.append(f"no username {username} password {password}")
    if scp_server_disable:
        configs.append(f"no ip scp server enable")
    
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error("Failed to unconfigure scp parameters,"
             "Error:\n{error}".format(error=e)
        )
        raise


