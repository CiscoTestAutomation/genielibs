'''IOSXE Common configure functions for sirius telemetry'''

# Unicon
from unicon.core.errors import SubCommandFailure

def configure_pae(device):
    """ pae
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : : Failed configuring device
    """
    try:
        device.configure('pae')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable product analytics on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_pae(device):
    """ no pae
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    try:
        device.configure('no pae')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable product analytics on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_license_smart_transport_smart(device):
    """ license smart transport smart
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : : Failed configuring device
    """
    try:
        device.configure('license smart transport smart')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable smart transport on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_license_smart_transport(device):
    """ no license smart transport
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : : Failed configuring device
    """
    try:
        device.configure('no license smart transport')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable smart transport on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
