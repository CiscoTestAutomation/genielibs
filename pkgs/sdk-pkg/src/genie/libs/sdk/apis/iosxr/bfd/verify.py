"""Common verification functions for bfd"""

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)

def verify_bfd_session_destination_details_session_state(
    device,
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
                "show bfd session destination {address} detail".format(
                    address=address
                )
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        state = out.q.contains('session').get_values('state', 0)
        if state == expected_session_state:
            return True
        timeout.sleep()

    return False

def verify_bfd_session_destination_details_client(
    device,
    address,
    expected_client,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd neighbors details session state

        Args:
            device ('obj'): device to use
            address ('str'): IP address for command
            expected_client ('str'): Client to verify
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
                "show bfd session destination {address} detail".format(
                    address=address
                )
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        client_ = out.q.contains('.*{}.*'.format(expected_client), regex=True).get_values('owner_info')
        if expected_client in client_:
            return True
        timeout.sleep()

    return False

def verify_bfd_ipv6_session_destination_details_session_state(
    device,
    address,
    expected_session_state,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd neighbors details session state

        Args:
            device ('obj'): device to use
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
                "show bfd ipv6 session destination {address} detail".format(
                    address=address
                )
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        state = out.q.contains('session').get_values('state', 0)
        if state == expected_session_state:
            return True
        timeout.sleep()

    return False

def verify_bfd_ipv6_session_destination_details_client(
    device,
    address,
    expected_client,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd neighbors details session state

        Args:
            device ('obj'): device to use
            address ('str'): IP address for command
            expected_session_state ('str'): state to verify
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
                "show bfd ipv6 session destination {address} detail".format(
                    address=address
                )
            )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        client_ = out.q.contains('.*{}.*'.format(expected_client), regex=True).get_values('owner_info')
        if expected_client in client_:
            return True
        timeout.sleep()

    return False

def verify_bfd_session_destination(
    device,
    address,
    ipv6=False,
    expected_session_state=None,
    expected_det_time=None,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd session destination details

        Args:
            device ('obj'): device to use
            address ('str'): IP address for command
            ipv6 ('bool'): Run ipv6 show command. Default to false.
            expected_session_state ('str'): Session state to verify
            expected_det_time ('str'): Expect det time value.
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
            if ipv6:
                out = device.parse(
                    "show bfd ipv6 session destination {address}".format(
                        address=address
                    )
                )
            else:
                out = device.parse(
                    "show bfd session destination {address}".format(
                        address=address
                    )
                )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if expected_session_state:
            state = out.q.contains('session').get_values('state', 0)
            if state == expected_session_state:
                return True
        
        if expected_det_time:
            async_detection_time = out.q.get_values('async_detection_time', 0)
            if async_detection_time == expected_det_time:
                return True

        timeout.sleep()

    return False

def verify_bfd_session_destination_detail(
    device,
    address,
    expected_session_state=None,
    expected_received_parameters_state=None,
    ipv6=False,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd session destination detail

        Args:
            device ('obj'): device to use
            address ('str'): IP address for command
            expected_session_state ('str'): Session state to verify
            expected_received_parameters_state ('str'): Received parameter state to verify
            ipv6 ('bool'): Run ipv6 show command. Default to false
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
            if ipv6:
                out = device.parse(
                "show bfd ipv6 session destination {address} detail".format(
                    address=address
                )
            )
            
            else:
                out = device.parse(
                    "show bfd session destination {address} detail".format(
                        address=address
                    )
                )
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if expected_session_state:
            state = out.q.contains('session').get_values('state', 0)
            if state != expected_session_state:
                timeout.sleep()
                continue
        
        if expected_received_parameters_state:
            received_parameters_state = out.q.contains(
                'received_parameters').get_values('state', 0)
            if received_parameters_state != expected_received_parameters_state:
                timeout.sleep()
                continue
        
        return True

    return False

def verify_bfd_session_destination_detail_no_output(
    device,
    address,
    ipv6=False,
    max_time=60,
    check_interval=10,
):
    """ Verifies bfd session destination has no output

        Args:
            device ('obj'): device to use
            address_family ('str'): Address family value
            address ('str'): IP address for command
            ipv6 ('bool'): Run ipv6 show command. Default to false
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
            if ipv6:
                out = device.parse(
                "show bfd ipv6 session destination {address} detail".format(
                    address=address
                )
            )
            
            else:
                out = device.parse(
                    "show bfd session destination {address} detail".format(
                        address=address
                    )
                )
        except SchemaEmptyParserError:
            return True
        
        timeout.sleep()

    return False