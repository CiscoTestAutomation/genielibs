# Python
import logging
import re

# PyATS
from ats.utils.objects import R, find

# Genie
from genie.utils.diff import Diff
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def get_platform_standby_rp(device, max_time=1200, interval=120):
    """ Get standby router slot on device
        Args:
            device ('obj'): Device object
            max_time ('int'): Max time in seconds retrieving router information
            interval ('int'): Interval in seconds retrieving router information
        Raise:
            None
        Return:
            Integer: Number of RP
    """

    log.info("Getting standby slot")

    rs = R(
        ["slot", "(?P<val1>.*)", "rp", "(?P<val2>.*)", "state", "ok, standby"]
    )

    timeout = Timeout(max_time=max_time, interval=interval)
    while timeout.iterate():
        try:
            output = device.parse("show platform")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ret = find([output], rs, filter_=False, all_keys=True)
        if ret:
            standby_rp = ret[0][1][1]
            srp = re.search("(?P<srp>(\d))", standby_rp).groupdict()["srp"]
            if srp:
                log.info(
                    "Standby RP on '{dev}' is: '{standby_rp}'".format(
                        dev=device.name, standby_rp=standby_rp
                    )
                )
                return srp

        timeout.sleep()

    return None


def get_diffs_platform(platform_before, platform_after):
    """ Check differences between two parsed outputs from 'show platform'

        Args:
            platform_before ('str'): Parsed output from 'show platform'
            platform_after ('str'): Parsed output from 'show platform'
        Return:
            True
            False
        Raises:
            None
    """

    dd = Diff(platform_before, platform_after, exclude=["insert_time"])
    dd.findDiff()

    for slot in platform_after["slot"]:
        for rp_lc in platform_after["slot"][slot]:
            for type_ in platform_after["slot"][slot][rp_lc]:
                state_after = platform_after["slot"][slot][rp_lc][type_][
                    "state"
                ]

                state_before = (
                    platform_before["slot"]
                    .get(slot, {})
                    .get(rp_lc, {})
                    .get(type_)
                    .get("state", False)
                )

                if not state_before:
                    log.info(
                        "Found differences between outputs:\n{out}".format(
                            out=dd
                        )
                    )
                    return False

                for subslot in platform_before["slot"][slot][rp_lc].get(
                    "subslot", []
                ):

                    subslot_state = (
                        platform_after["slot"][slot][rp_lc]
                        .get(subslot, {})
                        .get("state", False)
                    )

                    if not subslot_state:
                        log.info(
                            "Found differences between outputs:\n{out}".format(
                                out=dd
                            )
                        )

                if "ok" in state_after and "ok" in state_before:
                    continue
                else:
                    log.info(
                        "Found differences between outputs:\n{out}".format(
                            out=dd
                        )
                    )
                    return False
    return True
