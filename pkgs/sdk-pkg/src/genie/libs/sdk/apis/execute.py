'''Common execute functions'''

# Python
import re
import os
import time
import logging
import json

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.libs.sdk.powercycler import powercyclers
from genie.libs.sdk.powercycler.base import PowerCycler

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


def execute_clear_line(device, alias='cli'):
    ''' Executes 'clear line <port>' to clear busy console port on device
        Args:
            device ('obj'): Device object
            alias ('str'): Alias used for console port connection
                           Default: 'cli'
        Returns:
            None
    '''


    # Init
    connected = set()

    # Find device's terminal server information
    terminal_server = getattr(device, 'peripherals', {}).get('terminal_server', {})
    if not terminal_server:
        raise Exception("Terminal server information is not provided in the "
                        "testbed YAML file for device '{}'\nUnable to clear "
                        "the console port line".format(device.name))

    for server, ports in terminal_server.items():
        # Fix ports type if incorrect from user
        if not isinstance(ports, list):
            ports = [ports]

        # Connect to terminal server
        term_serv_dev = device.testbed.devices[server]
        if term_serv_dev not in connected:
            term_serv_dev.connect(init_exec_commands=[], init_config_commands=[])
            connected.add(term_serv_dev)

        # Execute clear line on port
        for port in ports:
            try:
                term_serv_dev.execute("clear line {}".format(port))
            except Exception as e:
                log.error("Failed to clear line '{}'\n{}".format(port, str(e)))
                raise
            else:
                log.info("Executed 'clear line {}' on terminal server '{}'".\
                         format(port, term_serv_dev.name))

    # Disconnect from terminal server
    log.info("Disconnecting from terminal server...")
    for item in connected:
        item.destroy()

    # Disconnect from actual device now that line has been successfully cleared
    log.info("Disconnecting from {} as line was cleared successfully".\
             format(device.name))
    device.disconnect(alias=alias)


def execute_power_cycle_device(device, delay=30):
    ''' Powercycle a device

    Args:
        device ('obj'): Device object

        delay (int, optional): Time in seconds to sleep between turning the
            device off and then back on. Defaults to 30.

    Raises:
        Exception if powercycling fails.

    Returns:
        None
    '''

    # Destroy device object
    device.destroy_all()

    # Find device's power cycler information
    power_cyclers = getattr(device, 'peripherals', {}).get('power_cycler')
    if not power_cyclers:
        raise Exception("Powercycler information is not provided in the "
                        "testbed YAML file for device '{}'\nUnable to "
                        "powercycle device".format(device.name))

    # type(device['peripherals']['power_cycler']) should be a list to support
    # redundant PDUs. It can also be a dict in case of single PDU (legacy).
    if isinstance(power_cyclers, dict):
        power_cyclers = [power_cyclers]

    pcs = []

    # Initialize each power cycler. Save the powercycler object and outlets
    # for later user
    for power_cycler in power_cyclers:
        if power_cycler.get('outlets'):
            # Cyberswitching based powercyclers require the testbed object
            power_cycler['testbed'] = device.testbed

            pcs.append(
                (PowerCycler(**power_cycler), power_cycler['outlets'])
            )
        else:
            raise Exception("Powercycler outlets have not been provided:\n"
                            "    Device: {}\n"
                            "    Powercycler info: {}".format(device.name, power_cycler))

    # Turn power cyclers off
    for pc, outlets in pcs:
        try:
            device.api.change_power_cycler_state(
                powercycler=pc, state='off', outlets=outlets)
        except Exception as e:
            raise Exception("Failed to powercycle device off:\n{}".format(str(e)))

        log.info("Powercycled device '{}' to 'off' state".format(device.name))

    log.info("Waiting '{}' seconds before powercycling device on".format(delay))
    time.sleep(delay)

    # Turn power cyclers on
    for pc, outlets in pcs:
        try:
            device.api.change_power_cycler_state(
                powercycler=pc, state='on', outlets=outlets)
        except Exception as e:
            raise Exception("Failed to powercycle device on:\n{}".format(str(e)))

        log.info("Powercycled device '{}' to 'on' state".format(device.name))


def change_power_cycler_state(device, powercycler, state, outlets):
    ''' Turn on the power cycler
        Args:
            device ('obj'): Device object
            powercycler ('obj'): Powercycler object
            state ('str'): Power cycler state on/off
            outlets ('str'): Power cycler outlets
        Returns:
            None
    '''

    # Verify valid state given
    try:
        assert state in ['on', 'off']
    except AssertionError:
        raise Exception("Invalid state provided for powercycler\n"
                        "Acceptable states are 'on' or 'off'")

    if state == 'on':
        powercycler.on(*outlets)
    elif state == 'off':
        powercycler.off(*outlets)


