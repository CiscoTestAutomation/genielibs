"""Common verify functions for aaa"""

# Python
import logging
from genie.utils.timeout import Timeout
from genie.libs.parser.iosxe.show_logging import ShowLogging
import re
# unicon
from unicon.eal.dialogs import Dialog, Statement

logger = logging.getLogger(__name__)


def verify_show_run_aaa(device, config_list, timeout=100):
    """
    Verify that the configurations available in show run aaa
    Args:
        device ('obj'): Device object
        config_list ('list'): List of configuration command details
        timeout ('int): timeout value for the command execution
           ex.)
               cmd1 = '''aaa group server radius Test-VRf
                        server name Test-radius
                        ip vrf forwarding Mgmt-vrf
                        ip radius source-interface GigabitEthernet0/0
                        '''
                cmd2 = '''
                        aaa group server radius Test-radius
                        server name Test-server
                        ip vrf forwarding Mgmt-vrf
                        '''
                cmd3 = 'aaa group server radius rad1'

               config_list = [cmd1, cmd2, cmd3]
    Returns:
        True - if provided commands are available in 'show run aaa'
        False - if any of the provided commands are not available in 'show run aaa'
    """

    cmd = 'show run aaa'
    logger.info('verifying the config list : {}'.format(config_list))
    try:
        out = device.execute(cmd, timeout=timeout)
        out_set = set(filter(lambda l: l != '', list(map(lambda l: l.strip(), out.splitlines()))))

        for command in config_list:
            cmd_set = set(filter(lambda l: l != '', list(map(lambda l: l.strip(), command.split("\n")))))
            if cmd_set.issubset(out_set):
                continue
            else:
                logger.info('Command {} not found in show run aaa configuration'.format(cmd_set))
                return False

        return True

    except Exception as error:
        logger.warning('error {} occurred while verifying show run aaa config on device {}'.format(error, device))
        return False


def verify_pattern_in_output(output, pattern_list):
    """
        Verifies pattern list in output in sequence
        Args:
            output (str): Output string in which pattern needs to be verified
            pattern_list (list): List of patterns to verify in output
        Returns:
            bool
    """
    # construct the flags dict
    flag_dict = {'p' + str(i) + '_flag': False for i in range(1, len(pattern_list) + 1)}
    start_index = 1
    for line in output.splitlines():
        line = line.strip()
        # Check the first pattern
        if pattern_list[0].match(line):
            flag_dict['p1_flag'] = True

        # Check remaining patterns
        for i in range(start_index, len(pattern_list)):
            if flag_dict['p' + str(i) + '_flag'] and pattern_list[i].match(line):
                flag_dict['p' + str(i + 1) + '_flag'] = True
                start_index += 1
                break

        # verify whether all the patterns are matched
        if flag_dict['p' + str(len(pattern_list)) + '_flag']:
            return True

    return False


