import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# PyATS
from ats.utils.objects import R, find

# PLATFORM
from genie.libs.sdk.apis.iosxe.platform.get import get_diffs_platform

log = logging.getLogger(__name__)


def is_platform_slot_in_state(
    device, slot, state="ok, active", max_time=1200, interval=120
):
    """ Verify if slot is in state

        Args:
            device ('obj'): Device object
            slot ('str'): Slot number
            state ('str'): State being checked
            max_time ('int'): Max time checking
            interval ('int'): Interval checking
        Return:
            True
            False
        Raises:
            None
    """
    log.info("Verifying state of slot {slot}".format(slot=slot))
    timeout = Timeout(max_time=max_time, interval=interval)

    rs = R(["slot", slot, "rp", "(?P<val2>.*)", "state", state])

    while timeout.iterate():
        try:
            output = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ret = find([output], rs, filter_=False, all_keys=True)
        if ret:
            log.info(
                "Slot {slot} reached state '{state}'".format(
                    slot=slot, state=state
                )
            )
            return True

        timeout.sleep()

    return False


def verify_changes_platform(
    device, platform_before, platform_after, max_time=1200, interval=120
):
    """ Verify if there are changes between outputs from 'show platform'
        Args:
            device ('obj'): Device object
            platform_before ('str'): Parsed output from 'show platform'
            platform_after ('str'): Parsed output from 'show platform'
            max_time ('int'): Max time in seconds retrying
            interval ('int'): Interval of each retry
        Return:
            True
            False
        Raises:
            None
    """

    timeout = Timeout(max_time=max_time, interval=interval)
    while timeout.iterate():
        if get_diffs_platform(
            platform_before=platform_before, platform_after=platform_after
        ):
            return True
        else:
            try:
                platform_after = device.parse("show platform")
            except SchemaEmptyParserError:
                pass

        timeout.sleep()

    return False
