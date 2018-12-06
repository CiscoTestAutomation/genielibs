
# python
from os import path

# module logger
import logging
log = logging.getLogger(__name__)

# parser
from genie.libs.parser.nxos.show_platform import ShowBoot, ShowVersion

def save_device_information(device, **kwargs):
    """Check boot variable from show version and show boot
    to see if they are consistent. Configure boot var if not same,
    and save running-configuration to startup-config.
    This is for N9K devices.

    Args:
      Mandatory:
        device (`obj`) : Device object.

    Raises:
        Exception: show command is failed to execute or
                   failed to get image information

    Example:
        >>> save_device_information(device=Device())
    """

    # Get current running image
    try:
        out = ShowVersion(device).parse()
        ver_kick_img = out['platform']['software']['kickstart_image_file']
        ver_sys_img = out['platform']['software']['system_image_file']

        ver_location = path.dirname(ver_sys_img)
        ver_sys_img = path.basename(ver_sys_img)
        ver_kick_img = path.basename(ver_kick_img)
    except Exception as e:
        raise Exception('Cannot get the image information from "show version"') from e

    # Get next reload image
    try:
        out = ShowBoot(device).parse()
        if 'sup_number' in out.get('next_reload_boot_variable', ''):
            sup = list(out['next_reload_boot_variable']['sup_number'].keys())
            next_sys_img = out['next_reload_boot_variable']['sup_number']['sup-1']['system_variable']
            next_kick_img = out['next_reload_boot_variable']['sup_number']['sup-1']['kickstart_variable']
        else:
            next_sys_img = out['next_reload_boot_variable']['system_variable']
            next_kick_img = out['next_reload_boot_variable']['kickstart_variable']

        next_sys_img = path.basename(next_sys_img)
        next_kick_img = path.basename(next_kick_img)
    except Exception as e:
        log.warning('Cannot get the next reload image information from "show boot"')
        next_sys_img = None
        next_kick_img = None

    # check if need to configure the boot vars
    if ver_sys_img == next_sys_img and ver_kick_img == next_kick_img:
        log.info('Device will reload with image {}'.format(ver_sys_img))
        device.system = ver_sys_img
        device.kickstart = ver_kick_img
    else:
        device.system = ver_sys_img
        device.kickstart = ver_kick_img
        # configure boot var
        if not sup:
            cfg_str = 'boot kickstart {loc}{kick_img}\nboot system {loc}{sys_img}'\
                       .format(loc=ver_location, sys_img=ver_sys_img, kick_img=ver_kick_img)
        else:
            cfg_str = ''
            for sup_item in sup:
                cfg_str += 'boot kickstart {loc}{kick_img} {sup}\nboot system {loc}{sys_img} {sup}\n'\
                           .format(loc=ver_location,
                                   sys_img=ver_sys_img, kick_img=ver_kick_img,
                                   sup=sup_item)
        device.configure(cfg_str)

    # Copy boot variables
    device.execute('copy running-config startup-config vdc-all')
