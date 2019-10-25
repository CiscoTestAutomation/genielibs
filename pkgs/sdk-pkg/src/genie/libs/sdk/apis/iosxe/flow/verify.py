""" Common verify functions for flow """

# Python
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_flow_with_source_and_destination_exists(
    device,
    flow_monitor,
    source_address,
    destination_address,
    max_time=60,
    check_interval=10,
):
    """ Verifies a flow under flow_monitor with specified
        source and destination address' exist

        Args:
            device ('obj'): Device to use
            flow_monitor ('str'): Flow monitor to search under
            source_address ('str'): Source address to match
            destination_address ('str'): Destination address to match
            max_time ('int'): Max time to keep checking
            check_interval ('int'): How often to check

        Raises:
            N/A

        Returns:
            True/False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        flow_address_pairs = device.api.get_flows_src_dst_address_pairs(
            device=device, flow_monitor=flow_monitor
        )

        if (source_address, destination_address) in flow_address_pairs:
            return True

        timeout.sleep()

    return False


def verify_flow_exporter_records_added_and_sent_are_equal(
    device, exporter, max_time=30, check_interval=10
):
    """ Verifies that flow exporter records added and sent are equal

        Args:
            device ('obj'): Device to use
            exporter ('str'): Exporter name
            max_time ('int'): Max time to keep checking
            check_interval ('int'): How often to check

        Raises:
            N/A

        Returns:
            True/False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse(
                "show flow exporter {exporter} statistics".format(
                    exporter=exporter
                )
            )
        except SchemaEmptyParserError:
            return False

        for client in (
            output.get("flow_exporter", {})
            .get(exporter, {})
            .get("client_send_stats", {})
        ):
            if exporter in client:
                added = (
                    output["flow_exporter"][exporter]["client_send_stats"][
                        client
                    ]
                    .get("records_added", {})
                    .get("total")
                )

                sent = (
                    output["flow_exporter"][exporter]["client_send_stats"][
                        client
                    ]
                    .get("records_added", {})
                    .get("sent")
                )

                log.info(
                    "Records added is: {added}. Records sent is {sent}".format(
                        added=added, sent=sent
                    )
                )
                
                if 0 < added == sent > 0:
                    return True

        timeout.sleep()

    return False
