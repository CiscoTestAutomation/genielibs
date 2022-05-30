"""Common get info functions for vlan"""

# Python
import logging
import re
# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)
def verify_Software_Fed_Ipv6_Mld_Snooping_Groups(device, state, vlan, key, value):
    '''
    Api method to call parser and return boolean True If Vlan Port Matched
    Args:
            device ('obj'): Device object
            state (string) : Device State (Such as : active, switch active, switch {1})
            vlan (string) : Device Vlan Port (Example : 20 ff1e::20)
            key (string) : Key depicts the key of the dict as output got from parser to varify it value
            value (string) : Value suppose to be the data inside the key which api will verify by compare this value and actual value inside output
    Returns:
            Boolean: Validation of Vlan Port True or False
    ''' 
    cmd = 'show platform software fed {state} ipv6 mld snooping groups vlan {vlan}'.format(state=state,vlan=vlan)  
    vlan = vlan.split(" ", 1)
    try:   
        output = device.parse(cmd) 
    except SchemaEmptyParserError as e:
        log.error('Device {} has no vlan information: {}'.format(device.name, e))
        return None

    if key == ('mem_port'):
        output_value = output['vlan'][vlan[0]][key]
        if value in output_value:
            return True
        else:
            return False  

    elif key == ('cck_ep') or key == ('fail_flag'):
        output_value = output['vlan'][vlan[0]][key]
        value = int(value)
        if value == output_value:
            return True
        else:
            return False  
        
    else:
        output_value = output['vlan'][vlan[0]][key]
        if value == output_value:
            return True
        else:
            return False 


