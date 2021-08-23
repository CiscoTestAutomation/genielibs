'''
IOSXR specific clean stages
'''

# Python
import os
import time
import logging
import re

# pyATS
from pyats.log.utils import banner
from pyats.utils.fileutils import FileUtils

# Genie
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.clean.stages.iosxe.stages import TftpBoot as IOSXETftpBoot
from genie.metaparser.util.schemaengine import Optional

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


class LoadPies(BaseStage):
    """This stage installs provided pies onto the device.

Stage Schema
------------
load_pies:

    files (list): List of XR pies to install

    server (str, optional): Hostname or IP address of server to use for install
        command. Defaults to None (Looks in the testbed YAML for a TFTP server)

    prompt_level (str, optional): Prompt-level argument for install command.
        Defaults to 'none'.

    synchronous (bool, optional): Synchronous option for install command.
        Defaults to None.

    install_timeout (int, optional): Maximum time in seconds allowed for
        execution of the install command to complete. Defaults to 600.

    max_time (int, optional): Maximum time in seconds to wait while verifying
        the pies installed. Defaults to 300.

    check_interval (int, optional): Time interval in seconds while verifying
        the pies installed. Defaults to 30.

Example
-------
load_pies:
    files:
        - /auto/path/to/image/asr9k-mcast-px.pie-7.3.1.08I
        - /auto/path/to/image/asr9k-mgbl-px.pie-7.3.1.08I
        - /auto/path/to/image/asr9k-mpls-px.pie-7.3.1.08I
    server: 10.1.6.244
    prompt_level: 'all'
    synchronous: True
    timeout: 150
    max_time: 300
    check_interval: 20
"""

    # =================
    # Argument Defaults
    # =================
    SERVER = None
    PROMPT_LEVEL = 'none'
    SYNCHRONOUS = True
    INSTALL_TIMEOUT = 600
    MAX_TIME = 300
    CHECK_INTERVAL = 60

    # ============
    # Stage Schema
    # ============
    schema = {
        'files': list,
        Optional('server'): str,
        Optional('prompt_level'): str,
        Optional('synchronous'): bool,
        Optional('install_timeout'): int,
        Optional('max_time'): int,
        Optional('check_interval'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'install_pies',
        'verify_pies_installed'
    ]

    def install_pies(self, steps, device, files, server=SERVER,
                     prompt_level=PROMPT_LEVEL,
                     synchronous=SYNCHRONOUS,
                     install_timeout=INSTALL_TIMEOUT):

        self.installed_packages = []

        with steps.start("Install and activate pie files on device {}".\
                        format(device.name)) as step:

            # Install pie files on device
            for file in files:

                # Install and activate pie
                log.info(banner("Install and activate pie: {}".format(file)))

                try:
                    device.api.execute_install_pie(
                        image_dir=os.path.dirname(file),
                        image=os.path.basename(file),
                        server=server,
                        prompt_level=prompt_level,
                        synchronous=synchronous,
                        install_timeout=install_timeout)
                except Exception as e:
                    log.error(str(e))
                    step.failed("Unable to install or activate pie file {} on "
                                   "device {}".format(file, device.name))
                else:
                    self.installed_packages.append(os.path.basename(file).split(".pie")[0])
                    log.info("Installed and activated file {} on device {}".\
                            format(file, device.name))

            step.passed("Succesfully installed and activated all the pie files provided")

    def verify_pies_installed(self, steps, device, check_interval=CHECK_INTERVAL,
                              max_time=MAX_TIME):

        with steps.start("Verify installed pie files are activated on device {}".\
                        format(device.name)) as step:

            # Verify pie file is successfully installed
            if not device.api.verify_installed_pies(
                        installed_packages=self.installed_packages,
                        check_interval=check_interval,
                        max_time=max_time):
                step.failed("Unable to activate pie files on device {}".\
                                format(device.name))
            else:
                step.passed("Successfully activated pie files on device {}".\
                                format(device.name))


class TftpBoot(IOSXETftpBoot):
    """This stage boots a new image onto your device using the tftp booting
method.

Stage Schema
------------
tftp_boot:

    image (list): Image to boot with

    ip_address (list): Management ip address to configure to reach to the
        tftp server

    subnet_mask (str): Management subnet mask

    gateway (str): Management gateway

    tftp_server (str): Tftp server that is reachable with management interface

    timeout (int, optional): Max time during which tftp boot must
        complete. Defaults to 600.

    config_reg_timeout (int, optional): Max time to set config-register.
        Defaults to 30.

    device_reload_sleep (int, optional): Time in seconds to wait after
        reloading the device. Defaults to 20.

    recovery_username (str, optional): Enable username for device
        required after bootup. Defaults to None.

    recovery_password (str, optional): Enable password for device
        required after bootup. Defaults to None.

Example
-------
tftp_boot:
    image:
        - /auto/some-location/that-this/image/asr9k-mini-px.vm
    ip_address: [10.1.7.126, 10.1.7.127]
    gateway: 10.1.7.1
    subnet_mask: 255.255.255.0
    tftp_server: 11.1.7.251
    timeout: 1200
    config_reg_timeout: 60
    device_reload_sleep: 300
    recovery_username: admin
    recovery_password: nbv_12345

Note: There is more than one ip address, one for each supervisor.
"""

    # =================
    # Argument Defaults
    # =================
    RECOVERY_PASSWORD = None
    RECOVERY_USERNAME = None
    TIMEOUT = 600
    CONFIG_REG_TIMEOUT = 30
    CONFIG_REG_ROMMON = '0x1820'
    CONFIG_REG_NORMAL = '0x1922'
    DEVICE_RELOAD_SLEEP = 20

    # ============
    # Stage Schema
    # ============
    schema = {
        'image': list,
        'ip_address': list,
        'subnet_mask': str,
        'gateway': str,
        'tftp_server': str,
        Optional('timeout'): int,
        Optional('config_reg_timeout'): int,
        Optional('device_reload_sleep'): int,
        Optional('recovery_username'): str,
        Optional('recovery_password'): str,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'set_config_register',
        'go_to_rommon',
        'tftp_boot',
        'reconnect',
        'reset_config_register',
        'write_memory'
    ]

    def go_to_rommon(self, steps, device, device_reload_sleep=DEVICE_RELOAD_SLEEP):
        with steps.start("Bring device {} down to rommon > prompt prior to TFTP boot".\
                            format(device.name)) as step:

            # Reload device
            try:
                device.admin_execute("reload location all")
            except Exception as e:
                # We now want to overwrite the statemachine
                device.destroy_all()

                # Sleep to make sure the device is reloading
                time.sleep(device_reload_sleep)
            else:
                step.failed("Unable to bring the device down to rommon> prompt")


class InstallImageAndPackages(BaseStage):
    """This stage installs the provided image and optional packages onto
your device using the install CLI. The stage will also handle the
automatic reload.

Stage Schema
------------
install_image_and_packages:

    image (list): Image to install on the device.

    packages (list, optional): Packages to install on the device. Defaults to None.

    tftp_server (str, optional): TFTP Server that should be used when installing
        via tftp. Defaults to None.

    remove_inactive_pkgs (bool, optional): If True remove all the inactive
        packages before attempting installation. Defaults to True.

    install_timeout (int, optional): Max time in seconds allowed for install
        operations. Defaults to 300.

    reload_timeout (int, optional): Max time in seconds allowed for the reload
        to complete. Defaults to 900.

    commit_sleep (int, optional): Time in seconds to sleep before executing
        'install commit'. Defaults to 180.

    source_directory (str, optional): Directory to copy from. Defaults to 'harddisk:'

Example
-------
install_image_and_packages:
    image:
        - flash:image.iso
    packages:
        - flash:package.rpm

or

install_image_and_packages:
    image:
        - /tftp_path/image.iso
    packages:
        - /tftp_path/package.rpm
    tftp_server: tftp_server_1
    remove_inactive_pkgs: True
    install_timeout: 2700
    reload_timeout: 800
    commit_sleep: 180

or

images:
    - /path/to/system.iso
    - /path/to/package1.rpm
    - /path/to/package2.rpm

install_image_and_packages:
    source_directory: "disk1:"

"""

    # =================
    # Argument Defaults
    # =================
    TFTP_SERVER = None
    REMOVE_INACTIVE_PKGS = True
    INSTALL_TIMEOUT = 300
    RELOAD_TIMEOUT = 900
    COMMIT_SLEEP = 180
    SOURCE_DIRECTORY= 'harddisk:'

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('image'): list,
        Optional('packages'): list,
        Optional('tftp_server'): str,
        Optional('remove_inactive_pkgs'): bool,
        Optional('install_timeout'): int,
        Optional('reload_timeout'): int,
        Optional('commit_sleep'): int,
        Optional('source_directory'): str
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'clear_in_progress_installs',
        'remove_inactive_pkgs',
        'update_install_repository',
        'install_activate',
        'reconnect',
        'install_commit'
    ]

    # Commonly used patterns
    could_not_start_install_pattern = r".*Could not start this install operation.*"
    install_operation_aborted_pattern = r".*Install operation (?P<id>\d+) aborted.*"
    error_patterns = [
        could_not_start_install_pattern,
        install_operation_aborted_pattern
    ]
    successful_operation_string = \
        r".*Install operation (?P<id>\d+) finished successfully.*"

    def _getFileNameFromPath(self, str):
        """ Internal Method to retrieve fileame from an XR path.
        Work with the following format :
            - <dir>:<image>
            - <dir>:<special>/<folder>/<to>/<image_file>
            - <dir>:<folder>/<image>

        Returns:
            tuple (dirname, filename)
        """
        delimiter = '/'
        if str.find(delimiter) == -1:
            delimiter = ':'
        outList = str.split(delimiter)
        dirname = ''
        len(outList)
        for i in range(0, len(outList) - 1):
            dirname += outList[i] + delimiter

        filename = outList[-1]

        return dirname, filename

    def clear_in_progress_installs(self, steps, device, install_timeout=INSTALL_TIMEOUT):

        with steps.start("Running install commit to clear any in progress "
                         "installs") as step:

            try:
                device.execute("install commit")
                output = device.expect(
                    [self.successful_operation_string, self.install_operation_aborted_pattern],
                    timeout=install_timeout)
                error = re.search(self.install_operation_aborted_pattern, output.match_output)
                if error:
                    device.execute("show install log " + error.groupdict()['id'])
                    step.failed("The command 'install commit' aborted ")
            except Exception as e:
                step.failed("The command 'install commit' failed. Reason: "
                            "{}".format(str(e)))

    def remove_inactive_pkgs(self, steps, device,
                             remove_inactive_pkgs=REMOVE_INACTIVE_PKGS,
                             install_timeout=INSTALL_TIMEOUT):
        # Remove inactive packages to avoid installation errors
        if remove_inactive_pkgs:
            with steps.start("Running install remove inactive packages"
                             " to avoid installation errors") as step:
                try:
                    device.execute("install remove inactive all",
                                   error_pattern=self.error_patterns)
                    output = device.expect(
                        [self.successful_operation_string, self.install_operation_aborted_pattern],
                        timeout=install_timeout)
                    error = re.search(self.install_operation_aborted_pattern, output.match_output)
                    if error:
                        device.execute("show install log " + error.groupdict()['id'])
                        step.passx("The command 'install remove inactive all' aborted ")
                except Exception as e:
                    step.passx("The command 'install remove inactive all' failed. Reason: "
                               "{}".format(str(e)))

    def update_install_repository(self, steps, device, image,
                                  tftp_server=TFTP_SERVER,
                                  packages=None,
                                  install_timeout=INSTALL_TIMEOUT,
                                  source_directory=SOURCE_DIRECTORY):
        if packages is None:
            packages = []

        with steps.start("Adding image and any provided packages to the "
                         "install repository") as step:

            # Get Ip address of tftp server if tftp_server is provided
            if tftp_server:
                if not hasattr(device.testbed, 'servers'):
                    step.failed("Cannot find any servers in the testbed")
                fu = FileUtils(testbed=device.testbed)
                tftp_server = fu.get_hostname(tftp_server)

            # Get Image Files from install_image_and_packages

            # Get Image Files from TFTP path if tftp_server is provided
            if tftp_server:
                # Separate directory and image
                directory, image = self._getFileNameFromPath(image[0])
                pkgs = ''
                for pkg in packages:
                    _, pkg = self._getFileNameFromPath(pkg)
                    pkgs += ' ' + pkg

                directory = '{p}://{s}/{f}'.format(p='tftp', s=tftp_server, f=directory)

            # Get Image Files in device location
            elif ':' in image[0]:
                # Separate directory and image
                directory, image = self._getFileNameFromPath(image[0])
                # Get packages and remove directories
                # pkgs = ' pkg1 pkg2 pkg3 ...'
                pkgs = ''
                for pkg in packages:
                    _, pkg = self._getFileNameFromPath(pkg)
                    pkgs += ' ' + pkg

            else:
                directory = source_directory
                _, image = self._getFileNameFromPath(image[0])
                # Get packages and remove directories
                # pkgs = ' pkg1 pkg2 pkg3 ...'
                pkgs = ''
                for pkg in packages:
                    _, pkg = self._getFileNameFromPath(pkg)
                    pkgs += ' ' + pkg

            # install add tftp://tftp_server_ip/tftp_path/ <image> <pkg1> <pkg2> or
            # install add source flash: <image> <pkg1> <pkg2>
            cmd = 'install add source {dir} {image} {packages}'.format(
                dir=directory, image=image, packages=pkgs)

            try:
                device.execute(
                    cmd,
                    timeout=install_timeout,
                    error_pattern=self.error_patterns)

                out = device.expect(
                    [self.successful_operation_string],
                    trim_buffer=False,
                    timeout=install_timeout)
            except Exception as e:
                step.failed("The command '{cmd}' failed. Error: {e}"
                            .format(cmd=cmd, e=str(e)))

            out = out.match_output

            # If code execution reaches here the regex has already been matched
            # via the expect. So we know it will match again here. We just need
            # to retrieve the operation id for the next steps.
            p1 = re.compile(self.successful_operation_string)
            for line in out.splitlines():
                m = p1.match(line)
                if m:
                    self.operation_id = m.groupdict()['id']
                    break

            step.passed("The command '{cmd}' succeeded. The "
                        "operation ID is '{operation_id}'"
                        .format(cmd=cmd, operation_id=self.operation_id))

    def install_activate(self, steps, device, install_timeout=INSTALL_TIMEOUT):
        with steps.start("Activating operation ID {}".format(self.operation_id)) as step:

            cmd = 'install activate id {id}'.format(id=self.operation_id)

            install_activate_dialog = Dialog([
                Statement(pattern='.*This install operation will reload the '
                                  'system\, continue\?.*\[yes[:\/]no\]\:\[yes\].*',
                          action='sendline(yes)',
                          loop_continue=False,
                          continue_timer=False)])

            try:
                # send the install cmd
                device.sendline(cmd)

                # Process the dialog that appears
                install_activate_dialog.process(
                    device.spawn, timeout=install_timeout)

                # Wait for successful output
                device.expect(
                    [self.successful_operation_string],
                    timeout=install_timeout)
            except Exception as e:
                step.failed("Attempting to activate install id '{id}' "
                            "failed. Error: {e}"
                            .format(id=self.operation_id, e=str(e)))

    def reconnect(self, steps, device, reload_timeout=RELOAD_TIMEOUT):
        with steps.start("Reconnecting to '{dev}'".format(
                dev=device.name)) as step:

            timeout = Timeout(reload_timeout, 60)
            while timeout.iterate():
                timeout.sleep()
                device.destroy()

                try:
                    device.connect(learn_hostname=True)
                except Exception as e:
                    connection_error = e
                    log.info("Could not connect to {dev}"
                             .format(dev=device.hostname))
                else:
                    step.passed("Connected to {dev}"
                                .format(dev=device.hostname))

            step.failed("Could not connect to {dev}. Error: {e}"
                        .format(dev=device.hostname, e=str(connection_error)))

    def install_commit(self, steps, device, commit_sleep=COMMIT_SLEEP,
                       install_timeout=INSTALL_TIMEOUT):
        with steps.start("Completing install") as step:

            try:
                log.info("Sleeping for {sleep} seconds to wait for all nodes to come up"
                         .format(sleep=str(commit_sleep)))
                time.sleep(commit_sleep)
                device.execute("install commit")

                output = device.expect(
                    [self.successful_operation_string, self.install_operation_aborted_pattern],
                    trim_buffer=False,
                    timeout=install_timeout)
                error = re.search(self.install_operation_aborted_pattern, output.match_output)
                if error:
                    device.execute("show install log " + error.groupdict()['id'])
                    step.failed("The command 'install commit' aborted ")
            except Exception as e:
                step.failed("The command 'install commit' failed. Reason: {}".format(str(e)))