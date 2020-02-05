"""Common functions for traffic checks"""

# Python
import re
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.harness.exceptions import GenieTgnError

# Commons
from genie.libs.sdk.apis.utils import analyze_rate

log = logging.getLogger(__name__)


def set_traffic_transmit_rate(
    testbed, traffic_stream, set_rate, tolerance, max_time, check_interval
):
    """Set stream transmit rate

        Args:
            testbed (`obj`): Testbed object
            traffic_stream (`str`): Traffic stream name
            set_rate (`int`): Traffic set rate
            tolerance (`int`): Traffic tolerance
            max_time (`int`): Retry maximum time
            check_interval (`int`): Interval in seconds to do recheck

        Returns:
            None
        Raises:
            KeyError: Could not find device on testbed
            Exception: Failed to set transmit rate
    """
    try:
        ixia = testbed.devices["IXIA"]
    except KeyError:
        raise KeyError("Could not find IXIA device on testbed")

    rate, rate_unit, original_rate = analyze_rate(set_rate)

    # IXIA statistics doesn't have 'Gbps' option
    if rate_unit == "Gbps":
        original_rate = original_rate * 1000
        rate_unit = "Mbps"

    # Set the transmit rate
    try:
        ixia.set_layer2_bit_rate(
            traffic_stream=traffic_stream,
            rate=original_rate,
            rate_unit=rate_unit,
            start_traffic=False,
        )
    except Exception as e:
        raise Exception("Failed to set the transmit rate due to: {}".format(e))


def check_traffic_transmitted_rate(
    testbed,
    traffic_stream,
    set_rate,
    tolerance,
    max_time,
    check_interval,
    check_stream=True,
):
    """Check transmitted rate was set correctly or not

        Args:
            testbed (`obj`): Testbed object
            traffic_stream (`str`): Traffic stream name
            set_rate (`int`): Traffic set rate
            tolerance (`int`): Traffic tolerance
            max_time (`int`): Retry maximum time
            check_interval (`int`): Interval in seconds to do recheck

        Returns:
            None
        Raises:
            KeyError: Could not find device on testbed
            Exception: Traffic drops found
    """
    try:
        ixia = testbed.devices["IXIA"]
    except KeyError:
        raise KeyError("Could not find IXIA device on testbed")

    rate, rate_unit, original_rate = analyze_rate(set_rate)

    # IXIA statistics doesn't have 'Gbps' option
    if rate_unit == "Gbps":
        original_rate = original_rate * 1000
        rate_unit = "Mbps"

    # Start the traffic stream
    ixia.start_traffic_stream(traffic_stream, check_stream)

    log.info(
        "Verify the transmitted rate was set correctly, "
        "will retry for {} every {} seconds".format(max_time, check_interval)
    )

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():

        # Print IXIA traffic streams when doing a traffic check/retrieve call
        ixia.create_traffic_streams_table()

        # Check the transmitted rate was set correctly
        transmitted_rate = ixia.get_traffic_items_statistics_data(
            traffic_stream=traffic_stream,
            traffic_data_field="Tx Rate ({})".format(rate_unit),
        )

        expected_rate, expected_rate_unit, original_rate, tolerance_margin = get_traffic_rates(
            str(original_rate), tolerance
        )

        if (
            float(transmitted_rate) < original_rate + tolerance_margin
            and float(transmitted_rate) > original_rate - tolerance_margin
        ):
            log.info(
                "Transmitted rate '{transmitted_rate}{rate_unit}' is within "
                "the set rate '{rate}{rate_unit}', tolerance is {tolerance}%".format(
                    transmitted_rate=transmitted_rate,
                    rate=original_rate,
                    rate_unit=rate_unit,
                    tolerance=tolerance,
                )
            )
            return
        else:
            timeout.sleep()

    raise Exception(
        "Retrieved transmit rate for traffic stream '{}' is '{}' while "
        "we did set '{}{}', tolerance is {}%".format(
            traffic_stream,
            transmitted_rate,
            original_rate,
            rate_unit,
            tolerance,
        )
    )


