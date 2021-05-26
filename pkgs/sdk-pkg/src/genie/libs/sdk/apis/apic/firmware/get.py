""" Get type APIs for APIC """

import re
import logging

from genie.metaparser.util.exceptions import SchemaEmptyParserError, InvalidCommandError
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)

def get_firmware_repository_images(device, image_type=None):
    """ Returns a list of images in the firmware repository.

    Args:
        device (obj): Device to execute on
        image_type (str): Type of images to return

    Returns:
        (list): of images in the firmware repository

    Raises:
        N/A
    """
    try:
        out = device.parse('show firmware repository')
    except SchemaEmptyParserError:
        log.warning("'show firmware repository' parser returned nothing")
        return []

    # {
    # 	'name': {
    # 		'aci-catalog-dk9.70.8.2.bin': {
    # 			'version': {
    # 				'70.8(2)': {
    # 					'name': 'aci-catalog-dk9.70.8.2.bin',
    # 					'type': 'catalog',
    # 					'version': '70.8(2)',
    # 					'size': 0.129
    # 				}
    # 			}
    # 		}
    #    }
    # }
    if image_type:
        return out.q.contains_key_value('type', image_type).get_values('name')
    else:
        return out.q.get_values('name')

def get_firmware_repository_images_by_polling(device, image_type=None,
                                              max_time=120, check_interval=15):
    """ Polls the firmware repository for an image that matches
    'image_type'. Returns after a matching image is found.

    Args:
        device (obj): Device to execute on
        image_type (str): Type of images to return
        max_time (int, optional): Max time for polling. Defaults to 120.
        check_interval (int, optional): How often to poll. Defaults to 15.

    Returns:
        (list): of images in the firmware repository

    Raises:
        N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = device.api.get_firmware_repository_images(image_type=image_type)
        if result:
            return result

        timeout.sleep()

    return []

def get_firmware_upgrade_status(device, firmware_group=None):
    """ Returns a list of tuples containing node_id, status.

    Args:
        device (obj): Device to execute on
        firmware_group (str, optional): group to filter by. Defaults to None.

    Returns:
        (list of tuples): each containing "node_id, status"

    Raises:
        N/A
    """
    if firmware_group:
        cmd = 'show firmware upgrade status {}'.format(firmware_group)
    else:
        cmd = 'show firmware upgrade status'

    try:
        output = device.parse(cmd)
    except SchemaEmptyParserError:
        log.warning("'{}' parser returned nothing".format(cmd))
        return []

    info = []

    for node in output.get('node', {}):
        info.append((node, output['node'][node]['status']))

    return info


def get_firmware_version_from_image_name(device, image_name):
    """ Get the firmware version from the image name.

    Args:
        image_name (str): image filename

    Returns:
        string with image version
    """
    m = re.search(r'apic-dk9\.(\d+\.\d+)\.(\w+)', image_name)
    if m:
        version_major_minor = m.group(1)
        version_patch = m.group(2)
        version = '{}({})'.format(version_major_minor, version_patch)
        return version
