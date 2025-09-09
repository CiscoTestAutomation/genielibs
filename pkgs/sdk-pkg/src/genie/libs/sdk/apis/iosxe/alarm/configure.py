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
    

def configure_facility_alarm_temp_primary(device, threshold=None, value=None, notify=False, syslog=False, relay=False):
    ''' Configures facility alarm for temperature
        Args:
            device ('obj'): Device object
            threshold ('str'): Temperature threshold value(e.g., 'high', 'low')
            value ('int'): Temperature value
            notify ('bool'): If True, configure notify
            syslog ('bool'): If True, configure syslog
            relay ('bool'): If True, configure relay

        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Configuring alarm for temperature primary")
    try:
        cmds = []
        if threshold and value is not None:
            cmds.append(f"alarm facility temperature primary {threshold} {value}")
        if notify:
            cmds.append("alarm facility temperature primary notifies")
        if syslog:
            cmds.append("alarm facility temperature primary syslog")
        if relay:
            cmds.append("alarm facility temperature primary relay major")
        if cmds:
            device.configure(cmds)
    except SubCommandFailure as e:
        log.error(f"Failed to configure alarm for temperature primary: {e}")
        return False
    

def unconfigure_facility_alarm_temp_primary(device, threshold=None, value=None, notify=False, syslog=False, relay=False):
    ''' Unconfigures facility alarm for temperature
        Args:
            device ('obj'): Device object
            threshold ('str'): Temperature threshold value(e.g., 'high', 'low')
            value ('int'): Temperature value
            notify ('bool'): If True, unconfigure notify
            syslog ('bool'): If True, unconfigure syslog
            relay ('bool'): If True, unconfigure relay  

        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Unconfiguring alarm for temperature primary")
    try:
        cmds = []
        if threshold and value is not None:
            cmds.append(f"no alarm facility temperature primary {threshold} {value}")
        if notify:
            cmds.append("no alarm facility temperature primary notifies")
        if syslog:
            cmds.append("no alarm facility temperature primary syslog")
        if relay:
            cmds.append("no alarm facility temperature primary relay major")
        if cmds:
            device.configure(cmds)
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure alarm for temperature primary: {e}")
        return False
    

def configure_facility_alarm_temp_secondary(device, threshold=None, value=None, notify=False, syslog=False, relay=False):
    ''' Configures facility alarm for temperature secondary
        Args:
            device ('obj'): Device object
            threshold ('str'): Temperature threshold value(e.g., 'high', 'low')
            value ('int'): Temperature value
            notify ('bool'): If True, configure notify
            syslog ('bool'): If True, configure syslog
            relay ('bool'): If True, configure relay

        Returns:
            None
        Raises:
            SubCommandFailure           
    '''

    log.debug(f"Configuring alarm for temperature secondary")
    try:
        cmds = []
        if threshold and value is not None:
            cmds.append(f"alarm facility temperature secondary {threshold} {value}")
        if notify:
            cmds.append("alarm facility temperature secondary notifies")
        if syslog:
            cmds.append("alarm facility temperature secondary syslog")
        if relay:
            cmds.append("alarm facility temperature secondary relay major")
        if cmds:
            device.configure(cmds)
    except SubCommandFailure as e:
        log.error(f"Failed to configure alarm for temperature secondary: {e}")
        return False
    

def unconfigure_facility_alarm_temp_secondary(device, threshold=None, value=None, notify=False, syslog=False, relay=False):
    ''' Unconfigures facility alarm for temperature secondary
        Args:
            device ('obj'): Device object
            threshold ('str'): Temperature threshold value(e.g., 'high', 'low')
            value ('int'): Temperature value
            notify ('bool'): If True, unconfigure notify
            syslog ('bool'): If True, unconfigure syslog
            relay ('bool'): If True, unconfigure relay

        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    log.debug(f"Unconfiguring alarm for temperature secondary")
    try:
        cmds = []
        if threshold and value is not None:
            cmds.append(f"no alarm facility temperature secondary {threshold} {value}")
        if notify:
            cmds.append("no alarm facility temperature secondary notifies")
        if syslog:
            cmds.append("no alarm facility temperature secondary syslog")
        if relay:
            cmds.append("no alarm facility temperature secondary relay major")
        if cmds:
            device.configure(cmds)
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure alarm for temperature secondary: {e}")
        return False