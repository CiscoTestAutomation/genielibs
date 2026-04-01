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


def configure_flow_record_parameters(
    device,
    record_name,
    match_flow_field=None,
    match_interface_field=None,
    match_ipv4_src_address=None,
    match_ipv4_dst_address=None,
    match_ipv4_field=None,
    match_routing_field=None,
    match_transport_fields=None,
    collect_interface_field=None,
    collect_routing_fields=None,
    collect_transport_field=None,
    collect_counter_bytes=None,
    collect_counter_packets=None,
    ):
    """ Configure individual parameters under a flow record on Device.
        Only the provided (non-None) parameters will be configured.
        Args:
            device ('obj'): Device object
            record_name ('str'): Flow record name
            match_flow_field ('str', optional): Flow field to match.
                Ex: 'direction'. Default is None.
            match_interface_field ('str', optional): Interface direction to match.
                Ex: 'input'. Default is None.
            match_ipv4_src_address ('bool', optional): Configure 'match ipv4 source address'
                when set to True. Default is None.
            match_ipv4_dst_address ('bool', optional): Configure 'match ipv4 destination address'
                when set to True. Default is None.
            match_ipv4_field ('str', optional): Additional ipv4 field to match.
                Ex: 'protocol', 'tos'. Default is None.
            match_routing_field ('str', optional): Routing field to match.
                Ex: 'vrf input'. Default is None.
            match_transport_fields ('list', optional): List of transport fields to match.
                Ex: ['destination-port', 'source-port']. Default is None.
            collect_interface_field ('str', optional): Interface direction to collect.
                Ex: 'output'. Default is None.
            collect_routing_fields ('list', optional): List of routing fields to collect.
                Ex: ['source as peer 4-octet', 'destination as peer 4-octet']. Default is None.
            collect_transport_field ('str', optional): Transport field to collect.
                Ex: 'tcp flags'. Default is None.
            collect_counter_bytes ('bool', optional): Configure 'collect counter bytes'
                when set to True. Default is None.
            collect_counter_packets ('bool', optional): Configure 'collect counter packets'
                when set to True. Default is None.
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring flow record parameters on Device
    """
    config = [f'flow record {record_name}']

    if match_flow_field is not None:
        config.append(f'match flow {match_flow_field}')

    if match_interface_field is not None:
        config.append(f'match interface {match_interface_field}')

    if match_ipv4_dst_address:
        config.append('match ipv4 destination address')

    if match_ipv4_src_address:
        config.append('match ipv4 source address')

    if match_ipv4_field is not None:
        config.append(f'match ipv4 {match_ipv4_field}')

    if match_routing_field is not None:
        config.append(f'match routing {match_routing_field}')

    if match_transport_fields is not None:
        for field in match_transport_fields:
            config.append(f'match transport {field}')

    if collect_interface_field is not None:
        config.append(f'collect interface {collect_interface_field}')

    if collect_routing_fields is not None:
        for field in collect_routing_fields:
            config.append(f'collect routing {field}')

    if collect_transport_field is not None:
        config.append(f'collect transport {collect_transport_field}')

    if collect_counter_bytes:
        config.append('collect counter bytes')

    if collect_counter_packets:
        config.append('collect counter packets')

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Could not configure flow record {record_name}. Error:\n{e}')
