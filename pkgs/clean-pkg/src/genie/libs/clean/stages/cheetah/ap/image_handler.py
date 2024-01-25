"""Cheetah/AP Image Handler Class"""

from genie.libs.clean.stages.iosxe.image_handler import ImageHandler as IosxeImageHandler
from pyats.utils.fileutils import FileUtils


class ImageHandler(IosxeImageHandler):

    def __init__(self, device, images, *args, **kwargs):
        super().__init__(device, images, *args, **kwargs)

    def update_image_references(self, section):
        # section.parameters['image_mapping'] shall be saved in any
        # stage that modifies the image name/path
        if 'image_mapping' in section.parameters:

            for index, image in enumerate(self.image):
                # change the saved image to the new image name/path
                self.image[index] = section.parameters['image_mapping'].get(image, image)

    def update_stamp_ap_image(self, number=''):
        """Update clean section 'stamp_ap_image' with image information"""
        stamp_ap_image = self.device.clean.setdefault('stamp_ap_image' + number, {})
        if self.override_stage_images:
            stamp_ap_image.update({'ap_image_path': self.image[0]})
        else:
            stamp_ap_image.setdefault('ap_image_path', self.image[0])

    def update_copy_to_linux(self, number=''):
        """Update clean section 'copy_to_linux' with image information"""
        files = self.device.clean.setdefault('copy_to_linux' + number, {}). \
            setdefault('origin', {}).setdefault('files', [])
        files.clear()
        files.extend(self.image)

    def update_load_ap_image(self, number=''):
        """Update clean section 'load_ap_image' with image information"""
        load_ap_image = self.device.clean.setdefault('load_ap_image' + number, {})
        if self.override_stage_images:
            load_ap_image.update({'ap_image_path': self.image[0]})
        else:
            load_ap_image.setdefault('ap_image_path', self.image[0])

  