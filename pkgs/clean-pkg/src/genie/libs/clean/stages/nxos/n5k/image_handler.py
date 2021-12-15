'''NXOS N5K: Image Handler Class'''

import yaml

from genie.libs.clean.stages.image_handler import BaseImageHandler

from pyats.utils.schemaengine import Schema, ListOf, Optional


class ImageLoader(object):

    EXPECTED_IMAGE_STRUCTURE_MSG = """\
Expected one of the following structures for 'images' in the clean yaml

Other images are optional other files, in structure #1 the kickstart image must always come first, system image must always come second

Structure #1
------------
images:
- /path/to/kickstart.bin
- /path/to/system.bin
- /path/to/other/images.bin   <<< optional

Structure #2
------------
images:
  kickstart:
  - /path/to/kickstart.bin
  system:
  - /path/to/system.bin
  other:   <<< optional
  - /path/to/other/images.bin

Structure #3
------------
images:
  kickstart:
    file:
    - /path/to/kickstart.bin
  system:
    file:
    - /path/to/system.bin
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

        if len(images) < 2:
            return False
        else:
            setattr(self, 'kickstart', [images[0]])
            setattr(self, 'system', [images[1]])
            setattr(self, 'other', images[2:])
            return True

    def valid_structure_2(self, images):

        schema = {
            'kickstart': ListOf(str),
            'system': ListOf(str),
            Optional('other'): ListOf(str)
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if len(images['kickstart']) == 1 and len(images['system']) == 1:
            setattr(self, 'kickstart', images['kickstart'])
            setattr(self, 'system', images['system'])
            setattr(self, 'other', images.get('other', []))
            return True
        else:
            return False

    def valid_structure_3(self, images):

        schema = {
            'kickstart': {
                'file': ListOf(str)
            },
            'system': {
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

        if len(images['kickstart']['file']) == 1 and len(images['system']['file']) == 1:
            setattr(self, 'kickstart', images['kickstart']['file'])
            setattr(self, 'system', images['system']['file'])
            setattr(self, 'other', images.get('other', {}).get('file', []))
            return True
        else:
            return False


class ImageHandler(BaseImageHandler, ImageLoader):

    def __init__(self, device, images, *args, **kwargs):

        self.other = []

        # Check if images is one of the valid structures and
        # load into a consolidated structure
        ImageLoader.load(self, images)

        # Temp workaround for XPRESSO
        self.system = [self.system[0].replace('file://', '')]
        self.kickstart = [self.kickstart[0].replace('file://', '')]

        if hasattr(self, 'other'):
            self.other = [x.replace('file://', '') for x in self.other]

        self.original_system = [self.system[0].replace('file://', '')]
        self.original_kickstart = [self.kickstart[0].replace('file://', '')]

        super().__init__(device, *args, **kwargs)

    def update_image_references(self, section):
        # section.parameters['image_mapping'] shall be saved in any
        # stage that modifies the image name/path
        if 'image_mapping' in section.parameters:

            for index,image in enumerate(self.system):
                # change the saved image to the new image name/path
                self.system[index] = section.parameters['image_mapping'].get(image, image)

            for index,image in enumerate(self.kickstart):
                # change the saved image to the new image name/path
                self.kickstart[index] = section.parameters['image_mapping'].get(image, image)

            if hasattr(self, 'other'):
                for index,image in enumerate(self.other):
                    self.other[index] = section.parameters['image_mapping'].get(image, self.other[index])

    def update_tftp_boot(self, number=''):
        '''Update clean section 'tftp_boot' with image information'''
        image = self.device.clean.setdefault('tftp_boot'+number, {}).setdefault('image', [])

        # Update the same object id
        image.clear()
        image.extend(self.kickstart + self.system)

    def update_copy_to_linux(self, number=''):
        '''Update clean section 'copy_to_linux' with image information'''
        files = self.device.clean.setdefault('copy_to_linux'+number, {}).\
            setdefault('origin', {}).setdefault('files', [])

        # Update the same object id
        files.clear()
        files.extend(self.kickstart + self.system + self.other)

    def update_copy_to_device(self, number=''):
        '''Update clean stage 'copy_to_device' with image information'''
        files = self.device.clean.setdefault('copy_to_device'+number, {}).\
            setdefault('origin', {}).setdefault('files', [])

        # Update the same object id
        files.clear()
        files.extend(self.kickstart + self.system + self.other)

    def update_change_boot_variable(self, number=''):
        '''Update clean stage 'change_boot_variable' with image information'''

        images = self.device.clean.setdefault('change_boot_variable'+number, {}).\
            setdefault('images', {})

        kickstart = images.setdefault('kickstart', [])
        # Update the same object id
        kickstart.clear()
        kickstart.extend(self.kickstart)

        system = images.setdefault('system', [])
        # Update the same object id
        system.clear()
        system.extend(self.system)

    def update_verify_running_image(self, number=''):
        '''Update clean stage 'verify_running_image' with image information'''
        verify_running_image = self.device.clean. \
            setdefault('verify_running_image' + number, {})

        images = verify_running_image.setdefault('images', [])
        images.clear()

        if verify_running_image.get('verify_md5'):
            images.extend(self.original_kickstart + self.original_system)
        else:
            images.extend(self.kickstart + self.system)
