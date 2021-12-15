"""Common verify functions for aaa"""

# Python
import logging
from genie.utils.timeout import Timeout
from genie.libs.parser.iosxe.show_logging import ShowLogging

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


def verify_enable_password(device, password):
    
    """ To verify enable password
    Args:
        device (`obj`):   Device object
        password (`str`): password
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
    out = device.execute(cmd,reply=dialog,timeout=100,allow_state_change=True)
    
    if 'Access denied' not in out:
        logger.info('Enable password is successful')
        return True
    else:
        logger.error('Enable password is failed')
        return False


def verify_pattern_in_show_logging(device, pattern_list, exclude='', include='',
                                   output=None):
    """Verifies the pattern in show logging output
        Args:
            device (`obj`): Device object
            pattern_list (`list`): pattern list to be verified in the output
            exclude (`str`, optional): String to exclude from show logging
            include (`str`, optional): String to include from show logging
            output (`list`, optional): output of show logging in list
        Returns:
            True if pattern list matches in show logging output
            False if pattern list does not match in show logging output
    """
    if exclude:
        cmd = f'show logging | exclude {exclude}'
    elif include:
        cmd = f'show logging | include {include}'
    else:
        cmd = 'show logging'

    # parse the command
    output = device.parse(cmd, output=output)

    matched_pattern_list = []
    unmatched_pattern_list = []

    for p in pattern_list:
        if len(list(filter(p.match, output['logs']))) >= 1:
            matched_pattern_list.append(p)
        else:
            unmatched_pattern_list.append(p)

    if len(matched_pattern_list) == len(pattern_list):
        logger.debug(f"Verified the following regex patterns exist "
                    f"in show logging: {matched_pattern_list}")
        return True

    logger.debug(f"Failed to verify the following regex patterns exist "
                f"in show logging: {unmatched_pattern_list}")
    return False
