import logging
from genie.utils.timeout import Timeout

log = logging.getLogger(__name__)

def verify_boot_variable(device, boot_images, output=None):
    """ Verifies given boot_images are set to the next-reload BOOT vars

    Args:
        device (obj): The device to execute on.

        boot_images (list): The images that are expected to be configured
            as the boot variable for the next reload.

        output (str, optional): The device output from 'show boot'. If not
            provided the API will gather it from the device automatically.
            Defaults to None.

    Returns:
        True - if the expected images are configured
        False - if the expected images are NOT configured

    Raises:
        N/A
    """
    next_boot_variables = device.api.get_boot_variables(
        boot_var='next', output=output)

    if len(next_boot_variables) != len(boot_images):
        return False

    for index, expected_image in enumerate(boot_images):
        configured_image = next_boot_variables[index]

        # For cat9k 'flash' and 'bootflash' are the same directory.
        # Which means 'flash:image' is the same file as 'bootflash:image'
        if (expected_image.startswith('bootflash:') or
            expected_image.startswith('flash:')) and \
                (configured_image.startswith('bootflash:') or
                 configured_image.startswith('flash:')):

            log.info("On cat9k platforms, the 'flash:' and 'bootflash:' "
                     "directories are the same. Ignoring these "
                     "directories during comparison.")

            # Do the special compare where the directory is ignored
            if expected_image.split(':')[-1] != configured_image.split(':')[-1]:
                log.warning("The boot variables on the device {} do not equal "
                            "the expected images {}".format(next_boot_variables,
                                                            boot_images))
                return False

        else:
            if expected_image != next_boot_variables[index]:
                log.warning("The boot variables on the device {} do not "
                            "equal the expected images {}"
                            .format(next_boot_variables,
                                    boot_images))
                return False

    log.info("The boot variables on the device {} equal the expected "
             "images {}".format(next_boot_variables, boot_images))
    return True


