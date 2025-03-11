'''IOSXE execute functions for platform'''

# Python
import re
import logging
import time

# pyATS
from pyats.async_ import pcall
from pyats.utils.fileutils import FileUtils

# Genie
from genie.utils import Dq
from genie.harness.utils import connect_device
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import StateMachineError,SubCommandFailure

# Logger
log = logging.getLogger(__name__)


def execute_delete_boot_variable(device, boot_images=[], timeout=300):
    ''' Delete the boot variables
        Args:
            device ('obj'): Device object
            boot_images ('list', optional): List of strings of system images to delete as boot variable.default is an empty list
            timeout ('int'): Max time to delete boot vars in seconds
    '''

    if not boot_images:
        log.info("Removing boot variable on {device}".format(device=device))
        try:
            device.configure('no boot system')
        except SubCommandFailure as e:
            raise SubCommandFailure(
                "Could not removing boot variable on {device}. Error:\n{error}".format(device=device, error=e))
    else:
        for image in boot_images:
            try:
                device.configure("no boot system {}".format(image), timeout=timeout)
            except Exception as e:
                raise Exception("Failed to delete boot variables on '{}'\n{}".\
                            format(device.name, str(e)))
            else:
                log.info("Deleted '{}' from BOOT variable".format(image))


def execute_set_boot_variable(device, boot_images, timeout=300):
    ''' Set the boot variables
        Args:
            device ('obj'): Device object
            boot_images ('list'): List of strings of system images to set as boot variable
            timeout ('int'): Max time to set boot vars in seconds
    '''

    for image in boot_images:
        try:
            device.configure("boot system {}".format(image), timeout=timeout)
        except Exception as e:
            raise Exception("Failed to set boot variables on '{}'\n{}".\
                            format(device.name, str(e)))
        else:
            log.info("Added '{}' to BOOT variable".format(image))


def execute_set_config_register(device, config_register, timeout=300):
    '''Set config register to load image in boot variable
        Args:
            device ('obj'): Device object
            config_reg ('str'): Hexadecimal value to set the config register to
            timeout ('int'): Max time to set config-register in seconds
    '''

    try:
        device.configure("config-register {}".format(config_register),
                         timeout=timeout)
    except Exception as e:
        raise Exception("Failed to set config register for '{d}'\n{e}".\
                        format(d=device.name, e=str(e)))
    else:
        log.info("Set config-register to '{}'".format(config_register))


def _execute_write_erase(device, timeout=300):
    '''
    internal function of execute_write_erase for pcall
    '''

    log.info("Executing 'write erase' on the device")

    # Unicon Statement/Dialog
    write_erase = Statement(
        pattern=r".*remove all configuration files\! Continue\? \[confirm\]",
        action='sendline()',
        loop_continue=True,
        continue_timer=False)

    # Add permisson denied to error pattern
    origin = list(device.execute.error_pattern)
    error_pattern = ['.*[Pp]ermission denied.*']
    error_pattern.extend(origin)

    try:
        output = device.execute("write erase",
                                reply=Dialog([write_erase]),
                                timeout=timeout,
                                error_pattern=error_pattern)
    except Exception as err:
        log.error("Failed to write erase: {err}".format(err=err))
        raise Exception(err) from err
    finally:
        # restore original error pattern
        device.execute.error_pattern = origin

    if "[OK]" in output:
        log.info("Successfully executed 'write erase'")
    else:
        raise Exception("Failed to execute 'write erase'")


def execute_write_erase(device, timeout=300, devices=None, exclude_devices=None):
    ''' Execute 'write erase' on the device
        Args:
            device ('obj'): Device object
            timeout ('int'): Max time to for write erase to complete in seconds
            devices ('list`): list of device names. default to None
            exclude_devices ('list'): Exclude device list
        Usage:
            device.api.execute_write_erase(devices=['ce1', 'ce2', 'pe1'])
    '''
    if exclude_devices is None:
        exclude_devices = []
    if devices:
        device_list = [{
            'device': device.testbed.devices[dev]
        } for dev in devices if dev not in exclude_devices]
        ikwargs = device_list
        ckwargs = {'timeout': timeout}
        pcall(_execute_write_erase, ckwargs=ckwargs, ikwargs=ikwargs)
    else:
        _execute_write_erase(device=device, timeout=timeout)

def execute_write_memory(device, timeout=300):
    ''' Execute 'write memory' on the device
        Args:
            device ('obj'): Device object
            timeout ('int', optional): Max time for write memory to complete in seconds
                            Default is 300
    '''

    log.info("Executing 'write memory' on the device")

    dialog = Dialog([
        Statement(
            pattern=r'Continue\? \[no\]:\s*$',
            action='sendline(yes)',
            loop_continue=True)
    ])

    try:
        output = device.execute("write memory", reply=dialog, timeout=timeout)
    except Exception as err:
        log.error("Failed to execute 'write memory'\n{err}".format(err=err))
        raise Exception(err)

    if "[OK]" in output:
        log.info("Successfully executed 'write memory'")
    else:
        raise Exception("Failed to execute 'write memory'")


def execute_install_package(device, image_dir, image, save_system_config=True,
                            install_timeout=660, reconnect_max_time=120,
                            reconnect_interval=30, _install=True, install_commit_sleep_time=None):
    """ Installs package
        Args:
            device ("obj"): Device object
            image_dir ("str"): Directory image is located in
            image ("str"): Image name
            save_system_config ("bool"): If config changed do we save it?
            install_timeout ("int"): Maximum time for install. Default 660
            reconnect_max_time ("int"): Maximum time for reconnect. Default 120
            reconnect_interval ("int"): Time between reconnect attempts. Default 30
            install_commit_sleep_time ("int"): Sleep time before install commit command
            _install ("bool"): True to install, False to uninstall.
                Not meant to be changed manually.

        Raises:
            Exception

        Returns:
            True if install succeeded else False
    """
    dialog = Dialog([
        Statement(pattern=r".*Press Quit\(q\) to exit, you may save "
                          r"configuration and re-enter the command\. "
                          r"\[y\/n\/q\]",
                  action='sendline(y)' if save_system_config else 'sendline(n)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*This operation may require a reload of the "
                          r"system\. Do you want to proceed\? \[y\/n\]",
                  action='sendline(y)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r"^.*RETURN to get started",
                  action='sendline()',
                  loop_continue=False,
                  continue_timer=False)
    ])

    if _install:
        cmd = """install add file {dir}{image}
        install activate file {dir}{image}""".format(
            dir=image_dir, image=image
        )
    else:
        cmd = "install deactivate file {dir}{image}".format(
            dir=image_dir, image=image
        )

    try:
        device.execute(cmd, reply=dialog, timeout=install_timeout)
        device.enable()
    except StateMachineError:
        # this will be raised after 'Return to get started' is seen
        timeout = Timeout(reconnect_max_time, reconnect_interval)
        while timeout.iterate():
            device.destroy()
            try:
                connect_device(device)
            except Exception as e:
                connection_error = str(e)
                timeout.sleep()
                continue
            break
        else:
            raise Exception("Couldn't reconnect to the device. Error: {}"\
                            .format(connection_error))

    if _install:
        cmd = "install commit"
    else:
        cmd = """install commit
        install remove file {dir}{image}""".format(
            dir=image_dir, image=image
        )
    if install_commit_sleep_time:
        time.sleep(install_commit_sleep_time)
    device.execute(cmd, timeout=install_timeout)

    try:
        out = device.parse("show install summary")
    except SchemaEmptyParserError:
        out = {}

    for location in out.get("location"):
        for pkg in out['location'][location]['pkg_state']:
            pkg = out['location'][location]['pkg_state'][pkg]
            if (_install and
                    image in pkg['filename_version'] and
                    'C' == pkg['state']):
                # the image should exist; it was just installed
                return True
            elif (not _install and
                    image in pkg['filename_version']):
                # the image should not exist; it was just uninstalled.
                return False

    return False if _install else True


