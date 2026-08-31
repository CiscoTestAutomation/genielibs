"""
Module:
    genie.libs.sdk.apis.iosxe.cloud_mgmt

Authors:
    pyATS TEAM (pyats-support@cisco.com, pyats-support-ext@cisco.com)

Description:
    Module for cloud-mgmt execute APIs.
"""

import logging

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def _verify_tls_vif_down_or_absent(
    device, max_time=60, check_interval=5
):
    """Verify that TLS-VIF2 is absent or operationally down."""
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show ip interface brief")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        interface = output.get("interface", {}).get("TLS-VIF2")
        if interface is None:
            return True

        if (
            interface.get("status") == "down"
            and interface.get("protocol") == "down"
        ):
            return True

        timeout.sleep()

    return False


def _get_cloud_mgmt_reset_event_counts(device, level):
    """Return reset, recovery, and updater error counts from logging."""
    output = str(
        device.execute(
            "show logging | include CLOUD_MGMT_RESET|CONFIG_UPDATER_ERR"
        )
    )
    notification = f"Reset Notification Called with Reset Level : {level}"
    return (
        output.count(notification),
        output.count("CLOUD_MGMT_RESET_RECOVERY"),
        output.count("CONFIG_UPDATER_ERR"),
    )


def _verify_cloud_mgmt_reset_event(
    device,
    level,
    initial_counts,
    max_time=60,
    check_interval=5,
):
    """Verify that a new reset notification and recovery event are logged."""
    initial_notifications, initial_recoveries, _ = initial_counts
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        notifications, recoveries, _ = (
            _get_cloud_mgmt_reset_event_counts(device, level)
        )
        if (
            notifications > initial_notifications
            and recoveries > initial_recoveries
        ):
            return True
        timeout.sleep()

    return False


def _verify_cloud_mgmt_ready(
    device,
    level,
    max_time,
    check_interval,
    before_reset=False,
    tunnel_max_time=None,
):
    """Verify the cloud-mgmt state required before or after a reset."""
    phase = "before" if before_reset else "after"
    tunnel_max_time = tunnel_max_time or max_time

    if before_reset and not device.api.verify_cloud_mgmt_connect_status(
        expected_connect_status="enable",
        max_time=max_time,
        check_interval=check_interval,
    ):
        raise SubCommandFailure(
            f"Cloud-mgmt is not enabled before the Level {level} reset "
            f"on {device.name}"
        )

    if not device.api.verify_cloud_mgmt_tunnel_state(
        expected_primary_status="Up",
        expected_secondary_status="Up",
        max_time=tunnel_max_time,
        check_interval=check_interval,
    ):
        if before_reset:
            raise SubCommandFailure(
                f"Cloud-mgmt tunnels are not up before the Level {level} "
                f"reset on {device.name}"
            )
        raise SubCommandFailure(
            "Cloud-mgmt tunnels did not recover within "
            f"{tunnel_max_time} seconds after the Level {level} reset on "
            f"{device.name}"
        )

    if not device.api.verify_interface_state_up(
        interface="TLS-VIF2",
        max_time=max_time,
        check_interval=check_interval,
    ):
        raise SubCommandFailure(
            f"TLS-VIF2 {'is not up' if before_reset else 'did not recover'} "
            f"{phase} the Level {level} reset on {device.name}"
        )

    if not device.api.verify_cloud_mgmt_tunnel_config(
        expected_fetch_state="Config fetch succeeded",
        max_time=max_time,
        check_interval=check_interval,
    ):
        fetch_state = (
            "has not succeeded before"
            if before_reset
            else "did not succeed after"
        )
        raise SubCommandFailure(
            f"Cloud-mgmt config fetch {fetch_state} the Level {level} reset "
            f"on {device.name}"
        )


def _verify_cloud_mgmt_down_transition(
    device,
    level,
    max_time,
    check_interval,
):
    """Verify that cloud-mgmt tunnels and TLS-VIF2 transition down."""
    if not device.api.verify_cloud_mgmt_tunnel_state(
        expected_primary_status="Down",
        expected_secondary_status="Down",
        max_time=max_time,
        check_interval=check_interval,
    ):
        raise SubCommandFailure(
            "Cloud-mgmt tunnels did not transition down after the "
            f"Level {level} reset on {device.name}"
        )

    if not _verify_tls_vif_down_or_absent(
        device,
        max_time=max_time,
        check_interval=check_interval,
    ):
        raise SubCommandFailure(
            "TLS-VIF2 did not transition down or disappear after the "
            f"Level {level} reset on {device.name}"
        )


def _check_cloud_mgmt_updater_errors(device, level, initial_counts):
    """Raise when a new configuration updater error is logged."""
    _, _, initial_updater_errors = initial_counts
    _, _, current_updater_errors = _get_cloud_mgmt_reset_event_counts(
        device, level
    )
    if current_updater_errors > initial_updater_errors:
        raise SubCommandFailure(
            f"A new CONFIG_UPDATER_ERR was logged during the Level {level} "
            f"reset on {device.name}"
        )


