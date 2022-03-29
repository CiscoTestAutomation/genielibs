'''IOS: Image Handler Class'''

import yaml

from genie.libs.clean.stages.image_handler import BaseImageHandler

from pyats.utils.schemaengine import Schema, ListOf, Optional


class ImageLoader(object):

    EXPECTED_IMAGE_STRUCTURE_MSG = """\
Expected one of the following structures for 'images' in the clean yaml

Other images are optional other files, in structure #1 the image must always come first

Structure #1
------------
images:
- /path/to/image.bin
- /path/to/other/images.bin   <<< optional

Structure #2
------------
images:
  image:
  - /path/to/image.bin
  other:   <<< optional
  - /path/to/other/images.bin

Structure #3
------------
images:
  image:
    file:
    - /path/to/image.bin
  other:   <<< optional
    file:
    - /path/to/other/images.bin

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

        if not images:
            return False
        else:
            setattr(self, 'image', images[0:1])
            setattr(self, 'other', images[1:])
            return True

    def valid_structure_2(self, images):

        schema = {
            'image': ListOf(str),
            Optional('other'): ListOf(str)
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images['image']) != 1:
            return False
        else:
            setattr(self, 'image', images['image'])
            setattr(self, 'other', images.get('other', []))

        return True


    def valid_structure_3(self, images):

        schema = {
            'image': {
                'file': ListOf(str)
            },
            Optional('other'): {
                'file': ListOf(str)
            }
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images['image']['file']) != 1:
            return False
        else:
            setattr(self, 'image', images['image']['file'])
            setattr(self, 'other', images.get('other', {}).get('file', []))

        return True


class ImageHandler(BaseImageHandler, ImageLoader):

    def __init__(self, device, images, *args, **kwargs):

        # Set default
        self.packages = []
        self.other = []

        # Check if images is one of the valid structures and
        # load into a consolidated structure
        ImageLoader.load(self, images)

        # Temp workaround for XPRESSO
        self.image = [self.image[0].replace('file://', '')]

        if hasattr(self, 'other'):
            self.other = [x.replace('file://', '') for x in self.other]

        self.original_image = [self.image[0].replace('file://', '')]

        super().__init__(device, *args, **kwargs)

    def update_image_references(self, section):
        # section.parameters['image_mapping'] shall be saved in any
        # stage that modifies the image name/path
        if 'image_mapping' in section.parameters:

            for index, image in enumerate(self.image):
                # change the saved image to the new image name/path
                self.image[index] = section.parameters['image_mapping'].get(image, image)

            if hasattr(self, 'other'):
                for index,image in enumerate(self.other):
                    self.other[index] = section.parameters['image_mapping'].get(image, self.other[index])

    def update_tftp_boot(self, number=''):
        '''Update clean section 'tftp_boot' with image information'''

        tftp_boot = self.device.clean.setdefault('tftp_boot'+number, {})
        tftp_boot.update({'image': self.image})

    def update_copy_to_linux(self, number=''):
        '''Update clean section 'copy_to_linux' with image information'''

        files = self.device.clean.setdefault('copy_to_linux' + number, {}). \
            setdefault('origin', {}).setdefault('files', [])

        files.clear()
        files.extend(self.image + self.other)

    def update_copy_to_device(self, number=''):
        '''Update clean stage 'copy_to_device' with image information'''

        files = self.device.clean.setdefault('copy_to_device' + number, {}). \
            setdefault('origin', {}).setdefault('files', [])

        files.clear()
        files.extend(self.image + self.other)

    def update_change_boot_variable(self, number=''):
        '''Update clean stage 'change_boot_variable' with image information'''

        change_boot_variable = self.device.clean.setdefault('change_boot_variable'+number, {})
        change_boot_variable.update({'images': self.image})

    def update_verify_running_image(self, number=''):
        '''Update clean stage 'verify_running_image' with image information'''
        verify_running_image = self.device.clean. \
            setdefault('verify_running_image' + number, {})

        if verify_running_image.get('verify_md5'):
            verify_running_image.update({'images': self.original_image})
        else:
            verify_running_image.update({'images': self.image})

