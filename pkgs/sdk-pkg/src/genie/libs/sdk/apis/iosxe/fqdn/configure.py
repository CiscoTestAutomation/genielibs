"""Common configure functions for fqdn"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_fqdn_ttl_timeout_factor(device, factor):
    """ Configurer

        Args:
            device ('obj'): Device object
            factor ('int'): TTL timeout factor value (range 1-10)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring fqdn ttl-timeout-factor {factor} on {device}")

    try:
        device.configure(f"fqdn ttl-timeout-factor {factor}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure fqdn ttl-timeout-factor {factor} on {device}. Error:\n{e}"
        )

def unconfigure_fqdn_ttl_timeout_factor(device, factor):
    """ Unconfigure fqdn ttl-timeout-factor

        Args:
            device ('obj'): Device object
            factor ('int'): TTL timeout factor value (range 1-10)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring fqdn ttl-timeout-factor {factor} on {device}")

    try:
        device.configure(f"no fqdn ttl-timeout-factor {factor}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure fqdn ttl-timeout-factor {factor} on {device}. Error:\n{e}"
        )
