# Genie
from genie.metaparser.util.exceptions import (SchemaEmptyParserError,
                                              SchemaMissingKeyError)
import logging

# Logger
log = logging.getLogger(__name__)

def get_firmware_version(device):
    """
    Get components' firmware version (for cat 9600 and 9400 series)
    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: components' firmware dict
            example: {
                'name': [],
                'firmware_version': []
            }
    Raises:
        None
    """

    output = {}

    try:
        output = device.parse("show version")
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))
    
    if not output:
        log.error("Failed to get model number")
        return None

    model_num = int((output.get('version', {}).get('chassis'))[1:3])

    if model_num not in [96,94]:
        log.error("Not a supported model (Supported models are 9600, 9400 series)")
        return None

    deci_name_list = []
    str_name_list = []
    deci_fw_list = []
    str_fw_list = []

    try:
        output_fw = device.parse("show firmware version all")
    except Exception as e:
        log.error("Failed to parse 'show firmware version all': {e}".format(e=e))
        return None  
    
    out_index = output_fw.get("index", {})  

    for index in out_index:
        name = output_fw["index"][index].get('name')

        if 'PowerSupplyModule' in name and model_num==96:
            str_name_list.append(name)
            str_fw_list.append('(N/A, N/A, N/A)')
            continue
        else:
            fw = dict(output_fw["index"][index]).get('fw','NULL')

        if (fw.strip()).replace('.', '',1).isdigit():
            deci_name_list.append(name)
            deci_fw_list.append(fw)
        else:
            str_name_list.append(name)
            str_fw_list.append(fw)
    
    try:
        output_mod = device.parse("show module")   # Show module to get line card infos
    except Exception as e:
        log.error("Failed to parse 'show module': {e}".format(e=e))
        return None  

    out_mod = output_mod.get("module", {})
    
    for module in out_mod:
        model = output_mod["module"][module].get('model')

        if '-LC-' in model:
            name = 'Slot '+str(module)+ ' Linecard'
            fw = dict(output_mod["module"][module]).get('fw','NULL')

            if (fw.strip()).replace('.', '',1).isdigit():
                deci_name_list.append(name)
                deci_fw_list.append(fw)
            else:
                str_name_list.append(name)
                str_fw_list.append(fw)

    return {"name":[deci_name_list,str_name_list], "firmware_version":[deci_fw_list,str_fw_list]}

