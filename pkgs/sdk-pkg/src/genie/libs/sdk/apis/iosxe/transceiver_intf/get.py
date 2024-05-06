# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

import re
import logging
log = logging.getLogger(__name__)

# import parser utils
from genie.libs.parser.utils.common import Common


def transceiver_power_intf(device):
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
        out = device.parse('show interfaces transceiver detail')
    except SchemaEmptyParserError as e:
        log.error("Command 'show interfaces transceiver detail' did not return any results: {e}".format(e=e))
        return None

    transceiver_list = []
    
    for intf in out['interfaces']:

        if intf[:3] == 'Twe':
            name = 'TwentyFiveGigabitEthernet'+intf[3:]
        else:
            name = Common.convert_intf_name(intf)
        transceiver_list.append(name)
    for intf in out['interfaces']:
        output_power_instant = float(out['interfaces'][intf]['OpticalTX']['Value'])
        output_power_lst.append([(output_power_instant)-1,(output_power_instant)+1])
        input_power_instant = float(out['interfaces'][intf]['OpticalRX']['Value'])
        input_power_lst.append([(input_power_instant)-1,(input_power_instant)+1])
        current_instant = float(out['interfaces'][intf]['Current']['Value'])
        current_lst.append([(current_instant)-1,(current_instant)+1])
    
    return {'transceiver':transceiver_list , 'output_power':output_power_lst , 'input_power':input_power_lst , 'current':current_lst}


def transceiver_interval_intf(device):
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
        out = device.parse('show interfaces transceiver detail')
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


def transceiver_intf_components(device):
    """
    Get info about transceiver vendor, vendor_part, vendor_rev, serial_no, form_factor, connector_type
    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: "transceiver": [transceivers' name], "vendor_name": [transceivers' vendor_lst], "vendor_part": [transceivers' vendor_part_lst], "vendor_rev": [transceivers' vendor_rev_lst], "serial_no": [transceivers' serial_no_lst], "form_factor": [transceivers' form_factor_lst], "connector_type": [transceivers' connector_type_lst]
    Raises:
        None
    """
    try:
        out = device.parse('show interfaces transceiver detail')
    except SchemaEmptyParserError as e:
        log.error("Command 'show interfaces transceiver' did not return any results: {e}".format(e=e))
        return None

    transceiver_list = []
    vendor_lst = []
    vendor_part_lst = []
    vendor_rev_lst = []
    serial_no_lst = []
    form_factor_lst = []
    connector_type_lst = []
    for intf in out['interfaces']:
        if intf[:3] == 'Twe':
            name = 'TwentyFiveGigabitEthernet' + intf[3:]
        else:
            name = Common.convert_intf_name(intf)
        transceiver_list.append(name)

    for interface in transceiver_list:
        try:
            out = device.parse('show idprom interface {}'.format(interface))
        except SchemaEmptyParserError as e:
            log.error("Command did not return any results: {e}".format(e=e))
            return None

        if out.get('sfp_info'):
            info_dict = out['sfp_info']
            vendor_part = info_dict.get('cisco_part_number')
            form_factor = info_dict.get('product_identifier')
        elif out.get('idprom_for_transceiver'):
            info_dict = out['idprom_for_transceiver']
            vendor_part = info_dict.get('vendor_part_number')
            form_factor = info_dict.get('description')
        else:
            log.error("Unable to retrieve transceiver info for interface: {}".format(interface))
            continue

        vendor = info_dict.get('vendor_name')
        vendor_lst.append(vendor)
        vendor_part_lst.append(vendor_part)
        form_factor_lst.append("openconfig-transport-types:SFP" if re.search(r'(SFP|SFP\+)', form_factor, re.IGNORECASE) else None)

        vendor_rev = info_dict.get('vendor_revision')
        if '0x' in vendor_rev:
            temp = [x[2:] for x in vendor_rev.split()]
            vendor_rev = bytes.fromhex(''.join(temp)).decode('utf-8')
        vendor_rev_lst.append(vendor_rev.replace(" ", ""))

        serial_no = info_dict.get('serial_number')
        serial_no_lst.append(serial_no)

        connector_type = info_dict.get('connector_type')
        if connector_type:
            connector_type_lst.append("openconfig-transport-types:LC_CONNECTOR" if re.search(r'LC\.|LC|LC connector', connector_type, re.IGNORECASE) else None)

    return {'transceiver': transceiver_list, 'vendor_name': vendor_lst, 'vendor_part': vendor_part_lst,
            'vendor_rev': vendor_rev_lst, 'serial_no': serial_no_lst, 'form_factor': form_factor_lst,
            'connector_type': connector_type_lst}

