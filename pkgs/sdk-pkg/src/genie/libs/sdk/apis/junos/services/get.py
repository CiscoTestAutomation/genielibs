"""Common get functions for services"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_services_accounting_flow_exported(device):
    """ Get services accounting flow exported flows

    Args:
        device (obj): Device obj
    """

    try:
        out = device.parse('show services accounting flow')
    except SchemaEmptyParserError:
        return None
    
    # "services-accounting-information": {
    #     "flow-information": [
    #         {
    #             "flows-exported": '0',

    return out.q.get_values('flows-exported', 0) or None


def get_services_accounting_flow_active(device):
    """ Get services accounting flow active flows

    Args:
        device (obj): Device obj
    """

    try:
        out = device.parse('show services accounting flow')
    except SchemaEmptyParserError:
        return None
    
    # "services-accounting-information": {
    #     "flow-information": [
    #         {
    #             "active-flows": '0',

    return out.q.get_values('active-flows', 0) or None

def get_services_accounting_flow_expired(device):
    """ Get services accounting flow expired flows

    Args:
        device (obj): Device obj
    """

    try:
        out = device.parse('show services accounting flow')
    except SchemaEmptyParserError:
        return None
    
    # "services-accounting-information": {
    #     "flow-information": [
    #         {
    #             "flows-expired": '0',

    return out.q.get_values('flows-expired', 0) or None

def get_services_accounting_usage_five_second_load(device):
    """ Get services accounting usage five-second-load

        Args:
            device (`obj`): Device object
        Returns:
            One minute load value
    """

    try:
        out = device.parse('show services accounting usage')
    except SchemaEmptyParserError:
        return None
    
    # Example dictionary structure:
    # {'services-accounting-information': 
    #   {'usage-information': [{
    #       'interface-name': 'ex-9/0/0',
    #       'uptime': '79203479',
    #       'inttime': '0',
    #       'five-second-load': '1',
    #       'one-minute-load': '1'}]}}
    five_second_load = out.q.get_values('five-second-load', 0)
    if five_second_load:
        five_second_load = int(five_second_load)
    return five_second_load or None

def get_services_accounting_usage_one_minute_load(device):
    """ Get services accounting usage one-min-load

        Args:
            device (`obj`): Device object
        Returns:
            One minute load value
    """

    try:
        out = device.parse('show services accounting usage')
    except SchemaEmptyParserError:
        return None
    
    # Example dictionary structure:
    # {'services-accounting-information': {
    #    'usage-information': [{
    #       'interface-name': 'ex-9/0/0',
    #       'uptime': '79203479',
    #       'inttime': '0',
    #       'five-second-load': '1',
    #       'one-minute-load': '1'}]}}
    one_min_load = out.q.get_values('one-minute-load', 0)
    if one_min_load:
        one_min_load = int(one_min_load)
    return one_min_load or None


def get_services_accounting_flow_packets(device, criteria='flow-packets'):
    """ Get criteria from show services accounting flow

        Args:
            device (`obj`): Device object
            criteria ('str'): Criteria to return from show command
        Returns:
            flow packet value
    """

    try:
        out = device.parse('show services accounting flow')
    except SchemaEmptyParserError:
        return None
    
    # Example dictionary structure:
    #"flow-information": [
    #        {
    #            "interface-name": "ms-9/0/0",
    #            "local-ifd-index": "140",
    #            "flow-packets": "0",
    #            "flow-bytes": "0",
    #            "flow-packets-ten-second-rate": "0",
    #            "flow-bytes-ten-second-rate": "0",
    #            "active-flows": "0",
    #            "flows": "0",
    #            "flows-exported": "0",
    #            "flow-packets-exported": "9",
    #            "flows-expired": "0",
    #            "flows-aged": "0",
    #        }
    #    ]
    return out.q.get_values(criteria, 0)


def get_services_accounting_memory(device):
    """ Get services accounting memory

        Args:
            device (`obj`): Device object
        Returns:
            One minute load value
    """

    try:
        out = device.parse('show services accounting memory')
    except SchemaEmptyParserError:
        return None
    
    # Example dictionary structure:
    #"memory-information": [
    #        {
    #            "interface-name": "ms-9/0/0",
    #            "allocation-count": "1",
    #            "free-count": "0",
    #            "allocations-per-second": "0",
    #            "frees-per-second": "0",
    #            "memory-used": "862529184",
    #            "memory-free": "3164002312",
    #            "v9-memory-used": "48",
    #       }
    total_memory_used = out.q.get_values('memory-used', 0)
    if total_memory_used:
        return total_memory_used
    else:
        return None
        

def get_services_accounting_status(device, field, output=None):
    """ Get value of field from show services accounting status

        Args:
            device (`obj`): Device object
            field (`str`): field name in show output
            output (`str`): output of show services accounting status
        Returns:
            value (`str`): value of field
    """

    try:
        out = device.parse('show services accounting status', output=output)
    except SchemaEmptyParserError:
        return None

    # example of out
    # {
    #   "services-accounting-information": {
    #     "status-information": [
    #       {
    #         "interface-name": "ms-9/2/0",
    #         "status-as-count": "522533",
    #         "status-export-format": "9",
    #         "status-ifl-snmp-map-count": "49",
    #         "status-monitor-config-set": "Yes",
    #         "status-monitor-ifl-snmp-set": "Yes",
    #         "status-monitor-route-record-set": "Yes",
    #         "status-route-record-count": "1203181"
    #       }
    #     ]
    #   }
    # }
    field_value = out.q.get_values(field, 0)
    if field_value:
        return field_value
    else:
        return None


def get_services_accounting_flow(device, field, output=None):
    """ Get value of field from show services accounting flow

        Args:
            device (`obj`): Device object
            field (`str`): field name in show output
            output (`str`): output of show services accounting flow
        Returns:
            value (`str`): value of field
    """

    try:
        out = device.parse('show services accounting flow', output=output)
    except SchemaEmptyParserError:
        return None

    # example of out
    # {
    #   "services-accounting-information": {
    #     "flow-information": [
    #       {
    #         "active-flows": "9382",
    #         "flow-bytes": "11593270057235",
    #         "flow-bytes-ten-second-rate": "181450",
    #         "flow-packets": "13718715979",
    #         "flow-packets-exported": "972808092",
    #         "flow-packets-ten-second-rate": "231",
    #         "flows": "8130313171",
    #         "flows-aged": "8780965870",
    #         "flows-expired": "8130303789",
    #         "flows-exported": "8960674930",
    #         "interface-name": "ms-9/2/0",
    #         "local-ifd-index": "168"
    #       }
    #     ]
    #   }
    # }
    field_value = out.q.get_values(field, 0)
    if field_value:
        return field_value
    else:
        return None


def get_services_accounting_errors(device, field, output=None):
    """ Get value of field from show services accounting errors

        Args:
            device (`obj`): Device object
            field (`str`): field name in show output
            output (`str`): output of show services accounting errors
        Returns:
            value (`str`): value of field
    """

    try:
        out = device.parse('show services accounting errors', output=output)
    except SchemaEmptyParserError:
        return None

    # example of out
    # {
    #   "services-accounting-information": {
    #     "v9-error-information": [
    #       {
    #         "active-timeout-failures": "0",
    #         "export-packet-failures": "0",
    #         "flow-creation-failures": "0",
    #         "interface-name": "ms-9/2/0",
    #         "memory-overload": "No",
    #         "service-set-dropped": "0"
    #       }
    #     ]
    #   }
    # }
    field_value = out.q.get_values(field, 0)
    if field_value:
        return field_value
    else:
        return None


def get_services_accounting_aggregation_template_field(device,
                                                       template_name,
                                                       field,
                                                       source=None,
                                                       destination=None,
                                                       output=None):
    """ Get value of field from show service accounting aggregation template template-name {template-name} extensive

        Args:
            device (`obj`): Device object
            source (`str`, Optional): source address. Default to None
            destination (`str`, Optional): destination address. Default to None
            template_name (`str`): template name
            field (`str`): field name in show output
            output (`str`): output of show services accounting errors
        Returns:
            value (`str`): value of field
    """

    try:
        out = device.parse(
            'show services accounting aggregation template template-name {tn} extensive'
            .format(tn=template_name),
            output=output)
    except SchemaEmptyParserError:
        return None

    # example of out
    # {
    #   "services-accounting-information": {
    #     "flow-aggregate-template-detail": {
    #       "flow-aggregate-template-detail-ipv4": {
    #         "detail-entry": {
    #           "byte-count": "84",
    #           "destination-address": "200.0.0.1",
    #           "destination-mask": "30",
    #           "destination-port": "0",
    #           "end-time": "9823611",
    #           "input-snmp-interface-index": "1014",
    #           "output-snmp-interface-index": "624",
    #           "packet-count": "1",
    #           "protocol": {
    #             "#text": "1"
    #           },
    #           "source-address": "100.0.0.1",
    #           "source-mask": "30",
    #           "source-port": "8",
    #           "start-time": "9823611",
    #           "tcp-flags": "0",
    #           "tos": "0"
    #         }
    #       }
    #     }
    #   }
    # }
    entry = out['services-accounting-information'][
        'flow-aggregate-template-detail'][
            'flow-aggregate-template-detail-ipv4']['detail-entry']

    if source and destination:
        if entry['source-address'] == source and entry[
                'destination-address'] == destination:
            if field in entry:
                return entry[field]
            else:
                return None
    elif source:
        if entry['source-address'] == source:
            if field in entry:
                return entry[field]
            else:
                return None
    elif destination:
        if entry['destination-address'] == destination:
            if field in entry:
                return entry[field]
            else:
                return None
    else:
        if field in entry:
            return entry[field]
        else:
            return None
    return None
