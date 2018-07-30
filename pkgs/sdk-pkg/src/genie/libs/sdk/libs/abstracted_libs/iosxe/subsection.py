# python
import re
import logging
from os import path

# unicon
from unicon.eal.dialogs import Statement, Dialog

# Genie
from genie.utils.timeout import Timeout

# Abstract
from genie.abstract import Lookup

# Parser
from genie.libs import parser
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.parser.iosxe.show_platform import ShowRedundancy, \
                                                  ShowVersion, \
                                                  ShowPlatform
# import ats
from ats import aetest
from ats.log.utils import banner
from ats.utils.objects import find, R

# import genie.libs
from genie.libs import sdk
from genie.libs.sdk.triggers.xe_sanity.checkcommands.libs\
    .iosxe.checkcommands import get_requirements

# module logger
log = logging.getLogger(__name__)


def enter_shell(device, timeout=60):
    """Enter shell prompt on IOSXE deivces by using command
    "request platform software system shell switch active R0"

    Args:
      Mandatory:
        device (`obj`) : Device object.
      Optional:
        timeout (`int`) : Command execution timeout.

    Returns:
        None

    Raises:
        None

    Example:
        >>> enter_shell(device=Device())
    """

    # Run workon.sh on the RP shell
    dialog = Dialog([
        Statement(pattern=r'continue\? +\[y\/n\]',
                            action='sendline(y)',
                            loop_continue=True,
                            continue_timer=False)
    ])
    # store original pattern
    enable_state = device.state_machine.get_state('enable')
    device.origin_pattern = enable_state._pattern
    # Completely remove the enable state pattern and update it with new pattern.
    enable_state._pattern = [r'(.*)\:\/]\$']
    # enter shell
    device.execute('request platform software system shell switch active R0', reply=dialog)
    

def exit_shell(device):
    """Exit shell prompt on IOSXE deivces by using command
    "exit"

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Returns:
        None

    Raises:
        None

    Example:
        >>> exit_shell(device=Device())
    """

    enable_state = device.state_machine.get_state('enable')

    # revert back the pattern
    enable_state._pattern = device.origin_pattern

    # get out of shell
    device.execute('exit')


def save_device_information(device, **kwargs):
    """Save running-configuration to startup-config.
    This is for general IOSXE devices.

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Raises:
        None

    Example:
        >>> save_device_information(device=Device())
    """
    # configure config-register
    device.configure('config-register 0x2102')

    # save all configuration to startup for all slots        
    dialog = Dialog([
        Statement(pattern=r'Destination +filename +\[.*\].*',
                            action='sendline()',
                            loop_continue=True,
                            continue_timer=False)
    ])
    device.execute('copy running-config nvram:startup-config',
                        reply=dialog)
    device.execute('write memory')

def stack_ha_redundancy_state(device, timeout, platform_pts=None):
    """Stack HA Redundancy SSO State Check.

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Returns:
        None

    Raises:
        Exception: When show redundancy parser is errored
        AssertionError: When expected status is not reached

    Example:
        >>> early_stack_ha_redundancy_state(device=Device('R1'),
                timeout=timeout)
    """
    # check first from pts to see if the redundancy is ready
    if platform_pts and hasattr(platform_pts, 'redundancy_mode') and \
        'sso' in platform_pts.redundancy_mode and \
        hasattr(platform_pts, 'redundancy_communication') and \
        platform_pts.redundancy_communication:
        log.info('System redundancy mode is sso and redundancy_communication is enabled')
        pass_flag = True
    else:
        # learn it from show version in loop
        while timeout.iterate():

            # initial flag
            pass_flag = True

            # get output from show redundancy
            try:
                output = ShowRedundancy(device).parse()
            except Exception as e:
                raise Exception('Cannot get output from "show redundancy"',
                    from_exception=e)

            # Check if HA redundancy status is sso
            try:
                if 'sso' not in output['red_sys_info']['conf_red_mode'] or \
                   'Up' not in output['red_sys_info']['communications'] or \
                   'Duplex' not in output['red_sys_info']['hw_mode']:
                    log.warning('The System does not reach to "sso"')
                    timeout.sleep()
                    pass_flag = False
                    continue
                for slot in output['slot']:
                    if 'ACTIVE' not in output['slot'][slot]['curr_sw_state'] and \
                       'STANDBY HOT' not in output['slot'][slot]['curr_sw_state']:
                        log.warning('The {} does not reach to "ACTIVE|STANDBY HOT"'
                                    .format(slot))
                        timeout.sleep()
                        pass_flag = False
                        continue
            except Exception as e:
                log.warning(e)
                timeout.sleep()
                pass_flag = False
                continue
            break

    if not pass_flag:
        raise AssertionError('Redundancy status does not reach to "SSO"',
                from_exception=e)

