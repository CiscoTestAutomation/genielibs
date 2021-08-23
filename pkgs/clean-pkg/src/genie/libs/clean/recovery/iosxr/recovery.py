'''IOSXR specific recovery functions'''

# Python
import re
import time
import logging

# Unicon
from unicon.eal.expect import Spawn
from unicon.eal.dialogs import Statement
from unicon.plugins.iosxr.patterns import IOSXRPatterns

# Genie
from genie.libs.clean.recovery.iosxr.dialogs import (BreakBootDialog,
                                                     RommonDialog,
                                                     TftpRommonDialog)

# Logger
log = logging.getLogger()

# Power Cycler handlers
def sendbrk_handler(spawn, break_count):
    ''' Send break while rebooting device
        Args:
            spawn ('obj'): Spawn connection object
            break_count ('int'): Number of sending break times
        Returns:
            None
    '''

    count = 1
    xr_patterns = IOSXRPatterns()
    while count <= break_count:
        spawn.send("\035")
        spawn.expect([xr_patterns.telnet_prompt])
        spawn.send("send brk\r\r")
        time.sleep(1)
        count += 1


def recovery_worker(*args, **kwargs):

    if kwargs.get('golden_image'):
        return device_recovery(*args, **kwargs)
    elif kwargs.get('tftp_boot'):
        return tftp_recovery_worker(*args, **kwargs)


def device_recovery(start, device, console_activity_pattern, golden_image=None,
    break_count=10, timeout=600, recovery_password=None,
    tftp_boot=None, item=None, **kwargs):
    ''' A method for starting Spawns and handling the device statements during recovery
        Args:
            device ('obj'): Device object
            start ('obj'): Start method under device object
            console_activity_pattern ('str'): Pattern to send the break at
            golden_image ('dict'): information to load golden image on the device
            break_count ('int'): Number of sending break times
            timeout ('int'): Recovery process timeout
            recovery_password ('str'): Device password after recovery
        Returns:
            None
    '''

    # Set a target for each recovery session
    # so it's easier to distinguish expect debug logs on the console.
    device.instantiate(connection_timeout=timeout)

    # Get device console port information
    last_word_in_start_match = re.match('.*\s(\S+)$', start)
    last_word_in_start = last_word_in_start_match.group(1) \
        if last_word_in_start_match else ""

    # Set target
    target = "{}_{}".format(device.hostname, last_word_in_start)

    logfile = log.handlers[1].logfile if len(log.handlers) >=2 else None
    spawn = Spawn(spawn_command=start,
                  settings=device.cli.settings,
                  target=target,
                  log=log,
                  logfile=logfile)

    break_dialog = BreakBootDialog()
    break_dialog.add_statement(Statement(pattern=console_activity_pattern,
                                         action=sendbrk_handler,
                                         args={'break_count':break_count},
                                         loop_continue=True,
                                         continue_timer=False), pos=0)
    break_dialog.dialog.process(spawn, timeout=timeout)

    dialog = RommonDialog()
    dialog.dialog.process(spawn,
                          timeout=timeout,
                          context={
                              'boot_image': golden_image[0],
                              'break_count': break_count,
                              'password': recovery_password
                          })
    spawn.close()


def tftp_recovery_worker(start, device, console_activity_pattern, tftp_boot=None,
    break_count=10, timeout=600, recovery_username=None, recovery_password=None,
    golden_image=None, item=None, **kwargs):
    ''' A method for starting Spawns and handling the device statements during recovery
        Args:
            device ('obj'): Device object
            start ('obj'): Start method under device object
            console_activity_pattern ('str'): Pattern to send the break at
            tftp_boot ('dict'): Tftp boot information
            break_count ('int'): Number of sending break times
            timeout ('int'): Recovery process timeout
            recovery_username ('str'): Device username after recovery
            recovery_password ('str'): Device password after recovery
        Returns:
            None
    '''

    log.info('Set the device in rommon and load the device with tftp boot')
    break_dialog = BreakBootDialog()
    break_dialog.add_statement(Statement(pattern=console_activity_pattern,
                                         action=sendbrk_handler,
                                         args={'break_count':break_count},
                                         loop_continue=True,
                                         continue_timer=False), pos=0)

    # Set a target for each recovery session
    # so it's easier to distinguish expect debug logs on the console.
    device.instantiate(connection_timeout=timeout)

    # Get device console port information
    last_word_in_start_match = re.match('.*\s(\S+)$', start)
    last_word_in_start = last_word_in_start_match.group(1) \
        if last_word_in_start_match else ""

    # Set target
    target = "{}_{}".format(device.hostname, last_word_in_start)

    if len(log.handlers) >= 2:
        logfile= log.handlers[1].logfile
    else:
        logfile = None

    spawn = Spawn(spawn_command=start,
                  settings=device.cli.settings,
                  target=target,
                  log=log,
                  logfile=logfile)

    tftp_rommon_dialog = TftpRommonDialog()

    if not recovery_username:
        recovery_username = device.connections[device.context]['credentials'].\
                                    get('default', {}).get('username', {})
    if not recovery_password:
        recovery_password = device.connections[device.context]['credentials'].\
                                    get('default', {}).get('password', {})

    tftp_rommon_dialog.hostname_statement(device.hostname)

    # exec_prompt, username, password
    tftp_rommon_dialog.dialog.process(spawn, timeout=timeout,
                                context={'device_name': device.name,
                                         'ip': tftp_boot['ip_address'][item],
                                         'username': recovery_username,
                                         'password': recovery_password,
                                         'subnet_mask': tftp_boot['subnet_mask'],
                                         'gateway': tftp_boot['gateway'],
                                         'image': tftp_boot['image'],
                                         'tftp_server': tftp_boot['tftp_server'],
                                         'hostname': device.hostname})
    spawn.close()


def tftp_recover_from_rommon(spawn, session, context, device_name,
    ip, subnet_mask, gateway, image, tftp_server):
    '''Load new image on the device from rommon with tftp'''

    log.info("Assigning boot variables in rommon...")

    # rommon arg name mapping
    mapping_list = {
        'ip': 'IP_ADDRESS',
        'subnet_mask': 'IP_SUBNET_MASK',
        'gateway': 'DEFAULT_GATEWAY',
        'tftp_server': 'TFTP_SERVER',
    }

    for item in mapping_list:
        log.info("\nSet '{}' to {}".format(mapping_list[item], context[item]))
        try:
            spawn.sendline("{}={}".format(mapping_list[item], context[item]))
        except Exception as e:
            log.error(str(e))
            raise Exception("Unable to set {}={}".format(mapping_list[item], context[item]))


    # Build the boot command
    boot_cmd = 'boot tftp://{tftp}/{image}'.format(tftp=tftp_server,
                                                   image=image[0])

    # Send the boot command to the device
    log.info("Sending TFTP boot command...")
    try:
        spawn.sendline(boot_cmd)
    except Exception as e:
        raise Exception("Unable to boot {} error {}".format(boot_cmd, str(e)))
