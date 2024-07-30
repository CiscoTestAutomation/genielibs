''' Common Execute functions for IOX / app-hosting '''

# Python
import logging
import re
import time

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import SubCommandFailure

from genie.metaparser.util.exceptions import SchemaMissingKeyError

# Import parser
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)


def execute_change_installed_application_state(device, app_id, target_state, wait_timer=2):
    """
    Api to change the state of installed Application to target state
        Args:
            device ('obj') : Device object
            app_id ('str'): abort timer value
            target_state ('str') : target state of app_id (UNINSTALLED/DEPLOYED/ACTIVATED/RUNNING/STOPPED)
            wait_timer ('int', optional'):  interval timer ( default 2)) 
        Returns:
            None
        Raises:
            SubCommandFailure    
    """

    target_state = target_state.upper()
    current_state = ""
    applist = {}

    try:
        applist = device.parse('show app-hosting list')
    except SchemaMissingKeyError:
        log.error(f"No Application Found. It may not be installed")
        return False

    if applist:
        if app_id in applist['app_id']:
            current_state = applist['app_id'][app_id]['state']
            log.info(f'{app_id} has a current state {current_state} and target state is {target_state}')
        else:
            log.info(f"{app_id} not found in list of running applications")
            return False

    if target_state == current_state:
        log.info(f'{app_id} has same current state and target state is: {target_state}')
        return True

    if current_state == 'UNINSTALLED':
        # if current state is uninstalled exit
        log.error(f'{app_id} is not installed to change state')
        return False
    elif current_state == 'INSTALLING':
        log.error(f"Please wait for {app_id} to finish installing...")
        return False

    # States sequece is maintained based on the sequence of occurrence
    state_index = ['UNINSTALLED', 'DEPLOYED', 'ACTIVATED', 'RUNNING', 'STOPPED']

    current_state_index = state_index.index(current_state)
    target_state_index = state_index.index(target_state)

    if current_state == 'STOPPED':
        # bring the current state to the target state using the IOS commands required
        try:
            if target_state == 'DEPLOYED':
                device.execute('app-hosting deactivate appid %s' % app_id)
            elif target_state == 'UNINSTALLED':
                device.execute('app-hosting deactivate appid %s' % app_id)
                device.execute('app-hosting uninstall appid %s' % app_id)
                current_state = 'UNINSTALLED'
            elif target_state == 'ACTIVATED':
                device.execute('app-hosting activate appid %s' % app_id)
            elif target_state == 'RUNNING':
                device.execute('app-hosting start appid %s' % app_id)
            time.sleep(wait_timer)
        except SubCommandFailure:
            raise SubCommandFailure(f"Could not change application state for {app_id}")
        if current_state == 'UNINSTALLED' and target_state == 'UNINSTALLED':
            log.info(f'State of {app_id} changed to Target state {target_state}')
            return True
    else:
        # determine order of list traversal
        if target_state_index > current_state_index:
            for _ in state_index:
                if current_state != target_state:
                    # advance the device to the next application state
                    try:
                        if current_state == 'DEPLOYED':
                            device.execute('app-hosting activate appid %s' % app_id)
                        elif current_state == 'ACTIVATED':
                            device.execute('app-hosting start appid %s' % app_id)
                        elif current_state == 'RUNNING':
                            device.execute('app-hosting stop appid %s' % app_id)
                        elif current_state == 'STOPPED':
                            device.execute('app-hosting deactivate appid %s' % app_id)
                            time.sleep(wait_timer)
                    except SubCommandFailure:
                        raise SubCommandFailure(f"Could not change application state {app_id}")

                    # verify current state
                    try:
                        applist = device.parse('show app-hosting list')
                    except SchemaMissingKeyError as e:
                        log.error(f"No Application Found \n{e}")

                    if applist:
                        if app_id in applist['app_id']:
                            current_state = applist['app_id'][app_id]['state']
                        else:
                            log.info(f"{app_id} not found in list of running applications")
                else:
                    break

        elif target_state_index < current_state_index:
            for _ in reversed(state_index):
                if current_state != target_state:
                    try:
                        if current_state == 'ACTIVATED':
                            device.execute('app-hosting deactivate appid %s' % app_id)
                        elif current_state == 'RUNNING':
                            device.execute('app-hosting stop appid %s' % app_id)
                        elif current_state == 'STOPPED':
                            device.execute('app-hosting deactivate appid %s' % app_id)
                        elif current_state == 'DEPLOYED':
                            device.execute('app-hosting uninstall appid %s' % app_id)
                            current_state = 'UNINSTALLED'
                        time.sleep(wait_timer)
                    except SubCommandFailure:
                        raise SubCommandFailure(f"Could not change application state {app_id}")

                    if target_state == 'UNINSTALLED' and current_state == 'UNINSTALLED':
                        log.info(f'State of {app_id} changed to Target state {target_state}')
                        return True
                    else:
                        # verify/update current state
                        try:
                            applist = device.parse('show app-hosting list')
                        except SchemaMissingKeyError as e:
                            log.error(f"No Application Found \n{e}")

                        if applist:
                            if app_id in applist['app_id']:
                                current_state = applist['app_id'][app_id]['state']
                            else:
                                log.info(f"{app_id} not found in list of running applications")
                else:
                    break

    # verify current state
    try:
        applist = device.parse('show app-hosting list')
    except SchemaMissingKeyError as e:
        log.error(f"No Application Found \n{e}")

    if applist:
        if app_id in applist['app_id']:
            current_state = applist['app_id'][app_id]['state']
        else:
            log.info(f"{app_id} not found in list of running applications")

    log.info(f'{app_id} has a current state {current_state} and target state is {target_state}')
    if current_state == target_state:
        log.info(f'State of {app_id} changed to Target state {target_state}')
        return True
    else:
        log.error(f'Failed to change the State of {app_id} to Target state {target_state}')
        return False


