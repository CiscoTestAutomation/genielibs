# Python
import logging
from unicon.eal.dialogs import Statement, Dialog

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_logging_console(device):
    """ logging console
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('logging console')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging console on {device}. Error:\n{error}".format(device=device, error=e))


def unconfigure_logging_console(device):
    """ no logging console
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no logging console')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging console on {device}. Error:\n{error}".format(device=device, error=e))
           
def configure_logging_monitor(device):
    """ logging monitor
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('logging monitor')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging monitor on {device}. Error:\n{error}".format(device=device, error=e))


def unconfigure_logging_monitor(device):
    """ no logging monitor
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no logging monitor')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging monitor on {device}. Error:\n{error}".format(device=device, error=e))


def configure_terminal_length(device, line_num):
    """ terminal length 0
        Args:
            device (`obj`): Device object
            line_num ('int'): Number of lines on screen (0 for no pausing)
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure terminal length on {device}".format(device=device))

    try:
        device.execute('terminal length {line_num}'.format(line_num=line_num))
    except SubCommandFailure as e:
        raise SubCommandFailure(
             "Could not configure terminal length on {device}. Error:\n{error}".format(device=device, error=e))


def configure_terminal_width(device, char_num):
    """ terminal width 0
        Args:
            device (`obj`): Device object
            char_num ('int'): Number of characters on a screen line
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure terminal width on {device}".format(device=device))

    try:
        device.execute('terminal width {char_num}'.format(char_num=char_num))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure terminal width on {device}. Error:\n{error}".format(device=device, error=e))

def configure_terminal_exec_prompt_timestamp(device):
    """ terminal exec prompt timestamp
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configure terminal exec prompt timestamp on {device}".format(device=device))

    try:
        device.execute('terminal exec prompt timestamp')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not terminal exec prompt timestamp on {device}. Error:\n{error}".format(device=device, error=e))


def configure_logging_buffer_size(device, buffer_size):
    """ logging buffered <4096-2147483647>
        Args:
            device (`obj`): Device object
            buffer_size ('int'): Size of the buffer
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure logging buffer on {device}".format(device=device))

    try:
        device.configure('logging buffer {buffer_size}'.format(buffer_size=buffer_size))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not logging buffer on {device}. Error:\n{error}".format(device=device, error=e))

def configure_logging_buffered_errors(device):
    """ Confgiure logging buffered errors
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure logging buffered errors on {device}".format(device=device))
    
    try:
        device.configure('logging buffered errors')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging buffered errors on {device}. Error:\n{error}"
                .format(device=device, error=e))

def unconfigure_logging_buffered_errors(device):
    """ Unconfgiure logging buffered errors
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Unconfigure logging buffered errors on {device}".format(device=device))
    
    try:
        device.configure('no logging buffered errors')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging buffered errors on {device}. Error:\n{error}"
                .format(device=device, error=e))

def configure_logging_console_errors(device):
    """ Confgiure logging console errors
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Configure logging console errors on {device}".format(device=device))
    
    try:
        device.configure('logging console errors')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure logging console errors on {device}. Error:\n{error}"
                .format(device=device, error=e))

def unconfigure_logging_console_errors(device):
    """ Unconfgiure logging console errors
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("Unconfigure logging console errors on {device}".format(device=device))
    
    try:
        device.configure('no logging console errors')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure logging console errors on {device}. Error:\n{error}"
                .format(device=device, error=e))


