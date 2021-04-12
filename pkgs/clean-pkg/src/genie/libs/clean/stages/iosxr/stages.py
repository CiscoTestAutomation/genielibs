'''
IOSXR specific clean stages
'''

# Python
import os
import time
import logging
import re

# pyATS
from pyats import aetest
from pyats.async_ import pcall
from pyats.log.utils import banner

# Genie
from genie.libs import clean
from genie.abstract import Lookup
from genie.libs.clean.recovery.recovery import _disconnect_reconnect
from genie.libs.clean.utils import clean_schema
from genie.utils.timeout import Timeout

# MetaParser
from genie.metaparser.util.schemaengine import Optional

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Logger
log = logging.getLogger(__name__)


#===============================================================================
#                       stage: load_pies
#===============================================================================

@clean_schema({
    'files': list,
    Optional('server'): str,
    Optional('prompt_level'): str,
    Optional('synchronous'): bool,
    Optional('install_timeout'): int,
    Optional('max_time'): int,
    Optional('check_interval'): int,
})
@aetest.test
def load_pies(section, steps, device, files, server=None, prompt_level='none',
    synchronous=True, install_timeout=600, max_time=300, check_interval=60):
    """ This stage installs provided pies onto the device.

    Stage Schema
    ------------
    load_pies:
        files ('list'): List of XR pies to install
        server('str'): Hostname or IP address of server to use for install command
                     Default None (testbed YAML reverse lookup for TFTP server)
        prompt_level('str'): Prompt-level argument for install command
                           Default 'none' (Optional)
        synchronous ('bool'): Synchronous option for install command
                            Default True (Optional)
        install_timeout ('int'): Maximum time required for install command execution to complete
                               Default 600 seconds (Optional)
        max_time ('int'): Maximum time to wait while checking for pies installed
                        Default 300 seconds (Optional)
        check_interval ('int'): Time interval while checking for pies installed
                              Default 30 seconds (Optional)

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

    log.info("Section steps:\n1- Install and activate pie files provided"
             "\n2- Verify installed pie files are activated")

    # Init
    installed_packages = []

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
                installed_packages.append(os.path.basename(file).split(".pie")[0])
                log.info("Installed and activated file {} on device {}".\
                        format(file, device.name))

        step.passed("Succesfully installed and activated all the pie files provided")


    with steps.start("Verify installed pie files are activated on device {}".\
                    format(device.name)) as step:

        # Verify pie file is successfully installed
        if not device.api.verify_installed_pies(
                    installed_packages=installed_packages,
                    check_interval=check_interval,
                    max_time=max_time):
            step.failed("Unable to activate pie files on device {}".\
                            format(device.name))
        else:
            section.passed("Successfully activated pie files on device {}".\
                            format(device.name))


#===============================================================================
#                       stage: tftp_boot
#===============================================================================

@clean_schema({
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
})
@aetest.test
def tftp_boot(section, steps, device, ip_address, subnet_mask, gateway,
    tftp_server, image, timeout=600, config_reg_timeout=30,
    device_reload_sleep=20, recovery_username=None, recovery_password=None):
    """ This stage boots a new image onto your device using the tftp booting
    method.

    Stage Schema
    ------------
    tftp_boot:
        image: <Image to boot with `list`> (Mandatory)
        ip_address: <Management ip address to configure to reach to the TFTP server `str`> (Mandatory)
        subnet_mask: <Management subnet mask `str`> (Mandatory)
        gateway: <Management gateway `str`> (Mandatory)
        tftp_server: <tftp server is reachable with management interface `str`> (Mandatory)
        timeout: <Maximum time during which TFTP boot process must complete `int`> (Optional, Default 600 seconds)
        config_reg_timeout: <Time to wait after setting config-register `int`> (Optional, Default 30 seconds)
        device_reload_sleep: <Time to wait after reloading device `int`> (Optional, Default 20 seconds)
        recovery_username: <Enable username for device required after bootup `str`> (Optional, Default None)
        recovery_password: <Enable password for device required after bootup `str`> (Optional, Default None)

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

    log.info("Section steps:"
             "\n1- Set config-register to 0x1820"
             "\n2- Bring device down to rommon> prompt prior to TFTP boot"
             "\n3- Begin TFTP boot"
             "\n4- Reconnect to device after TFTP boot"
             "\n5- Reset config-register to 0x1922")

    # Set config-register to 0x1820
    with steps.start("Set config-register to 0x1820 on {}".\
                    format(device.name)) as step:
        try:
            device.api.execute_set_config_register(config_register='0x1820',
                                                   timeout=config_reg_timeout)
        except Exception as e:
            step.failed("Unable to set config-register to 0x1820 prior to TFTP"
                           " boot on {}".format(device.name))

    # Bring the device down to rommon > prompt prior to TFTP boot
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


    # Begin TFTP boot of device
    with steps.start("Begin TFTP boot of device {}".format(device.name)) as step:

        # Need to instantiate to get the device.start
        # The device.start only works because of a|b
        device.instantiate(connection_timeout=timeout)

        tftp_boot = {'ip_address': ip_address,
                     'subnet_mask': subnet_mask,
                     'gateway': gateway,
                     'tftp_server': tftp_server,
                     'image': image}
        try:
            abstract = Lookup.from_device(device, packages={'clean': clean})
            # Item is needed to be able to know in which parallel child
            # we are

            # device.start only gets filled with single rp devices
            # for multiple rp devices we need to use subconnections
            if device.is_ha and hasattr(device, 'subconnections'):
                start = [i.start[0] for i in device.subconnections]
            else:
                start = device.start

            result = pcall(abstract.clean.recovery.recovery.recovery_worker,
                           start=start,
                           ikwargs = [{'item': i} for i, _ in enumerate(start)],
                           ckwargs = \
                                {'device': device,
                                 'timeout': timeout,
                                 'tftp_boot': tftp_boot,
                                 'break_count': 0,
                                 # Irrelevant as we will not use this pattern anyway
                                 # But needed for the recovery
                                 'console_activity_pattern': '\\.\\.\\.\\.',
                                 'golden_image': None,
                                 'recovery_username': recovery_username,
                                 'recovery_password': recovery_password})
        except Exception as e:
            log.error(str(e))
            step.failed("Failed to TFTP boot the device '{}'".\
                           format(device.name))
        else:
            log.info("Successfully performed TFTP boot on device '{}'".\
                     format(device.name))

    # Disconnect and reconnect to the device
    with steps.start("Reconnect to device {} after TFTP boot".\
                        format(device.name)) as step:
        if not _disconnect_reconnect(device):
            # If that still doesnt work, Thats all we got
            step.failed("Cannot reconnect to the device {d} after TFTP boot".
                            format(d=device.name))
        else:
            log.info("Success - Have recovered and reconnected to device '{}'".\
                     format(device.name))

    # Reset config-register to 0x1922
    with steps.start("Reset config-register to 0x1922 on {}".\
                        format(device.name)) as step:
        try:
            device.api.execute_set_config_register(config_register='0x1922',
                                                   timeout=config_reg_timeout)
        except Exception as e:
            log.error(str(e))
            step.failed("Unable to reset config-register to 0x1922 after TFTP"
                           " boot on {}".format(device.name))


