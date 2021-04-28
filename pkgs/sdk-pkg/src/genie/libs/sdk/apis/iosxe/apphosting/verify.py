''' Common Verify functions for IOX / app-hosting '''

import logging
import time

log = logging.getLogger(__name__)

# Import parser
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

def verify_app_requested_state(device, app_list=None, requested_state='RUNNING', max_time=120, interval=10):
    ''' 
    verify_app_requested_state
    Check show app-hosting list and confirm the requested state of the passed in list of appids
    Args:
        device ('obj') : Device object
        app_list ('list') : list of appids
        requested_state ('str') : requested state of appid
        max_time ('int') : max time to wait
        interval ('int') : interval timer
    Returns:
        True
        False
    Raises:
        None    
    '''

    all_apps_achieved_requested_state = False
    
    if app_list is None:
        app_list = []
      
    timeout = Timeout(max_time=max_time, interval=interval)
    while timeout.iterate():
        try:
            old_timeout = device.execute.timeout
            device.execute.timeout = 120
            output = device.parse('show app-hosting list')
            device.execute.timeout = old_timeout
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        for app in app_list:            
            if output['app_id'][app]['state'] == requested_state:
                all_apps_achieved_requested_state = True
                continue
            else:
                log.info("App name %s not in the requested state %s yet, wait" % (app, requested_state))    
                all_apps_achieved_requested_state = False
                timeout.sleep()
        if all_apps_achieved_requested_state:
            break
    
    if all_apps_achieved_requested_state: 
        log.info("All Apps achieved the requested state!")
    else: 
        log.error("Not all apps achieved the requested state!")
    
    return all_apps_achieved_requested_state

def verify_iox_enabled(device, max_time=600, interval=10):
    ''' 
    verify_iox_enabled
    Check show iox and confirm all services are up and running
    Args:
        device ('obj') : Device object
        max_time ('int') : max time to wait
        interval ('int') : interval timer
    Returns:
        True
        False
    Raises:
        None
    '''

    timeout = Timeout(max_time=max_time, interval=interval)    
    while timeout.iterate():
        try:
            output = device.parse("show iox")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        if output.get('caf_service', '').strip().lower() == 'running' and \
            output.get('ha_service', '').strip().lower() == 'running' and \
            output.get('ioxman_service', '').strip().lower() == 'running' and \
            output.get('libvirtd', '').strip().lower() == 'running' and \
            output.get('dockerd', '').strip().lower() == 'running':
                log.info("IOX is enabled")
                return True
        else:
            timeout.sleep()        

    log.info("IOX was not enabled!")
    return False
    
def verify_iox_disabled(device, max_time=600, interval=10, redundancy=False):
    ''' 
    verify_iox_disabled
    Check show iox and confirm all services are not running
    Args:
        device ('obj') : Device object
        max_time ('int') : max time to wait
        interval ('int') : interval timer
    Returns:
        True
        False
    Raises:
        None
    '''
    
    timeout = Timeout(max_time=max_time, interval=interval)    
    while timeout.iterate():
        try:
            output = device.parse("show iox")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
       
        if output.get('caf_service', '').strip().lower() == 'not running' and \
            output.get('ha_service', '').strip().lower() == 'not running' and \
            output.get('ioxman_service', '').strip().lower() == 'not running' and \
            output.get('dockerd', '').strip().lower() == 'not running':
                log.info("IOX is disabled")
                return True
        else:
            timeout.sleep()

    log.info("IOX was not disabled!")
    return False

