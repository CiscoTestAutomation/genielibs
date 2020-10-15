'''IOSXE specific Dialogs'''

# Python
import re
import time
import logging

# Unicon
from unicon.eal.dialogs import Statement, Dialog, statement_decorator
from genie.libs.clean.stages.execute_dialogs import BreakBootDialog as \
                                               CommonBreakBootDialog
from genie.libs.clean.stages.execute_dialogs import RommonDialog as \
                                               CommonRommonDialog

# Genie
from genie.libs.clean.utils import print_message

log = logging.getLogger(__name__)


class BreakBootDialog(CommonBreakBootDialog):
    '''Dialog to stop the device to boot at reload time'''

    def __init__(self):

        # Rommon >
        self.add_statement(Statement(pattern=r'^(.*)(rommon(.*))+>.*$',
                                     action=print_message,
                                     args={'message': 'Device reached rommon prompt in break boot stage',
                                           'status': 0},
                                     loop_continue=False,
                                     continue_timer=False))

        # Login prompt
        self.add_statement(Statement(pattern=r'^.*(Username|login): ?$',
                                     action=print_message,
                                     args={'message': 'Device reached login prompt before rommon prompt',
                                           'status': 0},
                                     loop_continue=False,
                                     continue_timer=False))

        # Exec Prompt (ex: 'Router>')
        self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^>])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?>$',
                                     action='sendline(en)',
                                     loop_continue=True,
                                     continue_timer=False))

        # Privileged Exec Prompt (ex: 'Router#')
        self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^#])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?#$',
                                     action=print_message,
                                     args={'message': 'Device has reached privileged exec prompt',
                                           'status': 1},
                                     loop_continue=False,
                                     continue_timer=False))

class RommonDialog(CommonRommonDialog):

    def __init__(self):

        # Login prompt
        self.add_statement(Statement(pattern=r'^.*(Username|login): ?$',
                                     action=print_message,
                                     args={'message': 'Device reached login prompt before rommon prompt',
                                           'status': 0},
                                     loop_continue=False,
                                     continue_timer=False))

         # Would you like to enter the initial configuration dialog? [yes/no]:
        self.add_statement(Statement(pattern=r'^.*(initial|basic) configuration dialog *\?.*',
                                     action='sendline(no)',
                                     loop_continue=True,
                                     continue_timer=False))

        # Would you like to terminate autoinstall?
        self.add_statement(Statement(pattern=r'^.*terminate autoinstall *\?.*',
                                     action='sendline(yes)',
                                     loop_continue=True,
                                     continue_timer=False))

        # Press RETURN to get started
        self.add_statement(Statement(pattern=r'^.*Press RETURN to get started.*',
                                     action='sendline()',
                                     loop_continue=True,
                                     matched_retries=3,
                                     matched_retry_sleep=30,
                                     continue_timer=False))

        # Exec Prompt (ex: 'Router>')
        self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^>])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?>$',
                                     action='sendline(en)',
                                     loop_continue=True,
                                     continue_timer=False))

        # Privileged Exec Prompt (ex: 'Router#')
        self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^#])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?#$',
                                     action=print_message,
                                     args={'message': 'Device has reached privileged exec prompt',
                                           'status': 1},
                                     loop_continue=False,
                                     continue_timer=False))

    # Rommon >
    # switch:
    @statement_decorator(r'(.*)((rommon(.*))+>|switch *:).*', loop_continue=True, continue_timer=False)
    def boot_device(spawn, session, context):
        # Get value for BOOT var
        boot_image = context['boot_image']
        # Set BOOT var and wait
        spawn.sendline('BOOT={}'.format(boot_image))
        time.sleep(0.5)
        # # Print vars to log
        # spawn.sendline('set')
        # Boot device with BOOT var image
        spawn.sendline('boot {}'.format(boot_image))
        time.sleep(0.5)


    # Time taken to reboot after reload
    @statement_decorator(r'.*Time taken to reboot after reload.*', loop_continue=True, continue_timer=False)
    def get_exec_mode(spawn, session, context):
        # Keep sending carriage return until exec prompt found
        count = 1
        while count <= context['break_count']:
            time.sleep(0.5)
            spawn.send('\r')
            count += 1

        time.sleep(0.5)


    # Password:
    @statement_decorator(r'^.*[Pp]assword( for )?(\\S+)?: ?$', loop_continue=True, continue_timer=False)
    def send_password(spawn, session, context):
        # Send password to teh device when prompted
        spawn.sendline('{}'.format(context['password']))
        time.sleep(0.5)


    # grub>
    @statement_decorator(r'.*grub *>.*', loop_continue=True, continue_timer=False)
    def grub_boot_device(spawn, session, context):
        # '\033' == <ESC>
        spawn.send('\033')
        time.sleep(0.5)


    # Use the UP and DOWN arrow keys to select which entry is highlighted.
    # Use the ^ and v keys to select which entry is highlighted.
    @statement_decorator(r'.*Use the UP and DOWN arrow keys to select.*', loop_continue=True, continue_timer=False)
    @statement_decorator(r'.*Use the \^ and v keys to select.*', loop_continue=True, continue_timer=False)
    def grub_select_image(spawn, session, context):

        lines = re.split(r'\s{4,}', spawn.buffer)

        selected_line = None
        desired_line = None

        # Get index for selected_line and desired_line
        for index, line in enumerate(lines):
            if '*' in line:
                selected_line = index
            if context['boot_image'] in line:
                desired_line = index

        if not selected_line or not desired_line:
            raise Exception("Cannot figure out which image to select! "
                            "Debug info:\n"
                            "selected_line: {}\n"
                            "desired_line: {}\n"
                            "lines: {}"
                            .format(selected_line, desired_line, lines))

        num_lines_to_move = desired_line - selected_line

        # If positive we want to move down the list.
        # If negative we want to move up the list.
        if num_lines_to_move >= 0:
            # '\x1B[B' == <down arrow key>
            key = '\x1B[B'
        else:
            # '\x1B[A' == <up arrow key>
            key = '\x1B[A'

        for _ in range(abs(num_lines_to_move)):
            spawn.send(key)
            time.sleep(0.5)

        spawn.sendline()
        time.sleep(0.5)


class TftpRommonDialog(RommonDialog):
    def hostname_statement(self, hostname):
        # Exec Prompt (ex: 'Router>')
        self.add_statement(Statement(pattern=r'^(.*?)({hostname}|Router|Switch|ios|switch)(\\(standby\\))?(-stby)?(\\(boot\\))?(>)'.format(hostname=hostname),
                                     action=print_message,
                                     args={'message': 'Device has reached privileged exec prompt',
                                                      'status': 1},
                                     loop_continue=False,
                                     continue_timer=False))

    @statement_decorator(r'(.*)((rommon(.*))+>|switch *:).*', loop_continue=True, continue_timer=False)
    def boot_device(spawn, session, context):
        '''Load new image on the device from rommon with tftp'''
        device_name = context['device_name']
        ip = context['ip']
        subnet_mask = context['subnet_mask']
        gateway = context['gateway']
        image = context['image']
        tftp_server = context['tftp_server']
        hostname = context['hostname']

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


