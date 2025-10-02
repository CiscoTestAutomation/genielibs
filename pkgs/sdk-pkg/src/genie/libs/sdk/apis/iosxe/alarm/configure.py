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


def configure_alarm_contact(device, contact=None, description=False, severity=False, trigger=False,
                            description_text=None, severity_level=None, trigger_condition=None):
    ''' Configures alarm contact
        Args:
            device ('obj'): Device object
            contact ('str'): Contact information
            description ('bool'): If True, configure description
            severity ('bool'): If True, configure severity
            trigger ('bool'): If True, configure trigger
            description_text ('str'): Description text
            severity_level ('str'): Severity level
            trigger_condition ('str'): Trigger condition
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    log.debug(f"Configuring alarm contact")
    try:
        cmds = []
        if contact:
            if description:
                cmds.append(f"alarm contact {contact} description {description_text}")
            if severity:
                cmds.append(f"alarm contact {contact} severity {severity_level}")
            if trigger:
                cmds.append(f"alarm contact {contact} trigger {trigger_condition}")
        if cmds:
            device.configure(cmds)
    except SubCommandFailure as e:
        log.error(f"Failed to configure alarm contact: {e}")
        return False


def unconfigure_alarm_contact(device, contact=None, description=False, severity=False, trigger=False):
    ''' Unconfigures alarm contact
        Args:
            device ('obj'): Device object
            contact ('str'): Contact information
            description ('bool'): If True, unconfigure description
            severity ('bool'): If True, unconfigure severity
            trigger ('bool'): If True, unconfigure trigger
        Returns:
            None
        Raises:
            SubCommandFailure
    '''
    
    log.debug(f"Unconfiguring alarm contact")
    try:
        cmds = []
        if contact:
            if description:
                cmds.append(f"no alarm contact {contact} description")
            if severity:
                cmds.append(f"no alarm contact {contact} severity")
            if trigger:
                cmds.append(f"no alarm contact {contact} trigger")
        if cmds:
            device.configure(cmds)
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure alarm contact: {e}")
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


def configure_alarm_relay_mode(device, mode: str='negative'):
    ''' Configures alarm relay mode
        Args:
            device ('obj'): Device object          
            mode ('str'): Mode to configure 
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    log.debug(f"Configuring alarm relay mode to {mode}")
    try:
        cmd = [f"alarm relay-mode {mode}"]
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to configure alarm relay mode: {e}")
        return False


def unconfigure_alarm_relay_mode(device, mode: str = 'negative'):
    ''' Unconfigures alarm relay mode
        Args:
            device ('obj'): Device object
            mode ('str'): Mode to unconfigure (default is 'negative')
        Returns:
            None
        Raises:
            SubCommandFailure
    '''    

    log.debug("Unconfiguring alarm relay mode to negative")
    try:
        cmd = [f"no alarm relay-mode {mode}"]
        device.configure(cmd)
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure alarm relay mode: {e}")
        return False


def configure_alarm_profile(device, name, config_option, triggers, type=None):
    ''' Configures alarm profile
        Args:
            device ('obj'): Device object
            name ('str'): Profile name
            config_option ('str'): Configuration options[help, exit, no, alarm, notifies, relay-major, syslog]
            triggers ('list'): Profile trigger[1,2,3,4,5,6,fcs-error, link-fault etc]
            type ('str'): Profile type[alarm, notifies, relay-major, syslog]
        Returns:
            None
        Raises:
            SubCommandFailure

        Example:
            def configure_alarm_profile(name='test', config_option='alarm', triggers=['link-fault', 'fcs-error'])
            def configure_alarm_profile(name='test', config_option='no', triggers=['link-fault', 'fcs-error'], type='alarm')            
    '''      

    log.debug(f"Configuring alarm profile {name}")
    try:
        cmds = [f"alarm-profile {name}"]
        if config_option in ('help', 'exit'):
            cmds.append(f"{config_option}")
        elif config_option == 'no':
            for trig in triggers:
                cmds.append(f"no {type} {trig}")
        else:
            for trig in triggers:
                cmds.append(f"{config_option} {trig}")

        device.configure(cmds)
    except SubCommandFailure as e:
        log.error(f"Failed to configure alarm profile {name}: {e}")
        raise e
        

def unconfigure_alarm_profile(device, name):
    ''' Unconfigures alarm profile
        Args:
            device ('obj'): Device object
            name ('str'): Profile name
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    log.debug(f"Unconfiguring alarm profile {name}")
    try:
        cmds = [f"no alarm-profile {name}"]
        device.configure(cmds)
    except SubCommandFailure as e:
        log.error(f"Failed to unconfigure alarm profile {name}: {e}")
        raise e
