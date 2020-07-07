"""Common verification functions for log"""

# Python
import logging
import re

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def is_logging_ospf_spf_logged(device, expected_spf_delay=None, ospf_trace_log=None,
                            max_time=60, check_interval=10):
    """
    Verify SPF change log

    Args:
        device('obj'): device to use
        expected_spf_delay('int'): SPF change value   
        ospf_trace_log('str') : OSPF trace log
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show log {ospf_trace_log}"
    while timeout.iterate():
        try:
            output = device.parse('show log {ospf_trace_log}'.format(
                ospf_trace_log=ospf_trace_log))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        file_content_list = output['file-content']

        # log message:
        # Jun 12 03:32:19.068983 OSPF SPF scheduled for topology default in 8s
        p = (
            '.*OSPF SPF scheduled for topology default in (?P<spf_change>\d+)s'
        )

        for i in file_content_list:
            m = re.match(p, i)
            if m:
                if int(m.groupdict()['spf_change']) == expected_spf_delay:
                    return True

        timeout.sleep()
    return False  