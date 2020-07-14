"""Utility type functions that do not fit into another category"""

# Python
import re
import logging
import datetime

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


def verify_ping(device,
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
            cmd = 'ping {address} count {count}'.format(address=address,
                                                        count=count)
        else:
            cmd = 'ping {address}'.format(address=address)
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


def verify_file_details_exists(device,
                               root_path,
                               file,
                               max_time=30,
                               check_interval=10):
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
            out = device.parse(
                'file list {root_path} detail'.format(root_path=root_path))
        except SchemaEmptyParserError as e:
            timeout.sleep()
            continue
        file_found = Dq(out).contains_key_value('file-name',
                                                file,
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
    out = device.parse(
        'file list {root_path} detail'.format(root_path=root_path))
    try:
        file_info_list = out.q.contains(
            '{}|file-size'.format(file),
            regex=True).get_values('file-information')

        for file_info_dict in file_info_list:
            if 'file-name' in file_info_dict and 'file-size' in file_info_dict:
                return int(file_info_dict['file-size'])
    except:
        file_info_list = Dq(out).get_values('file-information')

        for file_info_dict in file_info_list:
            if file == file_info_dict.get('file-name'):
                return int(file_info_dict.get('file-size', 0))

    return None

def verify_diff_timestamp(device, expected_spf_delay=None, ospf_trace_log=None,\
                       max_time=60, check_interval=10):
    """
    Verify the difference between time on two logs

    Args:
        device('obj'): device to use
        expected_spf_delay('float'): SPF change value   
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

        # Example parsed output:
        #
        # {
        #     "file-content": [
        #     "        show log messages",
        #     "        Mar  5 00:45:00 sr_hktGCS001 newsyslog[89037]: "
        #     "logfile turned over due to size>1024K",
        #     "        Mar  5 02:42:53  sr_hktGCS001 sshd[87374]: Received "
        #     "disconnect from 10.1.0.1 port 46480:11: disconnected by user",
        #     "        Mar  5 02:42:53  sr_hktGCS001 sshd[87374]: "
        #     "Disconnected from 10.1.0.1 port 46480",
        #     "        Mar  5 02:42:53  sr_hktGCS001 inetd[6841]: "
        #     "/usr/sbin/sshd[87371]: exited, status 255",
        # }

        file_content_list = output['file-content']

        scheduled_time = start_time = datetime.datetime.now()

        for i in file_content_list:
            scheduled_time_str = device.api.get_ospf_spf_scheduled_time(i)
            if scheduled_time_str:
                scheduled_time = datetime.datetime.strptime(
                    scheduled_time_str, '%H:%M:%S.%f')

            start_time_str = device.api.get_ospf_spf_start_time(i)
            if start_time_str:
                start_time = datetime.datetime.strptime(
                    start_time_str, '%H:%M:%S.%f')

            time_change = (start_time - scheduled_time).seconds
            if time_change == expected_spf_delay:
                return True

        timeout.sleep()
    return False


def verify_file_size(device,
                     root_path,
                     file,
                     file_size,
                     max_time=30,
                     check_interval=10):
    """ Verify specified file size

    Args:
        device (obj): Device object
        root_path (str): Root path
        file (str): File name
        file_size (int): File size
        max_time (int, optional): Maximum sleep time. Defaults to 30.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse(
                'file list {root_path} detail'.format(root_path=root_path))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        file_info_list = Dq(out).get_values('file-information')

        for file_info_dict in file_info_list:
            if file == file_info_dict.get('file-name'):
                if int(file_info_dict.get('file-size', 0)) == int(file_size):
                    return True

    return False
