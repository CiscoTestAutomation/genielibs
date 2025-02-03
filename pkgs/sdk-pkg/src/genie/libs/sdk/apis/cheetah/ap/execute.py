# Python
import logging
import re
import time
from unicon.eal.dialogs import Statement, Dialog

#unicon
from unicon.core.errors import SubCommandFailure, TimeoutError



# Logger
log = logging.getLogger(__name__)

POST_RELOAD_WAIT_TIME=300

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


def execute_archive_download(device, image_path, max_timeout=300, username=None, password=None, reload=False, retries=3, retry_sleep_time=10):
    """
        Downloads image via tftp/http/sftp on AP and reloads the device.
        Args:
            device(object): device object
            image_path(str): path of the image in server
            max_timeout(int): the maximum timeout where device can perform the download
            username(str): Username of server where image resides
            password(str): Password of server where image resides
            reload(bool): Device reload if True else no reload
            retries(int): Number retried for downloading image
            retry_sleep_time(int): Number of seconds to sleep before next retry

        Returns:
            bool: True/False
        """
    dialog = Dialog([
        Statement(pattern=r'.*Username:\s*$',
                  action='sendline({})'.format(username),
                  loop_continue=True,
                  continue_timer=False),
        Statement(pattern=r'.*Password:\s*$',
                  action='sendline({})'.format(password),
                  loop_continue=True,
                  continue_timer=False)

    ])
    reload_dialog = Dialog([
        Statement(pattern=r'.*\[confirm\]',
                  action='send(\r)',
                  loop_continue=True,
                  continue_timer=False),

    ])
    boot_part_before_reload = re.search(r"BOOT path-list:(\s+\w+)", device.execute("show boot | inc BOOT")).group(1).strip()
    for i in range(retries):
        output = device.execute("archive download-sw /no-reload {}".format(image_path), timeout=max_timeout, reply=dialog)
        if "Successfully setup AP image" in output and "Image download completed" in output:
            log.debug("Successfully downloaded the image")
            break
        # sleep before next retry of downloading image
        log.debug("Sleep for {} seconds before next retry...".format(retry_sleep_time))
        time.sleep(retry_sleep_time)
    else:
        log.error("Failed to downloaded the image")
        return False
    if reload:
        try:
            device.reload(timeout=max_timeout, reply=reload_dialog, post_reload_wait_time=POST_RELOAD_WAIT_TIME)
            device.disconnect()
            device.connect()
        except (SubCommandFailure, TimeoutError):
            log.error("Failed to bring-up device after reload")
            return False
        else:
            boot_part_after_reload = re.search(r"BOOT path-list:(\s+\w+)", device.execute("show boot | inc BOOT")).group(1).strip()
            if boot_part_after_reload == boot_part_before_reload:
                log.error("Same boot part loaded after image downloading")
                return False 

    return True

