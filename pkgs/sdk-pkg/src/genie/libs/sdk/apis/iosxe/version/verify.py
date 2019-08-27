import logging

from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def is_version_image_installed(device, image):
    """ Verify if image is installed on device
        Args:
            device ('str'): Device object
            image ('str'): Image being verified
        Raise:
            None
        Return:
            True
            False
    """

    try:
        output = device.parse("show version")
    except SchemaEmptyParserError as e:
        return False

    installed_image = output["version"]["system_image"]

    if installed_image in image:
        return True
    else:
        log.error("Running image is {image}".format(image=installed_image))

    return False