def verify_test_aaa_cmd(device, servergrp, username, password, path):

    """ To verify radius connectivity with test aaa command
    Args:
        device (`obj`): Device object
        servergrp (`str`): Radius server group name
        username (`str`): username
        password (`str`): password
        path (`str`): legacy/new-code
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    output = device.execute(
        "test aaa group {servergrp} {username} {password} {path}".\
            format(servergrp=servergrp,username=username,password=password,\
            path=path)
        )   
    return output


def verify_enable_password(device, password,privilege_level=None):
    
    """ To verify enable password
    Args:
        device (`obj`)         :   Device object
        password (`str`)       :   password
        privilege_level('int') :   privilege level
    Return:
        None
    Raise:
        SubCommandFailure: Failed enabling
    """
    
    dialog =Dialog([Statement(pattern = r"^.*RETURN to get started",
                              action = "sendline()",
                              args = None,
                              loop_continue = True,
                              continue_timer = False)])
    cmd = 'exit'
    out = device.execute(cmd,reply=dialog,timeout=100,allow_state_change=True)
    
    dialog =Dialog([Statement(pattern = r"^.*(P|p)assword: $",
                              action = "sendline({pw})".format(pw=password),
                              args = None,
                              loop_continue = True,
                              continue_timer = False)])          
    cmd = 'enable'
    if privilege_level :
        cmd+=f" {privilege_level}"
    out = device.execute(cmd,reply=dialog,timeout=100,allow_state_change=True)
    
    if 'Access denied' not in out:
        logger.info('Enable password is successful')
        return True
    else:
        logger.error('Enable password is failed')
        return False


def verify_pattern_in_show_logging(device, pattern_list, exclude='', include='',
                                   output=None, match_full_output=False):
    """Verifies the pattern in show logging output

    Args:
        device (obj): Device object
        pattern_list (list): List of regex patterns to verify (as strings)
        exclude (str, optional): String to exclude from show logging output
        include (str, optional): String to include from show logging output
        output (dict, optional): Parsed 'show logging' command output
        match_full_output (bool, optional): 
            If True, check patterns in the entire output dictionary.
            If False, check only in output['logs']

    Returns:
        True if all patterns are found, False if any are missing
    """
    if exclude:
        cmd = f'show logging | exclude {exclude}'
    elif include:
        cmd = f'show logging | include {include}'
    else:
        cmd = 'show logging'

    # parse the command if output is not passed
    if output is None:
        if match_full_output:
            output = device.execute(cmd)
        else:
            output = device.parse(cmd)

    matched_pattern_list = []
    unmatched_pattern_list = []

    if match_full_output:
        output_str = output if isinstance(output, str) else str(output)
        for p in pattern_list:
            pattern = re.compile(p)
            if re.search(pattern, output_str):
                matched_pattern_list.append(p)
            else:
                unmatched_pattern_list.append(p)
    else:
        # Use logs list for searching
        logs = output.get('logs', [])
        for p in pattern_list:
            pattern = re.compile(p)
            if any(re.search(pattern, line) for line in logs):
                matched_pattern_list.append(p)
            else:
                unmatched_pattern_list.append(p)

    if not unmatched_pattern_list:
        logger.debug(f"Verified patterns in show logging: {matched_pattern_list}")
        return True

    logger.debug(f"Failed to verify patterns in show logging: {unmatched_pattern_list}")
    return False


def verify_login_credentials_enable_password(device,username,password,enable_prompt=True,enable_password=None,enable_level=None):
    """Verifies the device login with credentials and enable password
        Args:
            device (`obj`)         : Device object
            username('str')        : username
            password('str')        : password
            enable_prompt('bool')  : default True.
            enable_password('str') : enable password
            enable_level('int')    : enable privilege level
        Returns:
            True if login succeeds.
            False if login fails.
    """  
    login_dialog_1 = Dialog(
        [
            Statement(
                pattern=r".*Press RETURN to get started.*",
                action=f"sendline()",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r'^.*([Uu]sername|[Ll]ogin): ?$',
                action=f"sendline({username})",
                loop_continue=True,
                continue_timer=False,
            ),
            Statement(
                pattern=r'^.*[Pp]assword( for )?(S+)?: ?$',
                action=f"sendline({password})",
                loop_continue=True,
                continue_timer=False,
            ),
        ]
    ) 
 
    try :
        out=device.execute("exit",reply=login_dialog_1,timeout=10,allow_state_change=True)
    except Exception as e :
        logger.info(f"login failed:\nexception is :\n{e}")
        return False            

    if enable_prompt and enable_password != None :     
        cmd1="enable"
        if enable_level:
             cmd1+=f" {enable_level}"
        login_dialog_2 = Dialog(
            [
                Statement(
                    pattern=r'^.*[Pp]assword( for )?(S+)?: ?$',
                    action=f"sendline({enable_password})",
                    loop_continue=True,
                    continue_timer=False,
                ),
            ]
        )
        try :
            out=device.execute(cmd1,reply=login_dialog_2,timeout=10,allow_state_change=True)
            if re.search(r'Access denied',out)  :
                logger.info("invalid enable password")      
                return False
        except Exception as e :    
            logger.info(f"login failed for the enable password:\n{e}")   
            return False 
    return True


def verify_access_session_detail(
        device, mac, interface, status=None, oper_host_mode=None,
        user_name=None, domain=None, ipv4_address=None, current_policy=None,
        server_policies=None, local_policies=None, oper_control_dir=None,
        method_status=None, max_time=60, check_interval=5, **kwargs):
    """
    Verifies if all the given parameters are correct for the access
    session client details.
    Args:
        device('obj'): Device object
        mac('str'): MAC address of the client
        interface('str'): Interface name
        status('str', optional): Authentication status of the client,
            default is None
        oper_host_mode('str', optional): Operational host mode of the
            client, default is None
        user_name('str', optional): Username of the client, default is None
        domain('str', optional): Domain of the client, default is None
        ipv4_address('str', optional): IPv4 address of the client,
            default is None
        current_policy('str', optional): Current policy applied on the
            client, default is None
        server_policies('dict', optional): Server policies applied on the
            client, default is None
        local_policies('dict', optional): Local policies applied on the
            client, default is None
        oper_control_dir('str', optional): Operational control direction
            of the client, default is None
        method_status('dict', optional): Method status of the client,
            default is None
        max_time('int', optional): Maximum time to wait for the
            verification to pass, default is 60 seconds
        check_interval('int', optional): Time interval between checks,
            default is 5 seconds
        **kwargs: Additional key-value pairs to verify in the client
            details
    Returns:
        True/False
    Raises:
        None
    """

    def __dict_compare(expect, actual):
        for k in expect:
            if k in actual:
                if isinstance(expect[k], dict) and \
                        isinstance(actual[k], dict):
                    if not __dict_compare(expect[k], actual[k]):
                        return False
                elif isinstance(expect[k], list) and \
                        isinstance(actual[k], list):
                    for element in expect[k]:
                        if element not in actual[k]:
                            return False
                elif expect[k] != actual[k]:
                    logger.debug(
                        f"{k} mismatch: expected {expect[k]}, "
                        f"actual {actual[k]}")
                    return False
            else:
                logger.debug(f"expect key {k} does not exist in {actual}")
                return False
        return True

    kwargs.update({
        k: v for k, v in {
            'status': status,
            'oper_host_mode': oper_host_mode,
            'user_name': user_name,
            'domain': domain,
            'ipv4_address': ipv4_address,
            'current_policy': current_policy,
            'oper_control_dir': oper_control_dir,
            'method_status': method_status,
            'server_policies': server_policies,
            'local_policies': local_policies,
        }.items()
        if v is not None
    })

    timeout = Timeout(max_time, check_interval)
    entry = {}
    while timeout.iterate():
        entry = device.api.get_access_session_interface_mac_detail(
            interface=interface, mac=mac)
        if entry:
            if __dict_compare(kwargs, entry):
                logger.debug(
                    'Access session entry is verified PASSED. '
                    f'Expected values: {kwargs}, actual values: {entry}')
                return True
        timeout.sleep()

    logger.debug(
        'Access session entry verification FAILED. '
        f'Expected values: {kwargs}, actual values: {entry}')
    return False


def verify_access_session_timeout_remaining(
        device, mac, interface, max_remain=15, min_remain=5,
        max_time=120, check_interval=2):
    """
    Verifies if the remaining time for the access session timeout is
    within the specified range.
    Args:
        device('obj'): Device object
        mac('str'): MAC address of the client
        interface('str'): Interface name
        max_remain('int'): Maximum remaining time for the access session
            timeout, default is 15 seconds
        min_remain('int'): Minimum remaining time for the access session
            timeout, default is 5 seconds
        max_time('int'): Maximum time to wait for the
            verification to pass, default is 120 seconds
        check_interval('int'): Time interval between checks,
            default is 2 seconds
    Returns:
        True/False
    Raises:
        None
    """

    timeout = Timeout(max_time, check_interval)
    remain_time = None
    while timeout.iterate():
        output = device.api.get_show_access_session_interface_detail(
            interface=interface)
        if output:
            entry = output.get('interfaces', {}).get(
                interface, {}).get('mac_address', {}).get(mac, {})
            remain_time_str = entry.get('session_timeout', {}).get(
                'remaining')
            remain_time = int(re.match(r"\d+", remain_time_str).group()) \
                if remain_time_str else None
            if remain_time is not None and \
                    min_remain <= remain_time <= max_remain:
                logger.debug(
                    'Access session timeout remaining time is within '
                    'the expected range. Expected range: '
                    f'{min_remain}-{max_remain} seconds, actual: '
                    f'{remain_time} seconds')
                return True
        timeout.sleep()
    logger.debug(
        'Access session timeout remaining time is NOT within the '
        f'expected range. Expected range: {min_remain}-{max_remain}')
    return False


def verify_access_session_removed(
        device, mac, interface, max_time=60, check_interval=5):
    """
    Verifies if the access session for the given MAC address on the
    specified interface does not exist.
    Args:
        device('obj'): Device object
        mac('str'): MAC address of the client
        interface('str'): Interface name
        max_time('int'): Maximum time to wait for the verification to pass,
            default is 60 seconds
        check_interval('int'): Time interval between checks,
            default is 5 seconds
    Returns:
        True/False
    Raises:
        None
    """

    timeout = Timeout(max_time, check_interval)
    entry = {}
    while timeout.iterate():
        entry = device.api.get_access_session_interface_mac_detail(
            interface=interface, mac=mac)
        if not entry:
            logger.debug(
                'Access session entry does not exist as expected.')
            return True
        timeout.sleep()
    logger.debug(
        'Access session entry still exists. Expected it to be removed.')
    return False
