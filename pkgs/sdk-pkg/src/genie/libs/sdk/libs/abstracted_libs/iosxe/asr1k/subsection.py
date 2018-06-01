
# python
from os import path

# unicon
from unicon.eal.dialogs import Statement, Dialog

# module logger
import logging
log = logging.getLogger(__name__)

# parser
from genie.libs.parser.iosxe.show_platform import ShowVersion, ShowRedundancy

def save_device_information(device, **kwargs):
    """Check boot variable from show version and show reedundancy
    to see if they are consistent. Configure boot var if not same,
    and save running-configuration to startup-config.
    This is for asr1k devices.

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Raises:
        Exception: show command is failed to execute or
                   failed to get image information

    Example:
        >>> save_device_information(device=Device())
    """
    # get bootvar from show version
    try:
        out = ShowVersion(device).parse()
        ver_sys_img = out['version']['system_image']
    except Exception as e:
        raise Exception('Cannot get the image information '
                        'from "show version"') from e

    # get bootvar from show redundancy
    try:
        out = ShowRedundancy(device).parse()
        redundancy_image = []
        if 'slot' in out:
            for slot in out['slot']:
                redundancy_image.append(out['slot'][slot]['boot'])
            redundancy_image = list(set(redundancy_image))

            # active and standby image mismatch
            if len(redundancy_image) != 1:
                response = collections.OrderedDict()
                response[r"Destination +filename +\[.*\].*"] = "econ_send \\\r;exp_continue"
                response[r"Do +you +want +to +over +write? +\[confirm\]"] = "econ_send no\\\r;exp_continue"
                # copy image to standby bootflash: 
                # Destination filename [asr1000rpx.bin]?
                device.execute('copy {} stby-bootflash:'.format(ver_sys_img),
                               reply=response)
            redundancy_image = str(redundancy_image[0]).split(',')[0]
        else:
            redundancy_image = None
    except Exception as e:
        log.warning('Cannot get the boot image '
                    'information from "show redundancy"')
        redundancy_image = None


    # check if need to configure the boot vars
    if ver_sys_img:
        if ver_sys_img == redundancy_image:
            log.info('Device will reload with image {}'.format(ver_sys_img))
            device.system = ver_sys_img
        else:
            device.system = ver_sys_img
            # configure boot var
            cfg_str = 'no boot system\nboot system {sys_img}'.format(sys_img=ver_sys_img)
            device.configure(cfg_str)

    # configure config-register
    device.configure('config-register 0x2102')

    # save all configuration to startup for all slots
    dialog = Dialog([
        Statement(pattern=r'Destination +filename +\[.*\].*',
                            action='sendline()',
                            loop_continue=True,
                            continue_timer=False)
    ])
    device.execute('copy running-config nvram:startup-config',
                        reply=dialog)
    device.execute('write memory')
