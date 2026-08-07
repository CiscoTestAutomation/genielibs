"""
Module:
    genie.libs.sdk.apis.iosxe.cloud_mgmt

Authors:
    pyATS TEAM (pyats-support@cisco.com, pyats-support-ext@cisco.com)

Description:
    Module for cloud-mgmt verify APIs for Meraki/cloud management.
"""

import logging
from typing import Optional

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

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
