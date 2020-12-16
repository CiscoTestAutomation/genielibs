'''NXOS N9K: Image Handler Class'''

import yaml

from genie.libs.clean.stages.image_handler import BaseImageHandler

from pyats.utils.schemaengine import Schema, ListOf


class ImageLoader(object):

    EXPECTED_IMAGE_STRUCTURE_MSG = """\
Expected one of the following structures for 'images' in the clean yaml

Structure #1
------------
images:
- /path/to/image.bin

Structure #2
------------
images:
  system:
  - /path/to/image.bin

Structure #3
------------
images:
  system:
    file:
    - /path/to/image.bin
      
But got the following structure
-------------------------------
{}"""

    def load(self, images):
        if (not self.valid_structure_1(images) and
                not self.valid_structure_2(images) and
                not self.valid_structure_3(images)):

            raise Exception(self.EXPECTED_IMAGE_STRUCTURE_MSG.format(
                yaml.dump({'images': images})))

    def valid_structure_1(self, images):

        schema = ListOf(str)

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images) == 1:
            setattr(self, 'system', images)
            return True
        else:
            return False

    def valid_structure_2(self, images):

        schema = {
            'system': ListOf(str)
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images['system']) == 1:
            setattr(self, 'system', images['system'])
            return True
        else:
            return False

    def valid_structure_3(self, images):

        schema = {
            'system': {
                'file': ListOf(str)
            }
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images['system']['file']) == 1:
            setattr(self, 'system', images['system']['file'])
            return True
        else:
            return False


class ImageHandler(BaseImageHandler, ImageLoader):

    def __init__(self, device, images, *args, **kwargs):

        # Check if images is one of the valid structures and
        # load into a consolidated structure
        ImageLoader.load(self, images)

        # Temp workaround for XPRESSO
        self.system = [self.system[0].replace('file://', '')]

        super().__init__(device, *args, **kwargs)

    def update_image_references(self, section):
        # section.parameters['image_mapping'] shall be saved in any
        # stage that modifies the image name/path
        if 'image_mapping' in section.parameters:

            for index,image in enumerate(self.system):
                # change the saved image to the new image name/path
                self.system[index] = section.parameters['image_mapping'].get(image, self.system[index])

    def update_tftp_boot(self):
        '''Update clean section 'tftp_boot' with image information'''

        tftp_boot = self.device.clean.setdefault('tftp_boot', {})
        tftp_boot.update({'image': self.system})

    def update_copy_to_linux(self):
        '''Update clean section 'copy_to_linux' with image information'''

        origin = self.device.clean.setdefault('copy_to_linux', {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.system})

    def update_copy_to_device(self):
        '''Update clean stage 'copy_to_device' with image information'''

        origin = self.device.clean.setdefault('copy_to_device', {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.system})

    def update_change_boot_variable(self):
        '''Update clean stage 'change_boot_variable' with image information'''

        images = self.device.clean.setdefault('change_boot_variable', {}). \
                                   setdefault('images', {})
        images.update({'system': self.system})

    def update_verify_running_image(self):
        '''Update clean stage 'verify_running_image' with image information'''

        verify_running_image = self.device.clean.setdefault('verify_running_image', {})
        verify_running_image.update({'images': self.system})
