"""Common configure functions for OSPF"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_ospf_passive_interface(device, interface, area):
    """configure passive interface

        Args:
            device (`obj`): Device object
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
            area (`str`): IP address of area

        Returns:
            None
        
        Raise:
            SubCommandFailure
    """
    config = []
    config.append(
        "set protocols ospf area {} interface "
        "{} passive\n".format(area, interface)
    )

    try:
        device.configure("".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure passive on {interface}. Error:\n{error}".format(
                interface=interface, error=e
            )
        )


def configure_ospf_interface_metric_cost(device, interface, area, cost, cost_type='ospf'):
    """ Configure ospf interface metric cost

        Args:
            device ('obj'): Device to configure
            interface ('str'): Interface to configure
            area ('str'): Area
            cost_type ('str'): Cost type
            cost ('int'): Cost
    """
    if 'ospf' in cost_type.lower():
        config = 'set protocols ospf area {area} interface {interface} metric {cost}'.format(
            area=area, interface=interface, cost=cost
        )
    elif 'te' in cost_type.lower():
        config = 'set protocols ospf area {area} interface {interface} te-metric {cost}'.format(
            area=area, interface=interface, cost=cost
        )
    else:
        raise SubCommandFailure('Cost type {cost} not supported by api'.format(cost=cost))

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure cost {cost}. Error:\n{error}".format(
                cost=cost, error=e
            )
        )

def clear_ospf_trace_log(device, ospf_trace_log):
    """
    Clear log ospf_trace_log

    Args:
        device (`obj`): Device object
        ospf_trace_log(`str`): OSPF trace log

    Returns:
        None
    """
    log.info(
        f"Clearing log {ospf_trace_log}"
    )

    try:
        device.execute(
            f"clear log {ospf_trace_log}"
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not clear log on {ospf_trace_log}. Error:\n{e}")