def execute_uninstall_package(device, image_dir, image, save_system_config=True,
                              timeout=660, install_commit_sleep_time=None):
    """ Uninstalls package
        Args:
            device ("obj"): Device object
            image_dir ("str"): Directory image is located in
            image ("str"): Image name
            save_system_config ("bool"): If config changed do we save it?
            timeout ("int"): maximum time for install
            install_commit_sleep_time ("int"): Sleep time before install commit command

        Raises:
            Exception

        Returns:
            True if install succeeded else False
    """
    return execute_install_package(
        device,
        image_dir,
        image,
        save_system_config,
        timeout,
        _install=False,
        install_commit_sleep_time=install_commit_sleep_time)


def delete_unprotected_files(device,
                             directory,
                             protected,
                             files_to_delete=None,
                             dir_output=None,
                             allow_failure=False,
                             destination=None):
    """delete all files not matching regex in the protected list
        Args:
            device ('obj'): Device object
            directory ('str'): working directory to perform the operation
            protected ('list'): list of file patterns that won't be deleted. If it begins
                                and ends with (), it will be considered as a regex
            files_to_delete('list') list of files that should be deleted unless they are protected
            dir_output ('str'): output of dir command, if not provided execute the cmd on device to get the output
            allow_failure (bool, optional): Allow the deletion of a file to silently fail. Defaults to False.
            destination ('str') : Destination directory. default to None. i.e bootflash:/
        Returns:
            None
            """

    protected_set = set()
    fu_device = FileUtils.from_device(device)
    file_set = set(
        Dq(device.parse('dir {}'.format(directory),
                        output=dir_output)).get_values('files'))

    if isinstance(protected, str):
        protected = [protected]
    elif not isinstance(protected, (list, set)):
        raise TypeError("'{p}' must be a list")

    for pattern in protected:
        # it's a regex!
        if pattern.startswith('(') and pattern.endswith(')'):
            regexp = re.compile(pattern)
            protected_set.update(set(filter(regexp.match, file_set)))

        # just file names, exact match only
        elif pattern in file_set:
            protected_set.add(pattern)

    # if files_to_delete is given,updated protected files with the diff of file_set - files_to_delete
    # so that we only delete files that are in files_to_delete and NOT protected
    # in other words we remove the protected files from file_to_delete
    if files_to_delete:
        protected_set.update(file_set - set(files_to_delete))

    not_protected = file_set - protected_set
    error_messages = []

    if not_protected:
        log.info("The following files will be deleted:\n{}".format(
            '\n'.join(not_protected)))
        dont_delete_list = protected_set.intersection(files_to_delete)
        if dont_delete_list:
            log.info(
                "The following files will not be deleted because they are protected:\n{}"
                .format('\n'.join(dont_delete_list)))
        for file in not_protected:
            # it's a directory, dont delete
            if file.endswith('/'):
                continue
            log.info(f'Deleting the unprotected file "{file}"')
            try:
                if destination:
                    fu_device.deletefile(f"{destination}{file}", force=True, device=device)
                else:
                    fu_device.deletefile(file, force=True, device=device)
            except Exception as e:
                if allow_failure:
                    log.info(
                        f'Failed to delete file "{file}" but ignoring and moving on due to "allow_failure=True".'
                    )
                    continue

                error_messages.append(f'Failed to delete file "{file}" due to :{str(e)}')
        if error_messages:
            raise Exception('\n'.join(error_messages))
    else:
        log.info(
            "No files will be deleted, the following files are protected:\n{}".
            format('\n'.join(protected_set)))

def execute_card_OIR(device, card_number, switch_id = None, timeout=60):
    ''' Execute 'hw-module subslot <slot> oir power-cycle' on the device
        Args:
            device ('obj'): Device object
            card_number ('str'): Card number on which OIR has to be performed
            switch_id ('str', optional): Switch number(In case of SVL/Stack) on which OIR has to be performed. Default is None.
            timeout ('int',optional): Max time for card oir execution to complete in seconds.Defaults to 60
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    log.info("Executing 'hw-module [switch <switch_id>] subslot <slot> oir power-cycle' on the device")

    # Unicon Statement/Dialog
    dialog = Dialog([
             Statement(
             pattern=r".*Proceed with power cycle of module? [confirm]",
             action='sendline()',
             loop_continue=True,
             continue_timer=False)
             ])
    command = f'hw-module subslot {card_number} oir power-cycle'
    if switch_id:
        command = f'hw-module switch {switch_id} subslot {card_number} oir power-cycle'

    try:
        output = device.execute(
                 command,
                 reply=dialog,
                 timeout=timeout,
                 append_error_pattern=['.*Command cannot be executed.*'])
    except SubCommandFailure as err:
        log.error(f"Failed to execute {command}': {err}".format(err=err))
        raise


def execute_card_OIR_remove(device, card_number, switch_id = None, timeout=60):
    ''' Execute 'hw-module subslot <slot> oir remove' on the device
        Args:
            device ('obj'): Device object
            card_number ('str'): Card number on which OIR remove has to be performed
            switch_id ('str', optional): Switch number(In case of SVL/Stack) on which OIR remove has to be performed. Default is None.
            timeout ('int',optional): Max time for card oir removal to complete in seconds.Defaults to 60
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    log.info("Executing 'hw-module [switch <switch_id>] subslot <slot> oir remove' on the device")

    # Unicon Statement/Dialog
    dialog = Dialog([
             Statement(
             pattern=r".*Proceed with removal of module? [confirm]",
             action='sendline()',
             loop_continue=True,
             continue_timer=False)
             ])
    command = f'hw-module subslot {card_number} oir remove'
    if switch_id:
        command = f'hw-module switch {switch_id} subslot {card_number} oir remove'

    try:
        output = device.execute(
                 command,
                 reply=dialog,
                 timeout=timeout,
                 append_error_pattern=['.*Command cannot be executed.*'])
    except SubCommandFailure as err:
        log.error(f"Failed to execute {command}': {err}".format(err=err))
        raise



