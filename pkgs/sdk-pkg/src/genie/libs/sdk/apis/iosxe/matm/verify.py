"""Common get info functions for vlan"""

# Python
import logging
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_matm_mactable(device, state, vlan, mac, vlanport):
    '''
    Api method to call parser and return boolean True If Vlan Port Matched
    Args:
            device ('obj'): Device object
            state (string) : Device State (Such as : active, switch active, switch {1})
            vlan (string) : Device Vlan Port (Example : 10)
            mac (string) : Mac address as argument from user
            vlanport (string) : vlan port as argument from user to validate
    Returns:
            Boolean: Validation of Vlan Port True or False
    ''' 
    cmd = 'show platform software fed {state} matm macTable vlan {vlan}'.format(state=state,vlan=vlan)    
    try:   
        output = device.parse(cmd)   

    except SchemaEmptyParserError as e:
        log.error('Device {} with ' + mac +' has no vlan information: {}'.format(device.name, e))
        return None
    
    port_value = output['mac'][mac]['port']
    
    return vlanport in port_value