def _execute_cloud_mgmt_level_3_reset(device, command, reset_timeout):
    """Execute Level 3 and wait for the console to return after reset."""
    try:
        reload_result = device.reload(
            reload_command=command,
            prompt_recovery=True,
            timeout=reset_timeout,
            return_output=True,
        )
    except Exception as error:
        raise SubCommandFailure(
            f"Level 3 reset did not complete on {device.name}. "
            f"Error:\n{error}"
        ) from error

    output = getattr(reload_result, "output", "")
    if (
        not isinstance(output, str)
        or "Reset Level: 3" not in output
        or "Triggered Successfully" not in output
    ):
        raise SubCommandFailure(
            "Cloud-mgmt reset level 3 did not trigger successfully on "
            f"{device.name}. Output:\n{output}"
        )

    return output


def execute_cloud_mgmt_reset_level(
    device,
    level,
    timeout=60,
    transition_timeout=60,
    recovery_timeout=180,
    check_interval=5,
    reset_timeout=600,
):
    """Execute a cloud-management reset on the device.

    For Levels 1 and 2, verify that cloud management is enabled and its
    configuration fetch succeeded. Level 1 must transition both tunnels down
    and remove or bring down ``TLS-VIF2``. Level 2 must log a new reset and
    recovery event and perform the same down/up transition. Both levels must
    return to a healthy state within the supplied recovery timeout. Level 3
    waits for the device console to return after its factory reset.

    Args:
        device (`obj`): Device object
        level (`int`): Reset level (1, 2, or 3)
            Level 1 - Restarts nextunnel; tunnels go Down then recover Up
            Level 2 - Triggers config rollback; tunnels recover automatically
            Level 3 - Full process manager reload (device reloads)
        timeout (`int`, optional): Maximum command timeout in seconds.
            Defaults to 60.
        transition_timeout (`int`, optional): Maximum time to verify the
            initial state, Level 1 down transition, or Level 2 reset event.
            Defaults to 60.
        recovery_timeout (`int`, optional): Maximum time to wait for tunnel
            recovery. Defaults to 180.
        check_interval (`int`, optional): Interval between state checks in
            seconds. Defaults to 5.
        reset_timeout (`int`, optional): Maximum time to wait for the Level 3
            factory reset and console recovery. Defaults to 600.

    Returns:
        str: Command output

    Raises:
        ValueError: If `level` is not 1, 2, or 3
        SubCommandFailure: If the command fails, does not report success, or
            Level 1 or Level 2 state verification fails, or the Level 3
            factory reset does not recover its console.
            Note: If a reset is already in progress, the device returns
            "Reset test is already triggered / Reset : Test Failed" and
            this exception is raised. Wait for the previous reset to complete
            before issuing a new one.

    Example:
        >>> execute_cloud_mgmt_reset_level(device, level=1)
        >>> execute_cloud_mgmt_reset_level(device, level=2)
        >>> execute_cloud_mgmt_reset_level(device, level=3)
    """
    if (
        isinstance(level, bool)
        or not isinstance(level, int)
        or level not in (1, 2, 3)
    ):
        raise ValueError("level must be an integer with a value of 1, 2, or 3")

    if level in (1, 2):
        _verify_cloud_mgmt_ready(
            device,
            level=level,
            max_time=transition_timeout,
            check_interval=check_interval,
            before_reset=True,
        )

    level_2_event_counts = None
    if level == 2:
        level_2_event_counts = _get_cloud_mgmt_reset_event_counts(
            device, level
        )

    cmd = f"test platform software cloud-mgmt reset level {level}"
    log.debug(f"Executing '{cmd}' on {device.name}")

    if level == 3:
        return _execute_cloud_mgmt_level_3_reset(
            device, cmd, reset_timeout
        )

    try:
        output = device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute '{cmd}' on {device.name}. Error:\n{e}"
        )

    expected_level = f"Reset Level: {level}"
    if (
        not isinstance(output, str)
        or expected_level not in output
        or "Triggered Successfully" not in output
    ):
        raise SubCommandFailure(
            f"Cloud-mgmt reset level {level} did not trigger successfully "
            f"on {device.name}. Output:\n{output}"
        )

    if level in (1, 2):
        _verify_cloud_mgmt_down_transition(
            device,
            level=level,
            max_time=transition_timeout,
            check_interval=check_interval,
        )

    if level == 2 and not _verify_cloud_mgmt_reset_event(
        device,
        level=level,
        initial_counts=level_2_event_counts,
        max_time=transition_timeout,
        check_interval=check_interval,
    ):
        raise SubCommandFailure(
            "Level 2 reset notification and recovery events were not "
            f"observed on {device.name}"
        )

    if level == 2:
        _check_cloud_mgmt_updater_errors(
            device,
            level=level,
            initial_counts=level_2_event_counts,
        )

    if level in (1, 2):
        _verify_cloud_mgmt_ready(
            device,
            level=level,
            max_time=transition_timeout,
            check_interval=check_interval,
            tunnel_max_time=recovery_timeout,
        )

        if level == 2:
            _check_cloud_mgmt_updater_errors(
                device,
                level=level,
                initial_counts=level_2_event_counts,
            )

    return output
