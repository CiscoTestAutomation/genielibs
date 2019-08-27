"""Common verification functions for bfd"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)


def verify_bfd_configuration(
    device,
    interface,
    interval,
    state,
    protocols,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd configuration is applied with correct interval and protocol

        Args:
            device ('obj'): device to use
            interface ('str'): interface bfd is configured on
            interval ('str'): interval to verify
            state ('str'): state to verify
            protocols ('list'): protocols to verify
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    log.info(
        "Verifying BFD is {} and has the following applied: interval {}, protocols {}".format(
            state, interval, protocols
        )
    )
    while timeout.iterate():
        try:
            out = device.parse(
                "show bfd neighbors interface {} details".format(interface)
            )
        except SchemaEmptyParserError:
            return False

        if out:
            for our_address in out.get("our_address", {}):
                for neighbor_address in out["our_address"][our_address].get(
                    "neighbor_address", {}
                ):
                    sub_dict = out["our_address"][our_address][
                        "neighbor_address"
                    ][neighbor_address]
                    if (
                        "state" in sub_dict
                        and state.lower() in sub_dict["state"].lower()
                        and "registered_protocols" in sub_dict
                        and set(x.lower() for x in protocols).issubset(
                            x.lower() for x in sub_dict["registered_protocols"]
                        )
                        and "session" in sub_dict
                    ):
                        session_dict = sub_dict["session"]
                        if (
                            "state" in session_dict
                            and state.lower() in session_dict["state"].lower()
                            and "echo_function" in session_dict
                            and session_dict["echo_function"]
                            and "echo_interval_ms" in session_dict
                            and session_dict["echo_interval_ms"] == interval
                        ):
                            return True
        timeout.sleep()

    return False