def free_up_disk_space(device, destination, required_size, skip_deletion,
    protected_files, compact=False, min_free_space_percent=None,
    dir_output=None, allow_deletion_failure=False):

    '''Delete files to create space on device except protected files
    Args:
        device ('Obj') : Device object
        destination ('str') : Destination directory, i.e bootflash:/
        required_size ('int') : Check if enough space to fit given size in bytes.
                                If this number is negative it will be assumed
                                the required size is not available.
        skip_deletion ('bool') : Only performs checks, no deletion
        protected_files ('list') : List of file patterns that wont be deleted
        compact ('bool'): Compact option for n9k, used for size estimation,
                          default False
        min_free_space_percent ('int'): Minimum acceptable free disk space %.
                                        Optional,
        dir_output ('str'): Output of 'dir' command
                            if not provided, executes the cmd on device
        allow_deletion_failure (bool, optional): Allow the deletion of a file to silently fail. Defaults to False
    Returns:
         True if there is enough space after the operation, False otherwise
    '''
    # For n9k compact copy:
    # observationally, depending on release, the compacted image is 36-48% the
    # size of the original image. For now we'll use 60% as a conservative estimate.
    if compact:
        required_size *=.6

    # Parse directory output to check 
    dir_out = dir_output or device.execute('dir {}'.format(destination))

    # Get available free space on device
    available_space = device.api.get_available_space(
        directory=destination, output=dir_out)

    log.debug('available_space: {avs}'.format(avs=available_space))

    # Check if available space is sufficient
    if min_free_space_percent:

        # Get total space
        total_space = device.api.get_total_space(
            directory=destination, output=dir_out)

        # Get current available space in %
        avail_percent = available_space / total_space * 100

        log.info("There is {avail} % of free space on the disk, which is "
                 "{compare} than the target of {target} %.".\
                 format(avail=round(avail_percent, 2), compare='less' if \
                        avail_percent < min_free_space_percent else 'greater',
                        target=min_free_space_percent))

        # get bigger of required_space or min_free_space_percent
        required_size = round(
            max(required_size, min_free_space_percent * .01 * total_space))

    # If there's not enough space, delete non-protected files
    if device.api.verify_enough_disk_space(required_size=required_size,
                                           directory=destination,
                                           dir_output=dir_out):
        if required_size < 0:
            log.info("Required disk space is unknown, will not delete files")
        else:
            log.info("Verified there is enough space on the device. "
                     "No files are deleted")
        return True

    if skip_deletion:
        log.error("'skip_deletion' is set to True and there isn't enough space "
                  "on the device, files cannot be deleted.")
        return False
    else:
        log.info("Deleting unprotected files to free up some space")

        running_images = []
        log.info("Sending 'show version' to learn the current running images")
        running_image = device.api.get_running_image()
        if isinstance(running_image, list):
            for image in running_image:
                running_images.append(os.path.basename(image))
        else:
            running_images.append(os.path.basename(running_image))

        # convert to set for O(1) lookup
        protected_files = set(protected_files)
        parsed_dir_out = device.parse('dir {}'.format(destination), output=dir_out)
        dq = Dq(parsed_dir_out)

        # turn parsed dir output to a list of files for sorting
        # Large files are given priority when deleting
        file_list = []
        running_image_list = []
        for file in dq.get_values('files'):
            # separate running image from other files
            if any(file in image for image in running_images):
                running_image_list.append((file, int(dq.contains(file).get_values('size')[0])))
            else:
                file_list.append((file, int(dq.contains(file).get_values('size')[0])))

        file_list.sort(key=lambda x: x[1], reverse=True)

        # add running images to the end so they are deleted as a last resort
        file_list.extend(running_image_list)
        log.debug('file_list: {fl}'.format(fl=file_list))

        for file, size in file_list:
            device.api.delete_unprotected_files(directory=destination,
                                                protected=protected_files,
                                                files_to_delete=[file],
                                                dir_output=dir_out,
                                                allow_failure=allow_deletion_failure)

            if device.api.verify_enough_disk_space(required_size, destination):
                log.info("Verified there is enough space on the device after "
                         "deleting unprotected files.")
                return True

        # Exhausted list of files - still not enough space
        log.error('There is still not enough space on the device after '
                  'deleting unprotected files.')
        return False

def execute_reload(device, prompt_recovery, reload_creds, sleep_after_reload=120,
    timeout=800):
    ''' Reload device
        Args:
            device ('obj'): Device object
            prompt_recovery ('bool'): Enable/Disable prompt recovery feature
            reload_creds ('str'): Credential name defined in the testbed yaml file to be used during reload
            sleep_after_reload ('int'): Time to sleep after reload in seconds, default: 120
            timeout ('int'): reload timeout value, defaults 800 seconds.
    '''

    log.info("Reloading device '{d}'".format(d=device.name))

    credentials = ['default']

    if reload_creds:
        credentials.insert(0, reload_creds)

    try:
        device.reload(prompt_recovery=prompt_recovery, reload_creds=credentials,
                      timeout=timeout)
    except Exception as e:
        log.error("Error while reloading device {}".format(device.name))
        raise e

    log.info("Waiting '{}' seconds after reload ...".format(sleep_after_reload))
    time.sleep(sleep_after_reload)


