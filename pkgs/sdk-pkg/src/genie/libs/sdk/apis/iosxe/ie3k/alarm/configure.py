# Python
import logging

logger = logging.getLogger(__name__)

from unicon.core.errors import SubCommandFailure

def configure_facility_alarm_sdcard_enable(device):
    """ Configure facility alarm sdcard enable
        Args:
            device ('obj'): device to use
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed to configure facility alarm sdcard enable
    """
    try:
        device.configure("alarm facility sd-card enable")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to configure facility alarm sdcard enable") from e
    

def configure_facility_alarm_sdcard_notifies(device):
    """ Configure facility alarm sdcard notifies
        Args:
            device ('obj'): device to use
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed to configure facility alarm sdcard notifies
    """
    try:
        device.configure("alarm facility sd-card notifies")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to configure facility alarm sdcard notifies") from e
    

def configure_facility_alarm_sdcard_relay(device):
    """ Configure facility alarm sdcard relay
        Args:
            device ('obj'): device to use
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed to configure facility alarm sdcard relay
    """
    try:
        device.configure("alarm facility sd-card relay major")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to configure facility alarm sdcard relay") from e
    

def configure_facility_alarm_sdcard_syslog(device):
    """ Configure facility alarm sdcard syslog
        Args:
            device ('obj'): device to use
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed to configure facility alarm sdcard syslog
    """
    try:
        device.configure("alarm facility sd-card syslog")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to configure facility alarm sdcard syslog") from e
    

def unconfigure_facility_alarm_sdcard_enable(device):
    """ Unconfigure facility alarm sdcard enable
        Args:
            device ('obj'): device to use
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed to unconfigure facility alarm sdcard enable
    """
    try:
        device.configure("no alarm facility sd-card enable")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to unconfigure facility alarm sdcard enable") from e
    

def unconfigure_facility_alarm_sdcard_notifies(device):
    """ Unconfigure facility alarm sdcard notifies
        Args:
            device ('obj'): device to use
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed to unconfigure facility alarm sdcard notifies
    """
    try:
        device.configure("no alarm facility sd-card notifies")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to unconfigure facility alarm sdcard notifies") from e
    

def unconfigure_facility_alarm_sdcard_relay(device):
    """ Unconfigure facility alarm sdcard relay
        Args:
            device ('obj'): device to use
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed to unconfigure facility alarm sdcard relay
    """
    try:
        device.configure("no alarm facility sd-card relay major")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to unconfigure facility alarm sdcard relay") from e
    

def unconfigure_facility_alarm_sdcard_syslog(device):
    """ Unconfigure facility alarm sdcard syslog
        Args:
            device ('obj'): device to use
        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed to unconfigure facility alarm sdcard syslog
    """
    try:
        device.configure("no alarm facility sd-card syslog")
    except SubCommandFailure as e:
        raise SubCommandFailure("Failed to unconfigure facility alarm sdcard syslog") from e    