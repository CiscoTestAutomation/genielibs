""" NXOS ACI: Image Handler Class """

import yaml

from genie.libs.clean.stages.image_handler import BaseImageHandler

from pyats.utils.schemaengine import Schema, ListOf, Optional


class ImageLoader(object):

    EXPECTED_IMAGE_STRUCTURE_MSG = """\
Expected one of the following structures for 'images' in the clean yaml

Structure #1
------------
images:
- /path/to/switch_image.bin

Structure #2
------------
images:
  switch:
  - /path/to/switch_image.bin

Structure #3
------------
images:
  switch:
    file:
    - /path/to/switch_image.bin

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
            setattr(self, 'switch', images)
            return True
        else:
            return False

    def valid_structure_2(self, images):

        schema = {
            'switch': ListOf(str)
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if ('switch' in images and
                len(images['switch']) == 1):

            setattr(self, 'switch', images['switch'])
            return True
        else:
            return False

    def valid_structure_3(self, images):

        schema = {
            'switch': {
                'file': ListOf(str)
            }
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if ('switch' in images and
                len(images['switch']['file']) == 1):

            setattr(self, 'switch', images['switch']['file'])
            return True
        else:
            return False


class ImageHandler(BaseImageHandler, ImageLoader):

    def __init__(self, device, images, *args, **kwargs):

        # Set defaults
        self.switch = []
        self.other = []

        # Check if images is one of the valid structures and
        # load into a consolidated structure
        ImageLoader.load(self, images)

        # Temp workaround for XPRESSO
        if self.switch:
            self.switch = [self.switch[0].replace('file://', '')]

        super().__init__(device, images, *args, **kwargs)


    def update_image_references(self, section):
        if 'image_mapping' in section.parameters:
            for index, image in enumerate(self.switch):
                # change the saved image to the new image name/path
                self.switch[index] = section.parameters['image_mapping'].get(
                    image, self.switch[index])

    def update_copy_to_linux(self, number=''):
        '''Update clean section 'copy_to_linux' with image information'''

        # Init 'copy_to_linux' defaults
        origin = self.device.clean.setdefault('copy_to_linux'+number, {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.switch})

    def update_copy_to_device(self, number=''):
        '''Update clean stage 'copy_to_device' with image information'''

        origin = self.device.clean.setdefault('copy_to_device'+number, {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.switch})

    def update_fabric_clean(self, number=''):
        '''Update clean stage 'fabric_clean' with image information '''

        fabric_clean = self.device.clean.setdefault('fabric_clean'+number, {})
        if fabric_clean.get('copy_boot_image', {}).get('origin', {}):
            fabric_clean['copy_boot_image']['origin'].update({'files': self.switch})

