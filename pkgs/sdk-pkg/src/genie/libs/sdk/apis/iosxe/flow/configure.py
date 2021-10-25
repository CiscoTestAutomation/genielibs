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
