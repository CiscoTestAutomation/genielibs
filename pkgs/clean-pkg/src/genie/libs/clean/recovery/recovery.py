'''Common OS recovery functions'''

# Python
import re
import time
import logging

# pyATS
from pyats.async_ import pcall
from pyats.results import Passed
from pyats.log.utils import banner

from unicon.eal.dialogs import Statement

# Genie
from genie.libs import clean
from genie.abstract import Lookup
from genie.libs.clean.utils import clean_schema

# MetaParser
from genie.metaparser.util.schemaengine import Optional, Or

# Logger
log = logging.getLogger(__name__)

CONTINUE_RECOVERY = ['Connect']


def _disconnect_reconnect(device):

    ''' Disconnect and reconnect the device
        Args:
            device ('obj'): Device object
        Returns:
            None
    '''

    # Disconnect from the device
    log.info("Disconnecting from device '{}'".format(device.name))
    try:
        device.destroy_all()
    except Exception:
        # Bah if cant destroy the connection  its still okay
        pass

    # Let's try to reconnect
    log.info("Trying to reconnect to device '{}'".format(device.name))
    try:
        # If the device is in rommon, just raise an exception
        rommon = Statement(pattern=r'^(.*)(rommon(.*)|loader(.*))+>.*$',
                           action=rommon_raise_exception,
                           args={},
                           loop_continue=False,
                           continue_timer=False)
        device.instantiate(learn_hostname=True)
        device.connect_reply.append(rommon)
        device.connect(learn_hostname=True)
    except Exception as e:
        # Cant connect!
        # re-destroy in case the connection error in bad state
        log.info('Could not connect to the device\n{e}'.format(e=str(e)))
        device.destroy_all()
        return False
    else:
        # Can connect all good
        log.info('Connected to the device successfully')
        return True
    finally:
        try:
            device.connect_reply.remove(rommon)
        except Exception:
            pass

def rommon_raise_exception():
    log.error('Device is in rommon')
    raise Exception('Device is in rommon')

def _connectivity(device, console_activity_pattern=None, console_breakboot_char=None,
                  grub_activity_pattern=None, grub_breakboot_char=None, break_count=10,
                  timeout=None, golden_image=None, tftp_boot=None,
                  recovery_password=None, clear_line=True, powercycler=True,
                  powercycler_delay=30, section=None, reconnect_delay=60):

    '''Powercycle the device and start the recovery process
       Args:
           device ('obj'): Device object
           console_activity_pattern: <Break pattern on the device for normal boot mode, 'str'>
           console_breakboot_char: <Character to send when console_activity_pattern is matched, 'str'>
           grub_activity_pattern: <Break pattern on the device for grub boot mode, 'str'>
           grub_breakboot_char: <Character to send when grub_activity_pattern is matched, 'str'>
           break_count ('int'): Number of sending break times
           timeout ('int'): Recovery process timeout
           golden_image ('dict'): information to load golden image on the device
           tftp_boot ('dict'): Tftp boot information
           recovery_password ('str'): Device password after recovery
           powercycler: <Should powercycler execute, 'bool'> (Default: True)
           clear_line: <Should clearline execute, 'bool'> (Default: True)
           powercycler_delay: <Powercycler delay between on/off>, 'int'> (Default: 30)
           reconnect_delay: <Once device recovered, delay before final reconnect>, 'int'> (Default: 60)
       Returns:
           None
    '''

    # Step-2: Clear console port line
    if clear_line:
        log.info(banner("Clearing the console port line"))

        try:
            device.api.execute_clear_line()
        except Exception as e:
            log.warning(str(e))
            log.warning("Unable to clear console port line")
        else:
            log.info("Successfully cleared console port line on device '{}'".\
                     format(device.name))
            # Attempt disconnecting and reconnecting after clearing line
            if _disconnect_reconnect(device):
                # All good!
                log.info("Successfully re-connected to device '{}'".\
                         format(device.name))
                return
            else:
                log.warning("Cannot re-connect to device '{}' after clearing "
                            "console port line".format(device.name))

    # Step-3: Powercycle device
    if powercycler:
        log.info(banner("Powercycling device '{}'".format(device.name)))

        try:
            device.api.execute_power_cycle_device(delay=powercycler_delay)
        except Exception as e:
            log.error(str(e))
            raise Exception("Failed to powercycle device '{}'".format(device.name))
        else:
            log.info("Successfully powercycled device '{}' during recovery".\
                     format(device.name))

    # Step-4: Boot device with given golden image
    if golden_image:
        log.info(banner("Booting device '{}' with the Golden images".\
                        format(device.name)))
        log.info("Golden image information found:\n{}".format(golden_image))
    elif tftp_boot:
        log.info(banner("Booting device '{}' with the Tftp images".\
                        format(device.name)))
        log.info("Tftp boot information found:\n{}".format(tftp_boot))
    else:
        # This case is for the simple boot
        # Not yet supported
        raise Exception('Global recovery only support golden image and tftp '
                         'boot recovery and neither was provided')

    # Need to instantiate to get the device.start
    # The device.start only works because of a|b
    device.instantiate(connection_timeout=timeout)

    # For each default connection, start a fork to try to recover the device
    try:
        abstract = Lookup.from_device(device, packages={'clean': clean})
        # Item is needed to be able to know in which parallel child
        # we are

        if device.is_ha and hasattr(device, 'subconnections'):
            start = [i.start[0] for i in device.subconnections]
        else:
            start = device.start

        pcall(
            abstract.clean.recovery.recovery.recovery_worker,
            start=start,
            ikwargs = [{'item': i} for i, _ in enumerate(start)],
            ckwargs = {
                'device': device,
                'console_activity_pattern': console_activity_pattern,
                'console_breakboot_char': console_breakboot_char,
                'grub_activity_pattern': grub_activity_pattern,
                'grub_breakboot_char': grub_breakboot_char,
                'break_count': break_count,
                'timeout': timeout,
                'golden_image': golden_image,
                'tftp_boot': tftp_boot,
                'recovery_password': recovery_password}
        )
    except Exception as e:
        log.error(str(e))
        raise Exception("Failed to recover the device '{}'".\
                        format(device.name))
    else:
        log.info("Successfully recovered the device '{}'".\
                 format(device.name))

    log.info('Sleeping for {r} before reconnection'.format(r=reconnect_delay))
    time.sleep(reconnect_delay)

    # Step-5: Disconnect and reconnect to the device
    if not _disconnect_reconnect(device):
        # If that still doesn't work, Thats all we got
        raise Exception("Cannot recover the device '{d}'\nCannot run clean".\
                        format(d=device.name))
    else:
        log.info("Success - Have recovered and reconnected to device '{}'".\
                 format(device.name))


