"""Common get info functions for hardware"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils.timeout import Timeout

# Unicon
from unicon.core.errors import SubCommandFailure

# pyATS
from pyats.utils.objects import find, R


log = logging.getLogger(__name__)


def get_hardware_all_fans_speed(device):
    """ Get fan speed for all fans 

        Args:
            device (`obj`): Device object
        Returns:
            fans (`list`): Fans info
        Raises:
            None
    """
    fans = []
    p = re.compile(r"Fan +Speed +(?P<speed>.*)%")

    try:
        out = device.parse("show environment | include Fan")
    except (SchemaEmptyParserError, SubCommandFailure) as e:
        return fans

    reqs = R(
        [
            "slot",
            "(?P<slot>.*)",
            "sensor",
            "(?P<sensor>.*)",
            "state",
            "(?P<state>.*)",
        ]
    )
    found = find([out], reqs, filter_=False, all_keys=True)
    if found:
        fans = GroupKeys.group_keys(
            reqs=reqs.args, ret_num={}, source=found, all_keys=True
        )

    for fan in fans:
        fan["speed"] = int(p.search(fan["state"]).groupdict()["speed"])
        log.info(
            "Found fan on {fan[slot]} with Speed {fan[speed]}%".format(fan=fan)
        )
    return fans


def get_hardware_rp_slot(
    device, state="standby", max_time=90, check_interval=30
):
    """ Get RP slot from device

        Args:
            device (`obj`): Device object
            state (`str`): RP state
            max_time (`int`): max wait time 
            check_interval (`int`): check interval 
        Returns:
            result (`str`): RP slot in required state
            None
        Raises:
            None
    """
    log.info(
        "Finding {st} RP on device {dev}".format(st=state, dev=device.name)
    )
    reqs = R(
        [
            "slot",
            "(?P<slot>.*)",
            "(?P<type>.*)",
            "(?P<name>.*)",
            "state",
            "(?P<state>.*)",
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
        keys = GroupKeys.group_keys(
            reqs=reqs.args, ret_num={}, source=found, all_keys=True
        )
        for key in keys:
            if "R" in key["slot"] and state in key["state"]:
                log.info(
                    "Found {st} RP {key[name]} on slot {key[slot]}".format(
                        st=state, key=key
                    )
                )
                return key["slot"]
        timeout.sleep()

    return None


def get_hardware_esp_slot(
    device, state="standby", max_time=90, check_interval=30
):
    """ Get ESP slot from device

        Args:
            device (`obj`): Device object
            state (`str`): ESP state
            max_time (`int`): max wait time 
            check_interval (`int`): check interval 
        Returns:
            result (`str`): ESP slot in required state
            None
        Raises:
            None
    """
    log.info(
        "Finding {st} ESP on device {dev}".format(st=state, dev=device.name)
    )
    reqs = R(
        [
            "slot",
            "(?P<slot>.*)",
            "(?P<type>.*)",
            "(?P<name>.*)",
            "state",
            "(?P<state>.*)",
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
        keys = GroupKeys.group_keys(
            reqs=reqs.args, ret_num={}, source=found, all_keys=True
        )
        for key in keys:
            if "F" in key["slot"] and state in key["state"]:
                log.info(
                    "Found {st} ESP {key[name]} on slot {key[slot]}".format(
                        st=state, key=key
                    )
                )
                return key["slot"]
        timeout.sleep()

    return None


def get_hardware_slot_state(device, slot):
    """ Get slot state

        Args:
            device (`obj`): Device object
            slot (`str`): Slot
        Returns:
            state (`str`): Slot state
            None
        Raises:
            None
    """
    log.info("Getting slot {} state on device {}".format(slot, device.name))
    try:
        out = device.parse("show platform")
    except SchemaEmptyParserError:
        return None

    reqs = R(
        [
            "slot",
            str(slot),
            "(?P<type>.*)",
            "(?P<name>.*)",
            "state",
            "(?P<state>.*)",
        ]
    )
    found = find([out], reqs, filter_=False, all_keys=True)
    if found:
        keys = GroupKeys.group_keys(
            reqs=reqs.args, ret_num={}, source=found, all_keys=True
        )
        return keys[0]["state"]
    else:
        return None


def get_hardware_inserted_sfp(device, prev_slots, sfp_descr, intf_type):
    """ Get newly inserted SFP

        Args:
            device (`obj`): Device object
            prev_slots (`dict`): Previous sfp slot dict
            sfp_descr (`str`): SFP descr
            intf_type (`str`): Interface type
        Returns:
            interface (`str`): Interface name
    """
    intf_sfp_dict = {}
    curr_slots = get_hardware_sfp_slot_dict(device, sfp_descr)
    for slot in curr_slots:
        if slot not in prev_slots:
            intf = intf_type + slot
            intf_sfp_dict.update({intf: curr_slots[slot]})
            log.info(
                "Found newly inserted SFP {} with interface {}".format(
                    curr_slots[slot], intf
                )
            )

    if len(intf_sfp_dict) == 1:
        return list(intf_sfp_dict.keys())[0]
    elif len(intf_sfp_dict) == 0:
        log.error(
            "Failed to detect newly inserted SFP on {}".format(device.name)
        )
    else:
        log.error("Found multiple inserted SFPs {}".format(intf_sfp_dict))

    return None


def get_hardware_sfp_slot_dict(device, sfp_descr=".*"):
    """ Get SFP slot dict

        Args:
            device (`obj`): Device object
            sfp_descr (`str`): SFP descr
        Returns:
            sfp_slot_dict (`dict`): SFP slot dict
                example: {
                    '1/1/6':{'slot': '1', 
                             'subslot': '1 transceiver 6', 
                             'lc': 'ASR1000-SIP10', 
                             'pid': 'SFP-GE-S', 
                             'descr': 'GE SX'}}
        Raises:
            None
    """
    log.info("Getting inventory on {}".format(device.name))
    keys = []
    try:
        out = device.parse("show inventory")
    except SchemaEmptyParserError:
        return keys

    reqs = R(
        [
            "slot",
            "(?P<slot>.*)",
            "lc",
            "(?P<lc>.*)",
            "subslot",
            "(?P<subslot>.*)",
            "(?P<pid>.*)",
            "descr",
            "(?P<descr>" + sfp_descr + ")",
        ]
    )
    found = find([out], reqs, filter_=False, all_keys=True)

    if found:
        keys = GroupKeys.group_keys(
            reqs=reqs.args, ret_num={}, source=found, all_keys=True
        )

    sfp_slot_dict = {}
    p = re.compile(r"(?<=\d)( +\w+ )(?=\d)")
    for sfp in keys:
        slot = sfp["slot"] + "/" + re.sub(p, "/", sfp["subslot"])
        sfp_slot_dict.update({slot: sfp})

    return sfp_slot_dict


def get_hardware_interface_sfp_descr(device, interface, sfp_slot_dict=""):
    """ Get interface SFP descr

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            sfp_slot_dict (`dict`): SFP slot dict
                example: {
                    '1/1/6':{'slot': '1', 
                             'subslot': '1 transceiver 6', 
                             'lc': 'ASR1000-SIP10', 
                             'pid': 'SFP-GE-S', 
                             'descr': 'GE SX'}}
        Returns:
            descr (`str`): Interface SFP descr
        Raises:
            None
    """
    if not sfp_slot_dict:
        sfp_slot_dict = get_hardware_sfp_slot_dict(device)

        if not sfp_slot_dict:
            return None

    p = re.compile(r"^.*?(?=\d\S*)")
    slot = re.sub(p, "", interface)
    if slot in sfp_slot_dict:
        return sfp_slot_dict[slot].get("descr")
