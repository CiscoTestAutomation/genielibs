'''IOSXR specific Dialogs'''

# Python
import time
import logging

# Unicon
from unicon.eal.dialogs import Statement, statement_decorator
from genie.libs.clean.recovery.dialogs import BreakBootDialog as CommonBreakBootDialog
from genie.libs.clean.recovery.dialogs import RommonDialog as CommonRommonDialog

# Genie
from genie.libs.clean.utils import print_message

# Logger
log = logging.getLogger()


class BreakBootDialog(CommonBreakBootDialog):
      '''Dialog to stop the device to boot at reload time'''

      def __init__(self):
            # Rommon >
            self.add_statement(Statement(pattern=r'^(.*)(rommon(.*))+>.*$',
                                          action=print_message,
                                          args={'message': 'Device reached rommon prompt in break boot stage'},
                                          loop_continue=False,
                                          continue_timer=False))

            # Login prompt
            self.add_statement(Statement(pattern=r'^.*(Username|login)\:.*$',
                                          action=print_message,
                                          args={'message': 'Device reached login prompt before rommon prompt'},
                                          loop_continue=False,
                                          continue_timer=False))

            # Standby prompt (ex: 'This (D)RP Node is not ready or active for login /configuration')
            self.add_statement(Statement(pattern=r'^.*This \(D\)RP Node is not ready or active for login \/configuration$',
                                          action=print_message,
                                          args={'message': 'Device reached login prompt before rommon prompt'},
                                          loop_continue=False,
                                          continue_timer=False))

            # Privileged Exec Prompt (ex: 'RP/0/RSP0/CPU0#')
            self.add_statement(Statement(pattern=r'^RP\/0\/RSP(0|1)\/CPU0\:.*#$',
                                          action=print_message,
                                          args={'message': 'Device has reached privileged exec prompt'},
                                          loop_continue=False,
                                          continue_timer=False))

            # Privileged Exec Prompt (ex: 'PE1 con0/RSP0/CPU0 is in standby')
            self.add_statement(Statement(pattern=r'^(\S+ )?con(0|1)\/RSP(0|1)\/CPU0 +is +in +standby',
                                          action=print_message,
                                          args={'message': 'Device has reached privileged exec prompt'},
                                          loop_continue=False,
                                          continue_timer=False))

            # Privileged Exec Prompt (ex: 'PE1 con0/RSP0/CPU0 is in standby')
            self.add_statement(Statement(pattern=r'^(?:(\S+))? *con(0|1)/RSP(0|1)/CPU0 +is(( +in +standby)|( +now +available)).*',
                                         action='sendline()',
                                         loop_continue=True,
                                         matched_retry_sleep=30,
                                         continue_timer=False))

            # Press RETURN to get started
            self.add_statement(Statement(pattern=r'^.*Press RETURN to get started.*',
                                         action='sendline()',
                                         loop_continue=True,
                                         continue_timer=False))
                                         
class RommonDialog(CommonRommonDialog):

      def __init__(self):
            # Login prompt
            self.add_statement(Statement(pattern=r'^.*(Username|login)\:.*$', #^.*(Username|login): ?$',
                                          action=print_message,
                                          args={'message': 'Successfully recovered Active RP'},
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
                                          continue_timer=False))

            # Exec Prompt (ex: 'Router>')
            self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^>])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?>$',
                                          action='sendline(en)',
                                          loop_continue=True,
                                          continue_timer=False))

            # Privileged Exec Prompt (ex: 'Router#')
            self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^#])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?#$',
                                          action=None,
                                          args=None,
                                          loop_continue=False,
                                          continue_timer=False))

            # Standby prompt (ex: 'This (D)RP Node is not ready or active for login /configuration')
            self.add_statement(Statement(pattern=r'^.*This \(D\)RP +Node +is +not +ready +or +active +for +login \/configuration',
                                         action=print_message,
                                         args={'message': 'Successfully recovered Standby RP'},
                                          loop_continue=False,
                                          continue_timer=False))

            # Privileged Exec Prompt (ex: 'RP/0/RSP0/CPU0#')
            self.add_statement(Statement(pattern=r'^RP\/0\/RSP(0|1)\/CPU0\:.*#$',
                                          action='sendline()',
                                          args=None,
                                          loop_continue=False,
                                          continue_timer=False))

            # Privileged Exec Prompt (ex: 'PE1 con0/RSP0/CPU0 is in standby')
            self.add_statement(Statement(pattern=r'^.*(\S+)?.*con(0|1)\/RSP(0|1)\/CPU0 +is(( +in +standby)|( +now +available))',
                                         action='sendline()',
                                         args=None,
                                          loop_continue=False,
                                          continue_timer=False))

      
      # rommon >
      @statement_decorator(r'^(.*)(rommon(.*))+>.*$', loop_continue=True, continue_timer=False)
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


class TftpRommonDialog(RommonDialog):

    def __init__(self):

        # Press RETURN to get started
        self.add_statement(Statement(pattern=r'^.*Press RETURN to get started.*',
                                     action='sendline()',
                                     loop_continue=True,
                                     matched_retries=3,
                                     matched_retry_sleep=30,
                                     continue_timer=False))

        # Privileged Exec Prompt (ex: 'Router#')
        self.add_statement(Statement(pattern=r'^(Router|Switch|ios|switch|.+[^#])(\\(standby\\))?(\\(-stby)\\)?(\\(boot\\))?#$',
                                     action=print_message,
                                     args={'message': 'Device has reached privileged exec prompt'},
                                     loop_continue=False,
                                     continue_timer=False))


    def hostname_statement(self, hostname):
        '''Notify exec prompt has been reached '''

        # Exec Prompt (ex: 'Router>')
        self.add_statement(Statement(pattern=r'^(.*?)({hostname}|Router|Switch|ios|switch)(\\(standby\\))?(-stby)?(\\(boot\\))?(>)'.format(hostname=hostname),
                                     action=print_message,
                                     args={'message': 'Device has reached exec prompt'},
                                     loop_continue=False,
                                     continue_timer=False))


    @statement_decorator(r'(.*)(rommon(.*))+>.*', loop_continue=True, continue_timer=False)
    def boot_device(spawn, session, context):
        ''' Load new image on the device from rommon with tftp '''

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
        boot_cmd = 'boot tftp://{tftp}/{image}'.format(tftp=context['tftp_server'],
                                                       image=context['image'][0])

        # Send the boot command to the device
        log.info("Sending TFTP boot command...")
        try:
            spawn.sendline(boot_cmd)
        except Exception as e:
            raise Exception("Unable to boot {} error {}".format(boot_cmd, str(e)))


    # Username
    @statement_decorator(r'^.*(Username|login): ?$', loop_continue=True, continue_timer=False)
    def send_username(spawn, session, context):
        '''Send login username to the device '''

        time.sleep(0.5)
        spawn.sendline('{}'.format(context['username']))


    # Password:
    @statement_decorator(r'^.*[Pp]assword( for )?(\\S+)?: ?$', loop_continue=True, continue_timer=False)
    def send_password(spawn, session, context):
        ''' Send login password to the device '''

        time.sleep(0.5)
        spawn.sendline('{}'.format(context['password']))