def process_check(device):
    """Verify that all critical process are up and running

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Returns:
        None

    Raises:
        Exception: Cannot enter into shell get the output
        AssertionError: When expected status is not reached
        AttributeError: Process is not in the output

    Example:
        >>> process_check(device=Device())
    """
    
    def parse_shell_process_output(output):
        """parse the output from shell command "workon.sh RP 0 status"

        Args:
          Mandatory:
            output (`str`) : Device output.

        Returns:
            Dictionary

        Raises:
            None

        Example:
            >>> parse_shell_process_output(output=
                '''run_caf_sh      unavail      (respawn:global:optional)''')
            >>> {'run_caf_sh': {'state': 'up',
                                'options': 'respawn:global:optional'}}
        """
        # initial return dictionary
        ret_dict = {}

        # set pattern
        p = re.compile(r'^(?P<name>[\w\_\-]+) +(?P<state>(up|unavail)) +'
                '\((?P<options>[\w\:\_\-]+)\)$')

        for line in output.splitlines():
            line = line.strip()
            # auto_upgrade_client_sh           up      (respawn:global:optional)
            #  run_caf_sh      unavail      (respawn:global:optional)
            m = p.match(line)
            if m:
                group = m.groupdict()
                name = group.pop('name')
                ret_dict.setdefault(name, {}).update(
                    {k:v for k,v in group.items()})
        return ret_dict

    # get into shell
    try:
        enter_shell(device)
    except Exception as e:
        raise Exception(e)

    # get output from shell
    try:
        out = device.execute('workon.sh RP 0 status', timeout=60)
    except Exception as e:
        raise Exception(e)

    # exit shell
    try:
        exit_shell(device)
    except Exception as e:
        raise Exception(e)

    # parse shell output
    ret = parse_shell_process_output(out)
    if not ret:
        raise Exception('No Processes found in the output')

    # check below processes
    process_list = ['fman_rp', 'hman', 'linux_iosd_image', 'sif_mgr',
                    'periodic_sh', 'platform_mgr', 'plogd', 'psd',
                    'sort_files_by_inode_sh','stack_mgr']

    # check each process's status is up
    for process in process_list:
        if process in ret:
            if 'up' not in ret[process]['state']:
                log.warning('Process {p} is {s}, should be up!!!'
                    .format(p=process, s=ret[process]['state']))
                raise AssertionError('Process {p} is {s}, should be up!!!'
                    .format(p=process, s=ret[process]['state']))
            else:
                log.info('Process {p} is {s} as expected.'
                    .format(p=process, s=ret[process]['state']))
        else:
            log.warning('Process {p} is not found'.format(p=process))
            raise AttributeError('Process {p} is not found'.format(p=process))

    for process in ['btrace_rotate_sh', 'btrace_rotate', 'btman', 'btrace_manager']:
        try:
            if 'up' not in ret[process]['state']:
                raise AssertionError('Process {p} is {s}, should be up!!!'
                    .format(p=process, s=ret[process]['state']))
            else:
                btrace_failed = False
                log.info('Process {p} is {s} as expected.'
                    .format(p=process, s=ret[process]['state']))
                break
        except Exception:
            btrace_failed = True
            continue

    # check btrace process states
    if btrace_failed:
        log.warning('Process btrace_rotate_sh is not found in the output')
        raise AttributeError('Process btrace_rotate_sh is not found in the output')

