"""Common configure functions for flow exporter"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def config_flow_exporter(device, exporter_name, monitor_name, dest_ip, udp_port):
    """ Config Flow Exporter on Device

        Args:
            device (`obj`): Device object
            exporter_name (`str`): Flow exporter name
            monitor_name (`str`): Flow monitor name
            dest_ip (`str`): Destination IP
            udp_port (`str`): UDP port
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure([
                          "et-analytics",
                          "ip flow-export destination {dest_ip} {udp_port}".format(dest_ip=dest_ip,udp_port=udp_port),
                          "flow exporter {exporter_name}".format(exporter_name=exporter_name),
                          "destination {dest_ip}".format(dest_ip=dest_ip),
                          "transport udp {udp_port}".format(udp_port=udp_port),
                          "flow exporter {monitor_name}".format(monitor_name=monitor_name),
                          "flow monitor {exporter_name}".format(exporter_name=exporter_name),
                          "exporter {exporter_name}".format(exporter_name=exporter_name),
                          "record netflow ipv4 app-client-server-stats",
                          "flow monitor {monitor_name}".format(monitor_name=monitor_name),
                          "exporter {monitor_name}".format(monitor_name=monitor_name),
                          "record {monitor_name}".format(monitor_name=monitor_name)
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure flow exporter {exporter_name}'.format(exporter_name=exporter_name)
        )

def unconfig_flow_exporter(device, exporter_name, monitor_name):
    """ Unconfigures Flow Exporter on Device

        Args:
            device (`obj`): Device object
            exporter_name (`str`): Flow exporter name
            monitor_name (`str`): Flow monitor name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure(["no flow monitor {monitor_name}".format(monitor_name=monitor_name),
                          "no flow monitor {exporter_name}".format(exporter_name=exporter_name),
                          "no flow exporter {exporter_name}".format(exporter_name=exporter_name),
                          "no et-analytics"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure flow exporter {exporter_name} and flow monitor {monitor_name}'.format(exporter_name=exporter_name,monitor_name=monitor_name)
        )


def config_flow_monitor_on_interface(device, interface, exporter_name):
    """ Config Flow Monitor on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            exporter_name (`str`): Flow exporter name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.configure([
                          "interface {interface}".format(interface=interface),
                          "et-analytics enable",
                          "ip flow monitor {exporter_name} input".format(exporter_name=exporter_name),
                          "ip flow monitor {exporter_name} output".format(exporter_name=exporter_name)])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure flow monitor {exporter_name} on interface {interface}'.format(exporter_name=exporter_name, 
                 interface=interface)
        )


def clear_flow_monitor_statistics(device):
    """ Clears Flow Monitor statistics on device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        device.execute(["clear flow monitor eta-mon cache",
                        "clear flow monitor eta-mon statistics",
                        "clear flow monitor avc cache",
                        "clear flow monitor avc statistics",
                        "show platform software fed active fnf clear-et-analytics-stats"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not clear flow monitor statistics'
        )

def configure_fnf_exporter(device, exporter_name, dest_ip, source_int,
                           udp_port, timeout):
    
    """ Config Flow Exporter on Device 
        Args:
            device (`obj`): Device object
            exporter_name (`str`): Flow exporter name
            dest_ip (`str`): Destination IP
            source_int('str'): Interface
            udp_port (`str`): UDP port
            timeout ('int'): Timeout
            
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed configuring fnf exporter
    """
    try:
        device.configure([
                          "flow exporter {exporter_name}".
                          format(exporter_name=exporter_name),
                          "destination {dest_ip}".format(dest_ip=dest_ip),
                          "source {int}".format(int=source_int),
                          "transport udp {udp_port}".format(udp_port=udp_port),
                          "template data timeout {timeout}".
                          format(timeout=timeout),
                          "option vrf-table timeout {timeout}".
                          format(timeout=timeout),
                          "option sampler-table timeout {timeout}".
                          format(timeout=timeout),
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
                'Could not configure fnf exporter {exporter_name}'.
                format(exporter_name=exporter_name)
        )

def unconfigure_flow_exporter_monitor_record(device, exporter_name, monitor_name,
                                          record_name):
    
    """ Unconfigures Flow Exporter,Monitor and Record on Device
        Args:
            device (`obj`): Device object
            exporter_name (`str`): Flow exporter name
            monitor_name (`str`): Flow monitor name
            record_name (`str`): Flow record name
            
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed unconfiguring Flow Exporter,monitor,record
    """

    try:
        device.configure(["no flow monitor {monitor_name}".
                           format(monitor_name=monitor_name),
                          "no flow exporter {exporter_name}".
                           format(exporter_name=exporter_name),
                          "no flow record {record_name}".
                           format(record_name=record_name)
                        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure flow exporter {exporter_name} and flow'
            'monitor {monitor_name} and flow record {record_name}'.
            format(exporter_name=exporter_name, monitor_name=monitor_name,
                   record_name=record_name)
        )

def configure_fnf_monitor_on_interface(device, interface, monitor_name, direction):
    
    """ Config Fnf Monitor on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            monitor_name (`str`): Flow monitor name
            direction ('str'): Direction of monitor (input/output)
            
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed configuring interface with flow monitor
    """

    try:
        device.configure([
                          "interface {interface}".format(interface=interface),
                          "ip flow monitor {monitor_name} {direction}".
                          format(monitor_name=monitor_name, direction=direction)])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not configure fnf monitor {monitor_name} on'
            'interface {interface}'.format(monitor_name=monitor_name,
                                          interface=interface)
        )


def unconfigure_fnf_monitor_on_interface(device, interface, monitor_name):
    """ Unconfig Flow Monitor on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be unconfigured
            monitor_name (`str`): Flow monitor name
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring interface with flow monitor
    """

    try:
        device.configure([
                          "interface {interface}".format(interface=interface),
                          "no ip flow monitor {monitor_name} input".
                          format(monitor_name=monitor_name)])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not unconfigure flow monitor {monitor_name} on'
            'interface {interface}'.format(monitor_name=monitor_name,
                                          interface=interface)
        )
       
def clear_flow_monitor(device, name, option=''):
    """ clear flow monitor data
        Args:
            device (`obj`):           Device object
            name ('str'):             Name of the flow (eg: created[ipv4_input] or user defined[monitor_ipv4_out])
            option ('str', optional): Which data to clear. Default will clear all flow monitor info or
                                      can give perticular option to clear eg:cache/statistics
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Clear flow monitor data on {device}".format(device=device))

    try:
        device.execute('clear flow monitor {name} {option}'.format(name=name,option=option))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear flow monitor data on {device}. Error:\n{error}".format(device=device, error=e)
        )


