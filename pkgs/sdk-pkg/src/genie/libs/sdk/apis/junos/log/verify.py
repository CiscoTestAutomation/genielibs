"""Common verification functions for log"""

# Python
import re
import logging
import operator

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
            r'.*OSPF SPF scheduled for topology default in (?P<spf_change>\d+)s'
        )

        for i in file_content_list:
            m = re.match(p, i)
            if m:
                if int(m.groupdict()['spf_change']) == expected_spf_delay:
                    return True

        timeout.sleep()
    return False

def verify_log_exists(device, file_name, expected_log,
                            max_time=120, check_interval=10, invert=False,
                            match=None):
    """
    Verify log exists

    Args:
        device('obj'): device to use  
        file_name('str') : File name to check log
        expected_log ('str'): Expected log message
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check
        invert ('bool', 'optional'): Inverts to check if it doesn't exist

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    op = operator.truth
    if invert:
        op = lambda val : operator.not_(operator.truth(val))

    timeout = Timeout(max_time, check_interval)

    # show commands: "show log {file_name}"
    while timeout.iterate():
        try:
            if match:
                cmd = 'show log {file_name} | match "{match}"'.format(
                    file_name=file_name,
                    match=match)
                output = device.execute(cmd)
                log_output = device.parse(cmd, output=output)
            else:
                log_output = device.parse('show log {file_name}'.format(
                    file_name=file_name))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        log_found = log_output.q.contains(
                    '.*{}.*'.format(expected_log), regex=True)

        if op(log_found):
            return True
        else:
            log_found = ''.join(log_output['file-content']).replace("'",'')
            if op(re.findall(r"{}".format(expected_log),log_found)):
                return True

        timeout.sleep()
    return False


def verify_no_log_output(device, file_name,max_time=60,
                         check_interval=10, invert=False, match=None, exclude=None):
    """
    Verify no log exists

    Args:
        device('obj'): device to use  
        file_name('str') : File name to check log
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check
        invert ('bool', 'optional'): Inverts to check if it doesn't exist
        match ('str' or 'list', 'optional'): used in show log command to specify output
        exclude ('str' or 'list', 'optional'): used in show log command to exclude output

    Returns:  
        Boolean       
    Raises:
        N/A    
    """

    timeout = Timeout(max_time, check_interval)

    cmd = ['show log {file_name}'.format(file_name=file_name), 'except "show log"']
    if match:
        if type(match) is str:
            cmd.append('match "{match}"'.format(match=match))
        elif type(match) is list:
            for m in match:
                cmd.append('match "{match}"'.format(match=m))

    if exclude:
        if type(exclude) is str:
            cmd.append('except "{exclude}"'.format(exclude=exclude))
        elif type(exclude) is list:
            for e in exclude:
                cmd.append('except "{exclude}"'.format(exclude=e))

    cmd = '|'.join(cmd)

    while timeout.iterate():
        log_output=""
        try:
            output = device.execute(cmd)
            if output:
                log_output = device.parse('show log {file_name}'.format(
                    file_name=file_name), output=output)
        except SchemaEmptyParserError:
            return True

        #"file-content": [
        #    "        show log messages",
        #    "        Mar  5 00:45:00 sr_hktGCS001 newsyslog[89037]: "
        #    "logfile turned over due to size>1024K",
        #    "        Mar  5 02:42:53  sr_hktGCS001 sshd[87374]: Received "
        #    "disconnect from 10.1.0.1 port 46480:11: disconnected by user",
        if not log_output:
            return True

        # {'file-content': ['', '', '', '', '{master}']}
        elif set(log_output['file-content']) == {'', '{master}'}:
            return True
        elif set(log_output['file-content']) == {'', ''}:
            return True

        timeout.sleep()
        continue

    return False


def verify_log_contain_keywords(device,
                                filename,
                                keywords,
                                max_time=60,
                                check_interval=10,
                                filter=None,
                                output=None,
                                invert=False):
    """
    Verify if keywords are in log messages

    Args:
        device(`obj`): device to use  
        filename(`str`) : File name to check log
        max_time (`int`): Maximum time to keep checking
        check_interval (`int`): How often to check
        filter (`bool`, optional): flag to use `match` to filter by keywords
                                   Default to None
        keywords (`list`, `str`): list of keywords to find
        output (`str`): output of show command. Default to None
        invert (`bool`): invert result. (check all keywords not in log)
                         Default to False

    Returns:  
        Boolean : if True, find the keywords in log
    Raises:
        N/A    
    """

    if not isinstance(keywords, list):
        keywords = [str(keywords)]

    # create match keywords which can be passed to show something | match {match_list}
    match_list = '|'.join(keywords)

    if filter:
        cmd = 'show log {file_name} | match "{match_list}"'.format(
            file_name=filename, match_list=match_list)
    else:
        cmd = 'show log {filename}'.format(filename=filename)

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(cmd, output=output)
        except SchemaEmptyParserError:
            return bool(invert)

        # example of out
        # {
        #   "file-content": [
        #     "Sep 18 16:14:45  P4 rpd[6962]: RPD_OSPF_NBRDOWN: OSPF neighbor 34.0.0.1 (realm ospf-v2 ge-0/0/0.0 area 0.0.0.0) state changed from Full to Down due to KillNbr (event reason: interface went down)",
        #     "Sep 18 16:14:45  P4 bfdd[6909]: BFDD_STATE_UP_TO_DOWN: BFD Session 34.0.0.1 (IFL 333) state Up -> Down LD/RD(32/16) Up time:23:52:11 Local diag: AdminDown Remote diag: None Reason: Received Upstream Destroy Session.",
        #     "Sep 18 16:16:09  P4 rpd[6962]: RPD_BGP_NEIGHBOR_STATE_CHANGED: BGP peer 3.3.3.3 (Internal AS 65000) changed state from Established to Idle (event HoldTime) (instance master)"
        #   ]
        # }

        # found : dictionary where storing key/value, keyword/match line
        # example:
        # found = {
        #     'RPD_OSPF_NBRDOWN': 'Sep 18 16:14:45  P4 rpd[6962]: RPD_OSPF_NBRDOWN: OSPF neighbor 34.0.0.1 (realm ospf-v2 ge-0/0/0.0 area 0.0.0.0) state changed from Full to Down due to KillNbr (event reason: interface went down)',
        # }
        found = {}
        for line in out.q.get_values('file-content'):
            line = line.strip()
            for kw in keywords:
                if kw in line or re.match(kw, line):
                    found[kw] = line

        if not invert and len(found) == len(keywords) or invert and not found:
            return True
        elif not invert:
            timeout.sleep()
        else:
            # in case of revert=True, no need to retry
            return False

    return False
