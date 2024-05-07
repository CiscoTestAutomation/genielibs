# Genie
from genie.metaparser.util.exceptions import (SchemaEmptyParserError,
                                              SchemaMissingKeyError)
import re
import logging

# Logger
log = logging.getLogger(__name__)

# import parser utils
from genie.libs.parser.utils.common import Common

def get_component_details(device):
    """
    Get components detail

    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: components' details dict
            example: {
                'name': [],
                'descr_raw': [],
                'part_number': [],
                'serial_number': [],
                'hardware_version': []
            }
    Raises:
        None
    """

    try:
        out = device.parse('show inventory raw')
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
        return None

    name_list = []
    descr_list = []
    part_no_list = []
    serial_no_list = []
    hw_ver_list = []

    # Unknown PID
    p00 = re.compile(
        r'^Unknown PID$')

    # Gi4/0/1
    # Te1/1/1
    # HundredGigE1/0/51
    p01 = re.compile(
        r'^((?!Ap)[\w]+)\d+\/\d+\/\d+$')

    # Switch 4 - FAN - T1 1
    p1 = re.compile(
        r'^Switch\s+(?P<sw_number>\d+)\s+\-\s+FAN\s+\-\s+T1\s+(?P<fan_number>\d+)$')
    
    # Gi4/0/1
    # Te1/1/1 Container
    # HundredGigE1/0/51
    p2 = re.compile(
        r'^(?P<ethernet>((?!Ap)([\w]+)))(?P<int_number>\d+\/\d+\/\d+)(\s+)?(?P<Container>Container)?$')
    
    # Switch 4 - Power Supply A Container
    # Switch 4 - PowerSupplyA
    # Switch 4 - Fan 1 Container
    # Switch 4 - HotSpot Temp Sensor
    # Switch 4 FRU Uplink Module 1
    # Switch 4 Slot 1 FRULink Container

    p3 = re.compile(
        r'^Switch\s+(?P<sw_number>\d+)\s+(\-\s+)?(Slot\s+(?P<slot_id>\d+\s+))?'
        r'(?P<keyword>(Power Supply)|Fan|(\w+\s+Temp Sensor)|RPS|(FRU Uplink Module)|FRULink|(Fixed Module))'
        r'(\s+)?(?P<id>\w|\d+)?(\s+)?(?P<Container>Container)?$')
    
    # Slot 4 Temp:    inlet
    p4 = re.compile(
        r'^Slot\s+(?P<slot_id>\d+)\s+Temp:\s+(?P<keyword>\w+)$')

    # Internal POE Bay
    # c95xx Stack
    # Ap3/0/1 Container
    # R0 - NMTGE
    # Hard Disk Container R0
    # Slot 3 USB Container
    # Slot 4 Disk0 SATA
    # slot R0
    p5 = re.compile(
        r'^((Internal POE Bay)|(c\d+\w+\s+Stack)|(Ap\d+\/\d+\/\d+\s+Container)|(Hard Disk Container\s+\w+)|(R\d+\s+\-\s+NMTGE)|([Ss]lot\s+(\w)?\d+(.*)?))$')

    # Power Supply Bay 8
    p6 = re.compile(
        r'^Power Supply Bay\s+(?P<bay_number>\d+)$')

    # Fan Tray Bay
    p7 = re.compile(
        r'^Fan Tray Bay$')

    comps_dict = out.get("name", {})

    for name_raw in comps_dict:

        part_no = dict(comps_dict[name_raw]).get('pid','NULL')
        serial_no = dict(comps_dict[name_raw]).get('sn','NULL')
        
        descr_list.append(dict(comps_dict[name_raw]).get('description','NULL'))
        hw_ver_list.append(dict(comps_dict[name_raw]).get('vid','NULL'))

        # Unknown PID
        m = p00.match(part_no)
        if m:
            part_no = 'UnknownPID'
        part_no_list.append(part_no)

        # Gi4/0/1
        # Te1/1/1
        # HundredGigE1/0/51
        m = p01.match(name_raw)
        if m:
            if serial_no != 'NULL':
                serial_no = serial_no+(16-len(serial_no))*" "
        serial_no_list.append(serial_no)

        # Switch 4 - FAN - T1 1
        m = p1.match(name_raw)
        if m:
            group = m.groupdict()
            name = "Fan"+group['sw_number']+"/"+group['fan_number']
            name_list.append(name)
            continue
        
        # Gi4/0/1
        # Te1/1/1 Container
        # HundredGigE1/0/51
        m = p2.match(name_raw)
        if m:
            group = m.groupdict()
            ethernet = group['ethernet']
            int_number = group['int_number']

            if group['Container']:
                if ethernet == 'Twe':
                    name = 'TwentyFiveGEthernetContainer'+int_number
                else:
                    name_longintf = Common.convert_intf_name(ethernet+int_number)
                    name_split_list = name_longintf.split('Ethernet')
                    name = name_split_list[0]+"EthernetContainer"+name_split_list[1]
            else:
                if ethernet == 'Twe':
                    name = 'TwentyFiveGigabitEthernet'+int_number
                else:
                    name = Common.convert_intf_name(ethernet+int_number)
                
            name_list.append(name)
            continue

        # Switch 4 - Power Supply A Container
        # Switch 4 - PowerSupplyA
        # Switch 4 - Fan 1 Container
        # Switch 4 - HotSpot Temp Sensor
        # Switch 4 FRU Uplink Module 1
        # Switch 4 Slot 1 FRULink Container
        m = p3.match(name_raw)
        if m:
            group = m.groupdict()

            if group['Container']:
                name0 = group['keyword']+group['Container']+group['sw_number']
            else:
                name0 = group['keyword']+group['sw_number']

            if group['id']:
                name1 = name0+'/'+group['id']
            elif group['slot_id']:
                name1 = name0+'/'+group['slot_id']
            else:
                name1 = name0

            name_list.append(name1.replace(' ', ''))
            continue
        
        # Slot 4 Temp:    inlet
        m = p4.match(name_raw)
        if m:
            group = m.groupdict()
            name = "Slot"+group['slot_id']+'/'+group['keyword']
            name_list.append(name)
            continue
        
        # Internal POE Bay
        # c95xx Stack
        # Ap3/0/1 Container
        # R0 - NMTGE
        # Hard Disk Container R0
        # Slot 3 USB Container
        # Slot 4 Disk0 SATA
        # slot R0
        m = p5.match(name_raw)
        if m:
            name_list.append(name_raw)
            continue

        # Power Supply Bay 8
        m = p6.match(name_raw)
        if m:
            group = m.groupdict()
            name = "PowerSupplyContainer"+group['bay_number']
            name_list.append(name)
            continue
        
        # Fan Tray Bay
        m = p7.match(name_raw)
        if m:
            group = m.groupdict()
            name = "FanContainer"
            name_list.append(name)
            continue

        name = name_raw.replace(' ', '')
        name_list.append(name)

    return {"name":name_list, "descr_raw":descr_list, "part_number":part_no_list, "serial_number":serial_no_list, "hardware_version":hw_ver_list}


