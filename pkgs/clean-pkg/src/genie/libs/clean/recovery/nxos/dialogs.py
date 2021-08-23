'''NXOS specific Dialogs'''

# Python
import re
import logging
from time import sleep

# Unicon
from unicon.eal.dialogs import Statement, statement_decorator
from genie.libs.clean.recovery.dialogs import BreakBootDialog as CommonBreakBootDialog
from genie.libs.clean.recovery.dialogs import RommonDialog as CommonRommonDialog

# Genie
from genie.libs.clean.utils import print_message

log = logging.getLogger(__name__)


class BreakBootDialog(CommonBreakBootDialog):
    '''Dialog to stop the device to boot at reload time'''

    def __init__(self):
        self.add_statement(Statement(pattern=r'(.*)(loader(.*))+>',
                                     action=print_message,
                                     args={'message':"Device reached loader prompt"},
                                     loop_continue=False,
                                     continue_timer=False,
                                     trim_buffer=False))

        self.add_statement(Statement(pattern=r'^.*(Username|login): ?$',
                                     action=print_message,
                                     args={'message': "Device reached login before loader prompt",
                                           'raise_exception': True},
                                     loop_continue=False,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^[^\n]*#\s?$',
                                     action=print_message,
                                     args={'message': "Device reached enable mode before loader prompt",
                                           'raise_exception': True},
                                     loop_continue=False,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'Abort( Power On)? Auto Provisioning .*:',
                                     action='sendline(yes)',
                                     args=None,
                                     loop_continue=True,
                                     continue_timer=False))


class RommonDialog(CommonRommonDialog):
    def __init__(self):
        self.add_statement(Statement(pattern=r'^.*.*Press RETURN to get started',
                                     action='sendline(\r)',
                                     args=None,
                                     loop_continue=True,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^.*(Enter|Confirm) the password for .*admin',
                                     action='sendline_ctx(password)',
                                     args=None,
                                     loop_continue=True,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'.*Enable the SNMP port\? \(yes\/no\) \[y\]:',
                                     action='sendline(\r)',
                                     args=None,
                                     loop_continue=True,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^.*Boot up system with default vdc \(yes\/no\) \[y\]\:',
                                    action='sendline(yes)',
                                    args=None,
                                    loop_continue=True,
                                    continue_timer=False))

        self.add_statement(Statement(pattern=r'Do you want to enable admin vdc\s?\(yes\/no\)\s?\[n\]\:',
                                     action='sendline(no)',
                                     args=None,
                                     loop_continue=True,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'Abort( Power On)? Auto Provisioning .*:',
                                     action='sendline(yes)',
                                     args=None,
                                     loop_continue=True,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^.*Do you want to enforce secure password standard \(yes\/no\) \[y\]\:',
                                     action='sendline(no)',
                                     args=None,
                                     loop_continue=True,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^.*(initial|basic) configuration dialog.*\s?',
                                     action='sendline(no)',
                                     args=None,
                                     loop_continue=True,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^(.*)Would you like to terminate autoinstall\? ?\[yes\]: $',
                                     action='sendline(yes)',
                                     args=None,
                                     loop_continue=True,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^.*(Username|login): ?$',
                                     action=print_message,
                                     args={'message': "Device reached login prompt"},
                                     loop_continue=False,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^[^\n]*Password:\s?$',
                                     action=None,
                                     args=None,
                                     loop_continue=False,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^[^\n]*#\s?$',
                                     action=None,
                                     args=None,
                                     loop_continue=False,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'($prompt|Router|Switch|ios|switch)(\(standby\))?(\(boot\))?(>|#)',
                                     action=None,
                                     args=None,
                                     loop_continue=False,
                                     continue_timer=False))

        self.add_statement(Statement(pattern=r'^[^\n]*>\s?$',
                                     action=None,
                                     args=None,
                                     loop_continue=False,
                                     continue_timer=False))


    @statement_decorator(r'.*Do you wish to proceed anyway.*', loop_continue=True, continue_timer=False)
    def proceed_anyway(spawn, session):
        sleep(0.5)
        spawn.sendline('y')


    @statement_decorator(r'(.*)(loader(.*))+>', loop_continue=True, continue_timer=False)
    def loader_prompt_handler(spawn, session, context):
        """Handles loader prompt interactions """
        if session.get("loader_count"):
            if session['loader_count'] == 1:

                if 'kick' in context:
                    image = context['kick']
                else:
                    image = context['sys']

                cmd = "boot " + image
                spawn.sendline(cmd)
                session['loader_count'] += 1
            else:
                raise Exception('Loader prompt encountered again'
                                ', Maybe golden image do not exist for  % ', str(spawn))
        else:
            spawn.send("\r")
            sleep(2)
            session['loader_count'] = 1


    @statement_decorator(r'^.*switch\(boot\)#\s?', loop_continue=True, continue_timer=False)
    def switch_prompt_handler(spawn, session, context):
        if session.get("switch_count"):
            if session['switch_count'] == 1:
                spawn.sendline("wr erase boot")
                sleep(5)
                session['switch_count'] += 1
            elif session['switch_count'] == 2:
                image = context['sys']
                cmd = "load  " + image
                spawn.sendline(cmd)
                session['switch_count'] += 1
        else:
            spawn.sendline("write erase")
            sleep(2)
            session['switch_count'] = 1

    @statement_decorator(r'^(.*)(bash-\S+|Linux)[#\$]\s?', loop_continue=True, continue_timer=False)
    def bash_prompt_handler(spawn, session, context):
        # clean up disk space in case NXOS goes to bash prompt during reload
        # no info about protected_files in this situation, so protect only given
        # golden image and delete other thinkable image files
        m = re.search("'(?P<storage>\S+)' is FULL", spawn.buffer)
        if m:
            spawn.buffer = ''
            storage = m.group('storage')

            if storage in context['sys']:
                image_name = context['sys'].split('/')[-1]

            log.info("Detected {s} is FULL. Cleaning up image files except for {i}".format(s=storage, i=image_name))
            spawn.sendline('cd {s}'.format(s=storage.split(':')[0]))
            sleep(1)
            spawn.sendline('mv {i} protected_image_{spid}'.format(i=image_name, spid=spawn.pid))
            sleep(1)
            spawn.sendline('rm -rf *bin')
            sleep(30)
            spawn.sendline('rm -rf system-image*')
            sleep(30)
            spawn.sendline('mv protected_image_{spid} {i}'.format(i=image_name, spid=spawn.pid))
            sleep(1)
            spawn.sendline('exit')
        else:
            spawn.sendline('exit')

class TftpRommonDialog(RommonDialog):
    def hostname_statement(self, hostname):
        # Exec Prompt (ex: 'Router>')
        self.add_statement(Statement(pattern=r'($prompt|{hostname}|Router|Switch|ios|switch)(\(standby\))?(\(boot\))?(>|#)'.format(hostname=hostname),
                                     action=None,
                                     args=None,
                                     loop_continue=False,
                                     continue_timer=False))


    @statement_decorator(r'(.*)((loader(.*))+>|switch *:).*', loop_continue=True, continue_timer=False)
    def loader_prompt_handler(spawn, session, context):
        '''Load new image on the device from rommon with tftp'''
        device_name = context['device_name']
        ip = context['ip']
        subnet_mask = context['subnet_mask']
        gateway = context['gateway']
        image = context['image']
        tftp_server = context['tftp_server']
        hostname = context['hostname']

        config = {'ip': "set ip {ip} {sub}".format(ip=ip, sub=subnet_mask),
                  'gateway': "set gw {gateway}".format(gateway=gateway)}

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

