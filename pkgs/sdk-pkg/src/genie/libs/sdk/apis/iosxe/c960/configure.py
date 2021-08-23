"""Common configure functions for flow exporter"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_flow_record(
    device,
    record_name,
    match_ipv4_field_1,
    match_flow_field='direction',
    match_int_field='input',
    match_ipv4_field_2='tos',
    match_transport_field_1='destination-port',
    match_transport_field_2='source-port',
    collect_counter_bytes='True',
    collect_counter_packets='True',
    collect_int_field='output',
    ):
    
    """ Config Flow Record on Device
        Args:
            device (`obj`): Device object
            record_name (`str`): Flow record name
            match_ipv4_field_1 ('str'): First IPv4 field to be configured
            match_flow_field ('str'): Flow field to be configured
            match_int_field ('str'): Interface field to be configured
            match_ipv4_field_2 ('str'): Second IPv4 field to be configured
            match_transport_field_1 ('str'): First transport field to be configured
            match_transport_field_2 ('str'): Second transport field to be configured
            collect_counter_bytes ('bool'): Enable counter field bytes
            collect_counter_packets ('bool'): Enable counter field packets
            collect_int_field ('str'): Collect interface field to be configured
            
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed configuring Flow Record on Device
    """
    
    try:
        device.configure([
                'flow record {record_name}'.format(record_name=record_name),
                'match flow {match_flow_field}'.format(match_flow_field=match_flow_field),
                'match interface {match_int_field}'.format(match_int_field=match_int_field),
                'match ipv4 destination address',
                'match ipv4 {match_ipv4_field_1}'.format(match_ipv4_field_1=match_ipv4_field_1),
                'match ipv4 source address',
                'match ipv4 {match_ipv4_field_2}'.format(match_ipv4_field_2=match_ipv4_field_2),
                'match routing vrf input',
                'match transport {match_transport_field_1}'.format(match_transport_field_1=match_transport_field_1),
                'match transport {match_transport_field_2}'.format(match_transport_field_2=match_transport_field_2),
                'collect interface {collect_int_field}'.format(collect_int_field=collect_int_field),
                'collect routing source as peer 4-octet',
                'collect routing destination as peer 4-octet',
                'collect transport tcp flags',
                ])

        if collect_counter_bytes:
            device.configure([
                                  'flow record {record_name}'.format(record_name=record_name), 
                                  'collect counter bytes'
                                  ])

        if collect_counter_packets:
            device.configure([
                                  'flow record {record_name}'.format(record_name=record_name),
                                  'collect counter packets'
                                  ])
                
    except SubCommandFailure:
        raise SubCommandFailure('Could not configure flow record {record_name}'.format(record_name=record_name))


def configure_flow_monitor(device, monitor_name, exporter_name, record_name,
                        timeout):
    """ Config Flow Monitor on Device
        Args:
            device (`obj`): Device object
            monitor_name (`str`): Flow Monitor name
            exporter_name (`str`): Flow exporter name
            record_name (`str`): Flow record name
            timeout ('int'): Timeout
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring flow monitor
    """
    
    try:
        device.configure([
                          "flow monitor {monitor_name}".
                          format(monitor_name=monitor_name),
                          "exporter {exporter_name}".
                          format(exporter_name=exporter_name),
                          "cache timeout inactive {timeout}".
                          format(timeout=timeout),
                          "cache timeout active {timeout}".
                          format(timeout=timeout),
                          "record {record_name}".
                          format(record_name=record_name)
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
               'Could not configure flow monitor {monitor_name}'.
               format(monitor_name=monitor_name)
        )