def check_traffic_expected_rate(
    testbed, traffic_stream, expected_rate, tolerance,
    traffic_gen='IXIA'
):
    """Check the expected rate

        Args:
            testbed (`obj`): Testbed object
            traffic_stream (`str`): Traffic stream name
            expected_rate (`str`): Traffic expected received rate
            tolerance (`str`): Traffic loss tolerance percentage
            traffic_gen (`str`): Traffic generating device

        Returns:
            None
        Raises:
            KeyError: Could not find device on testbed
            Exception: Traffic drops found
    """
    try:
        ixia = testbed.devices[traffic_gen]
    except KeyError:
        raise KeyError("Could not find {} device on testbed".format(traffic_gen))

    # Print IXIA traffic streams when doing a traffic check/retrieve call
    table = ixia.get_traffic_item_statistics_table(["Rx Rate (Mbps)"])

    # needed for logic in next block
    setattr(table, 'border', False)
    setattr(table, 'header', False)

    # gets the row that 'traffic_stream' is on
    row = [x.strip() for x in table.get_string(fields=['Traffic Item']).splitlines()].index(traffic_stream)
    # gets the 'Rx Rate (Mbps)' value at the above row
    retrieved_rate = float(table.get_string(fields=['Rx Rate (Mbps)'], start=row, end=row+1))

    # Since retrieved_rate is always going to be Mbps
    retrieved_rate_in_bytes = retrieved_rate * 1000000

    if ">" in expected_rate or "<" in expected_rate:
        # Split and check below 4 conditions
        # >0.6M, <0.8M
        # <0.8M, >0.6M
        # <0.8M
        # >0.6M
        left_expected_rate = None
        right_expected_rate = None
        expected_rate_list = expected_rate.split(',')
        left_expected_rate = expected_rate_list[0]
        if len(expected_rate_list) == 2:
            right_expected_rate = expected_rate_list[1]
        if left_expected_rate:
            # Check left part of split
            # >0.6M
            # Check if left value contains '>' or '<'
            left_is_greater = '>' in left_expected_rate
            left_rate_filtered = (left_expected_rate.split('>')[1].
                strip() if left_is_greater else left_expected_rate.split('<')[1].strip())
            left_rate_in_bytes, left_original_rate_unit, left_original_rate, _ = get_traffic_rates(
                    left_rate_filtered, tolerance,
                )
            rate_provided = '{}{}{}'.format('>' if left_is_greater else '<', left_original_rate, 
                                left_original_rate_unit)
            rate_converted = '{}{}Mbps'.format('>' if left_is_greater else '<', 
                                left_rate_in_bytes / 1000000)

            left_tolerance_in_bytes = left_rate_in_bytes * (tolerance / 100)
            left_rate_tolerance_diff = (left_rate_in_bytes - left_tolerance_in_bytes) if left_is_greater else (left_rate_in_bytes + left_tolerance_in_bytes)
            rate_expected = left_original_rate
            # Check right part of split if exist
            # <0.8M
            if right_expected_rate:
                # Check if right value contains '>' or '<'
                right_is_greater = '>' in right_expected_rate
                right_rate_filtered = (right_expected_rate.split('>')[1].
                    strip() if right_is_greater else right_expected_rate.split('<')[1].strip())
                right_rate_in_bytes, right_original_rate_unit, right_original_rate, _ = get_traffic_rates(
                        right_rate_filtered, tolerance,
                    )
                if right_original_rate > rate_expected:
                    rate_expected = right_original_rate
                rate_provided = '{}, {}{}{}'.format(rate_provided, '>' if right_is_greater else '<', 
                                    right_original_rate, right_original_rate_unit)
                rate_converted = '{}, {}{}Mbps'.format(rate_converted, '>' if right_is_greater else '<', 
                                right_rate_in_bytes / 1000000)
                
                right_tolerance_in_bytes = right_rate_in_bytes * (tolerance / 100)
                right_rate_tolerance_diff = (right_rate_in_bytes - right_tolerance_in_bytes)  if right_is_greater else (right_rate_in_bytes + right_tolerance_in_bytes)
            
            log.info('Rate provided in datafile is {rate_provided}. '
                    'Converted to Mbps it is {rate_converted}'
                    .format(rate_provided=rate_provided, rate_converted=rate_converted))
            
            log_message = "Expected rate for traffic stream '{stream}' is '{expected} Mbps' " \
                                "(tolerance {tolerance}%,".format(
                                    stream=traffic_stream,
                                    expected=rate_expected,
                                    tolerance=tolerance)

            # Merge proper log message
            # Log message from the Left side of expected rate
            if right_expected_rate:
                if left_is_greater:
                    log_message = "{log_message} {gt} Mbps<>{lt} Mbps".format(
                        log_message=log_message,
                        gt=left_rate_tolerance_diff / 1000000,
                        lt=right_rate_tolerance_diff / 1000000)
                else:
                    log_message = "{log_message} {gt} Mbps<>{lt} Mbps".format(
                        log_message=log_message,
                        gt=right_rate_tolerance_diff / 1000000,
                        lt=left_rate_tolerance_diff / 1000000)
            else:
                if left_is_greater:
                    log_message = "{log_message} {expected_after_tolerance} Mbps{condition}".format(
                        log_message=log_message,
                        expected_after_tolerance=left_rate_tolerance_diff / 1000000,
                        condition='<')
                else:
                    log_message = "{log_message} {condition}{expected_after_tolerance} Mbps".format(
                        log_message=log_message,
                        expected_after_tolerance=left_rate_tolerance_diff / 1000000,
                        condition='>')
            # # Log message from the Right side of expected rate
            # Join left and right in last
            log_message = "{log_message}) and got '{actual} Mbps'".format(
                log_message=log_message,actual=retrieved_rate)

            # Failure check
            rate_check = True
            if (left_is_greater and (retrieved_rate_in_bytes < left_rate_tolerance_diff)):
                rate_check = False
            if (not left_is_greater and (retrieved_rate_in_bytes > left_rate_tolerance_diff)):
                rate_check = False
            if right_expected_rate:
                if (right_is_greater and (retrieved_rate_in_bytes < right_rate_tolerance_diff)):
                    rate_check = False
                if (not right_is_greater and (retrieved_rate_in_bytes > right_rate_tolerance_diff)):
                    rate_check = False
            if not rate_check:
                raise Exception(log_message)
            log.info(log_message)

    else:
        rate_in_bytes, original_rate_unit, original_rate, _ = get_traffic_rates(
            expected_rate, tolerance)

        log.info('Rate provided in datafile is {original_rate}{original_rate_unit}. '
                 'Converted to Mbps it is {converted}Mbps'
                 .format(original_rate=original_rate,
                         original_rate_unit=original_rate_unit,
                         converted=rate_in_bytes / 1000000))

        tolerance_in_bytes = rate_in_bytes * (tolerance / 100)

        if (
            retrieved_rate_in_bytes < rate_in_bytes + tolerance_in_bytes
            and retrieved_rate_in_bytes > rate_in_bytes - tolerance_in_bytes
        ):

            log.info(
                "Expected rate for traffic stream '{stream}' is '{expected} Mbps' "
                "(tolerance {tolerance}%, {gt} Mbps<>{lt} Mbps) and got '{actual} Mbps'"
                    .format(
                    stream=traffic_stream,
                    expected=rate_in_bytes / 1000000,
                    tolerance=tolerance,
                    gt=(rate_in_bytes - tolerance_in_bytes) / 1000000,
                    lt=(rate_in_bytes + tolerance_in_bytes) / 1000000,
                    actual=retrieved_rate,
                )
            )
        else:
            raise Exception(
                "Expected rate for traffic stream '{stream}' is '{expected} Mbps' "
                "(tolerance {tolerance}%, {gt} Mbps<>{lt} Mbps) and got '{actual} Mbps'"
                    .format(
                    stream=traffic_stream,
                    expected=rate_in_bytes / 1000000,
                    tolerance=tolerance,
                    gt=(rate_in_bytes - tolerance_in_bytes) / 1000000,
                    lt=(rate_in_bytes + tolerance_in_bytes) / 1000000,
                    actual=retrieved_rate,
                )
            )


