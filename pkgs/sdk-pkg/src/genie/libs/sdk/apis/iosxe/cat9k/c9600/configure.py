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
    collect_counter_bytes=True,
    collect_counter_packets=True,
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
                          f"flow monitor {monitor_name}",
                          f"exporter {exporter_name}",
                          f"cache timeout inactive {timeout}",
                          f"cache timeout active {timeout}",
                          f"record {record_name}"
                          ])
    except SubCommandFailure:
            raise SubCommandFailure(
               f'Could not configure flow monitor {monitor_name}'
            )

def  configure_mac_address_table_notification_change(device):
    """ Config mac-address-table notification change on Device
        Args:
            device (`obj`): Device object
            
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring flow monitor
    """
    log.info("mac-address-table notification change on device")
    try:
        device.configure("mac-address-table notification change")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure mac-address-table notification change device {device.name}. Error:\n{e}"
            )
            

def  unconfigure_mac_address_table_notification_change(device):
    """ unConfig mac-address-table notification change on Device
        Args:
            device (`obj`): Device object
            
        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring mac-address-table notification change
    """
    log.info("no mac-address-table notification change on device")
    try:
        device.configure("no mac-address-table notification change")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure mac-address-table notification change device {device.name}. Error:\n{e}"
            )

def  configure_datalink_flow_monitor(device, interface, flow_name, direction):
    """ Config datalink flow monitor on Device
        Args:
            device ('obj'): Device object
            interface ('str'): interface
            flow_name ('str'): different flow names.
            direction ('str'): Input or Output direction.
            ex:)
                input    Apply Flow Monitor on input traffic
                output   Apply Flow Monitor on output traffic
                sampler  Optional Sampler to apply to this Flow Monitor
        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring datalink flow monitor
    """

    config = [f'interface {interface}', f'datalink flow monitor {flow_name} {direction}']
    
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure datalink flow monitor m4out device {device.name}. Error:\n{e}")

def  unconfigure_datalink_flow_monitor(device, interface, flow_name, direction):
    """ Unconfigure datalink flow monitor on Device
        Args:
            device ('obj'): Device object
            interface('str'): interface
            flow_name ('str'): different flow names.
            direction ('str'): Input or Output direction.
            ex:)
                input    Apply Flow Monitor on input traffic
                output   Apply Flow Monitor on output traffic
                sampler  Optional Sampler to apply to this Flow Monitor
        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring datalink flow monitor
    """
    config=[f'interface {interface}', f'no datalink flow monitor {flow_name} {direction}']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure datalink flow monitor device {device.name}. Error:\n{e}")