def execute_card_OIR_insert(device, card_number, switch_id = None, timeout=60):
    ''' Execute 'hw-module subslot <slot> oir insert' on the device
        Args:
            device ('obj'): Device object
            card_number ('str'): Card number on which OIR insert has to be performed
            switch_id ('str', optional): Switch number(In case of SVL/Stack) on which OIR insert has to be performed. Default is None.
            timeout ('int',optional): Max time for card oir insertion to complete in seconds.Defaults to 60
        Returns:
            None
        Raises:
            SubCommandFailure
    '''

    log.info("Executing 'hw-module [switch <switch_id>] subslot <slot> oir insert' on the device")

    # Unicon Statement/Dialog
    dialog = Dialog([
             Statement(
             pattern=r".*Proceed with insertion of module? [confirm]",
             action='sendline()',
             loop_continue=True,
             continue_timer=False)
             ])
    command = f'hw-module subslot {card_number} oir insert'
    if switch_id:
        command = f'hw-module switch {switch_id} subslot {card_number} oir insert'

    try:
        output = device.execute(
                 command,
                 reply=dialog,
                 timeout=timeout,
                 append_error_pattern=['.*Command cannot be executed.*'])
    except SubCommandFailure as err:
        log.error(f"Failed to execute {command}': {err}".format(err=err))
        raise


def execute_clear_platform_software_fed_active_acl_counters_hardware(device):
    """ clear platform software fed active acl counters hardware
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear platform software fed active acl counters hardware")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear counters on {device}. Error:\n{e}")


def execute_clear_platform_software_fed_switch_acl_counters_hardware(device,switch_num):
    """ clear platform software fed switch acl counters hardware
        Args:
            device ('obj'): Device object
            switch_num ('int'): Switch number to clear acl counters
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear platform software fed switch {switch_num} acl counters hardware".format(switch_num=switch_num))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not clear counters on {device}. Error:\n{e}")

def execute_issu_install_package(device, image_dir, image, save_system_config=True,
                            install_timeout=660, reconnect_max_time=600,
                            reconnect_interval=60, append_error_pattern = ['.*FAILED.*']):
    """ Installs issu package
        Args:
            device ("obj"): Device object
            image_dir ("str"): Directory image is located in
            image ("str"): Image name
            save_system_config ("bool"): If config changed do we save it?
            install_timeout ("int"): Maximum time for install. Default 660
            reconnect_max_time ("int"): Maximum time for reconnect. Default 600
            reconnect_interval ("int"): Time between reconnect attempts. Default 60

        Raises:
            Exception

        Returns:
            True if install succeeded else False
    """

    dialog = Dialog([
        Statement(pattern=r'Press Quit\(q\) to exit, you may save configuration and re-enter the command.*\[y\/n\/q\]',
                  action='sendline(y)' if save_system_config else 'sendline(n)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'^.*RETURN to get started.*',
                  action='sendline()',
                  loop_continue=True,
                  continue_timer=False)
        ])

    cmd = """install add file {dir}:{image} act issu commit""".format(dir=image_dir, image=image)

    try:
        device.execute(cmd, reply=dialog, timeout=install_timeout,append_error_pattern=append_error_pattern)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not execute on {device}. Error:\n{error}".format(device=device, error=e))

    time.sleep(100)
    log.info(f"Waiting for {device.hostname} to reload")

    timeout = Timeout(reconnect_max_time,reconnect_interval)
    while timeout.iterate():
        timeout.sleep()
        device.destroy()

        try:
            device.connect(learn_hostname=True)
        except Exception as e:
            connect_exception = e
            log.info("The device is not ready")
        else:
            return True

    log.info("Failed to reload", from_exception=connect_exception)
    return False

def execute_clear_platform_software_fed_switch_active_cpu_interface(device):
    """ clear platform software fed switch active cpu-interface
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear platform software fed switch active cpu-interface")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear active cpu-interface on device")

def execute_clear_platform_software_fed_switch_mode_acl_stats(device,switch_mode):
    """ clear platform software fed {switch_mode} acl stats
        Args:
            device ('obj'): Device object
            switch_mode ('str'): active|standby|switch active|switch standby
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:

        device.execute(f'clear platform software fed {switch_mode} acl stats')
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear counters on {device}. Error:\n{e}")

def execute_clear_ipdhcp_snooping_database_statistics(device):

    """ clear ip dhcp  snooping database statistics
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute('clear ip dhcp  snooping database statistics')

    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure('Could not clear ip dhcp  snooping database statistics')

def execute_switch_card_OIR(device, switch_number, slot, timeout=60):
    ''' Execute 'hw-module switch <switch_number> subslot <slot> oir power-cycle' on the device
        Args:
            device ('obj'): Device object
            switch_number('str'): Switch number on which OIR has to be performed
            slot ('str'): Slot on which OIR has to be performed
            timeout ('int',optional): Max time for card oir execution to complete in seconds.Defaults to 60
    '''

    log.debug("Executing 'hw-module switch <switch_number> subslot <slot> oir power-cycle' on the device")

    # Unicon Statement/Dialog
    dialog = Dialog([
             Statement(
             pattern=r"Proceed with power cycle of module? [confirm]",
             action='sendline()',
             loop_continue=True,
             continue_timer=False)
             ])
    command = ["hw-module switch {} subslot {} oir power-cycle".format(switch_number,slot)]

    try:
        output = device.execute(
                 command,
                 reply=dialog,
                 timeout=timeout,
                 append_error_pattern=['.*Command cannot be executed.*'])
    except Exception as err:
        log.error("Failed to execute 'hw-module switch <switch_number> subslot <slot> oir power-cycle': {err}".format(err=err))
        raise Exception(err)

    if output:
        log.debug("Successfully executed 'hw-module switch <switch_number> subslot <slot> oir power-cycle'")
    else:
        raise Exception("Failed to execute 'hw-module switch <switch_number> subslot <slot> oir power-cycle'")

def execute_clear_platform_software_fed_active_cpu_interface(device):
    """ clear platform software fed active cpu-interface
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear platform software fed active cpu-interface")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear active cpu-interface on device")

