"""Utility type functions that do not fit into another category"""

# Python
import re
import logging
import datetime
import operator

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

def verify_file_details_exists(device,
                               root_path,
                               file,
                               max_time=30,
                               check_interval=10,
                               invert=False):
    """ Verify file details exists

        Args:
            device ('obj'): Device object
            root_path ('str'): Root path for command
            file ('str'): File name
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
            invert ('bool', optional): Invert to check for file absense, default: False
        Returns:
            Boolean
        Raises:
            None
    """
    op = operator.truth
    if invert:
        op = lambda file_found : operator.not_(operator.truth(file_found))

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
        if op(file_found):
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
            int
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

def delete_file_on_device(device, file_name):
    """ Deletes file on device

    Args:
        device (obj): Device object
        file_name ('str'): File name
    """
    try:
        device.execute('file delete {}'.format(file_name))
    except Exception as e:
        raise Exception('Failed to delete file: {e}'.format(e=str(e)))

def get_file_timestamp(device, root_path, file):
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

    file_info_list = out.get('directory-list', {}).get('directory', {}).get('file-information')

    for file_info_dict in file_info_list:
        if file_info_dict.get('file-name') == file:
            timestamp = file_info_dict.get('file-date', {}).get('@junos:format')
            if not timestamp:
                return None
            timestamp = re.sub(' +', ' ', timestamp)
            return datetime.datetime.strptime(timestamp, "%b %d %H:%M")\
                            .replace(year=datetime.datetime.now().year)

    return None

def get_system_users(device):
    """ Get list of users via show system user

        Args:
            device ('obj'): Device object

        Returns:
            result (`list`): Get list of username and ip address pairs

        Raises:
            N/A
    """
    user_list = []

    try:
        output = device.parse('show system users')
    except SchemaEmptyParserError:
        return user_list

    # schema = {
    #     "user-table": {
    #         "user-entry": [
    #             {
    #                 "command": str,
    #                 "from": str,
    #                  ...

    user_table = Dq(output).get_values('user-entry')
    if user_table:
        for user in user_table:
            user_list.append({user['user']: user['from']})
    return user_list

def get_system_connections_sessions(device):
    """ Get list of system connections via show system connections

        Args:
            device ('obj'): Device object

        Returns:
            result (`list`): Get list of system connection sessions

        Raises:
            N/A
    """
    connections = []

    try:
        output = device.parse('show system connections')
    except SchemaEmptyParserError:
        return connections

    # "output": {
    #     "connections-table": [
    #         {
    #             "proto": str,
    #             "recv-Q": str,
    #             "send-Q": str,
    #             "local-address": str,
    #             "foreign-address": str,
    #             "state": str,
    #         }
    #         ...

    connections = Dq(output).get_values('connections-table')
    return connections

def execute(device, command, alternative_command=None, fail_regex=None):
    """ Execute command to device

        Args:
            device ('obj'): Device object
            command ('str'): Command with a higher priority
            alternative_command ('str'): An alternative command that would be executed if the given command creates an error
        
        Returns:
            output which is generated by command
            
        Raises:
            N/A or SubCommandFailure       
    """  
    out = None
    try:
        out = device.execute(command)
        if fail_regex:
            if re.search(fail_regex, out):
                raise SubCommandFailure('failed regex has been hit, trying alternative command')
    except SubCommandFailure:
        try:
            if alternative_command:
                out = device.execute(alternative_command)
            else:
                raise SubCommandFailure('Please provide an alternative command to execute.')
        except SubCommandFailure as e:
            raise SubCommandFailure("Both command '{command}' and alternative command '{alternative_command}' failed to execute.".format(
                                        command=command,
                                        alternative_command=alternative_command))
    return out

def request_login_other_re(device):
    """ Execute 'request routing-engine login other-routing-engine'
        
        Args:
            device ('obj'): Device object

        Returns:
            bool

        Raises:
            N/A
    """
    try:
        output = device.execute('request routing-engine login other-routing-engine')
        p = re.compile(r'^[\s\S]*(No +route +to +host)[\s\S]*$')
        if p.match(output):
            return False
    except Exception as e:
        return False
    return True

def quick_configure_by_jinja2(device, templates_dir, template_name, **kwargs):
    """Configure device with Jinja2 using a quick method

    Args:
            device ('obj'): Device object
            templates_dir ('str'): Template directory
            template_name ('str'): Template name
            kwargs ('obj'): Keyword arguments
        Returns:
            Boolean
        Raises:
            None
    """

    log.info("Configuring {filename} on {device}".format(
        filename=template_name,
        device=device.alias))
    template = device.api.get_jinja_template(
        templates_dir=templates_dir,
        template_name=template_name)
    if not template:
        raise Exception('Could not get template')

    device.state_machine.go_to('config', device.spawn)
    device.sendline('load set terminal')
    device.sendline(template.render(**kwargs))
    device.sendline('\x04')
    device.execute('commit synchronize')
    device.state_machine.go_to('enable', device.spawn)

    
def get_show_output_line_count(device, command, output=None):
    """ Count number of line from show command output

        Args:
            device (`obj`): Device object
            command (`str`): show command
            output (`str`): output of show command. Default to None
        
        Returns:
            line_count (`int`): number of lines based on show command output
            
        Raises:
            N/A
    """  
    out = None
    try:
        if output:
            out = output
        else:
            out = device.execute(command+" | count")
    except SubCommandFailure as e:
        log.warn("Couldn't get line count properly: {e}".format(e=e))
        return 0

    p = re.compile(r'^Count:\s+(?P<line_count>\d+)\s+lines')

    for line in out.splitlines():
        line = line.strip()

        m = p.match(line)
        if m:
            return int(m.groupdict()['line_count'])

    log.warn("Couldn't get line count properly.")
    return 0
