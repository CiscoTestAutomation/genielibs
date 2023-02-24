"""Common clear functions"""
import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def clear_platform_qos_statistics_internal_cpu_policer(device, state=None, switch_num=None):
    """ clear platform hardware qos statistics internal cpu policer
        Args:
            device (`obj`): Device object
            state (str, optional): Switch state active or standby
            switch_num(str, optional): switch number 1 or 2 or 3 ..
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("clear platform hardware qos statistics internal cpu policer on {device}".format(device=device))
    try:
        if state:
            device.execute('clear platform hardware fed switch {state} qos statistics internal cpu policer'.format(state=state))
        elif switch_num:
            device.execute('clear platform hardware fed switch {switch_num} qos statistics internal cpu policer'.format(switch_num=switch_num))
        else:
            device.execute('clear platform hardware fed active qos statistics internal cpu policer')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear qos statistics on {device}. Error:\n{error}".format(device=device, error=e)
        )

def clear_platform_qos_dscp_cos_counters_interface(device, intf, state=None, switch_num=None):
    """ clear platform hardware fed switch active qos dscp-cos counters interface
        Args:
            device (`obj`): Device object
            intf (str): interafce name to clear qos dscp-cos counters
            state (str, optional): Switch state active or standby
            switch_num(str, optional): switch number 1 or 2 or 3 ..
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("clear platform hardware fed switch active qos dscp-cos counters interface on {device}".format(device=device))
    try:
        if state:
            device.execute('clear platform hardware fed switch {state} qos dscp-cos counters interface {intf}'.format(state=state,intf=intf))
        elif switch_num:
            device.execute('clear platform hardware fed switch {switch_num} qos dscp-cos counters interface {intf}'.format(switch_num=switch_num,intf=intf))            
        else:
            device.execute('clear platform hardware fed active qos dscp-cos counters interface {intf}'.format(intf=intf))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear qos dscp-cos counters on {device}. Error:\n{error}".format(device=device, error=e)
        )