@clean_schema({
    Optional('image'): list,
    Optional('packages'): list,
    Optional('install_timeout'): int,
    Optional('reload_timeout'): int
})
@aetest.test
def install_image_and_packages(section, steps, device, image, packages,
                           install_timeout=300, reload_timeout=900):
    """ This stage installs the provided image and optional packages onto
    your device using the install CLI. The stage will also handle the
    automatic reload.

    Stage Schema
    ------------
    install_image_and_packages:
        image:
            - <image to install> (Mandatory)
        packages:
            - <package to install> (Optional)
            - <package to install> (Optional)
        install_timeout: <timeout used for install operations, 'int', Default 300> (Optional)
        reload_timeout: <timeout used for device reloads, 'int', Default 900> (Optional)


    Example
    -------
    install_image_and_packages:
        image:
            - flash:image.iso
        packages:
            - flash:package.rpm

    """

    
    def _getFileNameFromPath(str):
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
        outList=str.split(delimiter)
        dirname = ''
        len(outList)
        for i in range(0,len(outList)-1):
            dirname += outList[i]+delimiter

        filename = outList[-1]

        return dirname, filename
    
    # Commonly used patterns
    error_patterns = [
        r".*Could not start this install operation.*",
        r".*Install operation \d+ aborted.*"]

    successful_operation_string = \
        r".*Install operation (?P<id>\d+) finished successfully.*"

    if ':' not in image[0]:
        section.failed("The image provided is not in the format '<dir>:<image>'"
                        "or '<dir>:<folder>/<image>'.")

    with steps.start("Running install commit to clear any in progress "
                     "installs") as step:

        try:
            device.execute("install commit")
            device.expect(
                [successful_operation_string],
                timeout=install_timeout)
        except Exception as e:
            step.failed("The command 'install commit' failed. Reason: "
                        "{}".format(str(e)))

    with steps.start("Adding image and any provided packages to the "
                     "install repository") as step:

        # Separate directory and image
        directory, image = _getFileNameFromPath(image[0])

        # Get packages and remove directories
        # pkgs = ' pkg1 pkg2 pkg3 ...'
        pkgs = ''
        for pkg in packages:
            _, pkg = _getFileNameFromPath(pkg)
            pkgs += ' '+pkg
            
        # install add source flash: <image> <pkg1> <pkg2>
        cmd = 'install add source {dir} {image} {packages}'.format(
            dir=directory, image=image, packages=pkgs)

        try:
            device.execute(
                cmd,
                timeout=install_timeout,
                error_pattern=error_patterns)

            out = device.expect(
                [successful_operation_string],
                trim_buffer=False,
                timeout=install_timeout)
        except Exception as e:
            step.failed("The command '{cmd}' failed. Error: {e}"
                        .format(cmd=cmd, e=str(e)))

        out = out.match_output

        # If code execution reaches here the regex has already been matched
        # via the expect. So we know it will match again here. We just need
        # to retrieve the operation id for the next steps.
        p1 = re.compile(successful_operation_string)
        for line in out.splitlines():
            m = p1.match(line)
            if m:
                operation_id = m.groupdict()['id']
                break

        step.passed("The command '{cmd}' succeeded. The "
                    "operation ID is '{operation_id}'"
                    .format(cmd=cmd, operation_id=operation_id))

    with steps.start("Activating operation ID {}".format(operation_id)) as step:

        cmd = 'install activate id {id}'.format(id=operation_id)

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
                [successful_operation_string],
                timeout=install_timeout)
        except Exception as e:
            step.failed("Attempting to activate install id '{id}' "
                        "failed. Error: {e}"
                        .format(id=operation_id, e=str(e)))

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

    with steps.start("Completing install") as step:

        try:
            device.execute("install commit")

            device.expect(
                [successful_operation_string],
                trim_buffer=False,
                timeout=install_timeout)
        except Exception as e:
            step.failed("The command 'install commit' failed. Reason: {}".format(str(e)))

