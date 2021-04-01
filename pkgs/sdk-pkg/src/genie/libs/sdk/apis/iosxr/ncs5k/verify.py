import logging

log = logging.getLogger(__name__)

def verify_current_image(device, images):
    '''Verify current images on the device
        Args:
            device (`obj`): Device object
            images (`list`): List of images expected on the device
        Returns:
            None
    '''
    if not images:
        raise Exception("At least one image must be provided in the "
                        "'images' list")

    # Get current running image
    version = device.api.get_software_version()
    if version is None:
        raise Exception("Failed to get the software version.")

    if all(version in image for image in images):
        log.info("The running software version ({}) is found in all the "
                 "expected images: {}".format(version, images))
    else:
        raise Exception("The running software version ({}) is not found "
                        "in all the expected images: {}".format(version, images))
