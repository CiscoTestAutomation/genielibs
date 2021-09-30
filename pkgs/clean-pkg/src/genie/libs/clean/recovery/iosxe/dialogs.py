'''IOSXE specific Dialogs'''

# Python
import re
import time
import logging

# Unicon
from unicon.eal.dialogs import Statement, statement_decorator
from unicon.plugins.generic.statements import buffer_settled
from genie.libs.clean.recovery.dialogs import RommonDialog as TelnetDialog

# Genie
from genie.libs.clean.utils import print_message

log = logging.getLogger(__name__)


class BreakBootDialog(TelnetDialog):
    '''Dialog to stop the device to boot at reload time'''

    def __init__(self):

        # Rommon >
        self.add_statement(Statement(pattern=r'^(.*)((rommon(.*))+>|switch *:).*$',
                                     action=print_message,
                                     args={'message': 'Device reached rommon prompt in break boot stage'},
                                     trim_buffer=False))

        # grub>
        self.add_statement(Statement(pattern=r'.*grub *>.*',
                                     action=print_message,
                                     args={'message': 'Device reached grub prompt in break boot stage'},
                                     trim_buffer=False))

        # Login prompt
        self.add_statement(Statement(pattern=r'^.*(Username|login): ?$',
                                     action=print_message,
                                     args={'message': 'Device reached login prompt before rommon prompt',
                                           'raise_exception': True}))

        # Exec Prompt (ex: 'Router>')
        self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^>])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?>$',
                                     action='sendline(en)',
                                     loop_continue=True))

        # Privileged Exec Prompt (ex: 'Router#')
        self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^#])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?#$',
                                     action=print_message,
                                     args={'message': 'Device has reached privileged exec prompt'}))


class RommonDialog(TelnetDialog):

    def __init__(self):

        # Login prompt
        self.add_statement(Statement(pattern=r'^.*(Username|login): ?$',
                                     action=print_message,
                                     args={'message': 'Device reached login prompt before rommon prompt',
                                           'raise_exception': True}))

         # Would you like to enter the initial configuration dialog? [yes/no]:
        self.add_statement(Statement(pattern=r'^.*(initial|basic) configuration dialog *\?.*',
                                     action='sendline(no)',
                                     loop_continue=True))

        # Would you like to terminate autoinstall?
        self.add_statement(Statement(pattern=r'^.*terminate autoinstall *\?.*',
                                     action='sendline(yes)',
                                     loop_continue=True))

        # Exec Prompt (ex: 'Router>')
        self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^>])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?>$',
                                     action='sendline(en)',
                                     loop_continue=True))

        # Privileged Exec Prompt (ex: 'Router#')
        self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^#])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?#$',
                                     action=print_message,
                                     args={'message': 'Device has reached privileged exec prompt'}))


    # Press RETURN to get started
    @statement_decorator(r'^.*Press RETURN to get started.*', loop_continue=True)
    def press_return(spawn, session, context):
        max_time = time.time() + spawn.settings.RELOAD_WAIT
        while time.time() < max_time:
            if buffer_settled(spawn, spawn.settings.CONSOLE_TIMEOUT):
                spawn.sendline()
                return
        else:
            log.warning("Buffer did not settle within {} seconds. "
                        "Due to this, RETURN was never pressed."
                        .format(spawn.settings.RELOAD_WAIT))


    # Please reset before booting
    @statement_decorator(r'.*(P|p)lease reset before booting.*', loop_continue=True)
    def reset_rommon(spawn, session, context):
        spawn.sendline('confreg 0x0')
        time.sleep(0.5)
        spawn.sendline('reset')

    # Rommon >
    # switch:
    @statement_decorator(r'(.*)((rommon(.*))+>|switch *:).*', loop_continue=True)
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

    # Password:
    @statement_decorator(r'^.*[Pp]assword( for )?(\\S+)?: ?$', loop_continue=True)
    def send_password(spawn, session, context):
        # Send password to teh device when prompted
        spawn.sendline('{}'.format(context['password']))
        time.sleep(0.5)

    # grub>
    @statement_decorator(r'.*grub *>.*', loop_continue=True)
    def grub_boot_device(spawn, session, context):
        # '\033' == <ESC>
        spawn.send('\033')
        time.sleep(0.5)

    # Use the UP and DOWN arrow keys to select which entry is highlighted.
    # Use the ^ and v keys to select which entry is highlighted.
    @statement_decorator(r'.*Use the UP and DOWN arrow keys to select.*', loop_continue=True)
    @statement_decorator(r'.*Use the \^ and v keys to select.*', loop_continue=True)
    def grub_select_image(spawn, session, context):
        log.info("Finding an entry that includes the string '{}'".
                 format(context['boot_image']))

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

        log.info("Selecting the entry '{}' now.".format(lines[desired_line]))

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
    """ This class overrides the 'boot_device' statement to
        boot via tftp instead of a local file """

    @statement_decorator(r'(.*)((rommon(.*))+>|switch *:).*', loop_continue=True)
    def boot_device(spawn, session, context):
        '''Load new image on the device from rommon with tftp'''
        ip = context['ip']
        subnet_mask = context['subnet_mask']
        gateway = context['gateway']
        image = context['image']
        if image[0][0] != '/':
            image[0] = '/' + image[0]
        tftp_server = context['tftp_server']

        commands = [
            "TFTP_BLKSIZE=8192",
            f"IP_ADDRESS={ip}",
            f"IP_SUBNET_MASK={subnet_mask}",
            f"DEFAULT_GATEWAY={gateway}",
            "sync",
            f"boot tftp://{tftp_server}{image[0]}"
        ]

        # This is getting double logged somehow??
        log.info("Configuring the network and booting the device")

        # sendline to get the prompt - makes the logs pretty.
        try:
            spawn.sendline()
        except Exception as e:
            raise Exception("Connection to device has been lost. Something "
                            "closed the connection?\n{}".format(str(e)))

        for cmd in commands:
            try:
                spawn.sendline(cmd)
            except Exception as e:
                raise Exception("Connection to device has been lost. Something "
                                "closed the connection?\n{}".format(str(e)))
            # in case of 'sync', need a delay before sending other commands
            if 'sync' in cmd:
                time.sleep(3)
            else:
                time.sleep(0.5)
