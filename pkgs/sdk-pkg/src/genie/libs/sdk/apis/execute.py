'''Common execute functions'''

# Python
import os
import time
import logging

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
    '''Powercycle a device
        Args:
            device ('obj'): Device object
    '''

    # Destroy device object
    device.destroy_all()

    # Find device's power cycler information
    pc_dict = getattr(device, 'peripherals', {}).get('power_cycler', {})

    if not pc_dict:
        raise Exception("Powercycler information is not provided in the "
                        "testbed YAML file for device '{}'\nUnable to "
                        "powercycle device".format(device.name))

    if not pc_dict.get('outlets'):
        raise Exception("Powercycler 'outlets' have not been provided for "
                        "device '{}'".format(device.name))
    else:
        pc_outlets = pc_dict['outlets']

    pc_dict['testbed'] = device.testbed

    # Init powercycler
    pc = PowerCycler(**pc_dict)

    # Turn powercycler off
    try:
        device.api.change_power_cycler_state(powercycler=pc, state='off',
                                             outlets=pc_outlets)
    except Exception as e:
        raise Exception("Failed to powercycle device off\n{}".format(str(e)))
    else:
        log.info("Powercycled device '{}' to 'off' state".format(device.name))

    # Wait specified amount of time before turning powercycler back on
    log.info("Waiting '{}' seconds before powercycling device on".format(delay))
    time.sleep(delay)

    # Turn powercycler on
    try:
        device.api.change_power_cycler_state(powercycler=pc, state='on',
                                             outlets=pc_outlets)
    except Exception as e:
        raise Exception("Failed to powercycle device on\n{}".format(str(e)))
    else:
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
    dir_output=None):

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
    Returns:
         True if there is enough space after the operation, False otherwise
    '''
    # Check correct arguments provided
    if (min_free_space_percent is None and required_size is None):
        raise ValueError("Either 'required_size' or 'min_free_space_percent' "
                         "must be provided to perform disk space verification")

    # For n9k compact copy:
    # observationally, depending on release, the compacted image is 36-48% the
    # size of the original image. For now we'll use 60% as a conservative estimate.
    if compact:
        required_size *=.6

    # Parse directory output to check 
    dir_out = dir_output or device.execute('dir {}'.format(destination))

    # Get available free space on device
    available_space = device.api.get_available_space(directory=destination,
                                                 output=dir_out)

    # Check if available space is sufficient
    if min_free_space_percent:

        # Get total space
        total_space = device.api.get_total_space(directory=destination,
                                                 output=dir_out)

        # Get current available space in %
        avail_percent = available_space / total_space * 100

        log.info("There is {avail} % of free space on the disk, which is "
                 "{compare} than the target of {target} %.".\
                 format(avail=round(avail_percent, 2), compare='less' if \
                        avail_percent < min_free_space_percent else 'greater',
                        target=min_free_space_percent))

        # calculate the required free space in bytes relative to the total disk 
        # space based on given percentage if required size is also provided,
        # take the larger value of the two
        if required_size:
            required_size = round(max(required_size,
                                min_free_space_percent * .01 * total_space))
        else:
            required_size = round(min_free_space_percent * .01 * total_space)

    # If there're not enough space, delete non-protected files
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
        log.info("Sending 'show version' to learn the current running images")

        image = device.api.get_running_image()
        if isinstance(image, list):
            protected_files.extend([os.path.basename(i) for i in image])
        else:
            protected_files.extend([os.path.basename(image)])

        # convert to set for O(1) lookup
        protected_files = set(protected_files)
        parsed_dir_out = device.parse('dir {}'.format(destination), output=dir_out)
        dq = Dq(parsed_dir_out)
        # turn parsed dir output to a list of files for sorting
        # Large files are given priority when deleting
        file_list = []
        for file in dq.get_values('files'):
            file_list.append((file, int(dq.contains(file).get_values('size')[0])))
        file_list.sort(key=lambda x: x[1], reverse=True)

        # append files to delete list until the deleted file sizes reaches the target,
        to_delete = []
        remaining_size = required_size
        for file, size in file_list:

            # break if we reach the target
            if remaining_size < available_space:
                break
            # if the file is protected, move skip and check next one in the list
            elif file in protected_files:
                continue

            to_delete.append(file)
            remaining_size -= size
        # if target can not be reached, aka loop is not broken, fail
        else:
            if min_free_space_percent:
                log.error(
                    'It is not possible to reach the target free space percentage after deleting all '
                    'unprotected files. Operation will be aborted and no file has been deleted.')
                return False

        device.api.delete_unprotected_files(directory=destination,
                                            protected=protected_files,
                                            files_to_delete=to_delete,
                                            dir_output=dir_out)
        # after deletion verify again fail if still not enough space,
        # execute dir again since files are changed
        dir_out_after = device.execute('dir {}'.format(destination))
        if min_free_space_percent:
            available_space = device.api.get_available_space(directory=destination,
                                                             output=dir_out_after)
            total_space = device.api.get_total_space(directory=destination,
                                                     output=dir_out_after)

            available_percent = available_space / total_space * 100
            log.info(
                "There are {available}% of free space on the disk, which is {compare} than "
                "the target of {target}%.".format(available=round(available_percent, 2),
                                                  compare='less' if available_percent <
                                                                    min_free_space_percent else 'greater',
                                                  target=min_free_space_percent))

        if not device.api.verify_enough_disk_space(required_size, destination, dir_output=dir_out_after):
            log.error(
                'There is still not enough space on the device after deleting '
                'unprotected files.')
            return False
        else:
            log.info(
                "Verified there is enough space on the device after deleting "
                "unprotected files.")
            return True


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
    '''

    log.info("Copying {} to running-config on '{}'".format(file, device.name))
    try:
        output = device.copy(source=file, dest='running-config',
                             timeout=copy_config_timeout)
    except Exception as e:
        raise Exception("Failed to apply config file {} to running-config\n{}".\
                        format(file, str(e)))
    else:
        if '0 bytes copied' in output:
            raise Exception("Config file {} not applied to running-config".\
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

