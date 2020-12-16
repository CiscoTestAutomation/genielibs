"""Common verify functions for ddos"""

# Python
import re
import logging
import operator

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_ddos_statistics(device, text, expected_value, max_time=60, check_interval=10):
    """Verify statictis via show ddos-protection statistics

    Args:
        device (object): Device object
        text (str): Given description of the key
        expected_value (str): Expected value 
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.

    Returns:
        bool: True/False
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show ddos-protection statistics')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        # Sample output
        # {
        #     "ddos-statistics-information": {
        #         "aggr-level-control-mode": "Drop",
        #         "aggr-level-detection-mode": "Automatic",
        #         "ddos-flow-detection-enabled": "No",
        #         "ddos-logging-enabled": "Yes",
        #         "ddos-policing-fpc-enabled": "Yes",
        #         "ddos-policing-re-enabled": "Yes",
        #         "detection-mode": "Automatic",
        #         "flow-report-rate": "100",
        #         "flows-cumulative": "0",
        #         "flows-current": "0",
        #         "packet-types-in-violation": "0",
        #         "packet-types-seen-violation": "0",
        #         "total-violations": "0",
        #         "violation-report-rate": "100"
        #     }
        # }
        
        keys_dict = {
            'Policing on routing engine': 'ddos-policing-re-enabled',
            'Policing on FPC': 'ddos-policing-fpc-enabled',               
            'Flow detection': 'ddos-flow-detection-enabled',
            'Logging': 'ddos-logging-enabled',                          
            'Policer violation report rate': 'violation-report-rate',  
            'Flow report rate':'flow-report-rate',
            'Default flow detection ': 'detection-mode',      
            'Default flow level detection ': 'aggr-level-detection-mode',
            'Default flow level control ': 'aggr-level-control-mode',
            'Currently violated packet types': 'packet-types-in-violation',
            'Packet types have seen violations': 'packet-types-seen-violation',
            'Total violation counts': 'total-violations',      
            'Currently tracked flows': 'flows-current',        
            'Total detected flows': 'flows-cumulative'                  
        }
        if text in keys_dict.keys():
            if out.q.get_values(keys_dict[text],0) == expected_value:
                return True

        timeout.sleep()
    return False