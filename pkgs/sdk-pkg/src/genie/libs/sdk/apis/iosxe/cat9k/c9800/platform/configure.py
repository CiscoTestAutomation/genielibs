# Python
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

DEFAULT_RRM_DCA_CHANNELS = (
    '52', '56', '60', '64', '100', '104', '108', '112', '116', '120',
    '124', '128', '132', '136', '140', '144',
)


def enable_http_server(device):
    """Configure ip http server
    Args:
        device (obj): Device object
    Returns:
            None
    Raises:
            SubCommandFailure
    """

    try:
        device.configure("ip http server")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in enable http server "
            "on device {device} "
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully enabled http server for {}".format(device.name))


def set_clock_calendar(device):
    """Configure clock calendar-valid 
    Args:
        device (obj): Device object
    Returns:
            None
    Raises:
            SubCommandFailure
    """

    try:
        device.configure("clock calendar-valid")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in set valid clock calender "
            "on device {device} "
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully set clock calendar for {}".format(device.name))


def configure_rrm_dca_channel(device, channel_list=None):
    """Remove 5 GHz RRM DCA channels from the controller.

    Args:
        device (obj): Device object.
        channel_list (list[str], optional): Channels to remove. Defaults to
            the C9800 restricted-channel list.

    Returns:
        None

    Raises:
        SubCommandFailure: If the configuration fails.
    """
    if channel_list is None:
        channel_list = DEFAULT_RRM_DCA_CHANNELS

    commands = [f'wireless rf-network {device.name}']
    commands.extend(
        f'ap dot11 5ghz rrm channel dca remove {channel}'
        for channel in channel_list
    )
    commands.append('ap dot11 5ghz rrm group-mode auto')

    try:
        device.configure(commands)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Failed to remove RRM DCA channels on {device.name}: {error}'
        ) from error


def configure_ap_tx_power(device, access_points, tx_power='1'):
    """Configure transmit power for the specified access points.

    Args:
        device (obj): Device object.
        access_points (list[str]): Access point names to configure.
        tx_power (str, optional): Transmit-power level. Defaults to ``1``.

    Returns:
        None

    Raises:
        SubCommandFailure: If the configuration fails.
    """
    if not access_points:
        return

    try:
        for ap_name in access_points:
            ap_model = device.api.get_ap_model(ap_name)
            device.api.execute_ap_tx_power_commands(
                ap_name, ap_model, tx_power)

        device.configure([
            f'ap dot11 5ghz rrm txpower {tx_power}',
            f'ap dot11 24ghz rrm txpower {tx_power}',
        ])
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f'Failed to configure AP transmit power on {device.name}: '
            f'{error}'
        ) from error
