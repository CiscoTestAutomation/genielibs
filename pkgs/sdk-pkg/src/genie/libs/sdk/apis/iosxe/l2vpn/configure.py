"""Common configure functions for bgp"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_l2vpn_storm_control(
    device, interface, service_instance_id, storm_control
):
    """ Configures storm control under service instance

        Args:
            device('obj'): device to configure
            interface('str'): interface name
            service_instance_id:('int'): service instance id
            storm_control('list'): list of storm control configurations
                ex.)
                        [
                            {
                                'traffic_flow': 'unicast',
                                'name': 'cir',
                                'val': 8000
                            },
                            {
                                'traffic_flow': 'broadcast',
                                'name': 'cir',
                                'val': 8000
                            },
                            {
                                'traffic_flow': 'multicast',
                                'name': 'cir',
                                'val': 8000
                            }
                        ]
        Returns:
            N/A
        Raises:
            SubCommandFailure
    """
    log.info(
        "Configuring storm control under service "
        "instance: {} and interface: {}".format(service_instance_id, interface)
    )

    config = []
    config.append("interface {}\n".format(interface))

    config.append("service instance {} ethernet\n".format(service_instance_id))

    for sc in storm_control:
        traffic_flow = sc["traffic_flow"]
        name = sc["name"]
        val = sc["val"]

        config.append(
            "storm-control {} {} {}\n".format(traffic_flow, name, val)
        )
    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Configuration failed for storm control under service "
            "instance: {} and interface: {} with exception: {}".format(
                service_instance_id, interface, str(e)
            )
        )
