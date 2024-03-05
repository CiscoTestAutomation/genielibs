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
    comp_list = []
    deci_name_list = []
    str_name_list = []
    deci_fw_list = []
    str_fw_list = []

    def firmware_version_per_switch(device, cli, model_num, switch=''):
        fw_list = []

        try:
            output_fw = device.parse(cli.format(switch=switch))
        except SchemaEmptyParserError as e:
            return []
        except Exception as e:
            log.error(cli+": {e}".format(e=e))
            return None

        out_index = output_fw.get("index", {})  

        for index in out_index:
            name = output_fw["index"][index].get('name')

            if 'PowerSupplyModule' in name and model_num==96:
                if switch:
                    name = 'PowerSupplyModule' + str(switch) + '/' + name[len('PowerSupplyModule'):]
                fw = '(N/A, N/A, N/A)'
                continue
            else:
                fw = dict(output_fw["index"][index]).get('fw_version','NULL')
                if fw == 'unknown':
                    fw = 'NULL'

                if switch:
                    if 'FanTray' in name:
                        name = 'Fan' + str(switch) + '/' + 'Tray'
                    elif 'Supervisor' in name:
                        name = 'Switch ' + str(switch) + ' ' + name

            fw_list.append({name:fw})

        return fw_list

    # Parse show version to get model number
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
    
    # Parse show switch to get switches in stack to run firmware CLI
    try:
        output_switch = device.parse("show switch")    
        out_stack = output_switch.get("switch", {}).get("stack", {})
    except SchemaEmptyParserError as e:
        out_stack = [1]
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show version': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show version': {e}".format(e=e))

    if len(out_stack) > 1:
        fw_cli = "show firmware version switch {switch} all"
        for switch in out_stack:
            comp_list = firmware_version_per_switch(device, fw_cli, model_num, switch)

    elif len(out_stack) == 1:
        fw_cli = "show firmware version all"
        comp_list += firmware_version_per_switch(device, fw_cli, model_num)
    
    # Get components in show module output
    comp_list += get_module(device)

    for comp in comp_list:
        name = list(comp.keys())[0]
        fw = list(comp.values())[0]

        if (fw.strip()).replace('.', '',1).isdigit():
            deci_name_list.append(name)
            deci_fw_list.append(fw)
        else:
            str_name_list.append(name)
            str_fw_list.append(fw)

    return {"name":[deci_name_list,str_name_list], "firmware_version":[deci_fw_list,str_fw_list]}

def get_module(device):

    """
    Get componenets' firmware version from show module output
    Args:
        device (`obj`): Device object
    Returns:
        Dictionary: List of components' firmware dict
            example: [
                {<mod name1>: <firmware_version1>},
                {<mod name2>: <firmware_version2>}
            ]
    Raises:
        None
    """
    comp_list = []

    try:
        output_mod = device.parse("show module")   # Show module to get line card infos
    except SchemaMissingKeyError as e:
        log.error("Missing key while parsing 'show module': {e}".format(e=e))
    except Exception as e:
        log.error("Failed to parse 'show module': {e}".format(e=e))

    out_mod = output_mod.get("module", {})

    def model_output_processing(data, switch=''):
        mod_list = []
        for module in out_mod:
            model = output_mod["module"][module].get('model')
            if '-LC-' in model:
                name = 'Slot '+str(module)+ ' Linecard'

                if switch:
                    name = 'Switch ' + str(switch) + ' ' + name

                fw = dict(output_mod["module"][module]).get('fw','NULL')
                mod_list.append({name:fw})

        return mod_list

    if 'switches' not in out_mod:
        return model_output_processing(out_mod)
    else:
        for switch, data in out_mod.items():
            comp_list += model_output_processing(data, switch=switch)
        return comp_list
