'''
IOSXR specific clean stages
'''

# Python
import os
import time
import logging

# pyATS
from pyats import aetest
from pyats.async_ import pcall
from pyats.log.utils import banner
from pyats.utils.fileutils import FileUtils

# Genie
from genie.libs import clean
from genie.abstract import Lookup
from .recovery import tftp_recover_from_rommon
from ..recovery import _disconnect_reconnect
from genie.libs.clean.utils import clean_schema

# MetaParser
from genie.metaparser.util.schemaengine import Optional

# Logger
log = logging.getLogger()


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

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
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

    Example:
    --------
    devices:
      PE1:
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

    Flow:
    -----
    before:
      apply_configuration (Optional, user wants to boot device without PIE or SMU files)
    after:
      tftp_boot (Optional, user wants to boot device without PIE or SMU files)
    '''

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
                section.failed("Unable to install or activate pie file {} on "
                               "device {}".format(file, device.name),
                               goto=['exit'])
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
            section.failed("Unable to activate pie files on device {}".\
                            format(device.name), goto=['exit'])
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
    '''
    Clean yaml file schema:
    -----------------------
        tftp_boot:
            image: <Image to boot with `str`> (Mandatory)
            ip_address: <Management ip address to configure to reach to the TFTP server `str`> (Mandatory)
            subnet_mask: <Management subnet mask `str`> (Mandatory)
            gateway: <Management gateway `str`> (Mandatory)
            tftp_server: <tftp server is reachable with management interface `str`> (Mandatory)
            timeout: <Maximum time during which TFTP boot process must complete `int`> (Optional, Default 600 seconds)
            config_reg_timeout: <Time to wait after setting config-register `int`> (Optional, Default 30 seconds)
            device_reload_sleep: <Time to wait after reloading device `int`> (Optional, Default 20 seconds)
            recovery_username: <Enable username for device required after bootup `str`> (Optional, Default None)
            recovery_password: <Enable password for device required after bootup `str`> (Optional, Default None)

    Example:
    --------
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

    Flow:
    -----
        Before:
            Any
        After:
            Connect
    '''

    log.info("Section steps:\n1- Verify global recovery has not recovered device"
             "\n2- Set config-register to 0x1820"
             "\n3- Bring device down to rommon> prompt prior to TFTP boot"
             "\n4- Begin TFTP boot"
             "\n5- Reconnect to device after TFTP boot"
             "\n6- Reset config-register to 0x1922")

    # If the tftp boot has already ran - recovery
    # Then do not run it again and skip this section
    if section.parameters['common_data'].get('device_tftp_booted'):
        section.skipped('The device recovery has already booted the device with'
                        ' the provided tftp image - no need to do it again')

    # Set config-register to 0x1820
    with steps.start("Set config-register to 0x1820 on {}".\
                    format(device.name)) as step:
        try:
            device.api.execute_set_config_register(config_register='0x1820',
                                                   timeout=config_reg_timeout)
        except Exception as e:
            section.failed("Unable to set config-register to 0x1820 prior to TFTP"
                           " boot on {}".format(device.name), goto=['exit'])

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
            section.failed("Unable to bring the device down to rommon> prompt",
                            goto=['exit'])

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
            result = pcall(abstract.clean.stages.recovery.recovery_worker,
                           start=device.start,
                           ikwargs = [{'item': i} for i, _ in enumerate(device.start)],
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
            section.failed("Failed to TFTP boot the device '{}'".\
                           format(device.name), goto=['exit'])
        else:
            log.info("Successfully performed TFTP boot on device '{}'".\
                     format(device.name))

    # Disconnect and reconnect to the device
    with steps.start("Reconnect to device {} after TFTP boot".\
                        format(device.name)) as step:
        if not _disconnect_reconnect(device):
            # If that still doesnt work, Thats all we got
            section.failed("Cannot reconnect to the device {d} after TFTP boot".
                            format(d=device.name), goto=['exit'])
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
            section.failed("Unable to reset config-register to 0x1922 after TFTP"
                           " boot on {}".format(device.name), goto=['exit'])