def execute_clear_platform_hardware_fed_active_qos_statistics_interface(device,intf):
    """ clear platform hardware fed active qos statistics interface
        Args:
            device ('obj'): Device object
            inft ('str'): interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear platform hardware fed active qos statistics interface {intf}".format(intf=intf))
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear active cpu-interface on device")


def execute_diagnostic_start_switch_module_test(device,switch_num,mod_num,include):
    """ execute diagnostic start switch 1 module 1 test all
        Args:
            device ('obj'): Device object
            switch_num ('int'): Switch number(In case of SVL/Stack) on which diagnostic has to be performed
            mod_num ('int'): Module number on which diagnostic has to be performed
            include ('str'): test name(all) on which diagnostic has to be performed
        Returns:
            None
        Raises:
            SubCommandFailure
    """


    cmd = f"diagnostic start switch {switch_num} module {mod_num} test {include}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not execute diagnostic start switch {switch_num} module {mod_num} test {include} on device")


def execute_diagnostic_start_module_test(device,mod_num,include):
    """ execute diagnostic start module 1 test all
        Args:
            device ('obj'): Device object
            mod_num ('int'): Module number on which diagnostic has to be performed
            include ('str'): test name(all) on which diagnostic has to be performed
        Returns:
            None
        Raises:
            SubCommandFailure
    """


    cmd = f"diagnostic start module {mod_num} test {include}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not execute diagnostic start module {mod_num} test {include} on device")

def hardware_qfp_active_statistics_drop_clear(device):
    """ execute clear harware qfp stats drop clear command
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = "show platform hardware qfp active statistics drop clear"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not execute cler qfp stats drop command")

def hardware_qfp_active_ipsec_data_drop_clear(device):
    """ execute clear harware active ipsec data drop clear command
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = "show platform hardware qfp active feature ipsec data drop clear"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not execute active ipsec data drop clear command")


def execute_clear_parser_statistics(device):
    """ clear parser statistics
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear parser statistics")
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure("Could not clear parser statistics on device")

def execute_format(device, file_sys, timeout=300, file_sys_type=None):
    """ Execute 'format <file-system>' on the device
        Args:
            device ('obj'): Device object
            timeout ('int'): Max time to for format to complete in seconds
            file_sys ('str'): File system should be formatted
            file_sys_type ('str', optinal): File system type. Ex: FAT32, ext2. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to format the file system on device
    """

    log.info("Executing 'format file-system' on the device")

    dialog = Dialog([
        Statement(pattern=r".*Format operation may take a while\. Continue\? \[confirm\]",
                  action='sendline(\r)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Format operation will destroy all data in \"usbflash.*\:\"\.  Continue\? \[confirm\]",
                  action='sendline(\r)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*Format of usbflash.*\: complete",
                  action='sendline()',
                  loop_continue=True,
                  continue_timer=False)
    ])


    cmd = f"format {file_sys}{f' {file_sys_type}' if file_sys_type else ''}"

    try:
        device.execute(cmd, reply=dialog, timeout=timeout)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not format the file system Error:\n{error}".format(error=e

        ))

def create_dir_file_system(device, file_sys, dir_name, timeout=300):
    """ create directory in  '<file_system>' on the device
        Args:
            device ('obj'): Device object
            timeout ('int'): Max time to for format to complete in seconds
            file_sys ("str"): File system
            dir_name("str"): directory name should be created
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to create directory on file system
    """

    log.info("Executing 'mkdir file-system:dir_name' on the device")

    dialog = Dialog([
        Statement(pattern=r".*Create directory filename \[.*\]\?",
                  action='sendline()',
                  loop_continue=False,
                  continue_timer=False),

    ])

    cmd = "mkdir {dir}{dr_name}".format(dir=file_sys,dr_name=dir_name)

    try:
        output = device.execute(cmd, reply=dialog, timeout=timeout)
        log.info('created directory on file system')
    except Exception as err:
        log.error("Failed to execute the command: {err}".format(err=err))
        raise Exception(err)

def rename_dir_file_system(device, file_sys, file_name, des_file_sys, des_file_name, timeout=300):
    """ Rename directory in  '<file_system>' on the device
        Args:
            device ('obj'): Device object
            timeout ('int'): Max time to for format to complete in seconds
            file_sys ("str"): File system
            file_name("str"): directory name or file name
            des_file_name("str"): directory name or file name should be renamed
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to Rename directory on file system
    """

    log.info("Executing 'rename file-system:file_name file-system:des_file_name' on the device")

    dialog = Dialog([
        Statement(pattern=r".*Destination filename \[.*\]\?",
                  action='sendline()',
                  loop_continue=False,
                  continue_timer=False),

    ])
    cmd = "rename {dir}{f_name} {des_dir}{d_name}".format(dir=file_sys,f_name=file_name,des_dir=des_file_sys,d_name=des_file_name)

    try:
        output = device.execute(cmd, reply=dialog, timeout=timeout)
        log.info('Successfully renamed the file')
    except Exception as err:
        log.error("Failed to execute the command: {err}".format(err=err))
        raise Exception(err)

def show_switch_redirect(device, storage_type, file_name):
    """ storing output in a file format
        Example: show switch | redirect flash:test.txt

        Args:
            device ('obj'): Device object
            storage_type ('str'): the storage type (e.g. flash, bootflash, nvram)
            file_name ('str'): file to store the output in

        Returns:
            None

        Raises:
            SubCommandFailure

    """
    config = f"show switch | redirect {storage_type}:{file_name}"
    try:
        device.execute(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to redirect to {file_name} on the device {device.name}. Error:\n{e}")

def license_smart_sync_all(device):
    """ license smart sync all

        Args:
            device ('obj'): device to use
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.execute("license smart sync all")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute license smart sync all  on the device {device.name}. Error:\n{e}")

def terminal_no_monitor(device):
    """ terminal no monitor
    Args:
        device (`obj`): Device object

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"terminal no monitor"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not run terminal no monitor. Error:\n{error}".format(error=e)
        )


