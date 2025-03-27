'''IOSXE Common configure functions for sirius telemetry'''

# Unicon
from unicon.core.errors import SubCommandFailure


def configure_product_analytics(device):
    """ product-analytics
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    try:
        device.configure('product-analytics')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable product analytics on {device}. Error:\n{error}"
            .format(device=device, error=e)
        )


def unconfigure_product_analytics(device):
    """ no product-analytics
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    try:
        device.configure('no product-analytics')
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
            f"Could not configure telemetry ietf subscription on {device}. Error: \n{e}"
        )


def configure_telemetry_ietf_parameters(device, sub_id, stream, receiver_ip, receiver_port, protocol,
                                        filter_value='/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds',
                                        encoding='encode-kvgpb', update_policy='periodic',
                                        periodic_update_interval=500, source_address=None, source_vrf=None):
    """
    Configure telemetry ietf subscription with sub_id on device
        Args:
            device (`obj`): Device object
            sub_id('int'): <0-2147483647>  Subscription Identifier
            stream('str'): Stream type
            receiver_ip('str'): IP of the receiving server
            receiver_port('int'): Port of the receiving service on the server
            protocol('str'): The protocol over which telemetry updates are sent
            filter_value('str', Optional): The xpath filter. Default 'xpath'
            encoding('str', Optional): Encoding format. Default 'encode-kvgpb'
            update_policy('str', Optional): Update policy type - 'periodic' or 'on-update'. Default 'periodic'
            periodic_update_interval('int', Optional): The interval at which updates are sent in centiseconds. Default 500
            source_address('str', Optional): Source address for updates
            source_vrf('str', Optional): Source vrf for updates
        Returns:
            None
        Raises:
            SubCommandFailure : Failed configuring device
    """
    cmd = [
        f"telemetry ietf subscription {sub_id}",
        f"receiver ip address {receiver_ip} {receiver_port} protocol {protocol}",
        f"stream {stream}"
           ]

    if filter_value:
        cmd.append(f"filter xpath {filter_value}")
    if encoding:
        cmd.append(f"encoding {encoding}")
    if source_address:
        cmd.append(f"source-address {source_address}")
    if source_vrf:
        cmd.append(f"source-vrf {source_vrf}")
    if update_policy:
        if update_policy.lower() == 'periodic':
            cmd.append(f"update-policy periodic {periodic_update_interval}")
        elif update_policy.lower() == 'on-change':
            cmd.append("update-policy on-change")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure telemetry ietf subscription parameters on {device}. Error: \n{e}"
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
            f"Could not unconfigure telemetry ietf subscription on {device}. Error: \n{e}"
        )
