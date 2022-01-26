'''IOSXE CAT3K specific Dialogs'''

# Python
import logging

# Unicon
from unicon.eal.dialogs import statement_decorator
from genie.libs.clean.recovery.iosxe.dialogs import BreakBootDialog as XeBreakBootDialog
from genie.libs.clean.recovery.iosxe.dialogs import RommonDialog as XeRommonDialog
from genie.libs.clean.recovery.iosxe.dialogs import TftpRommonDialog as XeTftpRommonDialog

log = logging.getLogger(__name__)
class BreakBootDialog(XeBreakBootDialog):
    '''Dialog to stop the device to boot at reload time'''

    pass

class RommonDialog(XeRommonDialog):

    pass

class TftpRommonDialog(XeTftpRommonDialog):
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
            f"IP_ADDRESS={ip}/{subnet_mask}",
            f"IP_SUBNET_MASK={subnet_mask}",
            f"DEFAULT_GATEWAY={gateway}",
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