def execute_copy_to_running_config(device, file, copy_config_timeout=60):
    ''' Copying file to running-config on device
        Args:
            device ('obj'): Device object
            file ('str'): String object to copy to device
            copy_config_timeout ('int'): Timeout for copy in seconds (default: 60)
    '''

    log.info("Copying {} to running-config on '{}'".format(file, device.name))
    try:
        output = device.copy(source=file, dest='running-config',
                             timeout=copy_config_timeout)
    except Exception as e:
        raise Exception("Failed to apply config file {} to running-config\n{}".\
                        format(file, str(e)))
    else:
        if re.search('^0 bytes.*', output):
            raise Exception("Config file {} not applied to "\
                            "running-config - 0 bytes was copied".\
                            format(file))


def execute_copy_to_startup_config(device, file, dest='startup-config', copy_config_timeout=60):
    ''' Copying file to startup-config on device
        Args:
            device ('obj'): Device object
            file ('str'): String object to copy to device
            dest ('str'): Target to copy to (default: startup-config)
            copy_config_timeout ('int'): Timeout for copy in seconds (default: 60)
    '''

    log.info("Copying {} to startup-config on '{}'".format(file, device.name))
    try:
        output = device.copy(source=file, dest=dest,
                             timeout=copy_config_timeout)
    except Exception as e:
        raise Exception("Failed to apply config file {} to startup-config\n{}".\
                        format(file, str(e)))
    else:
        if re.search('^0 bytes.*', output):
            raise Exception("Config file {} not applied to "\
                            "startup-config - 0 bytes was copied".\
                            format(file))


def execute_copy_run_to_start(device, command_timeout=300, max_time=120,
    check_interval=30, copy_vdc_all=False):
    ''' Execute copy running-config to startup-config
        Args:
            device ('obj'): Device object
            command_timeout ('int'): Timeout value in sec, Default Value is 300 sec
            max_time ('int'): Maximum time in seconds, Default Value is 300 sec
            check_interval ('int'): Check interval in seconds, Default Value is 20 sec
            copy_vdc_all ('boolean'): Copy on all VDCs or not, Default Value is False
    '''

    # Build command
    cmd = "copy running-config startup-config"
    if copy_vdc_all:
        cmd += " vdc-all"

    # Build Unicon Dialogs

    startup = Statement(
        pattern=r'^.*Destination +(filename|file +name)(\s\(control\-c +to +abort\)\:)? +\[(\/)?startup\-config]\?',
        action='sendline()',
        loop_continue=True,
        continue_timer=False)
    proceed = Statement(
        pattern=r'.*proceed anyway?.*',
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)

    # XR platform specific when over-write the existing configurations
    yes_cmd = Statement(
        pattern=r'^.*The +destination +file +already +exists\. +Do +you +want +to +overwrite\? +\[no\]\:',
        action='sendline(y)',
        loop_continue=True,
        continue_timer=False)

    # Begin timeout
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.execute(cmd, timeout=command_timeout,
                                    reply=Dialog([startup, proceed, yes_cmd]))
        except Exception as e:
            raise Exception("Cannot save running-config to startup-config {}".\
                            format(str(e)))

        # IOSXE platform
        if "[OK]" in output or "Copy complete" in output:
            break

        # Copy in progress...
        if "system not ready" in output or "Building configuration..." in output:
            log.info("Still building configuration. Re-attempting save config "
                     "after '{}' seconds".format(check_interval))
            timeout.sleep()
            continue
    else:
        # No break
        raise Exception('Failed to save running-config to startup-config')

def execute(device, *args, **kwargs):
    ''' execute command to device
        Args:
            device (`obj`): Device object
        Return:
            output (`str`): output from command on device
    '''
    output = ''
    # get connected aliases
    connected_aliases = device.api.get_connected_alias()

    for alias, connection_dict in connected_aliases.items():
        # check if CLI(Unicon), or not
        if 'unicon' in connection_dict['connection_provider'].__module__:
            output = getattr(device, alias).execute(*args, **kwargs)
            return output

    if connected_aliases:
        raise Exception('Found aliases {a}, but not CLI(Unicon).'.format(a=connected_aliases.keys()))
    else:
        raise Exception('No connected alias found.')

def execute_and_parse_json(device, command):
    ''' execute the specified command on the device which must return output in JSON format.
        The JSON is parsed into a dict.

        Args:
            device (`obj`): Device object
        Return:
            output (`dict`): parsed JSON output from command on device as a dict
    '''

    output = {}
    try:
        output = execute(device, command)
        output = json.loads(output)
    except Exception as e:
        log.error("An exception occurred when trying to run or parse the output of a command as JSON. "
                "The command was '{}' and the exception is {}".format(command, e))
        output = {}
    return output
