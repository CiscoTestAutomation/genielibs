"""Common verification functions for services"""

# Python
import re
import logging
import operator
from datetime import datetime

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.utils import Dq

log = logging.getLogger(__name__)

def verify_services_accounting_flow_active(device, expected_count, max_time=60, check_interval=10):
    """Verify accounting flow active count

    Args:
        device (obj): Device object
        expected_count (int/str): Expected count
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        bool: True/False
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show services accounting flow')
        except SchemaEmptyParserError:
            return None
        
        # "services-accounting-information": {
        #     "flow-information": [
        #         {
        #             "active-flows": str,

        if out.q.get_values('active-flows', 0) == str(expected_count):
            return True
        timeout.sleep()


def verify_services_accounting_status(device, expected_export_format=None, route_record_threshold=None,
                               max_time=60, check_interval=10):
    """ Verify 'show services accounting status' against criteria

    Args:
        device (obj): Device object
        expected_export_format (str): Session address
        route_record_threshold (str): Expected session state
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:  
        Boolean

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show services accounting status')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        #"status-information": [
        #    {
        #        "interface-name": "ms-9/0/0",
        #        "status-export-format": "9",
        #        "status-route-record-count": "902244",
        #        "status-ifl-snmp-map-count": "296",
        #        "status-as-count": "0",
        #        "status-monitor-config-set": "Yes",
        #        "status-monitor-route-record-set": "No",
        #        "status-monitor-ifl-snmp-set": "Yes",
        #    }

        if expected_export_format and \
            out.q.get_values('status-export-format',0) != str(expected_export_format):
            timeout.sleep()
            continue
        if route_record_threshold and \
            int(out.q.get_values('status-route-record-count',0)) < int(route_record_threshold):
            timeout.sleep()
            continue

        return True
        

    return False


def verify_services_accounting_flow(device, expected_flow_packets_ten_second_rate=None, expected_active_flows=None,
                                    max_time=60, check_interval=10, invert=False):
    """ Verify 'show services accounting flow' against criteria

    Args:
        device (obj): Device object
        expected_flow_packets_ten_second_rate (str): flow packets ten second rate
        expected_active_flows (str): expected active flows
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
        invert (bool, optional): Inverts the API

    Returns:  
        Boolean

    Raises:
        N/A
    """

    op = operator.ne
    if invert:
        op = operator.eq

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show services accounting flow')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        #"flow-information": [
        #    {
        #        "interface-name": "ms-9/0/0",
        #        "local-ifd-index": "140",
        #        "flow-packets": "0",
        #        "flow-bytes": "0",
        #        "flow-packets-ten-second-rate": "0",
        #        "flow-bytes-ten-second-rate": "0",
        #        "active-flows": "0",
        #        "flows": "0",
        #        "flows-exported": "0",
        #        "flow-packets-exported": "9",
        #        "flows-expired": "0",
        #        "flows-aged": "0",
        #    }
        #]

        if expected_flow_packets_ten_second_rate and op(out.q.get_values('flow-packets-ten-second-rate', 0), str(expected_flow_packets_ten_second_rate)):
            timeout.sleep()
            continue
        if expected_active_flows and op(out.q.get_values('active-flows', 0), str(expected_active_flows)):
            timeout.sleep()
            continue

        return True
        

    return False


