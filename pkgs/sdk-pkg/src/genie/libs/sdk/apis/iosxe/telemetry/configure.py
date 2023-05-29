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
            SubCommandFailure : Failed configuring device
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
            SubCommandFailure : Failed configuring device
    """
    try:
        device.configure('license smart transport smart')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable smart transport smart on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_license_smart_transport(device):
    """ no license smart transport
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    try:
        device.configure('no license smart transport')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable smart transport on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_license_smart_transport_callhome(device):
    """ license smart transport callhome
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    try:
        device.configure('license smart transport callhome')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable smart transport callhome on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_netconf_yang(device):
    """ pae
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    try:
        device.configure('netconf-yang')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable netconf-yang on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_netconf_yang(device):
    """ no pae
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    try:
        device.configure('no netconf-yang')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable netconf-yang on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_telemetry_ietf_subscription(device, sub_id):
    """ configure telemetry ietf subscription with sub_id on device
        Args:
            device (`obj`): Device object
            sub_id('int'): <0-2147483647>  Subscription Identifier
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    command = f'telemetry ietf subscription {sub_id}'
    try:
        device.configure(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure telemetry ietf subscription on {device}. Error: \n{error}".format(device=device, error=e)
        )

def unconfigure_telemetry_ietf_subscription(device, sub_id):
    """ un-configure telemetry ietf subscription with sub_id on device
        Args:
            device (`obj`): Device object
            sub_id('int'): <0-2147483647>  Subscription Identifier
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    command = f'no telemetry ietf subscription {sub_id}'
    try:
        device.configure(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure telemetry ietf subscription on {device}. Error: \n{error}".format(device=device, error=e)
        )