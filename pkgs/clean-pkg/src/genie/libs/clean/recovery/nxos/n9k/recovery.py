'''NXOS N9K specific recovery functions'''

# Python
import re
import time
import logging

# Unicon
from unicon.eal.expect import Spawn
from unicon.eal.dialogs import Statement

# Genie
from genie.libs.clean.recovery.nxos.recovery import sendbrk_handler
from genie.libs.clean.recovery.nxos.dialogs import (BreakBootDialog,
                                                    RommonDialog,
                                                    TftpRommonDialog)


# Logger
log = logging.getLogger(__name__)

def recovery_worker(*args, **kwargs):

    if kwargs.get('golden_image'):
        return golden_recovery(*args, **kwargs)
    elif kwargs.get('tftp_boot'):
        return tftp_recovery_worker(*args, **kwargs)

def golden_recovery(start, device, console_activity_pattern, golden_image=None,
                    break_count=10, timeout=600, recovery_password=None,
                    tftp_boot=None, item=None, **kwargs):
    ''' A method for starting Spawns and handling the device statements during recovery
        Args:
            device ('obj'): Device object
            start ('obj'): Start method under device object
            console_activity_pattern ('str'): Pattern to send the break at
            golden_image ('str'): Image to load the device with
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
    last_word_in_start_match = re.match(r'.*\s(\S+)$', start)
    last_word_in_start = last_word_in_start_match.group(1) \
        if last_word_in_start_match else ""

    # Set target
    target = "{}_{}".format(device.hostname, last_word_in_start)

    # TODO: We need to fix that handlers[1]...
    # Make it stronger.
    # For now, if it doesnt exists, then just get out

    logfile = log.handlers[1].logfile if len(log.handlers) >= 2 else None
    spawn = Spawn(start,
                  settings=device.cli.settings,
                  target=target,
                  log=log,
                  logfile=logfile)

    break_dialog = BreakBootDialog()
    break_dialog.add_statement(Statement(pattern=console_activity_pattern,
                                         action=sendbrk_handler,
                                         args={'break_count': break_count},
                                         loop_continue=True,
                                         continue_timer=False),
                               pos=0)
    break_dialog.dialog.process(spawn, timeout=timeout)

    if 'system' not in golden_image:
        raise Exception("System image has not been provided in the "
                        "'device_recovery' section of the clean YAML")

    dialog = RommonDialog()
    dialog.dialog.process(spawn,
                          context={
                              'sys': golden_image.get('system'),
                              'password': recovery_password
                          },
                          timeout=timeout)
    spawn.close()


def tftp_recovery_worker(start, device, console_activity_pattern, tftp_boot=None,
                         break_count=10, timeout=600, recovery_password=None,
                         golden_image=None, item=None, **kwargs):
    ''' A method for starting Spawns and handling the device statements during recovery
        Args:
            device ('obj'): Device object
            start ('obj'): Start method under device object
            console_activity_pattern ('str'): Pattern to send the break at
            tftp_boot ('dict'): Tftp boot information
            break_count ('int'): Number of sending break times
            timeout ('int'): Recovery process timeout
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
    last_word_in_start_match = re.match(r'.*\s(\S+)$', start)
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

    rommon_dialog = TftpRommonDialog()
    rommon_dialog.hostname_statement(device.hostname)
    rommon_dialog.dialog.process(spawn, timeout=timeout,
                                 context={'device_name': device.name,
                                          'ip': tftp_boot['ip_address'][item],
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

    config = {'ip': "IP_ADDRESS={ip}".format(ip=ip),
              'subnet': "IP_SUBNET_MASK={sm}".format(sm=subnet_mask),
              'gateway': "DEFAULT_GATEWAY={gateway}".format(gateway=gateway)}

    for item, conf in config.items():
        log.info("Assign {} on {} device".format(item, device_name))
        try:
            spawn.sendline(conf)
        except Exception as e:
            raise Exception("Unable to assign {}:\n{}".
                            format(item, str(e)))

    # Build the boot command
    boot_cmd = 'boot tftp://{tftp}{image}'.format(tftp=tftp_server,
                                                  image=image[0])

    # Send the boot command to the device
    log.info("Send boot command {}".format(boot_cmd))
    try:
        spawn.sendline(boot_cmd)
    except Exception as e:
        raise Exception("Unable to boot {} error {}".format(boot_cmd,str(e)))

    # It remains in rommon for a few seconds
    time.sleep(5)
