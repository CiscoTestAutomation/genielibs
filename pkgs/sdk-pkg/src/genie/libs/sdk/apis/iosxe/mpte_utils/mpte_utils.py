"""
Description: API written for MPTE automation 
- Removes the elements (and its corresponding value if provided in 'value_list') 
  from a given list ('key_list') that are not present in the gnmi query
"""

from pyats.topology import loader
from yang.connector.gnmi import Gnmi
from genie.libs.sdk.triggers.blitz.gnmi_util import GnmiMessageConstructor
from google.protobuf import json_format

def remove_missing_comp(device, namespace, xpath, via, alias, key_list, value_list=None):
    """
    Removes the missing components from the API that are absent in the GNMI query for MPTE automation
    
    Args:
        device (`obj`): Device object
        namespace ('str'): namespace xpath
        xpath ('str'): xpath
        key_list ('list'): components' name list
        value_list ('list'): components' value list, by default, set to None
    Returns:
        list: [list of components' name, list of components' value]
    Raises:
        None
    """

    device.connect(alias=alias, via=via)

    if type(namespace) == str:
        namespace = namespace.split(":",maxsplit=1)
        namespace = {namespace[0]:namespace[1]}

    content = {'namespace': namespace, 'nodes': [{'xpath': xpath}]}

    gmc = GnmiMessageConstructor('get', content)
    resp = device.gnmi.get(gmc.payload)
    resp = json_format.MessageToDict(resp)['notification'][0]['update']

    key_list_gnmi = []
    for ele in resp: key_list_gnmi.append(ele['path']['elem'][1]['key']['name'])

    key_list_edit = []
    value_list_edit = []

    for index, value in enumerate(key_list):
        if value in key_list_gnmi:
            key_list_edit.append(value)
            if value_list != None:
                value_list_edit.append(value_list[index])

    return [key_list_edit, value_list_edit]
