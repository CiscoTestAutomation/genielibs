"""Common verify functions for aaa"""

# Python
import logging
from genie.utils.timeout import Timeout

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
