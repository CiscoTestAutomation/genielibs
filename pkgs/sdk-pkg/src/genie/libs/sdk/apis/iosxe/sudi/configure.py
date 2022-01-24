'''IOSXE Common configure functions for sudi 99'''

# Unicon
from unicon.core.errors import SubCommandFailure

def configure_platform_sudi_cmca3(device):
    """ platform sudi cmca3
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """

    try:
        device.configure('platform sudi cmca3')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable sudi cmca3 on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_platform_sudi_cmca3(device):
    """ no platform sudi cmca3
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : : Failed configuring device
    """

    try:
        device.configure('no platform sudi cmca3')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable sudi cmca3 on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_service_private_config_encryption(device):
    """ service private-config-encryption
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """

    try:
        device.configure('service private-config-encryption')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable service private-config-encryption on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_service_private_config_encryption(device):
    """ no service private-config-encryption
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """

    try:
        device.configure('no service private-config-encryption')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable service private-config-encryption on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