def configure_sampler(device, sampler_name, mode, num_packet, select_packet):
    
    """ Config Sampler
        Args:
            device (`obj`): Device object
            sampler_name (`str`): Name of sampler 
            mode (`str`): Mode to be configured
            num_packet ('int'): number of packets to select per window
            select_packet ('int'): Select M packets out of an N packet window
            
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed configuring Sampler
    """

    try:
        device.configure([
                          f"sampler {sampler_name}",
                          f"mode {mode} {num_packet} out-of {select_packet}"
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not configure sampler {sampler_name}'
            )
        

def unconfigure_sampler(device, sampler_name):
    
    """ Unconfig Sampler
        Args:
            device (`obj`): Device object
            sampler_name (`str`): Name of sampler 
                        
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed unconfiguring Sampler
    """

    try:
        device.configure([
                          f"no sampler {sampler_name}",
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not unconfigure sampler {sampler_name}'
            )   


def configure_fnf_monitor_sampler_interface(device, interface, monitor_name, sampler_name, direction):
    
    """ Config Fnf Monitor on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            monitor_name (`str`): Flow monitor name
            sampler_name ('str'): Sampler name
            direction ('str'): Direction of monitor (input/output)
            
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed configuring interface flow monitor with sampler
    """

    try:
        device.configure([
                          f"interface {interface}",
                          f"ip flow monitor {monitor_name} sampler {sampler_name} {direction}"
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not configure fnf monitor {monitor_name} with sampler {sampler_name} on'
            'interface {interface}'
        )


def configure_fnf_monitor_datalink_interface(device, interface, monitor_name, sampler_name, direction):
    
    """ Config Datalink Fnf Monitor on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            monitor_name (`str`): Flow monitor name
            sampler_name ('str'): Sampler name
            direction ('str'): Direction of monitor (input/output)
            
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed configuring interface datalink flow monitor with sampler
    """

    try:
        device.configure([
                          f"interface {interface}",
                          f"datalink flow monitor {monitor_name} sampler {sampler_name} {direction}"
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not configure datalink fnf monitor {monitor_name} with sampler {sampler_name} on'
            'interface {interface}'
        )


def unconfigure_fnf_monitor_datalink_interface(device, interface, monitor_name):
    
    """ Unconfig Datalink Fnf Monitor on Interface
        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
            monitor_name (`str`): Flow monitor name
                        
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed unconfiguring interface datalink flow monitor with sampler
    """

    try:
        device.configure([
                          f"interface {interface}",
                          f"no datalink flow monitor {monitor_name}"
                          ])

    except SubCommandFailure:
        raise SubCommandFailure(
            f'Could not unconfigure datalink fnf monitor {monitor_name} on'
            'interface {interface}'
        )


def configure_flow_monitor_cache_entry(device, monitor_name, record_name,
                        timeout, cache_entries):
    """ Config Flow Monitor with cache entry on Device
        Args:
            device (`obj`): Device object
            monitor_name (`str`): Flow Monitor name
            record_name (`str`): Flow record name
            timeout ('int'): Timeout
            cache_entries ('int'): Number of cache entries

        Return:
            None

        Raise:
            SubCommandFailure: Failed configuring flow monitor with cache entry 
    """
    
        
    try:
            device.configure([
                          f"flow monitor {monitor_name}",
                          f"cache timeout inactive {timeout}",
                          f"cache timeout active {timeout}",
                          f"cache entries {cache_entries}",
                          f"record {record_name}",
                          ])

    except SubCommandFailure:
            raise SubCommandFailure(
               f'Could not configure flow monitor {monitor_name} with cache entry'
            )


def unconfigure_flow_monitor(device, monitor_name):
    """ Unconfig Flow Monitor on Device
        Args:
            device (`obj`): Device object
            monitor_name (`str`): Flow Monitor name
                        
        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring flow monitor
    """
    
    try:
            device.configure([
                          f"no flow monitor {monitor_name}",
                            ])

    except SubCommandFailure:
            raise SubCommandFailure(
               f'Could not unconfigure flow monitor {monitor_name}'
            )           


def configure_fnf_record(
    device,
    record_name,
    match_ipv4_field_1,
    match_flow_field=None,
    match_int_field=None,
    match_ipv4_field_2=None,
    match_transport_field_1='destination-port',
    match_transport_field_2='source-port',
    collect_counter_bytes=True,
    collect_counter_packets=True,
    collect_int_field=None,
    datalink=False,
    collect_routing=True,
    datalink_type_1=None,
    datalink_type_2=None,
    datalink_subtype_1=None,
    datalink_subtype_2=None,
    address_type=None,
    collect_timestamp=False
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
            datalink ('bool') : Configure datalink fields
            collect_routing ('bool'): Configure routing attributes
            datalink_type_1 ('str'): First Datalink Type to be configured
            datalink_type_2 ('str'): Second datalink Type to be configure
            datalink_subtype_1 ('str'): First datalink subtype to be configured
            datalink_subtype_2 ('str'): Second datalink subtype to be configured
            address_type ('str'): Address type to be configured
            collect_timestamp ('bool'): Configure timestamp fields
            
        Return:
            None
            
        Raise:
            SubCommandFailure: Failed configuring Flow Record on Device
    """
    
    configs = [f'flow record {record_name}']
    if datalink :
        configs.extend([f'match datalink {datalink_type_1} {datalink_subtype_1} address {address_type}',
                        f'match datalink {datalink_type_1} {datalink_subtype_2} address {address_type}',
                        f'match datalink {datalink_type_2}'])
    
    if match_flow_field is not None:
                    configs.extend(f'match flow {match_flow_field}')
    if match_int_field is not None:
                    configs.extend(f'match interface {match_int_field}')
    if match_ipv4_field_2 is not None:
                    configs.extend(f'match ipv4 {match_ipv4_field_2}')
    if collect_routing :
                    configs.extend(['collect routing source as peer 4-octet',
                                  'collect routing destination as peer 4-octet'])
    if collect_counter_bytes:
                    configs.extend(['collect counter bytes long'])
    if collect_counter_packets:
                    configs.extend(['collect counter packets long'])
    if collect_timestamp :
                    configs.extend(['collect timestamp sys-uptime first',
                                   'collect timestamp sys-uptime last'])                      
                                     
    try:
        device.configure(configs)
        device.configure([f'flow record {record_name}',     
                'match ipv4 destination address',
                f'match ipv4 {match_ipv4_field_1}',
                'match ipv4 source address',
                'match routing vrf input',
                f'match transport {match_transport_field_1}',
                f'match transport {match_transport_field_2}',
                f'collect interface {collect_int_field}',
                'collect transport tcp flags',
                ])
             
    except SubCommandFailure:
        raise SubCommandFailure('Could not configure flow record {record_name}'.format(record_name=record_name))


def unconfigure_flow_record(device, record_name):
    """ Unconfig Flow Monitor on Device
        Args:
            device (`obj`): Device object
            record_name (`str`): Flow Record name
                        
        Return:
            None

        Raise:
            SubCommandFailure: Failed unconfiguring flow record
    """
    
    try:
        device.configure([
                      f"no flow record {record_name}",
                        ])

    except SubCommandFailure:
        raise SubCommandFailure(
           f'Could not unconfigure flow record {record_name}'
        )           