def request_platform_software_cflow_copy(device):
    """ request platform software cflow copy
    Args:
        device (`obj`): Device object

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"request platform software cflow copy"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not request platform software cflow copy. Error:\n{error}".format(error=e)
        )

def execute_install_three_step_issu_package(device, image_dir, image, save_system_config=True,
                            install_timeout=660, reconnect_max_time=200,
                            reconnect_interval=30, _install=True, install_commit_sleep_time=None,
                            append_error_pattern = ['.*FAILED.*']):
    """ Installs package
        Args:
            device ("obj"): Device object
            image_dir ("str"): Directory image is located in
            image ("str"): Image name
            save_system_config ("bool"): If config changed do we save it?
            install_timeout ("int"): Maximum time for install. Default 660
            reconnect_max_time ("int"): Maximum time for reconnect. Default 120
            reconnect_interval ("int"): Time between reconnect attempts. Default 30
            install_commit_sleep_time ("int"): Sleep time before install commit command
            _install ("bool"): True to install, False to uninstall.
                Not meant to be changed manually.
        Raises:
            Exception
        Returns:
            True if install succeeded else False
    """
    dialog = Dialog([
        Statement(pattern=r".*Press Quit\(q\) to exit, you may save "
                          r"configuration and re-enter the command\. "
                          r"\[y\/n\/q\]",
                  action='sendline(y)' if save_system_config else 'sendline(n)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r".*This operation may require a reload of the "
                          r"system\. Do you want to proceed\? \[y\/n\]",
                  action='sendline(y)',
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r"^.*RETURN to get started",
                  action='sendline()',
                  loop_continue=False,
                  continue_timer=False)
    ])

    if _install:
        cmd = """install add file {dir}{image}
        install activate issu""".format(
            dir=image_dir, image=image
        )

    try:
        device.execute('write mem')
        device.execute(cmd, reply=dialog, timeout=install_timeout,append_error_pattern=append_error_pattern)
        device.api.reconnect_device(max_time=600,interval=60)
        device.enable()
    except StateMachineError:
        timeout = Timeout(reconnect_max_time, reconnect_interval)
        while timeout.iterate():
            timeout.sleep()
            device.destroy()
            try:
                device.api.reconnect_device(max_time=600,interval=60)
            except Exception as e:
                connection_error = str(e)
                continue
            break
        else:
            raise Exception("Couldn't reconnect to the device. Error: {}"\
                            .format(connection_error))

    if _install:
        cmd = "install commit"

    try:
        output = device.execute(cmd, timeout=install_timeout)
    except Exception as e:
        log.error(f"Error while executing {cmd} on {device.name}: {e}")

    match = re.search(r"FAILED:*", output)
    result = 'failed' if match else 'successful'
    log.info(f"install three shot operation {result} on {device.name}")
    return output if not match else match

def execute_stack_power(device, switch_number, port_number, mode ):
    """ Enable stack-power stack
        Example : stack-power switch 1 port 1 enable

        Args:
            device ('obj'): device to use
			switch_number('int') : Switch number range <1-16>
            port_number	('int') : port number range <1-2>
            mode ('str') : enable/disable option
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"enable stack-power stack on {device.name}")
    config = f'stack-power switch {switch_number} port {port_number} {mode}'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to enable stack-power on device {device.name}. Error:\n{e}")

def execute_diagnostic_start_switch_test(device, switch_number, test_id=None, test_name=None):
    """ execute diagnostic start switch 1 test
        Args:
            device ('obj'): Device object
            test_id ('str'): Test ID list (e.g. 1,3-6) or Test Name or minimal  or complete
              Interface port number WORD    Port number list (e.g. 2,4-7)
            switch_number ('int'): Switch number on which diagnostic has to be performed
            test_name ('str'): Word , test name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"diagnostic start switch {switch_number} test "

    if test_name in ("non-disruptive", "per-port", "basic"):
        cmd += f"{test_name} port {test_id} "
    else:
        cmd += f"{test_id}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(
            f"Could not execute diagnostic start switch {switch_number} test {test_name} on device. Error:\n{e}")

def execute_install_label(device, id = None ,label_name = None, description_name = None, word = ""):
    """
    Performs install state on device
    Args:
            device ('obj'): device to use
            id('int' optional) : id range <1-4294967295>
            label_name  ('str' optional) : Add a label name to specified install point
            description_name ('str', optional) : Add a description to specified install point
            word ('str') : any name can give <Max character 32>
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    log.info(f'install label {id} {label_name} {word} on {device.name}')
    if label_name:
       config = f'install label {id} label-name {label_name} {word}'
    else:
        config = f'install label {id} description {description_name} {word}'
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to install label {id} {label_name} {word} on {device.name}. Error:\n{e}")

def execute_config_confirm(device):
    """ execute config confirm
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.execute("config confirm")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute config confirm. Error:\n{e}"
        )

def execute_device_dir_path(device, path):
    """ Execute device total bytes for local file
        Example: dir flash: | include bytes total | include
        Args:
            device ('obj'): Device object
            path ('str'): specifying path for flash:, flash-1:, flash2:/crashinfo:, crashinfo-1: , crashinfo2:
        Returns:
            output
        Raises:
            SubCommandFailure
    """
    try:
        output = device.execute(
            "dir {path} | include bytes total | include".format(path=path)
            )
        return output
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute dir {path} on device. Error:\n{e}"
            )

def execute_archive_config(device):
    """ execute archive config in switch
        Args:
            device ('obj'): Device object
        Returns:
            Execution output
        Raises:
            SubCommandFailure
    """
    cmd = f'archive config'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to do archive config on device {device}. Error:\n{e}"
            )

def execute_switch_clear_stack_mode(device):
    """ Execute clear stack-mode for a switch
        Example: switch clear stack-mode
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Executing 'switch clear stack-mode' on the device")
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Do you wish to continue\?\s*\[y\/n\]\? \[yes\]:",
                action='sendline(y)',
                loop_continue=False,
                continue_timer=False
            )
        ]
    )
    cmd = f'switch clear stack-mode'
    try:
        device.execute(cmd, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to clear the stack-mode on device {device.name}. Error:\n{e}'
        )

