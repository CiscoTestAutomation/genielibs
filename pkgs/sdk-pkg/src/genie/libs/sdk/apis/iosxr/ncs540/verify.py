from genie.libs.sdk.apis.iosxr.ncs5k.verify import verify_current_image as verify_current_image_ncs540

def verify_current_image(device, images, **kwargs):
    '''Verify current images on the device
        Args:
            device (`obj`): Device object
            images (`list`): List of images expected on the device
        Returns:
            None
    '''
    return verify_current_image_ncs540(device, images)

