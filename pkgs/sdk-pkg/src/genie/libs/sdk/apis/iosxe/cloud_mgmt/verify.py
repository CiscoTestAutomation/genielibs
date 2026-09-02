"""
Module:
    genie.libs.sdk.apis.iosxe.cloud_mgmt

Authors:
    pyATS TEAM (pyats-support@cisco.com, pyats-support-ext@cisco.com)

Description:
    Module for cloud-mgmt verify APIs for Meraki/cloud management.
"""

import logging
from typing import List, Optional

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.utils import _is_syslog_line

# Logger
log = logging.getLogger(__name__)

def verify_cloud_id(
    device,
    expected_cloud_id: str,
    switch_number: Optional[int] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the cloud ID of the device

    Args:
        device (`obj`): Device object
        expected_cloud_id (`str`): Expected cloud ID to verify against
        switch_number (`int`, optional): Switch number to target in a stack.
            When provided, the entry for that switch is looked up directly by
            key.  When omitted, the first switch entry returned by the parser
            is used.
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults to 15
        check_interval (`int`, optional): Check interval in seconds. Defaults to 5

    Returns:
        bool: True if the cloud ID matches the expected value, False otherwise
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt")
            if switch_number is not None:
                switch_entry = output.get('meraki', {}).get('switch', {}).get(str(switch_number))
                if switch_entry is None:
                    log.debug(f"Switch {switch_number} not found in 'show cloud-mgmt' output on device {device.name}")
                    timeout.sleep()
                    continue
                actual_cloud_id = switch_entry.get('meraki_sn')
            else:
                actual_cloud_id = output.q.get_values('meraki_sn', 0)

            if not actual_cloud_id:
                log.debug(f"Cloud ID not found in 'show cloud-mgmt' output on device {device.name}")
                timeout.sleep()
                continue

            if actual_cloud_id == expected_cloud_id:
                log.debug(f"Cloud ID verification successful on device {device.name}: "
                          f"\"{actual_cloud_id}\" matches expected \"{expected_cloud_id}\"")
                return True
            else:
                log.debug(f"Cloud ID verification failed on device {device.name}: "
                          f"\"{actual_cloud_id}\" does not match expected \"{expected_cloud_id}\"")
                timeout.sleep()
                continue

        except SchemaEmptyParserError as e:
            log.debug(f"Failed to parse 'show cloud-mgmt' on device {device.name}, giving error {e}")
            timeout.sleep()
            continue

    return False


def verify_current_mode(
    device,
    expected_current_mode: str,
    switch_number: Optional[int] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the current mode of the device

    Args:
        device (`obj`): Device object
        expected_current_mode (`str`): Expected current mode to verify against
        switch_number (`int`, optional): Switch number to target in a stack.
            When provided, the entry for that switch is looked up directly by
            key.  When omitted, the first switch entry returned by the parser
            is used.
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults to 15
        check_interval (`int`, optional): Check interval in seconds. Defaults to 5

    Returns:
        bool: True if the current mode matches the expected value, False otherwise
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt")
            if switch_number is not None:
                switch_entry = output.get('meraki', {}).get('switch', {}).get(str(switch_number))
                if switch_entry is None:
                    log.debug(f"Switch {switch_number} not found in 'show cloud-mgmt' output on device {device.name}")
                    timeout.sleep()
                    continue
                actual_current_mode = switch_entry.get('current_mode')
            else:
                actual_current_mode = output.q.get_values('current_mode', 0)

            if not actual_current_mode:
                log.debug(f"Current mode not found in 'show cloud-mgmt' output on device {device.name}")
                timeout.sleep()
                continue

            if actual_current_mode == expected_current_mode:
                log.debug(f"Current mode verification successful on device {device.name}: "
                          f"\"{actual_current_mode}\" matches expected \"{expected_current_mode}\"")
                return True
            else:
                log.debug(f"Current mode verification failed on device {device.name}: "
                          f"\"{actual_current_mode}\" does not match expected \"{expected_current_mode}\"")
                timeout.sleep()
                continue

        except SchemaEmptyParserError as e:
            log.debug(f"Failed to parse 'show cloud-mgmt' on device {device.name}, giving error {e}")
            timeout.sleep()
            continue

    return False


def verify_conversion_status(
    device,
    expected_conversion_status: str,
    switch_number: Optional[int] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the conversion status of the device

    Args:
        device (`obj`): Device object
        expected_conversion_status (`str`): Expected conversion status to verify against
        switch_number (`int`, optional): Switch number to target in a stack.
            When provided, the entry for that switch is looked up directly by
            key.  When omitted, the first switch entry returned by the parser
            is used.
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults to 15
        check_interval (`int`, optional): Check interval in seconds. Defaults to 5

    Returns:
        bool: True if the conversion status matches the expected value, False otherwise
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt")
            if switch_number is not None:
                switch_entry = output.get('meraki', {}).get('switch', {}).get(str(switch_number))
                if switch_entry is None:
                    log.debug(f"Switch {switch_number} not found in 'show cloud-mgmt' output on device {device.name}")
                    timeout.sleep()
                    continue
                actual_conversion_status = switch_entry.get('conversion_status')
            else:
                actual_conversion_status = output.q.get_values('conversion_status', 0)

            # Check for missing key separately from empty string value
            if actual_conversion_status is None:
                log.debug(f"Conversion status not found in 'show cloud-mgmt' output on device {device.name}")
                timeout.sleep()
                continue

            if actual_conversion_status == expected_conversion_status:
                log.debug(f"Conversion status verification successful on device {device.name}: "
                          f"\"{actual_conversion_status}\" matches expected \"{expected_conversion_status}\"")
                return True
            else:
                log.debug(f"Conversion status verification failed on device {device.name}: "
                          f"\"{actual_conversion_status}\" does not match expected \"{expected_conversion_status}\"")
                timeout.sleep()
                continue

        except SchemaEmptyParserError as e:
            log.debug(f"Failed to parse 'show cloud-mgmt' on device {device.name}, giving error {e}")
            timeout.sleep()
            continue

    return False


def verify_cloud_mgmt_migration_status(
    device,
    expected_migration_in_progress: str,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the cloud-mgmt migration in-progress status from 'show cloud-mgmt migration'

    Args:
        device (`obj`): Device object
        expected_migration_in_progress (`str`): Expected migration in-progress
            value to verify against (e.g. "YES" or "NO")
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults to 15
        check_interval (`int`, optional): Check interval in seconds. Defaults to 5

    Returns:
        bool: True if the migration in-progress status matches the expected value, False otherwise
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt migration")
            actual_migration_in_progress = output.q.get_values('migration_in_progress', 0)

            if actual_migration_in_progress is None:
                log.debug(f"cloud-mgmt migration status not found in 'show cloud-mgmt migration' "
                          f"output on device {device.name}")
                timeout.sleep()
                continue

            if actual_migration_in_progress == expected_migration_in_progress:
                log.debug(f"cloud-mgmt migration status verification successful on device {device.name}: "
                          f"\"{actual_migration_in_progress}\" matches expected \"{expected_migration_in_progress}\"")
                return True
            else:
                log.debug(f"cloud-mgmt migration status verification failed on device {device.name}: "
                          f"\"{actual_migration_in_progress}\" does not match expected \"{expected_migration_in_progress}\"")
                timeout.sleep()
                continue

        except SchemaEmptyParserError as e:
            log.debug(f"Failed to parse 'show cloud-mgmt migration' on device {device.name}, giving error {e}")
            timeout.sleep()
            continue

    return False


def verify_cloud_mgmt_connect_status(
    device,
    expected_connect_status: str,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the cloud-mgmt connect status of the device

    Args:
        device (`obj`): Device object
        expected_connect_status (`str`): Expected cloud-mgmt connect status to verify against
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults to 15
        check_interval (`int`, optional): Check interval in seconds. Defaults to 5

    Returns:
        bool: True if the cloud-mgmt connect status matches the expected value, False otherwise
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt connect")
            actual_connect_status = output.q.get_values('service_cloud-mgmt_connect', 0)

            if not actual_connect_status:
                log.debug(f"cloud-mgmt connect status not found in 'show cloud-mgmt connect' "
                          f"output on device {device.name}")
                timeout.sleep()
                continue

            if actual_connect_status == expected_connect_status:
                log.debug(f"cloud-mgmt connect status verification successful on device {device.name}: "
                          f"\"{actual_connect_status}\" matches expected \"{expected_connect_status}\"")
                return True
            else:
                log.debug(f"cloud-mgmt connect status verification failed on device {device.name}: "
                          f"\"{actual_connect_status}\" does not match expected \"{expected_connect_status}\"")
                timeout.sleep()
                continue

        except SchemaEmptyParserError as e:
            log.debug(f"Failed to parse 'show cloud-mgmt connect' on device {device.name}, giving error {e}")
            timeout.sleep()
            continue

    return False


def verify_cloud_mgmt_device_registration(
    device,
    expected_cloud_id: Optional[str] = None,
    expected_pid: Optional[str] = None,
    expected_serial_number: Optional[str] = None,
    expected_registration_status: Optional[str] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the cloud-mgmt device registration details of the device.
    At least one expected field must be provided.

    Args:
        device (`obj`): Device object
        expected_cloud_id (`str`, optional): Expected cloud ID to verify against
        expected_pid (`str`, optional): Expected product ID to verify against
        expected_serial_number (`str`, optional): Expected serial number to verify against
        expected_registration_status (`str`, optional): Expected registration status to verify against
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults to 15
        check_interval (`int`, optional): Check interval in seconds. Defaults to 5

    Returns:
        bool: True if the cloud-mgmt device registration details match the expected values, False otherwise
    """
    if all(v is None for v in [expected_cloud_id, expected_pid,
                                expected_serial_number, expected_registration_status]):
        log.debug(f"At least one expected field must be provided for verify_cloud_mgmt_device_registration on {device.name}")
        return False

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt connect")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        log.debug(f"Verifying cloud-mgmt connect on {device.name}")

        registration = output.get("cloud-mgmt_device_registration", {})
        device_records = registration.get("devices", {}).values()

        if not device_records:
            log.debug(f"No cloud-mgmt device registration records found on device {device.name}")
            timeout.sleep()
            continue

        found_match = False
        for record in device_records:
            if not isinstance(record, dict):
                continue
            cloud_id = record.get("cloud_id")
            pid = record.get("pid")
            serial_number = record.get("serial_number")
            status = record.get("status")

            if expected_cloud_id is not None and cloud_id != expected_cloud_id:
                continue
            if expected_pid is not None and pid != expected_pid:
                continue
            if expected_serial_number is not None and serial_number != expected_serial_number:
                continue
            if expected_registration_status is not None and status != expected_registration_status:
                continue

            found_match = True
            if expected_cloud_id is not None:
                log.debug(f" ::Expected cloud_id={expected_cloud_id}, Actual={cloud_id}")
                log.debug(f"cloud-mgmt device registration cloud ID verification successful on device {device.name}: "
                          f"\"{cloud_id}\" matches expected \"{expected_cloud_id}\"")
            if expected_pid is not None:
                log.debug(f" ::Expected pid={expected_pid}, Actual={pid}")
                log.debug(f"cloud-mgmt device registration pid verification successful on device {device.name}: "
                          f"\"{pid}\" matches expected \"{expected_pid}\"")
            if expected_serial_number is not None:
                log.debug(f" ::Expected serial_number={expected_serial_number}, Actual={serial_number}")
                log.debug(f"cloud-mgmt device registration serial number verification successful on device {device.name}: "
                          f"\"{serial_number}\" matches expected \"{expected_serial_number}\"")
            if expected_registration_status is not None:
                log.debug(f" ::Expected status={expected_registration_status}, Actual={status}")
                log.debug(f"cloud-mgmt device registration status verification successful on device {device.name}: "
                          f"\"{status}\" matches expected \"{expected_registration_status}\"")
            break

        if not found_match:
            log.debug(f"No device registration record on {device.name} matched all supplied expectations: "
                      f"cloud_id={expected_cloud_id}, pid={expected_pid}, "
                      f"serial_number={expected_serial_number}, status={expected_registration_status}")
            timeout.sleep()
            continue

        return True

    return False


def verify_cloud_mgmt_tunnel_state(
    device,
    expected_primary_status: Optional[str] = None,
    expected_secondary_status: Optional[str] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the cloud-mgmt tunnel state of the device.
    At least one of expected_primary_status or expected_secondary_status must be provided.

    Args:
        device (`obj`): Device object
        expected_primary_status (`str`, optional): Expected primary tunnel status to verify against
        expected_secondary_status (`str`, optional): Expected secondary tunnel status to verify against
        max_time (`int`, optional): Maximum time to wait for the expected status (in seconds). Defaults to 15
        check_interval (`int`, optional): Time interval between checks (in seconds). Defaults to 5

    Returns:
        bool: True if the cloud-mgmt tunnel state matches the expected values, False otherwise
    """
    if expected_primary_status is None and expected_secondary_status is None:
        log.debug(f"At least one of expected_primary_status or expected_secondary_status must be provided on {device.name}")
        return False

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            raw = device.execute("show cloud-mgmt connect")
            filtered = '\n'.join(
                line for line in str(raw).splitlines()
                if not line.strip().lower().startswith('mode button event')
                and not _is_syslog_line(line)
            )
            output = device.parse("show cloud-mgmt connect", output=filtered)
            actual_primary_status = output.q.contains("cloud-mgmt_tunnel_state").get_values("primary")
            actual_secondary_status = output.q.contains("cloud-mgmt_tunnel_state").get_values("secondary")
            primary_display = actual_primary_status[0] if actual_primary_status else None
            secondary_display = actual_secondary_status[0] if actual_secondary_status else None

            if expected_primary_status is not None:
                if primary_display == expected_primary_status:
                    log.debug(f"cloud-mgmt tunnel primary status verification successful on device {device.name}: "
                              f"\"{primary_display}\" matches expected \"{expected_primary_status}\"")
                else:
                    log.debug(f"cloud-mgmt tunnel primary status verification failed on device {device.name}: "
                              f"\"{primary_display}\" does not match expected \"{expected_primary_status}\"")
                    timeout.sleep()
                    continue

            if expected_secondary_status is not None:
                if secondary_display == expected_secondary_status:
                    log.debug(f"cloud-mgmt tunnel secondary status verification successful on device {device.name}: "
                              f"\"{secondary_display}\" matches expected \"{expected_secondary_status}\"")
                else:
                    log.debug(f"cloud-mgmt tunnel secondary status verification failed on device {device.name}: "
                              f"\"{secondary_display}\" does not match expected \"{expected_secondary_status}\"")
                    timeout.sleep()
                    continue

            return True

        except SchemaEmptyParserError as e:
            log.debug(f"Failed to parse 'show cloud-mgmt connect' on device {device.name}, giving error {e}")
            timeout.sleep()
            continue

    return False


def verify_cloud_mgmt_tunnel_interface_status(
    device,
    expected_status: Optional[str] = None,
    expected_rx_errors: Optional[int] = None,
    expected_tx_errors: Optional[int] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the cloud-mgmt tunnel interface status of the device.
    At least one expected field must be provided.

    Args:
        device (`obj`): Device object
        expected_status (`str`, optional): Expected tunnel interface status to verify against
        expected_rx_errors (`int`, optional): Expected number of RX errors to verify against
        expected_tx_errors (`int`, optional): Expected number of TX errors to verify against
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults to 15
        check_interval (`int`, optional): Check interval in seconds. Defaults to 5

    Returns:
        bool: True if the cloud-mgmt tunnel interface status matches the expected values, False otherwise
    """
    if all(v is None for v in [expected_status, expected_rx_errors, expected_tx_errors]):
        log.debug(f"At least one expected field must be provided for verify_cloud_mgmt_tunnel_interface_status on {device.name}")
        return False

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt connect")
            iface_q = output.q.contains("cloud-mgmt_tunnel_interface")
            actual_status = iface_q.get_values('status', 0)
            actual_rx_errors = iface_q.get_values('rx_errors', 0)
            actual_tx_errors = iface_q.get_values('tx_errors', 0)

            ok = True

            if expected_status is not None:
                if actual_status == expected_status:
                    log.debug(f"cloud-mgmt tunnel interface status verification successful on device {device.name}: "
                              f"\"{actual_status}\" matches expected \"{expected_status}\"")
                else:
                    log.debug(f"cloud-mgmt tunnel interface status verification failed on device {device.name}: "
                              f"\"{actual_status}\" does not match expected \"{expected_status}\"")
                    ok = False

            if expected_rx_errors is not None:
                if actual_rx_errors == expected_rx_errors:
                    log.debug(f"cloud-mgmt tunnel interface RX errors verification successful on device {device.name}: "
                              f"RX errors \"{actual_rx_errors}\" matches expected \"{expected_rx_errors}\"")
                else:
                    log.debug(f"cloud-mgmt tunnel interface RX errors verification failed on device {device.name}: "
                              f"RX errors \"{actual_rx_errors}\" does not match expected \"{expected_rx_errors}\"")
                    ok = False

            if expected_tx_errors is not None:
                if actual_tx_errors == expected_tx_errors:
                    log.debug(f"cloud-mgmt tunnel interface TX errors verification successful on device {device.name}: "
                              f"TX errors \"{actual_tx_errors}\" matches expected \"{expected_tx_errors}\"")
                else:
                    log.debug(f"cloud-mgmt tunnel interface TX errors verification failed on device {device.name}: "
                              f"TX errors \"{actual_tx_errors}\" does not match expected \"{expected_tx_errors}\"")
                    ok = False

            if ok:
                return True

            timeout.sleep()
            continue

        except SchemaEmptyParserError as e:
            log.debug(f"Failed to parse 'show cloud-mgmt connect' on device {device.name}, giving error {e}")
            timeout.sleep()
            continue

    return False


def verify_cloud_mgmt_tunnel_config(
    device,
    expected_fetch_fail: Optional[str] = None,
    expected_fetch_state: Optional[str] = None,
    expected_network_name: Optional[str] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the cloud-mgmt tunnel configuration of the device.
    At least one expected field must be provided.

    Args:
        device (`obj`): Device object
        expected_fetch_fail (`str`, optional): Expected fetch fail status to verify against
        expected_fetch_state (`str`, optional): Expected fetch state to verify against
        expected_network_name (`str`, optional): Expected network name to verify against
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults to 15
        check_interval (`int`, optional): Check interval in seconds. Defaults to 5

    Returns:
        bool: True if the cloud-mgmt tunnel config matches the expected values, False otherwise
    """
    if all(v is None for v in [expected_fetch_fail, expected_fetch_state, expected_network_name]):
        log.debug(f"At least one expected field must be provided for verify_cloud_mgmt_tunnel_config on {device.name}")
        return False

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt connect")
            actual_fetch_fail = output.q.get_values('fetch_fail', 0)
            actual_fetch_state = output.q.get_values('fetch_state', 0)
            actual_network_name = output.q.get_values('network_name', 0)

            ok = True

            if expected_fetch_fail is not None:
                if actual_fetch_fail == expected_fetch_fail:
                    log.debug(f"cloud-mgmt tunnel config fetch fail verification successful on device {device.name}: "
                              f"\"{actual_fetch_fail}\" matches expected \"{expected_fetch_fail}\"")
                else:
                    log.debug(f"cloud-mgmt tunnel config fetch fail verification failed on device {device.name}: "
                              f"\"{actual_fetch_fail}\" does not match expected \"{expected_fetch_fail}\"")
                    ok = False

            if expected_fetch_state is not None:
                if actual_fetch_state == expected_fetch_state:
                    log.debug(f"cloud-mgmt tunnel config fetch state verification successful on device {device.name}: "
                              f"\"{actual_fetch_state}\" matches expected \"{expected_fetch_state}\"")
                else:
                    log.debug(f"cloud-mgmt tunnel config fetch state verification failed on device {device.name}: "
                              f"\"{actual_fetch_state}\" does not match expected \"{expected_fetch_state}\"")
                    ok = False

            if expected_network_name is not None:
                if actual_network_name == expected_network_name:
                    log.debug(f"cloud-mgmt tunnel config network name verification successful on device {device.name}: "
                              f"\"{actual_network_name}\" matches expected \"{expected_network_name}\"")
                else:
                    log.debug(f"cloud-mgmt tunnel config network name verification failed on device {device.name}: "
                              f"\"{actual_network_name}\" does not match expected \"{expected_network_name}\"")
                    ok = False

            if ok:
                return True

            timeout.sleep()
            continue

        except SchemaEmptyParserError as e:
            log.debug(f"Failed to parse 'show cloud-mgmt connect' on device {device.name}, giving error {e}")
            timeout.sleep()
            continue

    return False


def verify_cloud_mgmt_migration_details(
    device,
    expected_current_booted_mode: Optional[str] = None,
    expected_migration_in_progress: Optional[str] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the migration details of the device

    Args:
        device (`obj`): Device object
        expected_current_booted_mode (`str`, optional): Expected current booted
            mode to verify against.
        expected_migration_in_progress (`str`, optional): Expected migration in
            progress status to verify against.
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults
            to 15.
        check_interval (`int`, optional): Check interval in seconds. Defaults
            to 5.

    Returns:
        bool: True if the migration details match the expected values, False
            otherwise.
    """
    if (expected_current_booted_mode is None
            and expected_migration_in_progress is None):
        log.debug(
            "At least one expected field must be provided for "
            f"verify_cloud_mgmt_migration_details on {device.name}"
        )
        return False
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt migration")
            actual_current_booted_mode = output.q.get_values(
                'current_booted_mode', 0
            )
            actual_migration_in_progress = output.q.get_values(
                'migration_in_progress', 0
            )

            if expected_current_booted_mode is not None:
                if not actual_current_booted_mode:
                    log.debug(
                        "Current booted mode not found in "
                        f"'show cloud-mgmt migration' output on {device.name}"
                    )
                    timeout.sleep()
                    continue
                if actual_current_booted_mode != expected_current_booted_mode:
                    log.debug(
                        "Current booted mode verification failed on device "
                        f"{device.name}: \"{actual_current_booted_mode}\" does "
                        f"not match expected \"{expected_current_booted_mode}\""
                    )
                    timeout.sleep()
                    continue
                log.debug(
                    "Current booted mode verification successful on device "
                    f"{device.name}: \"{actual_current_booted_mode}\" matches "
                    f"expected \"{expected_current_booted_mode}\""
                )

            if expected_migration_in_progress is not None:
                if not actual_migration_in_progress:
                    log.debug(
                        "Migration in progress status not found in "
                        f"'show cloud-mgmt migration' output on {device.name}"
                    )
                    timeout.sleep()
                    continue
                if (actual_migration_in_progress
                        != expected_migration_in_progress):
                    log.debug(
                        "Migration in progress status verification failed on "
                        f"device {device.name}: "
                        f"\"{actual_migration_in_progress}\" does not match "
                        f"expected \"{expected_migration_in_progress}\""
                    )
                    timeout.sleep()
                    continue
                log.debug(
                    "Migration in progress status verification successful on "
                    f"device {device.name}: "
                    f"\"{actual_migration_in_progress}\" matches expected "
                    f"\"{expected_migration_in_progress}\""
                )

            return True

        except SchemaEmptyParserError as e:
            log.debug(
                f"Failed to parse 'show cloud-mgmt migration' on device "
                f"{device.name}, giving error {e}"
            )
            timeout.sleep()
            continue

    return False


def verify_rommon_boot_device_mode(
    device,
    expected_boot_device_mode: Optional[str] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the ROMMON boot device mode.

    ``expected_boot_device_mode`` must be provided.

    Args:
        device (`obj`): Device object
        expected_boot_device_mode (`str`, optional): Expected boot device mode
            to verify against.
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults
            to 15.
        check_interval (`int`, optional): Check interval in seconds. Defaults
            to 5.

    Returns:
        bool: True if the rommon variables match the expected values, False
            otherwise.
    """
    if expected_boot_device_mode is None:
        log.debug(
            "expected_boot_device_mode must be provided for "
            f"verify_rommon_boot_device_mode on {device.name}"
        )
        return False

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show romvar")
            actual_rommon_variables = output.q.get_values('boot_device_mode', 0)

            if not actual_rommon_variables:
                log.debug(
                    "Rommon variables not found in 'show romvar' output on "
                    f"device {device.name}"
                )
                timeout.sleep()
                continue

            if actual_rommon_variables == expected_boot_device_mode:
                log.debug(
                    "Rommon variables verification successful on device "
                    f"{device.name}: \"{actual_rommon_variables}\" matches "
                    f"expected \"{expected_boot_device_mode}\""
                )
                return True
            else:
                log.debug(
                    "Rommon variables verification failed on device "
                    f"{device.name}: \"{actual_rommon_variables}\" does not "
                    f"match expected \"{expected_boot_device_mode}\""
                )
                timeout.sleep()
                continue

        except SchemaEmptyParserError as e:
            log.debug(
                f"Failed to parse 'show romvar' on device {device.name}, "
                f"giving error {e}"
            )
            timeout.sleep()
            continue

    return False


def verify_cloud_monitoring_compatibility(
    device,
    expected_cloud_monitoring_compatibility: Optional[str] = None,
    max_time: int = 15,
    check_interval: int = 5
) -> bool:
    """Verify the cloud monitoring compatibility of the device.

    ``expected_cloud_monitoring_compatibility`` must be provided.

    Args:
        device (`obj`): Device object
        expected_cloud_monitoring_compatibility (`str`, optional): Expected
            cloud monitoring compatibility to verify against.
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults
            to 15.
        check_interval (`int`, optional): Check interval in seconds. Defaults
            to 5.

    Returns:
        bool: True if the cloud monitoring compatibility matches the expected
            value, False otherwise.
    """
    if expected_cloud_monitoring_compatibility is None:
        log.debug(
            "expected_cloud_monitoring_compatibility must be provided for "
            f"verify_cloud_monitoring_compatibility on {device.name}"
        )
        return False

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse("show cloud-mgmt compatibility")
            actual_cloud_monitoring_compatibility = output.q.get_values(
                'cloud_mgmt_cloud_monitoring', 0
            )

            if not actual_cloud_monitoring_compatibility:
                log.debug(
                    "Cloud monitoring compatibility not found in "
                    "'show cloud-mgmt compatibility' output on device "
                    f"{device.name}"
                )
                timeout.sleep()
                continue

            if (actual_cloud_monitoring_compatibility
                    == expected_cloud_monitoring_compatibility):
                log.debug(
                    "Cloud monitoring compatibility verification successful "
                    f"on device {device.name}: "
                    f"\"{actual_cloud_monitoring_compatibility}\" matches "
                    f"expected \"{expected_cloud_monitoring_compatibility}\""
                )
                return True
            else:
                log.debug(
                    "Cloud monitoring compatibility verification failed on "
                    f"device {device.name}: "
                    f"\"{actual_cloud_monitoring_compatibility}\" does not "
                    "match expected "
                    f"\"{expected_cloud_monitoring_compatibility}\""
                )
                timeout.sleep()
                continue

        except SchemaEmptyParserError as e:
            log.debug(
                "Failed to parse 'show cloud-mgmt compatibility' on device "
                f"{device.name}, giving error {e}"
            )
            timeout.sleep()
            continue

    return False


def verify_cloud_mgmt_compatibility(
    device,
    expected_cloud_monitoring: Optional[str] = None,
    expected_boot_status: Optional[str] = None,
    expected_boot_mode: Optional[str] = None,
    expected_boot_message: Optional[str] = None,
    boot_message_match: str = "contains",
    expected_switch_number: Optional[int] = None,
    expected_sku_model: Optional[str] = None,
    expected_sku_status: Optional[str] = None,
    expected_bootloader_version: Optional[str] = None,
    expected_bootloader_status: Optional[str] = None,
    expected_expansion_module_model: Optional[str] = None,
    expected_expansion_module_status: Optional[str] = None,
    expected_compatible_ems: Optional[List[str]] = None,
    ems_match: str = "subset",
    max_time: int = 15,
    check_interval: int = 5,
) -> bool:
    """Verify parsed output from 'show cloud-mgmt compatibility'.

    Args:
        device (`obj`): Device object
        expected_cloud_monitoring (`str`, optional): Expected cloud monitoring
            status (for example, "Compatible").
        expected_boot_status (`str`, optional): Expected boot status (for
            example, "Incompatible" or "Compatible").
        expected_boot_mode (`str`, optional): Expected boot mode (for example,
            "INSTALL").
        expected_boot_message (`str`, optional): Expected boot message.
        boot_message_match (`str`, optional): "contains" or "exact". Defaults
            to "contains".
        expected_switch_number (`int`, optional): Expected switch number.
        expected_sku_model (`str`, optional): Expected SKU model.
        expected_sku_status (`str`, optional): Expected SKU status.
        expected_bootloader_version (`str`, optional): Expected bootloader
            version.
        expected_bootloader_status (`str`, optional): Expected bootloader
            status.
        expected_expansion_module_model (`str`, optional): Expected expansion
            module model.
        expected_expansion_module_status (`str`, optional): Expected expansion
            module status.
        expected_compatible_ems (`list`, optional): Expected compatible
            expansion modules.
        ems_match (`str`, optional): "subset" or "exact". Defaults to
            "subset".
        max_time (`int`, optional): Maximum time to wait in seconds. Defaults
            to 15.
        check_interval (`int`, optional): Check interval in seconds. Defaults
            to 5.

    Returns:
        bool: True if all specified values match, False otherwise
    """
    _all_expectations = [
        expected_cloud_monitoring, expected_boot_status, expected_boot_mode,
        expected_boot_message, expected_switch_number, expected_sku_model,
        expected_sku_status, expected_bootloader_version,
        expected_bootloader_status,
        expected_expansion_module_model, expected_expansion_module_status,
        expected_compatible_ems,
    ]
    if all(v is None for v in _all_expectations):
        log.debug(
            "At least one expected field must be provided for "
            f"verify_cloud_mgmt_compatibility on {device.name}"
        )
        return False
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse("show cloud-mgmt compatibility")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ok = True
        log.debug(f"Verifying cloud-mgmt compatibility on {device.name}")

        if expected_cloud_monitoring is not None:
            actual = out.q.get_values("cloud_mgmt_cloud_monitoring", 0)
            log.debug(
                " ::Expected cloud_mgmt_cloud_monitoring="
                f"{expected_cloud_monitoring}, Actual={actual}"
            )
            if actual != expected_cloud_monitoring:
                log.debug("Mismatch: cloud_mgmt_cloud_monitoring")
                ok = False

        if expected_boot_status is not None:
            actual = out.q.contains("boot_mode").get_values("status", 0)
            log.debug(
                f" ::Expected boot_mode.status={expected_boot_status}, "
                f"Actual={actual}"
            )
            if actual != expected_boot_status:
                log.debug("Mismatch: boot_mode.status")
                ok = False

        if expected_boot_mode is not None:
            actual = out.q.contains("boot_mode").get_values("mode", 0)
            log.debug(
                f" ::Expected boot_mode.mode={expected_boot_mode}, "
                f"Actual={actual}"
            )
            if actual != expected_boot_mode:
                log.debug("Mismatch: boot_mode.mode")
                ok = False

        if expected_boot_message is not None:
            actual = out.q.contains("boot_mode").get_values("message", 0) or ""
            log.debug(
                f" ::Expected boot_mode.message ({boot_message_match})="
                f"{expected_boot_message}, Actual={actual}"
            )
            if boot_message_match == "exact":
                if actual != expected_boot_message:
                    log.debug("Mismatch: boot_mode.message (exact)")
                    ok = False
            else:
                if expected_boot_message not in actual:
                    log.debug("Mismatch: boot_mode.message (contains)")
                    ok = False

        if any(v is not None for v in [
            expected_switch_number, expected_sku_model, expected_sku_status,
            expected_bootloader_version, expected_bootloader_status,
            expected_expansion_module_model, expected_expansion_module_status
        ]):
            if expected_switch_number is not None:
                sw_blocks = out.q.get_values("switch_details") or []
                sw_block = None
                for b in sw_blocks:
                    if b.get("switch_number") == expected_switch_number:
                        sw_block = b
                        break

                if sw_block is None:
                    log.debug(
                        "Switch entry not found for switch_number="
                        f"{expected_switch_number}"
                    )
                    ok = False
                else:
                    swq = Dq(sw_block)

                    if expected_sku_model is not None:
                        actual = swq.contains("sku").get_values("model", 0)
                        log.debug(
                            f" ::Expected sku.model={expected_sku_model}, "
                            f"Actual={actual}"
                        )
                        if actual != expected_sku_model:
                            log.debug("Mismatch: sku.model")
                            ok = False

                    if expected_sku_status is not None:
                        actual = swq.contains("sku").get_values("status", 0)
                        log.debug(
                            f" ::Expected sku.status={expected_sku_status}, "
                            f"Actual={actual}"
                        )
                        if actual != expected_sku_status:
                            log.debug("Mismatch: sku.status")
                            ok = False

                    if expected_bootloader_version is not None:
                        actual = swq.contains(
                            "bootloader_version"
                        ).get_values("version", 0)
                        log.debug(
                            " ::Expected bootloader_version.version="
                            f"{expected_bootloader_version}, Actual={actual}"
                        )
                        if actual != expected_bootloader_version:
                            log.debug("Mismatch: bootloader_version.version")
                            ok = False

                    if expected_bootloader_status is not None:
                        actual = swq.contains(
                            "bootloader_version"
                        ).get_values("status", 0)
                        log.debug(
                            " ::Expected bootloader_version.status="
                            f"{expected_bootloader_status}, Actual={actual}"
                        )
                        if actual != expected_bootloader_status:
                            log.debug("Mismatch: bootloader_version.status")
                            ok = False

                    if (expected_expansion_module_model is not None
                            or expected_expansion_module_status is not None):
                        em_list = sw_block.get("expansion_modules", [])
                        em_match = any(
                            (
                                expected_expansion_module_model is None
                                or r.get("model")
                                == expected_expansion_module_model
                            )
                            and (
                                expected_expansion_module_status is None
                                or r.get("status")
                                == expected_expansion_module_status
                            )
                            for r in em_list
                            if isinstance(r, dict)
                        )
                        log.debug(
                            " ::Expected expansion_modules model="
                            f"{expected_expansion_module_model}, status="
                            f"{expected_expansion_module_status}, "
                            f"Records={em_list}"
                        )
                        if not em_match:
                            log.debug(
                                "Mismatch: no expansion_modules record matched "
                                "model and status"
                            )
                            ok = False
            else:
                switch_specific = any(v is not None for v in [
                    expected_sku_model, expected_sku_status,
                    expected_bootloader_version, expected_bootloader_status,
                    expected_expansion_module_model,
                    expected_expansion_module_status
                ])
                if switch_specific:
                    log.debug(
                        "expected_switch_number must be provided when "
                        "verifying switch-specific fields"
                    )
                    ok = False
                else:
                    actual_first = out.q.get_values("switch_details", 0)
                    if not actual_first:
                        log.debug("No switch_details entries present")
                        ok = False

        if expected_compatible_ems is not None:
            actual_list = out.q.get_values("compatible_expansion_modules") or []
            log.debug(
                f" ::Expected compatible_expansion_modules ({ems_match})="
                f"{expected_compatible_ems}"
            )
            log.debug(f" ::Actual compatible_expansion_modules={actual_list}")

            if ems_match == "exact":
                if actual_list != expected_compatible_ems:
                    log.debug("Mismatch: compatible_expansion_modules (exact)")
                    ok = False
            else:
                missing = [
                    x for x in expected_compatible_ems if x not in actual_list
                ]
                if missing:
                    log.debug(
                        "Mismatch: compatible_expansion_modules missing "
                        f"{missing}"
                    )
                    ok = False

        if ok:
            return True

        timeout.sleep()

    return False
