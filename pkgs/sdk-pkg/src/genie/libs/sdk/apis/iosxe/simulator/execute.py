"""Execute CLI functions for IOS XE simulator."""

from unicon.core.errors import SubCommandFailure


def execute_clear_simulator_radius_request(device):
    """Execute ``clear simulator radius request all``.

        Args:
            device ('obj'): Device object

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to execute command
    """

    command = "clear simulator radius request all"

    try:
        device.execute(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not execute '{command}' on {device}. Error:\n{error}".format(
                command=command,
                device=device,
                error=e,
            )
        ) from e


def execute_clear_simulator_radius_testcase(device):
    """Execute ``clear simulator radius testcase all``.

        Args:
            device ('obj'): Device object

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to execute command
    """

    command = "clear simulator radius testcase all"

    try:
        device.execute(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not execute '{command}' on {device}. Error:\n{error}".format(
                command=command,
                device=device,
                error=e,
            )
        ) from e


def execute_simulator_radius_request_coa(
    device, profile_num, client_ip=None, host_ip=None
):
    """Execute simulator radius CoA request on device.

        Args:
            device (`obj`): Device object
            profile_num (`int`): Profile number
            client_ip (`str`, optional): Client IP address.
                Required together with host_ip. Defaults to None
            host_ip (`str`, optional): Host IP address.
                Required together with client_ip. Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    command = "simulator radius request 1 coa {profile_num}".format(
        profile_num=profile_num
    )
    if client_ip and host_ip:
        command += " client {client_ip} host {host_ip}".format(
            client_ip=client_ip,
            host_ip=host_ip,
        )

    try:
        device.execute(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to execute simulator radius request coa. Error: {error}".format(
                error=e
            )
        ) from e