def chasfs_properties(device, timeout):
    """Verify that Chasfs properties are updated by Stack Manager

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Returns:
        None

    Raises:
        AssertionError: When expected status is not reached
        AttributeError: Active/Standby switch missing from the list
        Exception: Cannot get into shell

    Example:
        >>> chasfs_properties(device=Device())
    """
    # get full stack/active stacks/active/standby
    if device.active and device.standby:
        # print out the expected stack information
        log.info('Expected Stack State:\n'
                 'Master(Active RP): {}\nStandby: {}\nMembers:{}'
                 .format(device.active, device.standby,device.members))
    else:
        raise AttributeError('There is no Active/Standby '
            'switches on device {}'.format(device.name))

    # get into shell
    try:
        enter_shell(device)
    except Exception as e:
        raise Exception(e)

    # create check mapping for what should check for each command
    # {command: check_pattern}
    switch_check_mapping = {
        'mode': {
            'command': 'echo -n chassis_role{n}:; cat /tmp/chassis/{n}/chassis_role; echo;',
            'pattern': 'chassis_role{n}\:(?P<value>{role})'
        },
        'state': {
            'command': 'echo -n chassis_state{n}:; cat /tmp/chassis/{n}/state; echo;',
            'pattern': 'chassis_state{n}\:(?P<value>compatible)'
        },
        'MAC address': {
            'command': 'echo -n macaddr{n}:; cat /tmp/chassis/{n}/macaddr; echo;',
            'pattern': 'macaddr{n}: *(?P<value>{mac_p})'
        }
    }
    system_check_mapping = {
        'Local comm_up': {
            'command': 'echo -n local_comm_up:;cat /tmp/chassis/local/stack_mgr/comm_up; echo;',
            'pattern': 'local_comm_up:(?P<value>success)'        
        },
        'active controller': {
            'command': 'echo -n local_rp_mastership_global-active-rp:;cat /tmp/chassis/'\
                       'local/rp/chasfs/mastership/global-active-rp; echo;',
            'pattern': 'local_rp_mastership_global\-active\-rp:(?P<value>[0-9]\/rp)'        
        },
        'standby controller': {
            'command': 'echo -n local_rp_mastership_global-standby-rp:;cat /tmp/chassis/'\
                       'local/rp/chasfs/mastership/global-standby-rp; echo;',
            'pattern': 'local_rp_mastership_global\-standby\-rp:(?P<value>[0-9]\/rp)'
        },
        'standby': {
            'command': 'echo -n local_rp_mastership_standby-rp-ehsa-state:;cat /tmp/'\
                       'chassis/local/rp/chasfs/mastership/standby-rp-ehsa-state; echo;',
            'pattern': 'local_rp_mastership_standby\-rp\-ehsa\-state:(?P<value>standby)'        
        },
        'sso-ready': {
            'command': 'echo -n local_rp_mastership_standby-rp-state:;cat /tmp/chassis/local/'\
                       'rp/chasfs/mastership/standby-rp-state; echo;',
            'pattern': 'local_rp_mastership_standby\-rp\-state:(?P<value>sso\-ready)'        
        }    
    }
    mac_pattern = '(?:(?:[0-9A-Fa-f]){2}[:-]){5}(?:[0-9A-Fa-f]){2}'

    while timeout.iterate():

        # initial flag
        pass_flag = True

        # Check active|standby|members: role, state, mac
        for key, item in switch_check_mapping.items():

            # compose the slots dictionary
            slots = {'controller': device.active, 'controller': device.standby}
            slots.update({'member': v for v in device.members})

            # check each slots
            for role, switch in slots.items():
                # get the output from shell                
                try:
                    out = device.execute(item['command'].format(n=switch), timeout=60)
                    out = out.splitlines()[-2].strip()
                except Exception:
                    out = ''

                # match the pattern
                if 'MAC' in key:
                    p = re.compile(r'{}'.format(item['pattern']\
                            .format(n=switch, mac_p=mac_pattern)))
                elif 'mode' in key:
                    p = re.compile(r'{}'.format(item['pattern']\
                            .format(n=switch, role=role)))
                else:
                    p = re.compile(r'{}'.format(item['pattern']\
                            .format(n=switch)))
                m = p.match(out)
                if m:
                    log.info('{k} is as expected: {v}'
                        .format(k=key, v=m.groupdict()['value']))
                else:
                    log.warning('{k} is not as expected.\nexpected: {e}\npoll value: {v}'
                        .format(k=key, e=p.pattern, v=out))
                    pass_flag = False
                    break

        # Check system: state, local common_up, controller, sso-ready
        for key, item in system_check_mapping.items():
            # get the output from shell
            try:
                out = device.execute(item['command'], timeout=60)
                out = out.splitlines()[-2].strip()
            except Exception:
                out = ''
            p = re.compile(r'{}'.format(item['pattern']))
            m = p.match(out)
            if m:
                log.info('{k} is as expected: {v}'
                    .format(k=key, v=m.groupdict()['value']))
            else:
                log.warning('{k} is not as expected.\nexpected: {e}\npoll value: {v}'
                    .format(k=key, e=p.pattern, v=out))
                pass_flag = False
                break
        if pass_flag:
            break
        else:            
            timeout.sleep()
            continue

    # exit shell
    try:
        exit_shell(device)
    except Exception as e:
        raise Exception(e)

    if not pass_flag:
        raise AssertionError('Chasfs state Cannot stabilized')