def check_traffic_drop_count(testbed, traffic_stream, drop_count):
    """Check for the drop count

        Args:
            testbed (`obj`): Testbed object
            traffic_stream (`str`): Traffic stream name
            drop_count (`str`): Expected drop count

        Returns:
            None
        Raises:
            KeyError: Could not find device on testbed
            Exception: Traffic drops found
    """
    try:
        ixia = testbed.devices["IXIA"]
    except KeyError:
        raise KeyError("Could not find IXIA device on testbed")

    # Stop all traffic streams
    ixia.stop_traffic()

    try:
        # Print IXIA traffic streams when doing a traffic check/retrieve call
        ixia.get_traffic_item_statistics_table(["Frames Delta"])

        # Check for no drops
        dropped_frames = ixia.get_traffic_items_statistics_data(
            traffic_stream=traffic_stream, traffic_data_field="Frames Delta"
        )
    except GenieTgnError as e:
        raise Exception(
            "Couldn't extract the dropped IXIA frames for traffic flow {}".format(
                traffic_stream
            )
        )

    if int(dropped_frames) <= int(drop_count):
        log.info(
            "Dropped IXIA frames for traffic flow '{}' is '{}' which is less than"
            " or equal to the expected drop count '{}'".format(
                traffic_stream, dropped_frames, drop_count
            )
        )
        return
    else:
        raise Exception(
            "Dropped IXIA frames for traffic flow '{}' is '{}' which is greater than"
            " the expected drop count '{}'".format(
                traffic_stream, dropped_frames, drop_count
            )
        )


def get_traffic_rates(expected_rate, tolerance):
    """Retrieve the formated traffic rates and tolerance margin

        Args:
            expected_rate (`str`): Expected traffic rate
            tolerance (`str`): Tolerance margin

        Returns:
            expected_rate, expected_rate_unit, original_rate, tolerance_margin
        Raise:
            Exception: Failed analyzing rate
    """
    try:
        expected_rate, expected_rate_unit, original_rate = analyze_rate(
            expected_rate
        )
    except Exception as e:
        raise Exception("{}".format(e))

    # Calculate tolerance
    tolerance_margin = float(original_rate) * (tolerance / 100)

    return expected_rate, expected_rate_unit, original_rate, tolerance_margin
