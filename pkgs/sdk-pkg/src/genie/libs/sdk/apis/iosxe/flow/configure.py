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

