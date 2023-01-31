"""Enable debug for mentioned parameters"""

# Python
import logging

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