def verify_services_accounting_errors(device, expected_service_set_dropped=None, expected_active_timeout_failures=None, 
                                      expected_export_packet_failures=None, expected_flow_creation_failures=None,
                                      max_time=60, check_interval=10):
    """ Verify if there are errors in 'show services accounting errors'

    Args:
        device (obj): Device object
        expected_service_set_dropped ('str'): service set dropped
        expected_active_timeout_failures ('str'): active timeout failures
        expected_export_packet_failures ('str'): exported packet failures
        expected_flow_creation_failures ('str'): flow creation failures
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:  
        Boolean

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show services accounting errors')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        #"v9-error-information": [
        #    {
        #        "interface-name": "ms-9/0/0",
        #        "service-set-dropped": "0",
        #        "active-timeout-failures": "0",
        #        "export-packet-failures": "0",
        #        "flow-creation-failures": "0",
        #        "memory-overload": "No",
        #    }
        #]

        if expected_service_set_dropped and \
            out.q.get_values('service-set-dropped',0) == str(expected_service_set_dropped):
            timeout.sleep()
            continue
        if expected_active_timeout_failures and \
            out.q.get_values('active-timeout-failures',0) == str(expected_active_timeout_failures):
            timeout.sleep()
            continue
        if expected_export_packet_failures and \
            out.q.get_values('export-packet-failures',0) == str(expected_export_packet_failures):
            timeout.sleep()
            continue
        if expected_flow_creation_failures and \
            out.q.get_values('flow-creation-failures',0) == str(expected_flow_creation_failures):
            timeout.sleep()
            continue

        return True
        

    return False


def verify_services_accounting_aggregation(device, name, expected_source_address=None, 
                                           expected_destination_address=None, expected_snmp_interface=None, 
                                           expected_mpls_label1=None,expected_mpls_label2=None,
                                           max_time=60, check_interval=10):
    """ Verify if there are errors in 'show services accounting errors'

    Args:
        device (obj): Device object
        expected_source_address ('str'): expected source address
        expected_destination_address ('str'): expected destination address
        expected_snmp_interface ('str'): expected snmp interface
        expected_mpls_label1 ('str'): expected mpls label1
        expected_mpls_label2 ('str'): expected mpls label2
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:  
        Boolean

    Raises:
        N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show services accounting aggregation template template-name {name} extensive'.format(name=name))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        #"flow-aggregate-template-detail": {
        #    "flow-aggregate-template-detail-ipv4": {
        #        "detail-entry": [{
        #            "source-address": "27.93.202.64",
        #            "destination-address": "106.187.14.158",
        #            "source-port": "8",
        #            "destination-port": "0",
        #            "protocol": {"#text": "1"},
        #            "tos": "0",
        #            "tcp-flags": "0",
        #            "source-mask": "32",
        #            "destination-mask": "30",
        #            "input-snmp-interface-index": "618",
        #            "output-snmp-interface-index": "620",
        #            "start-time": "79167425",
        #            "end-time": "79167425",
        #            "packet-count": "1",
        #            "byte-count": "84",
        #        }]
        #    }
        #}

        for entry in out['services-accounting-information']\
            ['flow-aggregate-template-detail']['flow-aggregate-template-detail-ipv4']\
            ['detail-entry']:

            passflag=True
            entry = Dq(entry)
            if expected_source_address and \
                entry.get_values('source-address', 0) != str(expected_source_address):
                passflag = False
            if expected_destination_address and \
                entry.get_values('destination-address', 0) != str(expected_destination_address):
                passflag = False
            if expected_snmp_interface and \
                entry.get_values('input-snmp-interface-index', 0) != str(expected_snmp_interface):
                passflag = False
            if expected_mpls_label1 and \
                entry.get_values('mpls-label-1', 0) != str(expected_mpls_label1):
                passflag = False
            if expected_mpls_label2 and \
                entry.get_values('mpls-label-2', 0) != str(expected_mpls_label2):
                passflag = False

            if (expected_source_address or expected_destination_address or expected_snmp_interface or expected_mpls_label1 or expected_mpls_label2) and passflag:
                return True

        timeout.sleep()

    return False


def verify_services_accounting_status_no_output(device, max_time=60, check_interval=10):
    """ Verify no output in 'show services accounting status'

    Args:
        device (obj): Device object
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:  
        Boolean

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show services accounting status')
        except SchemaEmptyParserError:
            return True
        
        #"status-information": [
        #    {
        #        "interface-name": "ms-9/0/0",
        #        "status-export-format": "9",
        #        "status-route-record-count": "902244",
        #        "status-ifl-snmp-map-count": "296",
        #        "status-as-count": "0",
        #        "status-monitor-config-set": "Yes",
        #        "status-monitor-route-record-set": "No",
        #        "status-monitor-ifl-snmp-set": "Yes",
        #    }

        timeout.sleep()
        continue

    return False


def verify_services_accounting_flow_no_output(device, max_time=60, check_interval=10):
    """ Verify no output in 'show services accounting flow'

    Args:
        device (obj): Device object
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:  
        Boolean

    Raises:
        N/A
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show services accounting flow')
        except SchemaEmptyParserError:
            return True
        
        #"status-information": [
        #    {
        #        "interface-name": "ms-9/0/0",
        #        "status-export-format": "9",
        #        "status-route-record-count": "902244",
        #        "status-ifl-snmp-map-count": "296",
        #        "status-as-count": "0",
        #        "status-monitor-config-set": "Yes",
        #        "status-monitor-route-record-set": "No",
        #        "status-monitor-ifl-snmp-set": "Yes",
        #    }

        timeout.sleep()
        continue

    return False
