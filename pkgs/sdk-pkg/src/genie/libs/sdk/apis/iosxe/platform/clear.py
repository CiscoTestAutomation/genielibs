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


def clear_ip_arp(device,ip):
    """ clear ip arp
        Args:
            device ('obj'): device to execute on
            ip ('int'): A.B.C.D  IP address of dynamic ARP entry
        Return:
            None
        Raises:
            SubCommandFailure
    """
    log.info("clear ip arp {ip} {device}".format(device=device.name,ip=ip))
    cmd = "clear ip arp {ip}".format(ip=ip)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not clear ip arp {device}, Error: {error}'.format(
                device=device.name, error=e
            )
        )

def platform_software_fed_punt_cpuq_clear(device, state=None):
    """ show platform software fed active punt cpuq clear
        Args:
            device ('obj'): Device object
            state (str, optional): Switch state active or standby
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("show platform software fed active punt cpuq clear {device}".format(device=device))

    if state:
        cmd = f'show platform software fed switch {state} punt cpuq clear'
    else:
        cmd = 'show platform software fed active punt cpuq clear'
    try:
        device.execute(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear cpuq punt counters on {device}. Error:\n{error}".format(device=device, error=e)
        )

def clear_active_punt_ios_cause(device, state=None):
    """ show platform software fed switch active punt ios-cause clear
        Args:
            device ('obj'): Device object
            state (str, optional): Switch state active or standby
        Return:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("show platform software fed switch active punt ios-cause clear")
    
    if state:
        cmd = f'show platform software fed switch {state} punt ios-cause clear'
    else:
        cmd = 'show platform software fed active punt ios-cause clear'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not clear punt ios-cause on {device}. Error:\n{error}'.format(device=device.name, error=e)
        )
        
def clear_platform_qos_statistics_iif_id(device, state, iif_id, switch=None):
    """ clear platform hardware qos statistics internal cpu policer
        Args:
            device ('obj'): Device object
            state ('str'): Switch state active or standby
            switch ('str', optional): Switch string
            iif_id('int'): iif id (1-4294967295)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"clear platform hardware fed switch qos statistics iif_id on {device}")
	
    command = f"clear platform hardware fed {state} qos statistics iif_id {iif_id}" 
    if switch:
        command = f"clear platform hardware fed {switch} {state} qos statistics iif_id {iif_id}"

    try:
        device.execute(command)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clear qos statistics iif_id on {device}. Error:\n{error}".format(device=device, error=e)
        )
        