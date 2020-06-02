"""Utility type functions that do not fit into another category"""

# Python
import re
import logging

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils import Dq
from genie.utils.timeout import Timeout
# Pyats
from pyats.utils.objects import find, R

# unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def verify_ping(
        device,
        address,
        loss_rate=0,
        count=None,
        max_time=30,
        check_interval=10):
    """ Verify ping loss rate on ip address provided

        Args:
            device ('obj'): Device object
            address ('str'): Address value
            loss_rate ('int'): Expected loss rate value
            count ('int'): Count value for ping command
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            Boolean
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if count:
            cmd = 'ping {address} count {count}'.format(
                address=address,
                count=count
            )
        else:
            cmd = 'ping {address}'.format(
                address=address
            )
        try:
            out = device.parse(cmd)
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue
        # Example dictionary structure:
        #     {
        #         "ping": {
        #             "address": "10.189.5.94",
        #             "data-bytes": 56,
        #             "result": [
        #                 {
        #                     "bytes": 64,
        #                     "from": "10.189.5.94",
        #                     "icmp-seq": 0,
        #                     "time": "2.261",
        #                     "ttl": 62
        #                 },
        #             ],
        #             "source": "10.189.5.94",
        #             "statistics": {
        #                 "loss-rate": 0,
        #                 "received": 1,
        #                 "round-trip": {
        #                     "avg": "2.175",
        #                     "max": "2.399",
        #                     "min": "1.823",
        #                     "stddev": "0.191"
        #                 },
        #                 "send": 1
        #             }
        #         }
        #     }
        loss_rate_found = Dq(out).get_values("loss-rate", 0)

        if loss_rate_found == loss_rate:
            return True
    return False

def verify_file_details_exists(device, root_path, file, max_time=30, check_interval=10):
    """ Verify file details exists

        Args:
            device ('obj'): Device object
            root_path ('str'): Root path for command
            file ('str'): File name
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            Boolean
        Raises:
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('file list {root_path} detail'.format(
                root_path=root_path
            ))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue
        file_found = Dq(out).contains_key_value(
            'file-name', file, 
            value_regex=True)
        if file_found:
           return True
        timeout.sleep()
    
    return False

def get_file_size(device, root_path, file):
    """ Get file size from device

        Args:
            device ('obj'): Device object
            root_path ('str'): Root path for command
            file ('str'): File name
        Returns:
            Boolean
        Raises:
            None
    """
    out = None
    out = device.parse('file list {root_path} detail'.format(
            root_path=root_path
        ))
    file_info_list = out.q.contains('{}|file-size'.format(file), 
        regex=True).get_values('file-information')
    
    for file in file_info_list:
        if 'file-name' in file and 'file-size' in file:
            return int(file['file-size'])
    return None
