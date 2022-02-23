"""Common verify functions for show issu incompatibility status"""

import logging

from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_issu_incompatibility_status(device, image, max_time=100, check_interval=5):
    """
    verify that Incompatibilty status is sucess on the device
    Args:
       device (`obj`): Device object
       image : image name 
       max_time : maximum time interval
       check_interval : check interval
    Returns:
    boolean  
    Raises:
       None
    """	
 
    timeout = Timeout(max_time, check_interval)
    cmd = "show incompatibility nxos {}".format(image)
    while timeout.iterate():
        try:
           output = device.parse(cmd,timeout = 100)
        except SchemaEmptyParserError as e:
           timeout.sleep()
           continue
    
        if 'incompatible_configuartion_list' not in output.keys():
           log.debug(" No incompitable configuration exist ")
           return True

    log.debug("Incompatibility configurations  : {}".format(dict(output['incompatible_configuartion_list'])))
    return False
    