def execute_install_application_bootflash(device, app_id, package_name, timeout=60, wait_timer=10):
    """
        Performs install application from bootflash
        Args:
            device ('obj'): Device object
            app_id ('str'): Application id name
            package_name ('str'): Name of the Application package in bootflash to install 
            timeout ('int, optional'): Timeout value ( default 60)
            wait_timer ('int, optional'): Time to wait before sending the result ( default 10 )
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"app-hosting install appid {app_id} "

    #Package name
    if package_name :
        cmd += f"package bootflash:{package_name}"
    log.info(f"Performing {cmd} on device {device.name}")

    try:
        device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Error while executing {cmd} on {device.name}:\n {e}'
        )

    log.info(f"Waiting for {wait_timer} seconds ")
    time.sleep(wait_timer)


def execute_guestshell_enable(device, timeout=60):
    """
        Execute guestshell enable
        Args:
            device ('obj'): Device object
            timeout ('int'): timout in seconds
        Returns:
            None
        Raises:
            SubCommandFailure
        
    """
    cmd = 'guestshell enable'
    try:
        device.execute(cmd, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not execute guestshell enable. Error {e}")


def execute_app_hosting_appid(device, appid, action, package_path=None):
    """ Execute app-hosting appid
        Args:
            device ('obj'): device to use
            appid ('str') : appid to configure
            action ('str'): app-hosting action. Ex: start, install, etc
            package_path ('str', optional): package install file path. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f"app-hosting {action} appid {appid}{f' package {package_path}' if package_path else ''}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not execute app-hosting appid. Error: {e}')

def set_stack_mode(dev, stack_mode, active_sw_number='', standby_sw_number=''):
    '''Entering to Set stack mode'''

    dialog = Dialog([
        Statement(pattern=r'.*Do you wish to proceed anyway\? \(y/n\)\s*\[n\]',
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)
    ])

    if stack_mode == '1+1':
        switch_active= f"switch {active_sw_number} role active"
        switch_standby= f"switch {standby_sw_number} role standby"
        dev.execute(switch_active, reply=dialog, timeout=5)
        dev.execute(switch_standby, reply=dialog, timeout=5)
        dev.api.execute_write_memory()
        log.info("Going to reload the Switch to change the stack-mode")
        if dev.reload(prompt_recovery=True):
            log.info('Reload successful')
            stack_mode_out = dev.parse("show switch stack-mode")
            stack_sws =stack_mode_out['switch'].keys()
            for switch in stack_sws:
                if stack_mode_out['switch'][switch]['mode'] == '1+1':
                    log.info('switch is set to 1+1 mode SUCCESSFULL')
                    return True
        else:
            log.info('Reload failed')

    elif stack_mode == 'N+1':
        log.info("setting Switch to N+1 mode")
        cmd= f"switch clear stack-mode"
        dev.execute(cmd, reply=dialog, timeout=5)
        dev.api.execute_write_memory()
        log.info("Going to reload the Switch to change the stack-mode")
        if dev.reload(prompt_recovery=True):
            log.info('Reload successful')
            return True
        else:
            log.info('Reload failed')
            return False


def execute_apphosting_cli(device, cli="", loops=10, wait_timer=10, unicon_timer=60):
    ''' 
    Args:
            device ('obj'): device to use
            cli('str'): app-hosting        Application hosting related informations
                        list               List the appliance
            loops('int'): time
            wait_timer('int'): time
            unicon_timer('int'): time
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    if not cli:
        cli = "show app-hosting list"

    for attempt in range (0,loops):
        output = device.execute(cli, timeout=unicon_timer)
        if 'The process for the command is not responding or is otherwise unavailable' in output:
            log.info("Wait 10 seconds and try again!")
            time.sleep(10)
        else: 
            return True

    return False


def install_wcs_enable_guestshell(device, appid_name, directory, package_name, timeout=300):
    '''
        Args:
            device ('obj'): device to use
            appid_name('str'): WORD  Name of application
            directory('str'): flash: Package path
            package_name('str'): flash:iperf3_signed.tar
            timeout('int'): Timeout in seconds. Default is 300
        Returns:
            True or False
        Raises:
            SubCommandFailure
    '''
    
    cli= f"app-hosting install appid {appid_name} package {directory}:{package_name}"
    if not execute_apphosting_cli(device, cli=cli):
        log.info("Unable to install wcs_docker app using CLI")
        return False
    time.sleep(timeout)
    try:
        output = device.execute("guestshell enable", timeout=timeout)
        if 'RUNNING' in output:
            log.info("Successfully enabled guestshell")
            return True
        else:
            return False
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Unable to execute guestshell. Error {e}")
