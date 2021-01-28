""" Execute type APIs for NXOS ACI Fabric"""

import logging
import os

from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)

def execute_clean_node_fabric(
        device,
        hostname=None,
        copy_protocol=None,
        image=None,
        destination_dir=None,
        copy_max_time=300,
        max_time=90):
    """ Cleans the node part of the ACI fabric

    Args:
        device (obj): Device to execute on

        hostname (str, optional): Hostname to copy boot image from if its not
            found. Defaults to None.

        copy_protocol (str, optional): Protocol to use for copying boot image
            if its not found. Defaults to None

        image (str, optional): Boot image to copy if its not found. Defaults
            to None.

        destination_dir (str, optional): Directory to copy the boot image to.
            Defaults to None.

        copy_max_time (int, optional): Max time in seconds allowed for copying
            the image. Defaults to 300.

        max_time (int, optional): Max time in seconds allowed for executing
            clean commands. Defaults to 90.

    Returns:
        True if successful
        False if failed

    Raises:
        N/A
    """

    clean_dialog = Dialog([
        Statement(
            pattern=r".*This command will wipe out this device\, Proceed\? \[y\/N\].*",
            action='sendline(y)'
        )
    ])

    # Check if a boot image is configured and exists
    boot_cfg = device.execute(
        'cat /mnt/cfg/0/boot/grub/menu.lst.local | grep boot')
    if boot_cfg:
        boot_cfg = boot_cfg.split()[1]

        if ':' in boot_cfg:
            boot_cfg = boot_cfg.split(':')[1]

        bootflash = device.execute('ls bootflash/')

        if boot_cfg in bootflash:
            image_found = True
        else:
            image_found = False

    else:
        image_found = False

    # There is no boot image and copy to device is not specified.
    # Can no longer proceed.
    if (not image_found and
            not hostname and
            not copy_protocol and
            not image and
            not destination_dir):
        log.error("No boot image exists and arguments to copy an image were "
                  "not specified.")
        return False

    # If the image does not exist on the device and copy image args are
    # specified, then copy the image.
    elif not image_found:
        server = hostname
        protocol = copy_protocol
        remote_path = image
        local_path = destination_dir

        testbed = device.testbed
        if (protocol in testbed.servers and
                'default' in testbed.servers[protocol].credentials and
                'username' in testbed.servers[protocol].credentials.default and
                'password' in testbed.servers[protocol].credentials.default):
            username = testbed.servers[protocol].credentials.default.username
            password = testbed.servers[protocol].credentials.default.password
        else:
            username = None
            password = None

        try:
            device.api.copy_to_device(
                protocol=protocol,
                server=server,
                remote_path=remote_path,
                local_path=local_path,
                timeout=copy_max_time,
                username=username,
                password=password
            )
        except Exception as e:
            log.error("Failed to copy image to the device. Error: {}"
                      .format(str(e)))
            return False
        else:
            boot_cfg = os.path.basename(remote_path)

    cmds = ['/bin/setup-clean-config.sh',
            '/bin/setup-bootvars.sh {}'.format(boot_cfg)]

    try:
        device.execute(
            cmds,
            timeout=max_time,
            reply=clean_dialog,
            error_pattern=[r".*Cant find image.*"])
    except Exception as e:
        log.error("Failed during cleaning the device. Error: {}".format(str(e)))
        return False
    else:
        return True
