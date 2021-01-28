'''IOSXE: Image Handler Class'''

import yaml

from genie.libs.clean.stages.image_handler import BaseImageHandler

from pyats.utils.schemaengine import Schema, ListOf, Optional


class ImageLoader(object):

    EXPECTED_IMAGE_STRUCTURE_MSG = """\
Expected one of the following structures for 'images' in the clean yaml

Structure #1
------------
images:
- /path/to/image.bin
- /path/to/optional_package1
- /path/to/optional_package2

Structure #2
------------
images:
  image:
  - /path/to/image.bin
  packages:   <<< optional
  - /path/to/optional_package1
  - /path/to/optional_package2

Structure #3
------------
images:
  image:
    file:
    - /path/to/image.bin
  packages:  <<< optional
    file:
    - /path/to/optional_package1
    - /path/to/optional_package2

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
            setattr(self, 'image', images)
            return True
        if len(images) >= 2:
            setattr(self, 'image', images[:1])
            setattr(self, 'packages', images[1:])
            return True
        else:
            return False

    def valid_structure_2(self, images):

        schema = {
            'image': ListOf(str),
            Optional('packages'): ListOf(str)
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images['image']) != 1:
            return False
        else:
            setattr(self, 'image', images['image'])

        if 'packages' in images:
            setattr(self, 'packages', images['packages'])

        return True


    def valid_structure_3(self, images):

        schema = {
            'image': {
                'file': ListOf(str)
            },
            Optional('packages'): {
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

        if 'packages' in images:
            setattr(self, 'packages', images['packages']['file'])

        return True


class ImageHandler(BaseImageHandler, ImageLoader):

    def __init__(self, device, images, *args, **kwargs):

        # Set default
        self.packages = []

        # Check if images is one of the valid structures and
        # load into a consolidated structure
        ImageLoader.load(self, images)

        # Temp workaround for XPRESSO
        self.image = [self.image[0].replace('file://', '')]
        if hasattr(self, 'packages'):
            self.packages = [x.replace('file://', '') for x in self.packages]

        super().__init__(device, *args, **kwargs)

    def update_image_references(self, section):
        # section.parameters['image_mapping'] shall be saved in any
        # stage that modifies the image name/path
        if 'image_mapping' in section.parameters:

            for index, image in enumerate(self.image):
                # change the saved image to the new image name/path
                self.image[index] = section.parameters['image_mapping'].get(image, image)

            for index, package in enumerate(self.packages):
                # change the saved package to the new package name/path
                self.packages[index] = section.parameters['image_mapping'].get(package, package)

    def update_tftp_boot(self):
        '''Update clean section 'tftp_boot' with image information'''

        tftp_boot = self.device.clean.setdefault('tftp_boot', {})
        tftp_boot.update({'image': self.image})

    def update_copy_to_linux(self):
        '''Update clean section 'copy_to_linux' with image information'''

        origin = self.device.clean.setdefault('copy_to_linux', {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.image + self.packages})

    def update_copy_to_device(self):
        '''Update clean stage 'copy_to_device' with image information'''

        origin = self.device.clean.setdefault('copy_to_device', {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.image + self.packages})

    def update_change_boot_variable(self):
        '''Update clean stage 'change_boot_variable' with image information'''

        change_boot_variable = self.device.clean.setdefault('change_boot_variable', {})
        change_boot_variable.update({'images': self.image})

    def update_verify_running_image(self):
        '''Update clean stage 'verify_running_image' with image information'''
        verify_running_image = self.device.clean.setdefault('verify_running_image', {})
        verify_running_image.update({'images': self.image})

    def update_install_image(self):
        '''Update clean stage 'install_image' with image information'''

        install_image = self.device.clean.setdefault('install_image', {})
        install_image.update({'images': self.image})

    def update_install_packages(self):
        '''Update clean stage 'install_packages' with package information'''

        install_packages = self.device.clean.setdefault('install_packages', {})
        install_packages.update({'packages': self.packages})