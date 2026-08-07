"""Common execute functions for IOS XE subscriber."""

from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement


_CONFIRM_DIALOG = Dialog(
    [
        Statement(
            pattern=r".*\[confirm\].*",
            action="sendline()",
            loop_continue=True,
            continue_timer=False,
        )
    ]
)


def execute_clear_subscriber_session_all(device, timeout=60):
    """Execute ``clear subscriber session all``.

        Args:
            device ('obj'): Device object
            timeout ('int', optional): Execute timeout in seconds. Defaults to 60

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to execute command
    """

    command = "clear subscriber session all"

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not execute '{command}' on {device}. Error:\n{error}".format(
                command=command,
                device=device,
                error=e,
            )
        ) from e


def execute_clear_subscriber_session_username(device, username, timeout=60):
    """Execute ``clear subscriber session username {username}``.

        Args:
            device ('obj'): Device object
            username ('str'): Subscriber username
            timeout ('int', optional): Execute timeout in seconds. Defaults to 60

        Returns:
            None

        Raises:
            SubCommandFailure: Failed to execute command
    """

    command = "clear subscriber session username {username}".format(
        username=username
    )

    try:
        return device.execute(command, reply=_CONFIRM_DIALOG, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not execute '{command}' on {device}. Error:\n{error}".format(
                command=command,
                device=device,
                error=e,
            )
        ) from e


def execute_show_subscriber_session_feature(device, feature):
    """ Execute show subscriber session feature on device

        Args:
            device (`obj`): Device object
            feature (`str`): Feature name (e.g. 'l4redirect', 'policing',
                'qos-peruser', 'session-timer')
        Returns:
            output (`str`): Output of execution
        Raises:
            SubCommandFailure
    """
    try:
        output = device.execute(
            f"show subscriber session feature {feature}"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute show subscriber session feature {feature}. "
            f"Error: {e}"
        )

    return output
