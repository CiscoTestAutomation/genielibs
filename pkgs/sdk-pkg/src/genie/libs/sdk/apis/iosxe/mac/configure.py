"""Common configure functions for mac"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def config_mac_aging_time(device, bridge_domain, aging_time):
    """ Config mac-aging time under bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
            aging_time (`int`): mac aging-time
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    log.info(
        "Configuring mac aging-time to {} seconds under "
        "bridge domain {}".format(aging_time, bridge_domain)
    )
    try:
        device.configure(
            [
                "bridge-domain {}".format(bridge_domain),
                "mac aging-time {}".format(aging_time),
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure aging time under bridge domain {bridge_domain}".format(
                bridge_domain=bridge_domain
            )
        )


def unconfig_mac_aging_time(device, bridge_domain):
    """ Unconfig mac-aging time under bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    log.info(
        "Removing mac aging-time configuration under "
        "bridge domain {}".format(bridge_domain)
    )
    try:
        device.configure(
            ["bridge-domain {}".format(bridge_domain), "no mac aging-time"]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure aging time under bridge domain {bridge_domain}".format(
                bridge_domain=bridge_domain
            )
        )


def config_mac_learning(device, bridge_domain):
    """ Config mac learning under bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    log.info(
        "Configuring mac learning under bridge domain {}".format(bridge_domain)
    )
    try:
        device.configure(
            ["bridge-domain {}".format(bridge_domain), "mac learning"]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure mac learning under bridge domain {bridge_domain}".format(
                bridge_domain=bridge_domain
            )
        )


def unconfig_mac_learning(device, bridge_domain):
    """ Unconfig mac learning under bridge domain

        Args:
            device (`obj`): device object
            bridge_domain (`int`): bridge domain id
        Return:
            None
        Raises:
            SubCommandFailure: Failed configuring device
    """
    log.info(
        "Removing mac learning under bridge domain {}".format(bridge_domain)
    )
    try:
        device.configure(
            ["bridge-domain {}".format(bridge_domain), "no mac learning"]
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure mac learning under bridge domain {bridge_domain}".format(
                bridge_domain=bridge_domain
            )
        )
