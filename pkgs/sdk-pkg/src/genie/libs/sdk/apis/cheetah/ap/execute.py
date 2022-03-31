# Python
import logging
from unicon.eal.dialogs import Statement, Dialog

#unicon
from unicon.core.errors import SubCommandFailure, TimeoutError

# Logger
log = logging.getLogger(__name__)


def execute_prime_ap(device, controller_ip_address, controller_name):
    try:
        device.execute("capwap ap primary-base {name} {ip}".format(name=controller_name, ip=controller_ip_address))
        device.execute("test capwap restart")
    except (SubCommandFailure, TimeoutError) as e:
        log.error("Failed to prime ap-{} to controller-{} due to error:\n {}".format(device.name, controller_name, e))
        return False
    return True


def execute_erase_ap(device):
    dialog = Dialog([
        Statement(pattern=r'Are you sure you want continue\? \[confirm\]',
                  action='send(\r)',
                  loop_continue=True,
                  continue_timer=False),
    ])
    try:
        device.execute("capwap ap erase all", reply=dialog)
    except (SubCommandFailure, TimeoutError) as e:
        log.error("Failed to erase configs on  ap-{} due to error:\n {}".format(device.name, e))
        return False
    return True


