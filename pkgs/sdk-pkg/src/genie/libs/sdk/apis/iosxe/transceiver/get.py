# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

import re
import logging
log = logging.getLogger(__name__)

# import parser utils
from genie.libs.parser.utils.common import Common

def transceiver_info(device) :
    """
    Get info about  transceiver vendor,vendor_part,vendor_rev,serial_no,form_factor,connector_type
    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: "transceiver":[transceivers' name], "vendor_name":[transceivers' vendor_lst], "vendor_part":[transceivers' vendor_part_lst] ,"vendor_rev":[transceivers' vendor_rev_lst , "serial_no" : [transceivers' serial_no_lst] , "form_factor" : [transceivers' form_factor_lst],"connector_type" : [transceivers' connector_type_lst]
    Raises:
        None
    """
    try:
        out = device.parse('show interfaces transceiver')
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
            name = 'TwentyFiveGigabitEthernet'+intf[3:]
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
        elif out.get('idprom_for_transceiver') :
            info_dict = out['idprom_for_transceiver']
            
        vendor = info_dict.get('vendor_name')
        vendor_lst.append(vendor)
        
        vendor_part = info_dict.get('cisco_part_number')
        vendor_part_lst.append(vendor_part)
        
        vendor_rev = info_dict.get('vendor_revision')
        if '0x' in vendor_rev:
            temp = [x[2:] for x in vendor_rev.split()]
            vendor_rev = bytes.fromhex(''.join(temp)).decode('utf-8')
        vendor_rev_lst.append(vendor_rev.replace(" ", ""))
        
        serial_no = info_dict.get('serial_number')
        serial_no_lst.append(serial_no)
        
        form_factor = info_dict.get('product_identifier')
        if form_factor == "SFP/SFP+" :
            form_factor_lst.append("openconfig-transport-types:SFP")
        
        
        connector_type = info_dict.get('connector_type')
        if connector_type == "LC connector" :
            connector_type_lst.append("openconfig-transport-types:LC_CONNECTOR")
        elif connector_type == "LC" :
            connector_type_lst.append("openconfig-transport-types:LC")
    
    return {'transceiver':transceiver_list , 'vendor_name' : vendor_lst , 'vendor_part' : vendor_part_lst , 'vendor_rev' : vendor_rev_lst , 'serial_no' : serial_no_lst ,'form_factor' : form_factor_lst , 'connector_type' : connector_type_lst}