def execute_switch_role(device, switch_number, mode):
    """ Execute switch <switch_number> role <mode> for a switch
        Example: switch 2 role active
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number (Range: 1-16)
            mode ('str'): set the new switch to Active or Standby mode
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Executing 'switch {switch_number} role {mode}' on the device")
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Do you want to continue\?\s*\[y\/n\]\? \[yes\]:.*",
                action='sendline(y)',
                loop_continue=True,
                continue_timer=False
            )
        ]
    )
    cmd = f'switch {switch_number} role {mode}'
    try:
        device.execute(cmd, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to change the switch {switch_number} mode to {mode} on {device.name}. Error:\n{e}'
        )

def uninstall_appliance_package(device, name):
    """ uninstall appliance package

        Args:
            device (`obj`): Device object
            name(`str`): appliance package name
        Return:
            None
        Raise:
            SubCommandFailure: Failed to uninstall appliance package
    """

    try:
        device.execute("virtual-service uninstall name {name}".format(name=name))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not uninstall appliance package, Error: {error}'.format(error=e)
        )


def execute_request_platform_software_package_install_switch_rollback_auto_copy(device, switch='all'):
    """ Execute request platform software package install switch rollback on-reboot auto-copy
        Args:
            device ('obj'): Device object
            switch('str', optional): Switch id, or 'all' for all switches
        Returns:
            Execution output
        Raises:
            SubCommandFailure
    """
    cmd = f'request platform software package install switch {switch} rollback on-reboot auto-copy'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to request platform software package install switch rollback on-reboot auto-copy on device {device}. Error:\n{e}"
            )


def request_platform_software_process_core(device, process_type, processor_slot, switch_type=None, chassis_type=None):
    """ Perform request platform software process core
        Args:
            device ('obj'): Device object
            process_type ('str'): Proess type. ex: ios, host-manager.
            processor_slot ('str'): Processor slot.
            switch_type ('str'): Switch type or number. ex: active, standby, 0.
            chassis_type ('str'): Chassis type or number. ex: active, standby, 0.
        Returns:
            Command output
        Raises:
            SubCommandFailure
    """

    cmd = f'request platform software process core {process_type} '
    if switch_type:
        cmd += f'switch {switch_type} '

    if chassis_type:
        cmd += f'chassis {chassis_type} '

    cmd += f'{processor_slot}'

    try:

        output = device.execute(cmd)
        return output
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to perform request platform software process core on the device. Error:\n{e}")

def execute_clear_redundancy_history(device):
    """ clear redundancy history
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    try:
        device.execute('clear redundancy history')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not execute clear redundancy history on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def execute_set_platform_hardware_fed_qos(device, mode, qos_type, interface, switch=None, oq_id=None, counter_set=None):
    """ Execute Fed qos interface on device
        Args:
            device ('obj'): Device object
            mode('str'): Switch mode. Ex: active, standby, 3
            qos_type('str'): multicast or port-mirror
            interface('str'): interface number
            switch('str', optional): Configure when switch is stack. Default is None
            oq_id('str', optional): multicast oq id. Default is None
            counter_set('str', optional): attach or detach counter set. Default is None
        Return:
            None
        Raise:
            SubCommandFailure: Failed to execute Fed qos interface on device
    """

    cmd = f'set platform hardware fed'
    if switch:
        cmd += f' switch {mode} qos {qos_type} interface {interface}'
    else:
        cmd += f' {mode} qos {qos_type} interface {interface}'
    if oq_id:
        cmd += f' oq_id {oq_id}{f" {counter_set}" if counter_set else ""}'

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not execute Fed qos interface on device, Error: {e}')


def execute_reload_fast(device, fast_type=None, username=None, password=None, prompt_wait_time=10, timeout=600):
    """ Execute Halt and perform a cold restart for XFSU device

    Args:
        device ('obj'): device to use
        fast_type ('fast_type', Optional): type can be "enhanced" or none based on version
        username ('username', Optional): Console username
        password ('password', Optional): Console Password
        timeout ('int, optional'): Timeout value (Default value - 600s)
        prompt_wait_time ('int, optional'): Time to wait before sending the prompt(Default value - 10s)
    Returns:
        True if reload fast is successful
    Raises:
        SubCommandFailure: Failed to execute Halt and perform a cold restart for XFSU device
    """
    log.debug(f"Performing Reload Fast on {device.name}")

    def slow_sendline(spawn):
        time.sleep(prompt_wait_time)
        spawn.sendline('')

    def send_password(spawn):
        time.sleep(prompt_wait_time)
        spawn.sendline(password)

    def send_username(spawn):
        time.sleep(prompt_wait_time)
        spawn.sendline(username)

    dialog = Dialog([
        Statement(pattern=r'.*\[y\/n\/q\]',
                  action='sendline(y)', loop_continue=True, continue_timer=True),
        Statement(pattern=r'Press RETURN to get started',
                  action=slow_sendline,
                  loop_continue=True, continue_timer=True),
        Statement(pattern=r'Username\:',
                  action=send_username,
                  loop_continue=True, continue_timer=True),
        Statement(pattern=r'Password\:',
                  action=send_password,
                  loop_continue=True, continue_timer=False),
        Statement(pattern=r'%s\>' % device.name,
                  action="sendline(enable)",
                  loop_continue=True, continue_timer=True)])

    cmd = "reload fast"
    if fast_type:
        cmd += f" {fast_type}"

    try:
        device.execute(cmd, reply=dialog, timeout=timeout, append_error_pattern=[r'.*FAILED\:.*'])
        log.debug(f"Reload Fast successfully executed")
        return True

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute and perform a reload fast for XFSU device {device}. Error:\n{e}")

def config_smart_save_license_usage(device, day, file_name):
    """ configure smart save license usage
        Args:
            device (`obj`): Device object
            day ('str'): Last days of usage
            file_name ('str'): Save usage reports to file
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to configure smart save license usage
    """
    log.debug("configure smart save license usage")

    cmd = f"license smart save usage day {day} file {file_name}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure smart save license usage. Error:\n{e}")

def config_smart_authorisation_request(device, feature_name, parameter):
    """ configure smart authorisation request
        Args:
            device ('obj'): Device object
            feature_name ('str'): Feature name
            parameter ('str'): all{Get auth code for all device in HA config} or
                local {Get auth code for all device in local device}

        Returns:
            None
        Raise:
            SubCommandFailure: Failed to configure smart authorisation request
    """
    log.debug("configure smart authorisation request")

    cmd = f"license smart authorization request add {feature_name} {parameter}"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure smart authorisation request. Error:\n{e}")


def execute_dir_file_system(device, file_system, sub_directory=None, timeout=120):
    """ Execute dir file_system
        Example: dir flash:
        Args:
            device ('obj'): Device object
            file_system ('str'): specifying filesystems such as bootflash:,usb:, flash:, flash-1:, flash2:/crashinfo:, crashinfo-1: , crashinfo2:
            sub_directory('str'): specifying the subdirectory inside the filesystem
            timeout ('int'): Max time to print dir output
        Returns:
            output
        Raises:
            SubCommandFailure
    """
    try:
        if sub_directory :
            output = device.execute(f"dir {file_system}/{sub_directory}",timeout=timeout)
        else:
            output = device.execute(f"dir {file_system}",timeout=timeout)

        return output
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute dir {file_system} on device. Error:\n{e}"
            )


