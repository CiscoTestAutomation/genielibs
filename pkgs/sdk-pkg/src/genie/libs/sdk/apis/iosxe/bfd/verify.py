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

def verify_bfd_neighbors_details_session_state(
    device,
    address_family,
    address,
    expected_session_state,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd neighbors details session state

        Args:
            device ('obj'): device to use
            address_family ('str'): Address family value
            address ('str'): IP address for command
            expected_session_state ('str'): Session state to verify
            max_time ('int'): Max time to retry. Default to 60
            check_interval ('int'): Number of check in interval. Default to 10
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    
    while timeout.iterate():
        try:
            out = device.parse(
                "show bfd neighbors {} {} details".format(address_family.lower(), 
                    address)
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        state = out.q.contains('session').get_values('state', 0)
        if state == expected_session_state:
            return True
        timeout.sleep()

    return False

def verify_bfd_neighbors_details_registered_protocols(
    device,
    address_family,
    address,
    expected_registered_protocol,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd configuration is applied with correct interval and protocol

        Args:
            device ('obj'): device to use
            address_family ('str'): Address family value
            address ('str'): IP address for command
            expected_registered_protocols ('list'): protocols to verify
            max_time ('int'): Max time to retry. Default to 60
            check_interval ('int'): Number of check in interval. Default to 10
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    
    while timeout.iterate():
        try:
            out = device.parse(
                "show bfd neighbors {} {} details".format(address_family.lower(), 
                    address)
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        registered_protocols = out.q.get_values('registered_protocols')
        if expected_registered_protocol in registered_protocols:
            return True
        timeout.sleep()

    return False

def verify_bfd_neighbors_details(
    device,
    address_family,
    address,
    expected_min_tx_int=None,
    expected_min_rx_int=None,
    expected_multiplier=None,
    expected_session_state=None,
    expected_rh_rs=None,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd neighbors details

        Args:
            device ('obj'): device to use
            address_family ('str'): Address family value
            address ('str'): IP address for command
            expected_session_state ('str'): Session state to verify
            max_time ('int'): Max time to retry. Default to 60
            check_interval ('int'): Number of check in interval. Default to 10
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    
    while timeout.iterate():
        try:
            out = device.parse(
                "show bfd neighbors {} {} details".format(address_family.lower(), 
                    address)
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if expected_session_state:
            state = out.q.get_values('state', 0)
            if state == expected_session_state:
                return True
        
        if expected_min_tx_int:
            min_tx_int_ = out.q.get_values('min_tx_int', 0)
            if min_tx_int_ == expected_min_tx_int:
                return True
        
        if expected_min_rx_int:
            min_rx_int_ = out.q.get_values('min_rx_int', 0)
            if min_rx_int_ == expected_min_rx_int:
                return True
        
        if expected_multiplier:
            multiplier_ = out.q.get_values('multiplier', 0)
            if multiplier_ == expected_multiplier:
                return True
        
        if expected_rh_rs:
            rh_rs_ = out.q.get_values('rh_rs', 0)
            if rh_rs_ == expected_rh_rs:
                return True

        timeout.sleep()

    return False

def verify_bfd_neighbors_details_no_output(
    device,
    address_family,
    address,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd neighbors details has not output

        Args:
            device ('obj'): device to use
            address_family ('str'): Address family value
            address ('str'): IP address for command
            max_time ('int'): Max time to retry. Default to 60
            check_interval ('int'): Number of check in interval. Default to 10
        Returns:
            True
            False
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    
    while timeout.iterate():
        try:
            out = device.parse(
                "show bfd neighbors {} {} details".format(address_family.lower(), 
                    address)
            )
        except SchemaEmptyParserError:
            return True

        timeout.sleep()

    return False