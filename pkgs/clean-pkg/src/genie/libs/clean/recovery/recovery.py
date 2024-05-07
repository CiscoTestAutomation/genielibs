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


def _recovery_steps(device, clear_line=True, powercycler=True,
                    powercycler_delay=30, reconnect_delay=60, **kwargs):

    '''Steps to recover device
    1. First step clear line
    2. Second step power cycle the device
    3. Third step boot the device using golden image or tftp

    Args:
        device ('obj'): Device object
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
            device.api.execute_clear_console()
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
    else:
        log.info('Clear line is not provided!')

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
    else:
        log.info("powercycle is not provided!")

    # Step-4: Boot device with given golden image or by tftp boot
    try:
        device.api.device_recovery_boot()
    except Exception as e:
        log.error(e)
        raise Exception(f"Failed to boot the device {device.name}")
    else:
        log.info(f"successfully booted the device {device.name}")

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
    Optional('console_breakboot_telnet_break'): bool,
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
        'tftp_server': str,
        Optional('ether_port'): int,
    },
    Optional('recovery_password'): str,
    Optional('clear_line'): bool,
    Optional('powercycler'): bool,
    Optional('powercycler_delay'): int,
    Optional('reconnect_delay'): int,
    Optional('connection_timeout'):int,
    Optional('post_recovery_configuration'): str,
})
def recovery_processor(
        section,
        console_activity_pattern=None,
        console_breakboot_char='\x03', # '\x03' == <ctrl>+C
        console_breakboot_telnet_break=False,
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
        connection_timeout=45
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
          console_breakboot_telnet_break: Use telnet `send break` to interrupt device boot
          grub_activity_pattern: <Break pattern on the device for grub boot mode, 'str'>
          grub_breakboot_char: <Character to send when grub_activity_pattern is matched, 'str'>
          timeout: <Timeout in seconds to recover the device, 'int'>
          recovery_password: <Device password after coming up, 'str'>
          recovery_username: <Device username after coming up, 'str'>
          recovery_en_password: <Device enable password after coming up, 'str'>
          powercycler: <Should powercycler execute, 'bool'> (Default: True)
          powercycler_delay: <Powercycler delay between on/off>, 'int'> (Default: 30)
          reconnect_delay: <Once device recovered, delay before final reconnect>, 'int'> (Default: 60)
          clear_line: <Should clearline execute, 'bool'> (Default: True)
          post_recovery_configuration: <Configuration to apply to the device, 'str'>
          connection_timeout: <timeout for state machine, 'int'>
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
    # If connect stage was not done, don't check recovery
    if 'Connect' not in section.parent.history:
        return

    log.info('Starting Device Recovery checks!')
    # Get device
    device = section.parameters['device']
    recovery_is_required = False
    # check if device is in any known state
    log.info(f'Check device {device.name} has valid unicon state.')
    try:
        if hasattr(device, 'is_ha') and device.is_ha:
            log.info('Device is HA! checking all the subconnections.')
            for index, connection in enumerate(device.subconnections,1):
                bring_to_any_state(connection, connection_timeout)
                log.info(f'subconnection {index} is in {connection.state_machine.current_state}')
        else:
            bring_to_any_state(device, connection_timeout)
            log.info(f'Device is in {device.state_machine.current_state}')

    except Exception as e:
        log.exception(f'Could not bring device to any valid state! Continue with recovery because of {e}.')
        recovery_is_required = True
    # Device is in rommon. try to boot the device before continuing with other recovery steps
    if device.is_ha:
        if not recovery_is_required and check_all_in_same_state(device, 'enable'):
            log.info('Device is already connected. No need for device recovery.')
            return
        elif not recovery_is_required and check_all_in_same_state(device, 'rommon'):
            log.info(f'device {device.name} is in rommon, booting the device!')
            try:
                device.api.device_recovery_boot()
            except Exception as e:
                log.exception('Could not boot device from rommon. Power cycling the device')
                recovery_is_required = True
            else:
                log.info('Successfully booted the device. No need for device recovery.')
                return

        # Device is in valid unicon state but its not rommon or enable will try to disconnect and connect.
        elif not recovery_is_required and check_any_connection_in_rommon(device):
            log.info("One of the subconnection's is in rommon.\n"
                    "device should be recovered.")
            recovery_is_required = True
        elif not recovery_is_required:
            if not _disconnect_reconnect(device):
                recovery_is_required =True
            else:
                log.info('Successfully disconnect and connect to device.\n'
                        'No Need to recover the device.')
                return
    # Single RP devices
    else:
        if not recovery_is_required and device.state_machine.current_state == 'rommon':
            log.info(f'device {device.name} is in rommon booting the device!')
            try:
                device.api.device_recovery_boot()
            except Exception as e:
                log.info('Could not boot device from rommon. Power cycling the device')
                recovery_is_required = True
            else:
                log.info('Successfully booted the device. No need for device recovery.')
                return

        # Device is in valid unicon state but its not rommon or enable will try to disconnect and connect.
        elif not recovery_is_required and device.state_machine.current_state != 'enable':
            if not _disconnect_reconnect(device):
                recovery_is_required =True
            else:
                log.info('Successfully disconnect and connect to device.\n'
                        'No Need to recover the device.')
                return

    if recovery_is_required:
        # Not good! Lets attempt recovery
        log.warning("Device '{}' is unreachable. Attempting to recover.".\
                    format(device.name))

        # Start Recovery Processor
        log.info(banner('Recovery Processor'))
        log.info('''\
Recovery Steps:
1. Attempt to bring device to a valid state - Failed
2. Clear line if provided
3. Powercycler the device if provided
4. From rommon, boot the device with golden image or TFTP boot ''')

        try:
            _recovery_steps(device, clear_line, powercycler,
                          powercycler_delay, reconnect_delay)
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
        log.info(f'Device {device.name} is still connected. No need to recover the device.')

def block_section(section):
    if section.parent.parameters.get('block_section'):
        section.blocked('Recovery has failed to restore the device - Blocking clean')

def bring_to_any_state(connection, connection_timeout):
    '''Bring connection to any state
    '''
    connection.spawn.sendline()
    connection.state_machine.go_to('any',
                                  connection.spawn,
                                  timeout=connection_timeout,
                                  context=connection.context)

def check_all_in_same_state(device, state):
    '''Check if all the subconnections are in same state
    '''
    for connection in device.subconnections:
        if connection.state_machine.current_state != state:
            return False
    return True

def check_any_connection_in_rommon(device):
    '''Check if all the subconnections are in same state
    '''
    for connection in device.subconnections:
        if connection.state_machine.current_state == 'rommon':
            return True
    return False
