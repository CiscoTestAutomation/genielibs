# Python
import logging
from os.path import getsize

# ATS
from pyats.utils.objects import R, find

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# ISSU
from genie.libs.sdk.apis.iosxe.issu.get import get_issu_free_space_on_disk

log = logging.getLogger(__name__)


def is_issu_terminal_state_reached_on_slot(
    device, slot, max_time=1200, interval=120
):
    """ Verify if a slot has reached
        Args:
            device ('obj'): Device object
            slot ('str'): Slot to check
            max_time ('int'): Max time checking
            interval ('int'): Interval of checking
        Raise:
            None
        Return:
            True
            False
    """
    log.info("Verifying terminal state of slot {slot}".format(slot=slot))

    timeout = Timeout(max_time=1200, interval=120)

    while timeout.iterate():
        try:
            output = device.parse("show issu state detail")
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue

        reached = (
            output["slot"].get(slot, {}).get("terminal_state_reached", False)
        )
        if reached:
            return True

        timeout.sleep()

    return False


def is_issu_in_state(device, slot, expected_state, max_time=1200, interval=30):
    """ Verify if ISSU is in state for a specific slot
        Args:
            device ('obj'): Device object
            slot ('str'): Slot for which we need to check ISSU state
            expected_state ('str'): Acceptable ISSU states are:
                                        - loadversion
                                        - runversion
                                        - acceptversion
                                        - commitversion
            max_time ('int'): Max time checking issu state
            interval ('int': Interval checking
        Raise:
            None
        Return
            True
            False
    """

    assert expected_state in [
        "loadversion",
        "runversion",
        "acceptversion",
        "commitversion",
    ]

    rs = R(["slot", slot, "last_operation", expected_state])

    timeout = Timeout(max_time=max_time, interval=interval)

    while timeout.iterate():
        try:
            output = device.parse("show issu state detail")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ret = find([output], rs, filter_=False, all_keys=True)
        if ret:
            return True

        timeout.sleep()

    return False


def is_issu_rollback_timer_in_state(
    device, slot, expected_state, max_time=120, interval=30
):
    """ Verify if issu rollback timer is in state
        Args:
            device ('obj'): Device object
            slot ('str'): Slot name
            expected_state ('str'): Expected state ('active', 'inactive')
            max_time ('int'): Max time checking 
            interval ('int'): Check interfal
        Return:
            True
            False
        Raise:
            SchemaEmptyParserError

    """

    assert expected_state in ["active", "inactive"]
    log.info(
        "Verifying roll back timer state on slot {slot}".format(slot=slot)
    )

    timeout = Timeout(max_time=max_time, interval=interval)

    while timeout.iterate():
        try:
            output = device.parse("show issu rollback-timer")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if (
            output
            and "rollback_timer_state" in output
            and output["rollback_timer_state"] == expected_state
        ):
            return True

        timeout.sleep()

    return False
