
# python
from os import path

# module logger
import logging
log = logging.getLogger(__name__)

# unicon
from unicon.eal.dialogs import Statement, Dialog

# parser
from genie.libs.parser.iosxe.show_platform import ShowVersion, \
                                       ShowBoot, \
                                       ShowRedundancy

def save_device_information(device, **kwargs):
    """Check boot variable from show boot and show reedundancy
    to see if they are consistent. Configure boot var if not same,
    and save running-configuration to startup-config.
    This is for c3850 devices.

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
    ver_sys_img = getattr(kwargs.get('platform_pts', {}), 'image', None)

    if not ver_sys_img:
        log.info('Cannot get image from PTS, get image from show version instead')
        log.info("Get device current image from 'show version' on {}".format(device.name))
        try:
            out = ShowVersion(device).parse()
            ver_sys_img = out['version']['system_image']
        except:
            raise Exception('Cannot get the image information '
                            'from "show version"') from e
    else:
        log.info('Device {d} version image is {i} from PTS'.format(i=ver_sys_img, d=device.name))

    # get bootvar from show boot
    try:
        out = ShowBoot(device).parse()
        current_boot_variable = out['current_boot_variable']
        next_reload_boot_variable = out['next_reload_boot_variable']
        if next_reload_boot_variable in current_boot_variable:
            next_reload_image = next_reload_boot_variable
        else:
            next_reload_image = current_boot_variable
    except Exception as e:
        log.warning('Cannot get the boot image '
                    'information from "show boot"')
        next_reload_image = None

    # check if need to configure the boot vars
    if ver_sys_img:
        if ver_sys_img == next_reload_image:
            log.info('Device will reload with image {}'.format(ver_sys_img))
            device.system = ver_sys_img
        else:
            device.system = ver_sys_img
            # configure boot var
            cfg_str = 'no boot system\nboot system {sys_img}'.format(sys_img=ver_sys_img)
            device.configure(cfg_str)

    # avoid manual boot
    device.configure('no boot manual')

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
