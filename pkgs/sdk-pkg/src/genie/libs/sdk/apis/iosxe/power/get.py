# Copyright (c) 2026 by Cisco Systems, Inc.
# All rights reserved.
"""External API functions for POE power management.

This module provides high-level API functions to retrieve Power over Ethernet (POE)
information from network devices. Functions use the standard Genie structured
parsers (via device.parse()) and reshape the parsed output into a simplified,
POE-focused structure.
"""

import logging
import time

from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.parser.utils.common import Common

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def _safe_float(value, default=0.0):
    """Convert value to float safely with default fallback.

    Args:
        value: Value to convert (any type)
        default: Default value if conversion fails (default: 0.0)

    Returns:
        float: Converted float value or default if conversion fails
    """
    try:
        return float(value)
    except Exception:
        return default


def get_poe_entry(device, interface, wait_up=False, max_retry=10, retry_delay=3):
    """Retrieve POE entry for a specific interface.

    Fetches Power over Ethernet power information for a given interface from the
    device. Supports optional retry logic to wait for interface to come online
    if POE power is not yet allocated.

    Args:
        device (obj): Device object with parse() and execute() methods
        interface (str): Interface name (e.g., 'GigabitEthernet1/0/1', 'Gi1/0/1')
        wait_up (bool): If True, retry up to max_retry times with retry_delay between
                       attempts waiting for the interface to appear in POE status.
                       If False, query once. (default: False)
        max_retry (int): Maximum number of retry attempts when wait_up=True.
                        (default: 10)
        retry_delay (int): Delay in seconds between retry attempts. (default: 3)

    Returns:
        dict: POE entry for the interface with keys:
            - 'mode' (str): Admin mode ('auto', 'never', etc.)
            - 'op_state' (str): Operational state ('on', 'off', etc.)
            - 'power' (float): Current power consumption (watts)
            - 'max' (float): Maximum allowed power (watts)
            - 'class' (str): IEEE power class
            - 'desc' (str): Device description on the interface

    Example:
        >>> entry = get_poe_entry(device, 'GigabitEthernet1/0/1')
        >>> entry['power']
        15.4
        >>> entry['mode']
        'auto'
    """
    key = Common.convert_intf_name(str(interface).strip())

    for attempt in range(max_retry if wait_up else 1):
        try:
            data = device.parse('show power inline')
        except SchemaEmptyParserError:
            log.info("Command has not returned any results, SchemaEmptyParserError")
            return

        interfaces = data.get("interface", {})
        if key in interfaces:
            values = interfaces[key]
            return {
                "mode": str(values.get("admin_state", "")).strip().lower(),
                "op_state": str(values.get("oper_state", "")).strip().lower(),
                "power": _safe_float(values.get("power"), 0.0),
                "max": _safe_float(values.get("max"), 0.0),
                "class": str(values.get("class", "")).strip().lower(),
                "desc": str(values.get("device", "")).strip(),
            }

        if wait_up and attempt < max_retry - 1:
            time.sleep(retry_delay)


def get_power_budget(device):
    """Retrieve POE module power budget information.

    Fetches module-level Power over Ethernet power budget statistics including
    currently used power and remaining available power.

    Args:
        device (obj): Device object with parse() and execute() methods

    Returns:
        tuple: (used_watts, remaining_watts) - Used POE power and remaining available
               power in watts (both as floats)

    Raises:
        RuntimeError: If unable to parse module power information

    Example:
        >>> used, remaining = get_power_budget(device)
        >>> used
        147.0
        >>> remaining
        1403.0
    """
    try:
        data = device.parse('show power inline')
    except SchemaEmptyParserError:
        log.info("Command has not returned any results, SchemaEmptyParserError")
        return

    watts = data.get("watts", {})
    if not watts:
        raise RuntimeError("Unable to parse module used/remain from show power inline")

    module = next(iter(watts.values()))
    used = _safe_float(module.get("used"), -1.0)
    remain = _safe_float(module.get("remaining"), -1.0)
    if used < 0 or remain < 0:
        raise RuntimeError("Unable to parse module used/remain from show power inline")
    return used, remain


def get_total_poe_power(device):
    """Retrieve total POE power supply capacity.

    Fetches the total Power over Ethernet power supply capacity from the device.
    This is the maximum available POE power that the module can supply.

    Args:
        device (obj): Device object with execute() and parse() methods

    Returns:
        float: Total POE power in watts

    Example:
        >>> total = get_total_poe_power(device)
        >>> total
        1550.0
    """
    try:
        data = device.parse('show power inline')
    except SchemaEmptyParserError:
        log.info("Command has not returned any results, SchemaEmptyParserError")
        return

    watts = data.get("watts", {})
    if not watts:
        return

    module = next(iter(watts.values()))
    return _safe_float(module.get("available"), 0.0)
