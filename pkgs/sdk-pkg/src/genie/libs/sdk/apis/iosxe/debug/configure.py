"""Enable debug for mentioned parameters"""

# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def enable_debug(device, parameter):
    """ Enable debug for the mentioned parameter
        Args:
            device ('obj'): device to use
            parameter ('str'): parameter for which debug has to be enabled
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling debug
    """
    log.info(
        "Enabling debug for name={parameter} "
        .format(parameter=parameter)
    )

    try:
        device.execute(
            [
            "debug {parameter}".format(parameter=parameter)
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable debug for {parameter}".format(
                parameter=parameter
            )
         )

def disable_debug(device, parameter):
    """ Disable debug for the mentioned parameter
        Args:
            device ('obj'): device to use
            parameter ('str'): parameter for which debug has to be disabled
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling debug
    """
    log.debug(
        "Disabling debug for name={parameter} "
        .format(parameter=parameter)
    )

    try:
        device.execute(
            "no debug {parameter}".format(parameter=parameter)
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable debug for {parameter}".format(
                parameter=parameter
            )
        )

def set_filter_packet_capture_inject(device, filter):
    """ Set filter for packet capture inject
        Args:
            device (`obj`): Device object
            filter (`str`): Filter to be set

        Return:
            None

        Raise:
            SubCommandFailure: Failed setting filter for packet capture inject
    """

    try:
        device.execute(['debug platform software fed active inject packet-capture '
                          'set-filter "{filter}"'.format(filter=filter)])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not Set filter for packet capture inject'
        )

def start_packet_capture_inject(device):
    """ Start packet capture inject
        Args:
            device (`obj`): Device object

        Return:
            None

        Raise:
            SubCommandFailure: Failed start packet capture inject
    """

    try:
        device.execute(["debug platform software fed active inject packet-capture start"])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not start packet capture inject'
        )

def stop_packet_capture_inject(device):
    """ Stop packet capture inject
        Args:
            device (`obj`): Device object

        Return:
            None

        Raise:
            SubCommandFailure: Failed stop packet capture inject
    """

    try:
        device.execute(["debug platform software fed active inject packet-capture stop"])

    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not stop packet capture inject'
        )

def debug_platform_memory_fed_callsite(
    device, action, switch_num=None, switch_type=None
    ):
    """ debug debug platform software memory fed configuration
        Args:
            device (`obj`): Device object
            action (`str`): action mustbe either start or stop or clear
            switch_num (`str`): Default value None. stack device switch number
            switch_type (`str`): Default value None. switch type is active or standby
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        if switch_num is not None and switch_type is None and action in ['clear', 'start', 'stop']:
            device.execute("debug platform software memory fed switch {switch_num} alloc callsite {action}".format(
                switch_num=switch_num,
                action=action
                ))
        elif switch_type in ['active', 'standby', 'member'] and action in ['clear', 'start', 'stop']:
            device.execute("debug platform software memory fed {switch_type} alloc callsite {action}".format(
                switch_type=switch_type,
                action=action
                ))

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure debug platform software memory fed backtrace commands on {device}. Error:\n{error}".format(device=device, error=e)
        )

def debug_platform_memory_fed_backtrace(
    device, action, switch_num=None, switch_type=None, callsiteid=None, depth=10
    ):
    """ debug debug platform software memory fed backtrace configuration
        Args:
            device (`obj`): Device object
            action (`str`): action mustbe either start or stop or clear
            switch_num (`str`): Default value None. stack device switch number
            switch_type (`str`): Default value None. switch type is active or standby
            callsiteid (`str`): Default value None. option to start particular callsiteid in the CLI
            depth(`str`): Default value is 10.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        if switch_num is not None and switch_type is None and action in ['clear', 'stop']:
            device.execute("debug platform software memory fed switch {switch_num} alloc backtrace {action}".format(
                switch_num=switch_num,
                action=action
                ))
        elif switch_num is not None and switch_type is None and action == 'start' and callsiteid is not None:
            device.execute("debug platform software memory fed switch {switch_num} alloc backtrace {action} {callsiteid} depth {depth}".format(
                switch_num=switch_num,
                action=action,
                callsiteid=callsiteid,
                depth=depth
                ))
        elif switch_type in ['active', 'standby', 'member'] and action in ['clear', 'stop']:
            device.execute("debug platform software memory fed {switch_type} alloc backtrace {action}".format(
                switch_type=switch_type,
                action=action
                ))
        elif switch_type in ['active', 'standby', 'member'] and action == 'start' and callsiteid is not None:
            device.execute("debug platform software memory fed {switch_type} alloc backtrace {action} {callsiteid} depth {depth}".format(
                switch_type=switch_type,
                action=action,
                callsiteid=callsiteid,
                depth=depth
                ))

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure debug platform software memory fed backtrace commands on {device}. Error:\n{error}".format(device=device, error=e)
        )