def execute_archive_tar(device, tar_filename, operation_type, src_filesystem, src_filepath=None, dest_filesystem=None, dest_filepath=None, timeout=120):
    """ Execute archive tar
        Example: archive tar /create usb0:usb_files.tar bootflash:/tracelogs
                 archive tar /xtract usb0:usb_files.tar usb0:new-tar-files
        Args:
            device ('obj'): Device object
            dest_filesystem ('str'): specifying filesystems such as bootflash:,usb:, tftp:
            tar_filename('str'): tar filename
            operation_type('str'): Option can be xtract, table, create
            src_filesystem ('str'): specifying filesystems such as bootflash:,usb:, tftp:
            src_filepath ('str',optional): specifying files path which need to be archived,Default is None
            dest_filepath ('str',optional): specifying destination path of tar file,Default is None
            timeout ('int',optional): Max time for completion of cli execution,Default is 120 seconds
        Returns:
            output
        Raises:
            SubCommandFailure
    """
    if operation_type not in ('create', 'xtract', 'table') :
        raise ValueError('Operation type must be "xtract", "table" or "create"')

    cmd = f"archive tar /{operation_type} "
    dest = f" {dest_filesystem}"
    if dest_filepath:
        dest += f"{dest_filepath}/"
    src = f" {src_filesystem}"
    if src_filepath:
        src += f"{src_filepath}/"
    if operation_type == 'create':
        cmd +=  f"{dest}{tar_filename} {src}"
    elif operation_type == 'xtract':
        cmd += f"{src}{tar_filename} {dest}"
    elif operation_type == 'table':
        cmd += f"{src}{tar_filename}"

    try:
        output = device.execute(cmd, timeout=timeout)
        return output
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not execute archive tar on device. Error:\n{e}"
            )


def clear_ip_mfib_counters(device):
    """ clear ip mfib counters
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug(f"Clear ip mfib counters on {device}")

    try:
        device.execute('clear ip mfib counters')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not clear ip mfib counters on {device}. Error:\n{e}"
        )


def execute_switch_card_OIR_power_force(device, card_slot, subslot):
    """ execute oir power force
    Args:
        device ('obj'): Device object
        card_slot('str'): card slot number
        subslot('str'): subslot number
    Return:
        None
    Raise:
        SubCommandFailure
    """
    log.info(f"Executing hw-module subslot {card_slot}/{subslot} oir power force")

    cmd=f"hw-module subslot {card_slot}/{subslot} oir power force"

    try:
        device.execute(cmd)

    except SubCommandFailure as e:

        raise SubCommandFailure(f"Could not execute hw-module subslot {card_slot}/{subslot} oir power force. Error:\n{e}")


def request_platform_software_package_expand(device, file_system, test_image, sub_directory=None,timeout=240):
    """ Perform request platform software package expand file {file_system}/{sub_directory}/{test_image}
        Perform request platform software package expand file {file_system}/{test_image}
        Args:
            device ('obj'): Device object
            file_system ('str'): bootflash: , harddisk: , usb0:
            test_image ('str'): image_name
            sub_directory ('str',optional):  subdirectory inside the filesystem where the test image is present,Default is None
            timeout ('int'): Max time
        Returns:
                None
        Raises:
                SubCommandFailure
    """

    try:
        if sub_directory:
            cmd = f'request platform software package expand file {file_system}/{sub_directory}/{test_image}'

        else :
            cmd = f'request platform software package expand file {file_system}/{test_image}'

        device.execute(cmd,timeout=timeout)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to perform request platform software package expand on the device. Error:\n{e}")


def execute_clear_ipv6_mld_group(device, interface=None):
    """ clear ipv6 mld group
        Args:
            device (`obj`)           : Device object
            interface('str',optional): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug(f"Clear ipv6 mld group on {device}")

    cmd = "clear ipv6 mld group"
    if interface:
        cmd += f" {interface}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear ipv6 mld group on {device}. Error:\n{e}")


def execute_clear_ip_igmp_group(device, interface=None):
    """ clear ipv6 mld group
        Args:
            device (`obj`)           : Device object
            interface('str',optional): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug(f"clear ip igmp group on {device}")
    cmd = "clear ip igmp group"
    if interface:
        cmd += f" {interface}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear ip igmp group on {device}. Error:\n{e}")

def execute_more_file(device, filepath, regex):
    """ Executes more file <filepath> | inc <regex>
        Example : more bootflash:test.txt | inc ucode
        Args:
            device ('obj'): device to use
            filepath ('str'): path to the file, including the filename (eg. bootflash:test.txt)
            regex ('str',optional): regular expression for the inc (eg. ucode)
        Returns:
            output
        Raises:
            SubCommandFailure
    """
    log.debug(f'Executing more {filepath} | i {regex} on {device.name}')
    cmd = f'more {filepath}'
    if regex:
        cmd += f' | i {regex}'
    try:
        output = device.execute(cmd)
        return output

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to execute more {filepath} | count {regex} on device {device.name}. Error:\n{e}'
        )

def execute_platform_virtualization(device, slot_type, slot_status):
    """ Executes set platform hardware rom-monitor virtualization <slot_type> <slot_status>
        Example : set platform hardware rom-monitor virtualization rp active
        Args:
            device ('obj'): device to use
            slot_type ('str'): slot type options F0,F1,FP,R0,R1,RP
            slot_status ('str', optional): options can be active,standby. Applicable only for slot types RP and FP.
        Returns:
            output
        Raises:
            SubCommandFailure
    """
    log.debug(f'Executing set platform hardware rom-monitor virtualization {slot_type} {slot_status} on {device.name}')
    cmd = f'set platform hardware rom-monitor virtualization {slot_type}'

    if slot_status:
        cmd += f' {slot_status}'

    try:
        output = device.execute(cmd)
        return output
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to execute set platform hardware rom-monitor virtualization {slot_type} {slot_status} on device {device.name}. Error:\n{e}'
        )

def clear_ip_pim_rp_mapping(device):
    """ clear ip pim rp-mapping
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Clear ip pim rp-mapping on {device}")

    try:
        device.execute('clear ip pim rp-mapping')

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not clear ip pim rp-mapping on {device}. Error:\n{e}")


