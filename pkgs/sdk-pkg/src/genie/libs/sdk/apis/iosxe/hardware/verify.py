"""Common verify functions for hardware"""

# Python
import re
import logging

# Genie
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout

# Ats
from pyats.utils.objects import find, R

# HARDWARE
from genie.libs.sdk.apis.iosxe.hardware.get import (
    get_hardware_rp_slot,
    get_hardware_esp_slot,
)

log = logging.getLogger(__name__)


def verify_hardware_fan_speed_increase(curr_fans, prev_fans):
    """ Verify fan speed increase

        Args:
            curr_fans (`list`): current fans
            prev_fans (`list`): previous fans
        Returns:
            result(`bool`): verify result
        Raises:
            None
    """
    result = True
    for cf in curr_fans:
        for pf in prev_fans:
            if cf["slot"] != pf["slot"]:
                continue
            elif cf["speed"] <= pf["speed"]:
                log.error(
                    "Fan on {pf[slot]} speed doesn't increase. "
                    "Initial speed: {pf[speed]} Current speed: {cf[speed]}".format(
                        pf=pf, cf=cf
                    )
                )
                result = False
            else:
                log.info(
                    "Fan on {pf[slot]} speed increases from "
                    "{pf[speed]} to {cf[speed]}".format(pf=pf, cf=cf)
                )

    return result


def verify_hardware_active_RP_changed(
    device, pre_act, max_time=300, check_interval=30
):
    """ Verify active RP has changed

        Args:
            device (`obj`): Device object
            pre_act (`str`): previous active ESP
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): verify result
            curr_act (`str`): current active ESP
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        curr_act = get_hardware_rp_slot(device, "active")
        if curr_act != pre_act:
            return True, curr_act
        timeout.sleep()

    curr_act = pre_act
    return False, curr_act


def verify_hardware_active_ESP_changed(
    device, pre_act, max_time=300, check_interval=30
):
    """ Verify active ESP has changed

        Args:
            device (`obj`): Device object
            pre_act (`str`): previous active ESP
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): verify result
            curr_act (`str`): current active ESP
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        curr_act = get_hardware_esp_slot(device, "active")
        if curr_act != pre_act:
            return True, curr_act
        timeout.sleep()

    curr_act = pre_act
    return False, curr_act


def verify_hardware_slot_removed(
    device, slot, max_time=300, check_interval=30
):
    """ Verify hardware slot has removed

        Args:
            device (`obj`): Device object
            slot (`str`): hardware slot
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): verify result
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if slot not in out["slot"]:
            return True
        timeout.sleep()

    return False


def verify_hardware_slot_exist(device, slot, max_time=300, check_interval=30):
    """ Verify hardware slot exists

        Args:
            device (`obj`): Device object
            slot (`str`): hardware slot
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): verify result
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if slot in out["slot"]:
            return True
        timeout.sleep()

    return False


def verify_hardware_spa_removed(device, spa, max_time=300, check_interval=30):
    """ Verify spa has removed

        Args:
            device (`obj`): Device object
            spa (`str`): spa slot
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): verify result
        Raises:
            None
    """
    slots = spa.split("/")
    reqs = R(
        [
            "slot",
            slots[0],
            "(?P<type>.*)",
            "(?P<name>.*)",
            "subslot",
            slots[1],
            "(?P<sub_dict>.*)",
        ]
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        found = find([out], reqs, filter_=False, all_keys=True)
        if not found:
            return True
        timeout.sleep()

    return False


def verify_hardware_spa_exist(device, spa, max_time=300, check_interval=30):
    """ Verify spa exists

        Args:
            device (`obj`): Device object
            spa (`str`): spa slot
            max_time (`int`): max time
            check_interval (`int`): check interval
        Returns:
            result(`bool`): verify result
        Raises:
            None
    """
    slots = spa.split("/")
    reqs = R(
        [
            "slot",
            slots[0],
            "(?P<type>.*)",
            "(?P<name>.*)",
            "subslot",
            slots[1],
            "(?P<sub_dict>.*)",
        ]
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        found = find([out], reqs, filter_=False, all_keys=True)
        if found:
            return True
        timeout.sleep()

    return False


def verify_hardware_redundancy_states(
    device,
    oper_state="sso",
    peer_state="STANDBY HOT",
    manual_swact="enabled",
    max_time=600,
    check_interval=30,
):
    """ Verify redundancy operational state is sso
        Manual Swact is enabled and
        Peer state is STANDBY HOT

        Args:
            device (`obj`): Device object
            max_time (`int`): Max time
            check_interval (`int`): Check interval
        Returns:
            result (`bool`): verified result
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            out = device.parse("show redundancy states")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        try:
            oper_state_v = out["redundancy_mode_operational"]
            manual_swact_v = out["manual_swact"]
            peer_state_v = out["peer_state"]
        except KeyError as e:
            log.info(
                "Failed to get redundancy states on {}".format(device.name)
            )
            continue

        log.info("Redundancy operational state is {}".format(oper_state_v))
        log.info("Manual swact is {}".format(manual_swact_v))
        log.info("Peer state is {}".format(peer_state_v))

        if (
            oper_state_v.lower() == oper_state.lower()
            and manual_swact_v.lower() == manual_swact.lower()
            and peer_state.lower() in peer_state_v.lower()
        ):
            return True
        timeout.sleep()

    return False
