# Copyright (c) 2026 by Cisco Systems, Inc.
# All rights reserved.
"""Verify functions for POE power management."""

import logging
from genie.libs.sdk.apis.iosxe.power.get import get_total_poe_power

log = logging.getLogger(__name__)


def verify_poe_psu(device):
    """Verify POE PSU is available on the device.

    Args:
        device ('obj'): Device object

    Returns:
        Boolean: True if POE PSU power is available

    Raises:
        RuntimeError: If total POE power is unavailable or non-positive
    """
    total_power = get_total_poe_power(device)
    if total_power is None:
        raise RuntimeError("Unable to determine POE total power")

    log.info("UUT router supports %s watts POE power", total_power)
    if total_power <= 0:
        raise RuntimeError("POE power is not available")
    return True


def verify_poe_entry_op_state(
    device,
    interface,
    expected_op_state,
    input_dict=None,
    wait_up=False,
    max_retry=10,
    retry_delay=3,
):
    """Verify the operational state of a POE interface.

    Args:
        device ('obj'): Device object
        interface ('str'): Interface name (e.g., 'GigabitEthernet1/0/1')
        expected_op_state ('str'): Expected operational state (e.g., 'on', 'off')
        input_dict ('dict', optional): Pre-fetched POE entry dict, default is None
        wait_up ('bool', optional): Retry until state is seen, default is False
        max_retry ('int', optional): Maximum retry attempts, default is 10
        retry_delay ('int', optional): Delay in seconds between retries, default is 3

    Returns:
        Boolean: True if op_state matches expected_op_state, else False

    Raises:
        None
    """
    log.info(
        "Checking op_state for interface {intf}, expected: {state}".format(
            intf=interface, state=expected_op_state
        )
    )
    if input_dict:
        entry = input_dict
    else:
        try:
            entry = device.api.get_poe_entry(
                interface=interface,
                wait_up=wait_up,
                max_retry=max_retry,
                retry_delay=retry_delay,
            )
        except Exception as e:
            log.error("Failed to get POE entry for {intf}: {e}".format(intf=interface, e=e))
            return False

    if not entry:
        log.error("No POE entry returned for interface {intf}".format(intf=interface))
        return False

    actual = entry.get("op_state", "")
    if actual == expected_op_state:
        log.info(
            "op_state matched: {state}".format(state=expected_op_state)
        )
        return True

    log.error(
        "op_state mismatch for {intf}: expected '{exp}', got '{got}'".format(
            intf=interface, exp=expected_op_state, got=actual
        )
    )
    return False


def verify_poe_entry_mode(
    device,
    interface,
    expected_mode,
    input_dict=None,
):
    """Verify the admin mode of a POE interface.

    Args:
        device ('obj'): Device object
        interface ('str'): Interface name (e.g., 'GigabitEthernet1/0/1')
        expected_mode ('str'): Expected admin mode (e.g., 'auto', 'never')
        input_dict ('dict', optional): Pre-fetched POE entry dict, default is None

    Returns:
        Boolean: True if mode matches expected_mode, else False

    Raises:
        None
    """
    log.info(
        "Checking mode for interface {intf}, expected: {mode}".format(
            intf=interface, mode=expected_mode
        )
    )
    if input_dict:
        entry = input_dict
    else:
        try:
            entry = device.api.get_poe_entry(interface=interface)
        except Exception as e:
            log.error("Failed to get POE entry for {intf}: {e}".format(intf=interface, e=e))
            return False

    if not entry:
        log.error("No POE entry returned for interface {intf}".format(intf=interface))
        return False

    actual = entry.get("mode", "")
    if actual == expected_mode:
        log.info("mode matched: {mode}".format(mode=expected_mode))
        return True

    log.error(
        "mode mismatch for {intf}: expected '{exp}', got '{got}'".format(
            intf=interface, exp=expected_mode, got=actual
        )
    )
    return False


