# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

import re
import logging
log = logging.getLogger(__name__)

# import parser utils
from genie.libs.parser.utils.common import Common


def transceiver(device):
    """
    Get instant value of a transceiver output_power,input_power and laser_biased_current
    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: "transceiver":[transceivers' name], "output_power_instant":[transceivers' output_power_instant], "input_power_instant":[transceivers' input_power_instant] ,"current_instant":[transceivers' current_instant]
    Raises:
        None
    """

    output_power_lst = []
    input_power_lst = []
    current_lst = []
    
    try:
        out = device.parse('show interfaces transceiver')
    except SchemaEmptyParserError as e:
        log.error("Command 'show interfaces transceiver' did not return any results: {e}".format(e=e))
        return None

    transceiver_list = []
    
    for intf in out['interfaces']:

        if intf[:3] == 'Twe':
            name = 'TwentyFiveGigabitEthernet'+intf[3:]
        else:
            name = Common.convert_intf_name(intf)
        transceiver_list.append(name)
    for intf in out['interfaces']:
        output_power_instant = float(out['interfaces'][intf]['opticaltx'])
        output_power_lst.append([output_power_instant-1,output_power_instant+1])
        input_power_instant = float(out['interfaces'][intf]['opticalrx'])
        input_power_lst.append([input_power_instant-1,input_power_instant+1])
        current_instant = float(out['interfaces'][intf]['current'])
        current_lst.append([current_instant-1,current_instant+1])
    
    return {'transceiver':transceiver_list , 'output_power':output_power_lst , 'input_power':input_power_lst , 'current':current_lst}



def transceiver_interval(device):
    """
    Get default interval value "30" of a transceiver output_power,input_power and laser_biased_current
    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: "transceiver":[transceivers' name], "output_power_interval":[transceivers' output_power_interval], "input_power_interval":[transceivers' input_power_interval] ,"current_interval":[transceivers' current_interval]
    Raises:
        None
    """
    default_interval = []
    
    try:
        out = device.parse('show interfaces transceiver')
    except SchemaEmptyParserError as e:
        log.error("Command 'show interfaces transceiver' did not return any results: {e}".format(e=e))
        return None
        
    transceiver_list = []
    
    for intf in out['interfaces']:

        if intf[:3] == 'Twe':
            name = 'TwentyFiveGigabitEthernet'+intf[3:]
        else:
            name = Common.convert_intf_name(intf)
        transceiver_list.append(name)
    for intf in transceiver_list :
        default_interval.append(int(30))
        
    return {'transceiver':transceiver_list , 'interval': default_interval }
        
def poe_p3(device):
    """
    Get power,class of a poe interfaces poe_power_used,poe_power_class
    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: "poe_intf":[poe_intf' name], "poe_power_used":[poe' poe_power_used_lst], "poe_power_class":[poe' poe_power_class_lst]
    Raises:
        None
    """
    try:
        out = device.parse('show power inline')
    except SchemaEmptyParserError as e:
        log.error("Command 'show power inline' did not return any results: {e}".format(e=e))
        return None

    poe_intf_lst = []
    poe_power_used_lst = []
    poe_power_class_lst = []
    
    for intf in out['interface']:
        if out['interface'][intf]['oper_state'] == "on" :
            poe_intf_lst.append(intf)
            poe_power_used_lst.append(out['interface'][intf]['power'])
            poe_power_class_lst.append(out['interface'][intf]['class'])
            
    return {'poe_intf':poe_intf_lst , 'poe_power_used' : poe_power_used_lst , 'poe_power_class' : poe_power_class_lst}


def poe_enabled_p4(device):
    """
    Get enabled interfaces of poe 
    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: "poe_intf":[poe_intf' name], "poe_enabled":[poe' poe_enabled_lst]
    Raises:
        None
    """
    try:
        out = device.parse('show power inline')
    except SchemaEmptyParserError as e:
        log.error("Command 'show power inline' did not return any results: {e}".format(e=e))
        return None
        
    poe_intf_lst = []
    poe_enabled_lst = []
    
    for intf in out['interface']:

        if intf[:3] == 'Twe':
            name = 'TwentyFiveGigabitEthernet'+intf[3:]
        else:
            name = Common.convert_intf_name(intf)
        poe_intf_lst.append(name)
        
    for values in out['interface'].values():
        poe_enabled = values['oper_state']
        if poe_enabled == "on" :
            poe_enabled_lst.append('true')
        else :
            poe_enabled_lst.append('false')
                    
    return {'poe_intf':poe_intf_lst , 'poe_enabled' : poe_enabled_lst }

               
