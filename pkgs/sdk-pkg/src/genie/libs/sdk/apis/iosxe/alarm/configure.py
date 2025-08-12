'''IOSXE configure functions for alarms '''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def configure_facility_alarm_power_supply_disable(device):
    ''' Configures facility alarm for power supply disable
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Configuring alarm for power supply disable")
    try:
        device.configure("alarm facility power-supply disable")                         
    except SubCommandFailure as e:
        log.error(f"Failed to configure alarm for power supply disable: {e}")
        return False
    

def unconfigure_facility_alarm_power_supply_disable(device):
    ''' Unconfigures facility alarm for power supply disable
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Unconfiguring alarm for power supply disable")
    try:
        device.configure("no alarm facility power-supply disable")                         
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure alarm for power supply disable: {e}")
        return False
   

def configure_facility_alarm_power_supply_notify(device):  
    ''' Configures facility alarm for power supply notify
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Configuring alarm for power supply notify")
    try:
        device.configure("alarm facility power-supply notifies")                         
    except SubCommandFailure as e:
        log.error(f"Failed to configure alarm for power supply notify: {e}")
        return False 
    
    
def unconfigure_facility_alarm_power_supply_notify(device):
    ''' Unconfigures facility alarm for power supply notify
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Unconfiguring alarm for power supply notify")
    try:
        device.configure("no alarm facility power-supply notifies")                         
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure alarm for power supply notify: {e}")
        return False


def configure_facility_alarm_power_supply_relay(device):
    ''' Configures facility alarm for power supply relay
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Configuring alarm for power supply relay")
    try:
        device.configure("alarm facility power-supply relay major")                         
    except SubCommandFailure as e:
        log.error(f"Failed to configure alarm for power supply relay: {e}")
        return False


def unconfigure_facility_alarm_power_supply_relay(device):
    ''' Unconfigures facility alarm for power supply relay
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Unconfiguring alarm for power supply relay")
    try:
        device.configure("no alarm facility power-supply relay major")                         
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure alarm for power supply relay: {e}")
        return False


def configure_facility_alarm_power_supply_syslog(device):
    ''' Configures facility alarm for power supply syslog
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Configuring alarm for power supply syslog")
    try:
        device.configure("alarm facility power-supply syslog")                         
    except SubCommandFailure as e:
        log.error(f"Failed to configure alarm for power supply syslog: {e}")
        return False


def unconfigure_facility_alarm_power_supply_syslog(device):
    ''' Unconfigures facility alarm for power supply syslog
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Unconfiguring alarm for power supply syslog")
    try:
        device.configure("no alarm facility power-supply syslog")                         
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure alarm for power supply syslog: {e}")
        return False