def learn_system(device, steps, platform_pts=None):
    """Learn and store the system properties

       Args:
           testbed (`obj`): Testbed object

       Returns:
           None

       Raises:
           pyATS Results
    """

    # learn show version
    if not platform_pts:
        with steps.start("Store image type/router type from 'show version' on {}"
          .format(device.name)) as step:
            try:
                output = ShowVersion(device=device).parse()
                device.image_type = output['version']['image_type']
                device.router_type = output['version']['rtr_type']
            except Exception as e:
                log.warning(e)
                step.passx('Cannot get required router info on {}'.format(device.name))

            log.info('Image type: {}\nRouter type: {}'
                        .format(device.image_type, device.router_type))

        # learn show version
        with steps.start("Store switches info from 'show platform' on {}"
          .format(device.name)) as step:

            req = {'active': [['slot', '(?P<switch>.*)', 'rp', '(.*)', 'role', 'Active']],
                   'standby': [['slot', '(?P<switch>.*)', 'rp', '(.*)', 'role', 'Standby']],
                   'members': [['slot', '(?P<switch>.*)', 'rp', '(.*)', 'role', 'Member']]}

            try:
                output = ShowPlatform(device=device).parse()
                ret = get_requirements(requirements=req, output=output)
                device.active = ret['active'][0]['switch']
                device.standby = ret['standby'][0]['switch']
                device.members = [i['switch'] for i in ret['members']]
            except Exception as e:
                log.warning(e)
                step.passx('Cannot get required router info on {}'.format(device.name))

            log.info('Active Switch: {}\nStandby Switch: {}\nMember Switch: {}'
                        .format(device.active, device.standby, device.members))
    else:
        with steps.start("Store image type/router type from PTS on {}"
          .format(device.name)) as step:
            try:
                # device.image_type = platform_pts.image_type
                device.image_type = 'developer image'
                device.router_type = platform_pts.rtr_type
            except Exception as e:
                log.warning(e)
                step.passx('Cannot get required router info on {}'.format(device.name))

            log.info('Image type: {}\nRouter type: {}'
                        .format(device.image_type, device.router_type))

        with steps.start("Store switches info from PTS on {}"
          .format(device.name)) as step:

            req = {'active': [['slot', 'rp', '(?P<switch>.*)', 'swstack_role', 'Active'],
                              ['slot', 'rp', '(?P<switch>.*)', 'state', 'Ready']],
                   'standby': [['slot', 'rp', '(?P<switch>.*)', 'swstack_role', 'Standby'],
                              ['slot', 'rp', '(?P<switch>.*)', 'state', 'Ready']],
                   'members': [['slot', 'rp', '(?P<switch>.*)', 'swstack_role', 'Member'],
                              ['slot', 'rp', '(?P<switch>.*)', 'state', 'Ready']]}

            try:
                ret = get_requirements(requirements=req, output=platform_pts)
                device.active = ret['active'][0]['switch']
                device.standby = ret['standby'][0]['switch']
                device.members = [i['switch'] for i in ret['members']]
            except Exception as e:
                log.warning(e)
                step.passx('Cannot get required switches info on {}'.format(device.name))

            log.info('Active Switch: {}\nStandby Switch: {}\nMember Switch: {}'
                        .format(device.active, device.standby, device.members))