def enable_debug_ilpower_event(device):
    """ debug ilpower event
        Args:
            device (`obj`): Device object

        Return:
            None

        Raise:
            SubCommandFailure: Failed to enable the debug ilpower event
    """

    try:
        device.execute(["debug ilpower event"])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not execute cli debug ilpower event. Error:\n{error}". format(error=e))

def enable_debug_pdm(device, parameter, enable):
    """ Enable debug for the mentioned parameter
        Args:
            device ('obj'): device to use
            parameter ('str'): parameter for which debug has to be enable for core or steering-policy
            enable ('str'): parameter for which debug has to be enabled
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling debug
    """
    log.debug(
        "Enabling debug for name={parameter} and {enable} "
        .format(parameter=parameter,enable=enable)
    )

    try:
        device.execute(
            "debug pdm {parameter} {enable}".format(parameter=parameter,enable=enable)
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not enable debug for {parameter}".format(
                parameter=parameter
            )
        )

def disable_debug_pdm(device, parameter, disable):
    """ Disable debug for the mentioned parameter
        Args:
            device ('obj'): device to use
            parameter ('str'): parameter for which debug has to be disable for core or steering-policy
            disable ('str'): parameter for which debug has to be disabled
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling debug
    """
    log.debug(
        "Disabling debug for name={parameter} and {disable} "
        .format(parameter=parameter,disable=disable)
    )

    try:
        device.execute(
            "no debug pdm {parameter} {disable}".format(parameter=parameter,disable=disable)
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not disable debug for {parameter}".format(
                parameter=parameter
            )
        )

def debug_vdsl_controller_slot_dump_internal(device, slot, filename='sfp', timeout=900):
    """ Debug cli to dump vdsl controller slot internal

    Args:
        device (obj): Device to execute on
        slot (str): slot/subslot number
        filename (str, optional): filename for dumping the debug in bootflash
        timeout (int, optional): Max time in seconds allowed for calculation.
            Defaults to 900Sec.
    Returns:
        True if Debug dump is successful else return False
    """
    # debug vdsl controller 0/0/1 dump internal sfp_test.dump

    if filename == 'sfp':
        msg = f"filename not provided. default name of dump file will be sfp"
        cmd =f'debug vdsl controller {slot} dump internal sfp.dump'
    else:
        msg = f"File name provided"
        cmd =f'debug vdsl controller {slot} dump internal {filename}'

    log.info(msg)
    try:
        device.execute(cmd,timeout=timeout)
    except Exception as e:
        log.warning(e)


def debug_platform_software_fed_switch_active_punt_packet_capture(
        device, 
        allow_buffer_limit=False, 
        buffer_limit=16384, 
        allow_circular_buffer_limit=False, 
        circular_buffer_limit=16384, 
        allow_set_filter=False, 
        set_filter_value=None, 
        allow_clear_filter=False, 
        start=False, 
        stop=False
        ):
    """debug platform software fed switch active punt packet-capture on SVL
    Args:
        device (obj): Device to execute on
        allow_buffer_limit(bool) : if user want to set buffer limit , Default False
        buffer_limit(int , optional): Number of packets to capture <256-16384> , Default 16384 (max)
        allow_circular_buffer_limit(bool) : if user want to set circular buffer limit , Default False
        circular_buffer_limit(int , optional): Number of packets to capture <256-16384> , Default 16384 (max)
        allow_set_filter(bool): if user want to set filter , Default False
        set_filter_value(str): user input of filter 
        allow_clear_filter(bool): if user want to clear all filters , Default False
        start(bool): starting the capture
        stop(bool): stop the capture
    Returns:
        None
    Raises:
        SubCommandFailure: debug_platform_software_fed_switch_active_punt_packet_capture Failed !
    """
    cmd = []
    
    if allow_buffer_limit:
        log.info("Setting the buffer limit to {buffer_limit}".format(buffer_limit=buffer_limit))
        cmd.append("debug platform software fed switch active punt packet-capture buffer limit {buffer_limit}".format(buffer_limit=buffer_limit))  
    if allow_circular_buffer_limit:
        log.info("Setting the circular buffer limit to {buffer_limit}".format(buffer_limit=circular_buffer_limit))
        cmd.append("debug platform software fed switch active punt packet-capture buffer circular limit {buffer_limit}".format(buffer_limit=circular_buffer_limit))
    if allow_set_filter:
        log.info("Setting filter as {}".format(set_filter_value))
        cmd.append("debug platform software fed switch active punt packet-capture set-filter {filter}".format(filter=set_filter_value)) 
    if allow_clear_filter:
        log.info("Clearing all the filters")
        cmd.append("debug platform software fed switch active punt packet-capture clear-filter")         
    if start:
        log.info("Starting capture")
        cmd.append("debug platform software fed switch active punt packet-capture start")
    if stop:
        log.info("Stopping capture")
        cmd.append("debug platform software fed switch active punt packet-capture stop")
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error("debug_platform_software_fed_switch_active_punt_packet_capture Failed ! {}".format(e))