def get_component_descr(device):
    """
    Get components' description

    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: components' description dict
            example: {
                'name': [],
                'descr': []
            }
    Raises:
        None
    """

    comp_dict = {}
    name_list = []
    descr_raw_list = []
    descr_list = []

    try:
        comp_dict = get_component_details(device)
    except Exception as e:
        log.error("get_comp_descr_dict api errored: {e}".format(e=e))
        return None

    descr_raw_list = comp_dict['descr_raw']
    name_list = comp_dict['name']

    if not descr_raw_list:
        return None
    
    # Switch 4 - C9300-24U - FAN 1
    p0 = re.compile(
        r'^Switch\s+(?P<sw_number>\d+)\s+\-\s+C\d+\-\d+\w+\s+\-\s+FAN\s+(?P<fan_number>\d+)$')

    # Cisco Catalyst 9400 Series Fan
    p1 = re.compile(
        r'^Cisco Catalyst\s+\d+\s+Series +Fan$')

    # Cisco Catalyst 9400 Series 7 Slot Chassis Fan Tray
    # Cisco Catalyst 9600 Series C9606 Chassis Fan Tray
    p2 = re.compile(
        r'^Cisco Catalyst\s+\d+\s+Series +[\d\w]+(\s+Slot)?\s+Chassis Fan Tray$')

    for index, descr_raw in enumerate(descr_raw_list):
        
        # Switch 4 - C9300-24U - FAN 1
        m = p0.match(descr_raw)
        if m:
            group = m.groupdict()
            descr = "Switch "+group['sw_number']+" -"+" FAN "+group['fan_number'] 
            descr_list.append(descr)
            continue

        # Cisco Catalyst 9400 Series Fan
        m = p1.match(descr_raw)
        if m:
            group = m.groupdict()
            descr = "FAN "+name_list[index][3:]  # 'Cisco Catalyst 9400 Series Fan' to 'FAN x/x' 
            descr_list.append(descr)
            continue

        # Cisco Catalyst 9400 Series 7 Slot Chassis Fan Tray
        # Cisco Catalyst 9600 Series C9606 Chassis Fan Tray
        m = p2.match(descr_raw)
        if m:
            group = m.groupdict()
            descr = "FAN Tray"  # 'Cisco Catalyst 9400 Series 7 Slot Chassis Fan Tray' to 'FAN Tray'
            descr_list.append(descr)
            continue
        
        descr_list.append(descr_raw)
    
    return {"name":name_list, "descr":descr_list}


def get_hardware_version(device, transceiver_value=" "):
    """
    Get components' hardware version

    Args:
        device (`obj`): Device object
        transceiver_value (str, optional): Value of the transceiver. Defaults to "".
    Returns:
        Dictionary: components' hardware version dict
            example: {
                'name': [[usbflash1],[Switch1, PowerSupply1/B]],
                'hardware_version': [[3.10],[P2A, V02]]
            }
    Raises:
        None
    """

    comp_dict = {}

    deci_hw_list = []
    str_hw_list = []
    str_name_list = []
    deci_name_list = []

    try:
        comp_dict = get_component_details(device)
    except Exception as e:
        log.error("get_hardware_version api errored: {e}".format(e=e))
        return None

    hw_raw_list = comp_dict['hardware_version']
    name_raw_list = comp_dict['name']

    if not hw_raw_list:
        return None

    # TenGigabitEthernet1/1/1
    # TwentyFiveGigabitEthernet1/0/51
    p0 = re.compile(
        r'^((GigabitEthernet|TenGigabitEthernet|FortyGigabitEthernet|TwentyFiveGigabitEthernet)(\d+\/\d+\/\d+))$')

    for index, hw in enumerate(hw_raw_list):

        # TenGigabitEthernet1/1/1
        # TwentyFiveGigabitEthernet1/0/51
        m = p0.match(name_raw_list[index])
        if m:
            if hw != 'NULL':
                hw = hw+transceiver_value

        hw_strip = hw.strip()
        ## Return two list one of int valued hardware version and another of string valued hardware version

        if hw_strip.replace('.', '',1).isdigit():
            deci_name_list.append(name_raw_list[index])
            deci_hw_list.append(hw)

        else:
            str_name_list.append(name_raw_list[index])
            str_hw_list.append(hw)

    return {"name":[deci_name_list, str_name_list], "hardware_version": [deci_hw_list, str_hw_list]}