def get_default_dir(device):
    """ Get the default directory of this device

        Args:
          Mandatory:
            device (`obj`) : Device object.

        Returns:
            default_dir (`str`): Default directory of the system

        Raises:
            Exception

        Example:
            >>> get_default_dir(device=device)
    """

    try:
        lookup = Lookup.from_device(device)
        parsed_dict = lookup.parser.show_platform.Dir(device=device).parse()
        default_dir = parsed_dict['dir']['dir'].replace('/', '')
    except SchemaEmptyParserError as e:
        raise Exception("No output when executing 'dir' command") from e
    except Exception as e:
        raise Exception("Unable to execute or parse 'dir' command") from e

    # Return default_dir to caller
    log.info("Default directory on '{d}' is '{dir}'".format(d=device.name,
                                                            dir=default_dir))
    return default_dir


@aetest.subsection
def check_xe_sanity_device_ready(self, testbed, steps,
    max_time=60, interval=10):
    """Check redudancy status, critial processes status and chassis properties

       Args:
           testbed (`obj`): Testbed object
           steps (`obj`): aetest steps object

       Returns:
           None

       Raises:
           pyATS Results
    """    
    log.info(banner('Check redudancy status,\n'
        'critial processes status,\n'
        'chassis properties'))
    # get uut
    devices = testbed.find_devices(alias='uut')

    for uut in devices:
        lookup = Lookup.from_device(uut)
        # get platform pts
        
        platform_pts = self.parameters.get('pts', {}).get('platform', {}).get('uut', None)

        # check redudancy
        with steps.start("Perform Redundancy Check on device {} - "
            "to check if device reach 'SSO' status".format(uut.name)) as step:

            # create timeout object
            timeout = Timeout(max_time=int(max_time),
                              interval=int(interval))
            try:
                lookup.sdk.libs.abstracted_libs\
                  .subsection.stack_ha_redundancy_state(
                      device=uut, timeout=timeout, platform_pts=platform_pts)
            except Exception as e:
                step.passx('Redundancy state SSO not reached in the stack',
                            from_exception=e)
        # check Process
        with steps.start("Verify that all critical process are up "
          "and running on device {}".format(uut.name)) as step:
            try:
                lookup.sdk.libs.abstracted_libs\
                  .subsection.process_check(device=uut)
            except Exception as e:
                step.passx('Processes verification test failed')

        # check Chasfs
        with steps.start("Verify that Chasfs properties are updated "
          "by Stack Manager on device {}".format(uut.name)) as step:
            try:
                lookup.sdk.libs.abstracted_libs\
                  .subsection.chasfs_properties(device=uut, timeout=timeout)
            except Exception as e:
                step.passx('Chasfs verification test failed\n{}'.format(e))