def execute_event_manager_run_with_reload(device,username,password,
                                            embedded_event_name="RELOAD",sleep_time=10):
    """ Execute event manager with Embedded Event Manager policy name
        Args:
            device ('obj'): device to use
            embedded_event_name ('str'): Embedded Event Manager policy name
            username ('str'): username
            password ('str'): password
            sleep_time : sleep time
        Returns:
            True if reload successful else False
        Raises:
            SubCommandFailure
    """
    def slow_sendline(spawn):
        time.sleep(sleep_time)
        spawn.sendline()

    def send_password(spawn):
        time.sleep(sleep_time)
        spawn.sendline(password)

    def send_username(spawn):
        time.sleep(sleep_time)
        spawn.sendline(username)

    dialog = Dialog ([
             Statement(pattern=r'.*\[y\/n\/q\]',
                               action='sendline(y)', loop_continue=True, continue_timer=True),

             Statement(pattern=r'.*Press RETURN to get started.*',
                               action= slow_sendline,
                               loop_continue=True, continue_timer=True),
             Statement(pattern=r'Username\:',
                               action= send_username,
                               loop_continue=True, continue_timer=True),
             Statement(pattern=r'Password\:',
                               action= send_password,
                               loop_continue=True, continue_timer=False),
             Statement(pattern=r'%s\>' % device.name,
                               action= "sendline(enable)",
                               loop_continue=True, continue_timer=True),
             Statement(pattern=r'Password\:',
                               action= send_password,
                               loop_continue=True, continue_timer=False),
             Statement(pattern=r'%s\#' % device.name,
                               action= None,
                               loop_continue=False, continue_timer=False)])

    cmd = f'event manager run {embedded_event_name}'
    try:
        output = device.execute(cmd, reply=dialog)
    except Exception as err:
        log.error("Failed to execute the command: {err}".format(err=err))

    if 'FAILED:' in output:
        log.debug(f"Reload is failed on {device.name}")
        return False
    log.debug(f"Reload is successful on {device.name}")
    return True

def request_platform_software_trace_rotate_all(device):
    """ Request platform software trace rotate all
    Args:
        device (`obj`): Device object

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = f"request platform software trace rotate all"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not perform request platform software rotate all {device}. Error:\n{e}")

def platform_software_fed_switch_phy_options(device, mode, lpn, phy_info, read_mode, phy_mode, phy_side, phy_device_id, phy_page_number, phy_register_address):
    """
    Execute 'test platform software fed switch' command with the specified parameters.

    Args:
        device (obj): Device object
        mode(str) : 'active'
        lpn (int): Local Port Number value (1-96)
        phy_info (int): Phy mode (0-1)
        read_mode (str): read,write,dump
        phy_mode(int) : <0-1> 0/1 - Mode - Mdio clause 22/45
        phy_side (int): Phy line/system side (0-1)
        phy_device_id (int): Phy device_id (0-255)
        phy_page_number (int): Phy page number (0-65535)
        phy_register_address (int): Phy register address (0-65535)

    Returns:
        str: Output of the command
    Raises:
        SubCommandFailure: Failed executing the command
    """

    cmd = f"test platform software fed switch {mode} xcvr lpn {lpn} {phy_info} {read_mode} {phy_mode} {phy_side} {phy_device_id} {phy_page_number} {phy_register_address}"

    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute command. Error:\n{e}")

def test_platform_software_usb_fake_insert_remove(device, switch_num, usbflash, action):
    """
    Execute 'test platform software usb slot <switch_num> <usbflash> <action>' command on the device.

    Args:
        device (obj): Device object
        switch_num (int): Slot or switch number
        usbflash (str): USB flash identifier ('usbflash1' or 'usbflash2')
        action (str): Action to perform ('fake-insert' or 'fake-remove')

    Returns:
        str: Output of the command
    """
    command = f"test platform software usb slot {switch_num} {usbflash} {action}"

    try:
        device.execute(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to perform fake insert/remove. Error:\n{e}")

def test_platform_software_fru_fake_insert_remove(device, switch_num, action):
    """
    Execute 'test platform software fed switch {switch_num} fru {action}' command on the device.

    Args:
        device (obj): Device object
        switch_num (int): Slot or switch number
        action (str): Action to perform ('fake-insert' or 'fake-remove')

    Returns:
        str: Output of the command
    """
    log.debug(f"Perform fake insert/remove for fru on {device}")

    command = f"test platform software fed switch {switch_num} fru {action}"

    try:
        device.execute(command)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to perform fake insert/remove for fru. Error:\n{e}")


def platform_hardware_fed_switch_phy_debug(device, mode, port_num, debug_command_options):
    """Execute a PHY debug command on the specified switch and port
    Args:
        device ('obj'): Device to use
        mode ('str'): Mode identifier (e.g., 'active')
        port_num ('int'): Port number
        debug_command_options ('str'): Debug command to execute
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    cmd = f"test platform hardware fed switch {mode} port {port_num} phy phy-debug Debug_Command {debug_command_options}"

    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to execute PHY debug command. Error:\n{e}")

def execute_diagnostic_start_switch_port(device, switch_number, test_id, port_num):
    """ execute diagnostic start switch 1 test
        Args:
            device ('obj'): Device object
            test_id ('str'): Test ID list (e.g. 1,3-6) or Test Name or minimal  or complete
              Interface port number WORD    Port number list (e.g. 2,4-7)
            switch_number ('int'): Switch number on which diagnostic has to be performed
            port ('str'): word (e.g. 1-8 or all)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if test_id and port_num:
        cmd = f"diagnostic start switch {switch_number} test {test_id} port {port_num}"
    else:
        raise ValueError("Both test_id and port_num must be provided.")
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(

        f"Could not execute diagnostic start switch {switch_number} test {test_id} on device. Error:\n{e}")

def request_platform_hardware_pfu(device, mode, route_processor, slot, action):
    """ request  platform  hardware  pfu  switch  1  R0 set-power-slot 0 on
        Args:
            device (obj): Device object
            mode (str): The switch number or mode. Specify as a number (e.g., '1', '2') or as a mode such as 'active' or 'standby' to identify the target switch.
            route_processor (str): The route processor unit for the switch, such as 'R0' or 'RP'. This typically identifies the control processor for the specified switch.
            slot (int): The slot number for the hardware component or module where the power will be set. Use '0' or a relevant slot number, depending on the switch type or configuration.
            action ('str'): off/on
        Returns:
            Command output
        Raises:
            SubCommandFailure
    """

    cmd = f'request platform hardware pfu switch {mode} {route_processor} set-power-slot {slot} {action}'

    try:
        output = device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to perform powerslot  off/on Error:\n{e}")

def request_platform_software_trace_archive(device):
    """Request platform software trace archive
    Args:
        device (`obj`): Device object
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring
    """
    cmd = "request platform software trace archive"
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not perform request platform software trace archive on {device}. Error:\n{e}")


def execute_issu_set_rollback_timer(device, timer=0):
    """
    Performs issu set rollback-timer on device
    Args:
        device ('obj'): Device object
		timer:	<0-7200>  Rollback timer in <seconds> format or hh:mm:ss  Rollback timer in hh:mm:ss format
    Returns:
        None
    Raises:
        SubCommandFailure
    """

    try:
        output = device.configure(f"issu set rollback-timer {timer}")
    except SubCommandFailure:
        raise SubCommandFailure("Rollback timer should be in <seconds> format (0-7200) or hh:mm:ss format")