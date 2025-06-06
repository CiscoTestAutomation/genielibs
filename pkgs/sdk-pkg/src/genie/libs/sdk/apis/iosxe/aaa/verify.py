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

