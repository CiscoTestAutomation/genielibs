"""Common get info functions for vlan"""

# Python
import logging
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)
def verify_Software_Fed_Igmp_Snooping(device, state, vlan, key, value):
    '''
    Api method to call parser and return boolean True If Vlan Port Matched
    Args:
            device ('obj'): Device object
            state (string) : Device State (Such as : active, switch active, switch {1})
            vlan (string) : Device Vlan Port (Example:10)
            key (string) : Key depicts the key of the dict as output got from parser to varify it value
            value (string) : Value suppose to be the data inside the key which api will verify by compare this value and actual value inside output
    Returns:
            Boolean: Validation of Vlan Port True or False
    ''' 
    cmd = 'show platform software fed {state} ip igmp snooping vlan {vlan}'.format(state=state,vlan=vlan)  
    try:   
        output = device.parse(cmd)  
        
    except SchemaEmptyParserError as e:
        log.error('Device {} has no vlan information: {}'.format(device.name, e))
        return None
    

    if key in ('mroute_port', 'flood_port'):
        output_value = output['vlan'][vlan][key]
        if value in output_value:
            return True
        else:
            return False
        
    else:
        output_value = output['vlan'][vlan][key]
        if value == output_value:
            return True
        else:
            return False 