@clean_schema({
    Optional('console_activity_pattern'): str,
    Optional('console_breakboot_char'): str,
    Optional('grub_activity_pattern'): str,
    Optional('grub_breakboot_char'): str,
    Optional('break_count'): int,
    Optional('timeout'): int,
    Optional('golden_image'): Or(list, {
        'system': str,
        Optional('kickstart'): str
    }),
    Optional('tftp_boot'): {
        'image': list,
        'ip_address': list,
        'subnet_mask': str,
        'gateway': str,
        'tftp_server': str
    },
    Optional('recovery_password'): str,
    Optional('clear_line'): bool,
    Optional('powercycler'): bool,
    Optional('powercycler_delay'): int,
    Optional('reconnect_delay'): int,
    Optional('post_recovery_configuration'): str,
})
def recovery_processor(
        section,
        console_activity_pattern=None,
        console_breakboot_char='\x03', # '\x03' == <ctrl>+C
        grub_activity_pattern=None,
        grub_breakboot_char='c',
        break_count=15,
        timeout=None,
        golden_image=None,
        tftp_boot=None,
        recovery_password=None,
        clear_line=True,
        powercycler=True,
        powercycler_delay=30,
        reconnect_delay=60,
        post_recovery_configuration=None,
        ):

    '''
    Clean yaml file schema:
    -----------------------
    devices:
      <device>:
        device_recovery:
          break_count: <Send break count, 'int'> (default to 15)
          console_activity_pattern: <Break pattern on the device for normal boot mode, 'str'>
          console_breakboot_char: <Character to send when console_activity_pattern is matched, 'str'>
          grub_activity_pattern: <Break pattern on the device for grub boot mode, 'str'>
          grub_breakboot_char: <Character to send when grub_activity_pattern is matched, 'str'>
          timeout: <Timeout in seconds to recover the device, 'int'>
          recovery_password: <Device password after coming up, 'str'>
          powercycler: <Should powercycler execute, 'bool'> (Default: True)
          powercycler_delay: <Powercycler delay between on/off>, 'int'> (Default: 30)
          reconnect_delay: <Once device recovered, delay before final reconnect>, 'int'> (Default: 60)
          clear_line: <Should clearline execute, 'bool'> (Default: True)
          post_recovery_configuration: <Configuration to apply to the device, 'str'>
          golden_image: <Golden image to boot the device with, 'list' or 'dict' in the format below>
            kickstart: <Golden kickstart image, 'str'>
            system: <Golden system image, 'str'>
          tftp_boot:
            image: <Image to boot with `list`> (Mandatory)
            ip_address: <Management ip address to configure to reach to the TFTP server `list`> (Mandatory)
            subnet_mask: <Management subnet mask `str`> (Mandatory)
            gateway: <Management gateway `str`> (Mandatory)
            tftp_server: <tftp server is reachable with management interface> (Mandatory)

    Example:
    --------
    devices:
      N95_1:
        device_recovery:
          break_count: 10
          console_activity_pattern: "\\.\\.\\.\\."
          timeout: 30000
          recovery_password: lab
          tftp_boot:
            image:
              - /My/image/image.bin
            # If HA, provide 2 ip addresses. One for each SUP
            ip_address: [10.1.2.15]
            gateway: 10.1.2.1
            subnet_mask: 255.255.255.0
            tftp_server: 10.1.7.251

    devices:
      asr1000:
        device_recovery:
          break_count: 10
          console_activity_pattern: "\\.\\.\\.\\."
          timeout: 30000
          recovery_password: lab
          golden_image:
            - /auto/path/images/some_image.bin

    devices:
      n9500:
        device_recovery:
          break_count: 10
          console_activity_pattern: "\\.\\.\\.\\."
          timeout: 30000
          recovery_password: lab
          golden_image:
            system: /auto/path/images/some_image.bin

    devices:
      n7700:
        device_recovery:
          break_count: 10
          console_activity_pattern: "\\.\\.\\.\\."
          timeout: 30000
          recovery_password: lab
          golden_image:
            system: /auto/path/images/some_system_image.bin
            kickstart: /auto/path/images/some_kickstart_image.bin

    Flow:
    -----
    before:
        None
    after:
        None
    '''
    log.info('Starting Device Recovery checks!')

    # Get device
    device = section.parameters['device']

    recovery_is_required = True

    # Step 1 - Do we have connectivity to the device - Try to reconnect
    if device.api.verify_connectivity() or _disconnect_reconnect(device):
        recovery_is_required = False

    if recovery_is_required:
        # Not good! Lets attempt recovery
        log.warning("Device '{}' is unreachable. Attempting to recover.".\
                    format(device.name))

        # Start Recovery Processor
        log.info(banner('Recovery Processor'))
        log.info('''\
Recovery Steps:
1. Attempt to connect to the device - Failed
2. Disconnect and reconnect from the device - Failed
3. Clear line if provided
4. Powercycler the device if provided
5. From rommon, boot the device with golden image TFTP boot or type boot''')

        try:
            _connectivity(device, console_activity_pattern, console_breakboot_char,
                          grub_activity_pattern, grub_breakboot_char, break_count, timeout,
                          golden_image, tftp_boot, recovery_password, clear_line, powercycler,
                          powercycler_delay, section, reconnect_delay)
        except Exception as e:
            # Could not recover the device!
            log.error(banner("*** Terminating Genie Clean ***"))
            section.parent.parameters['block_section'] = True
            section.failed(from_exception=e)

        if post_recovery_configuration:
            log.info('Applying post recovery configuration to the device')
            device.configure(post_recovery_configuration)

    if recovery_is_required and section.uid not in CONTINUE_RECOVERY:
        # Did not fail to recover but still terminate clean because the stage
        # was not in CONTINUE_RECOVERY.
        log.error(banner("*** Terminating Genie Clean ***"))
        section.parent.parameters['block_section'] = True
        section.failed("Device '{d}' has been recovered - "
                       "Terminating clean".format(d=device.name))
    elif recovery_is_required and section.uid in CONTINUE_RECOVERY:
        # Recovery either was not required or the stage was in CONTINUE_RECOVERY.
        # Modify the original results to Passed as we want clean to continue.
        try:
            section.result = Passed
            section.parent.result = Passed
            section.parent.parent.result = Passed
        except Exception:
            pass

    if recovery_is_required:
        section.passed("Device has been recovered. Continuing with pyATS Clean.")
    else:
        log.info(
            "Device '{}' is still connected. No need to recover the device.".
            format(device.name))


def block_section(section):
    if section.parent.parameters.get('block_section'):
        section.blocked('Recovery has failed to restore the device - Blocking clean')
