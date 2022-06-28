# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

import logging
# Logger
log = logging.getLogger(__name__)

def get_software_version(device):
    """
    Get software version information of a device
    Args:
        device (obj): Device object
    Returns:
        str: Device software version information as str
    Raises:
        None
    """
    try:
        out = device.parse('show version')
    except SchemaEmptyParserError as e:
        log.error("Command 'show version' did not return any results: {e}".format(e=e))
        return None

    version = out.get('version')
    ver_loc = version.get('location') 
    ver_platform = version.get('platform') 
    ver_imageid = version.get('image_id') 
    ver_ver = version.get('version')
    ver_label = version.get('label') 
    ver_copy = version.get('copyright_years')
    ver_comp_date = version.get('compiled_date')
    ver_comp_by = version.get('compiled_by') 
    
    return f"Cisco IOS Software [{ver_loc}], {ver_platform} Software ({ver_imageid}), \
Experimental Version {ver_ver} {ver_label}\nCopyright (c) {ver_copy} by Cisco Systems, \
Inc.\nCompiled {ver_comp_date} by {ver_comp_by}"

