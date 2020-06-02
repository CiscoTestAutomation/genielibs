'''
NXOS specific clean stages
'''

# Python
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
from ..recovery import _disconnect_reconnect
from genie.libs.clean.utils import clean_schema

# MetaParser
from genie.metaparser.util.schemaengine import Optional

# Logger
log = logging.getLogger(__name__)


@clean_schema({
    'images': {
        'system': str,
        Optional('kickstart'): str
    },
    Optional('copy_vdc_all'): bool,
    Optional('timeout'): int,
    Optional('max_time'): int,
    Optional('check_interval'): int,
    Optional('stabilize_time'): int,
    Optional('standby_copy_max_time'): int,
    Optional('standby_copy_check_interval'): int
})
@aetest.test
def change_boot_variable(section, steps, device, images, copy_vdc_all=False,
    timeout=300, max_time=300, check_interval=60, stabilize_time=100,
    standby_copy_max_time=300, standby_copy_check_interval=20):

    '''
    Clean yaml file schema:
    -----------------------
    devices:
        <device>:
            change_boot_variable:
                images:
                    kickstart: <kickstart image> (Optional)
                    system: <system image> (Mandatory)
                copy_vdc_all: <Copy on all VDCs, 'Boolean'> (Optional)
                timeout: <Execute timeout in seconds, 'int'> (Optional)
                max_time: <Maximum time section will take for checks in seconds, 'int'> (Optional)
                check_interval: <Time interval, 'int'> (Optional)
                stabilize_time: <Time in seconds till boot variables stabilization, 'int'> (Optional)
                standby_copy_max_time: <Maximum time section will take for checks in seconds, 'int'> (Optional)
                standby_copy_check_interval: <Time interval, 'int'> (Optional)


    Example:
    --------
    devices:
        N95_1:
            change_boot_variable:
                images:
                    kickstart: bootflash:/kisckstart.gbin
                    system: bootflash:/system.gbin
                copy_vdc_all: True
                timeout: 150
                max_time: 300
                check_interval: 20
                stabilize_time: 100
                standby_copy_max_time: 100
                standby_copy_check_interval: 10

    Flow:
    -----
    before:
        copy_to_device (Optional, If images to set as boot variable is not already on device)
    after:
        write_erase (Optional, user wants to reload with current running configuration or not)
    '''

    log.info("Section steps:\n1- Execute changing the boot variables"
             "\n2- Save running configuration to startup configuration"
             "\n3- Verify next boot variables as expected"
             "\n4- Verify files transfered successfully to the standby (if HA)")

    kickstart = images.get('kickstart')
    system = images.get('system')

    with steps.start("Changing the boot variables") as step:
        try:
            device.api.execute_change_boot_variable(kickstart=kickstart,
                                                    system=system,
                                                    timeout=timeout)
        except Exception as e:
            section.failed('{e}'.format(e=e), goto=['exit'])

    with steps.start("Save running configuration to startup "
                     "configuration") as step:
        try:
            device.api.execute_copy_run_to_start(copy_vdc_all=copy_vdc_all,
                                                 command_timeout=timeout,
                                                 max_time=max_time,
                                                 check_interval=check_interval)
        except Exception as e:
            step.failed('{e}'.format(e=e))


    with steps.start("Verify next boot variables") as step:
        try:
            device.api.is_next_reload_boot_variable_as_expected(
                                              kickstart=kickstart,
                                              system=system)
        except Exception as e:
            section.failed('{e}'.format(e=e), goto=['exit'])

    if device.is_ha:
        with steps.start("Verify the files transferred successfully to "
                         "the standby") as step:
            try:
                device.api.verify_files_copied_on_standby(
                                    max_time=standby_copy_max_time,
                                    check_interval=standby_copy_check_interval)
            except Exception as e:
                section.failed('{e}'.format(e=e))
    else:
        section.passed("Successfully loaded boot variables for {}".\
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
    'timeout': int,
    Optional('reboot_delay'): int,
    Optional('reconnect_delay'): int
})
@aetest.test
def tftp_boot(section, steps, device, ip_address, subnet_mask, gateway,
              tftp_server, image, timeout, reconnect_delay=60,
              reboot_delay=20):
    '''
    Clean yaml file schema:
    -----------------------
        tftp_boot:
            image: <Image to boot with `str`> (Mandatory)
            ip_address: <Management ip address to configure to reach to the TFTP server `str`> (Mandatory)
            subnet_mask: <Management subnet mask `str`> (Mandatory)
            gateway: <Management gateway `str`> (Mandatory)
            tftp_server: <tftp server is reachable with management interface> (Mandatory)
            timeout: <Maximum time for tftp boot `int`> (Mandatory)
            reboot_delay: <Maximum time for tftp boot `int`> (Optional)
            reconnect_delay: <Once device recovered, delay before final reconnect>, 'int'> (Default: 60)

    Example:
    --------
    tftp_boot:
        image:
          - /auto/some-location/that-this/image/stay-isr-image.bin
        ip_address: [10.1.7.126, 10.1.7.127]
        gateway: 10.1.7.1
        subnet_mask: 255.255.255.0
        tftp_server: 11.1.7.251

    There is more than one ip address, one for each supervisor.

    Flow:
    -----
        Before:
            Any
        After:
            Connect
    '''

    # If the tftp boot has already ran - recovery
    # Then do not run it again and skip this section
    if section.parameters['common_data'].get('device_tftp_booted'):
        section.skipped('The global recovery has already booted the device with'
                        ' the provided tftp image - no need to do it again')

    device.api.execute_write_erase_boot()
    # Using sendline, as we dont want unicon boot to kick in and send "boot" to
    # the device
    # Cannot use .reload as in case of HA, we need both sup to do the commands
    device.sendline('reload')
    device.sendline('y')
    device.sendline()
    log.info('** Rebooting the device **')

    # We now want to overwrite the statemachine
    device.destroy_all()
    # Sleep to make sure the device is reloading
    time.sleep(reboot_delay)

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
                             # Irrelevant as we will not use this pattern anyway
                             # But needed for the recovery
                             'break_count': 0,
                             'console_activity_pattern': '\\.\\.\\.\\.',
                             'golden_image': None,
                             'recovery_password': None})
    except Exception as e:
        log.error(str(e))
        section.failed("Failed to recover the device '{}'".\
                        format(device.name))
    else:
        log.info("Successfully recovered the device '{}'".\
                 format(device.name))

    log.info('Sleeping for {r} before reconnection'.format(r=reconnect_delay))
    time.sleep(reconnect_delay)

    # Disconnect and reconnect to the device
    if not _disconnect_reconnect(device):
        # If that still doesnt work, Thats all we got
        section.failed("Cannot reconnect to the device {d}".
                        format(d=device.name))
    else:
        log.info("Success - Have recovered and reconnected to device '{}'".\
                 format(device.name))

    log.info('Set the boot variables')
    output = device.api.get_running_image()
    if not output:
        section.failed('Could not retrieved the running image')
    image = output[0].rsplit('/', 1)[1]
    device.api.execute_change_boot_variable(system='bootflash:/{image}'
                                                  .format(image=image))
    device.api.execute_copy_run_to_start()