def verify_poe_entry_power_within(
    device,
    interface,
    min_watts,
    max_watts,
    input_dict=None,
):
    """Verify the POE power consumption of an interface is within a range.

    Args:
        device ('obj'): Device object
        interface ('str'): Interface name (e.g., 'GigabitEthernet1/0/1')
        min_watts ('float'): Minimum expected power in watts (inclusive)
        max_watts ('float'): Maximum expected power in watts (inclusive)
        input_dict ('dict', optional): Pre-fetched POE entry dict, default is None

    Returns:
        Boolean: True if power is within [min_watts, max_watts], else False

    Raises:
        None
    """
    log.info(
        "Checking power for interface {intf}, expected range: [{mn}, {mx}] W".format(
            intf=interface, mn=min_watts, mx=max_watts
        )
    )
    if input_dict:
        entry = input_dict
    else:
        try:
            entry = device.api.get_poe_entry(interface=interface)
        except Exception as e:
            log.error("Failed to get POE entry for {intf}: {e}".format(intf=interface, e=e))
            return False

    if not entry:
        log.error("No POE entry returned for interface {intf}".format(intf=interface))
        return False

    actual = entry.get("power", 0.0)
    if min_watts <= actual <= max_watts:
        log.info(
            "power {actual}W is within [{mn}, {mx}] W".format(
                actual=actual, mn=min_watts, mx=max_watts
            )
        )
        return True

    log.error(
        "power {actual}W is out of range [{mn}, {mx}] W for {intf}".format(
            actual=actual, mn=min_watts, mx=max_watts, intf=interface
        )
    )
    return False


def verify_power_budget(
    device,
    max_used_watts=None,
    min_remain_watts=None,
):
    """Verify the POE power budget thresholds.

    Args:
        device ('obj'): Device object
        max_used_watts ('float', optional): Maximum acceptable used power in watts.
                        If None, used power is not checked.
        min_remain_watts ('float', optional): Minimum acceptable remaining power in watts.
                          If None, remaining power is not checked.

    Returns:
        Boolean: True if all specified thresholds pass, else False

    Raises:
        None
    """
    try:
        result = device.api.get_power_budget()
    except Exception as e:
        log.error("Failed to get power budget: {e}".format(e=e))
        return False

    if result is None:
        log.error("get_power_budget returned None")
        return False

    used, remain = result

    if max_used_watts is not None:
        if used > max_used_watts:
            log.error(
                "Used power {used}W exceeds max allowed {max}W".format(
                    used=used, max=max_used_watts
                )
            )
            return False
        log.info("Used power {used}W <= {max}W: OK".format(used=used, max=max_used_watts))

    if min_remain_watts is not None:
        if remain < min_remain_watts:
            log.error(
                "Remaining power {remain}W is below minimum {min}W".format(
                    remain=remain, min=min_remain_watts
                )
            )
            return False
        log.info(
            "Remaining power {remain}W >= {min}W: OK".format(
                remain=remain, min=min_remain_watts
            )
        )

    return True


def verify_total_poe_power(
    device,
    expected_total_watts,
    tolerance_watts=0.0,
):
    """Verify the total POE power supply capacity.

    Args:
        device ('obj'): Device object
        expected_total_watts ('float'): Expected total POE power in watts
        tolerance_watts ('float', optional): Acceptable deviation in watts, default is 0.0

    Returns:
        Boolean: True if total power is within tolerance of expected, else False

    Raises:
        None
    """
    log.info(
        "Checking total POE power, expected: {exp}W (tolerance: ±{tol}W)".format(
            exp=expected_total_watts, tol=tolerance_watts
        )
    )
    try:
        actual = device.api.get_total_poe_power()
    except Exception as e:
        log.error("Failed to get total POE power: {e}".format(e=e))
        return False

    if actual is None:
        log.error("get_total_poe_power returned None")
        return False

    if abs(actual - expected_total_watts) <= tolerance_watts:
        log.info(
            "Total POE power {actual}W matches expected {exp}W (±{tol}W)".format(
                actual=actual, exp=expected_total_watts, tol=tolerance_watts
            )
        )
        return True

    log.error(
        "Total POE power {actual}W does not match expected {exp}W (±{tol}W)".format(
            actual=actual, exp=expected_total_watts, tol=tolerance_watts
        )
    )
    return False
