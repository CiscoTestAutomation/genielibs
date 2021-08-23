""" NXOS ACI: Image Handler Class """

import yaml

from genie.libs.clean.stages.image_handler import BaseImageHandler

from pyats.utils.schemaengine import Schema, ListOf, Optional


class ImageLoader(object):

    EXPECTED_IMAGE_STRUCTURE_MSG = """\
Expected one of the following structures for 'images' in the clean yaml

Other images are optional other files, in structure #1, if one image is provided it will be used for both controller and switch, otherwise controller must come first

Structure #1
------------
images:
- /path/to/controller_image.bin
- /path/to/switch_image.bin
- /path/to/other/images.bin   <<< optional

Structure #2
------------
images:
  controller:
  - /path/to/controller_image.bin
  switch:
  - /path/to/switch_image.bin
  other:   <<< optional
  - /path/to/other/images.bin

Structure #3
------------
images:
  controller:
    file:
    - /path/to/controller_image.bin
  switch:
    file:
    - /path/to/switch_image.bin
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

        if len(images) == 1:
            # This is not a bug. It is optional to clean only switches or only
            # controllers but we do not know what type of image the user
            # provided if they only provide 1.
            setattr(self, 'controller', images)
            setattr(self, 'switch', images)
            return True
        if len(images) >= 2:
            setattr(self, 'controller', images[:1])
            setattr(self, 'switch', images[1:2])
            setattr(self, 'other', images[2:])
            return True
        else:
            return False

    def valid_structure_2(self, images):

        schema = {
            Optional('controller'): ListOf(str),
            Optional('switch'): ListOf(str),
            Optional('other'): ListOf(str)
        }

        try:
            Schema(schema).validate(images)
        except Exception:
            return False

        if ('controller' in images and
                'switch' in images and
                len(images['controller']) == 1 and
                len(images['switch']) == 1):
            setattr(self, 'controller', images['controller'])
            setattr(self, 'switch', images['switch'])
            setattr(self, 'other', images.get('other', []))
            return True

        elif ('controller' in images and
              len(images['controller']) == 1):
            setattr(self, 'controller', images['controller'])
            setattr(self, 'other', images.get('other', []))
            return True

        elif ('switch' in images and
                len(images['switch']) == 1):
            setattr(self, 'switch', images['switch'])
            setattr(self, 'other', images.get('other', []))
            return True

        else:
            return False

    def valid_structure_3(self, images):

        schema = {
            Optional('controller'): {
                'file': ListOf(str)
            },
            Optional('switch'): {
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

        if ('controller' in images and
                'switch' in images and
                len(images['controller']['file']) == 1 and
                len(images['switch']['file']) == 1):
            setattr(self, 'controller', images['controller']['file'])
            setattr(self, 'switch', images['switch']['file'])
            setattr(self, 'other', images.get('other', {}).get('file', []))
            return True

        elif ('controller' in images and
              len(images['controller']['file']) == 1):
            setattr(self, 'controller', images['controller']['file'])
            setattr(self, 'other', images.get('other', {}).get('file', []))
            return True

        elif ('switch' in images and
              len(images['switch']['file']) == 1):
            setattr(self, 'switch', images['switch']['file'])
            setattr(self, 'other', images.get('other', {}).get('file', []))
            return True
        else:
            return False


class ImageHandler(BaseImageHandler, ImageLoader):

    def __init__(self, device, images, *args, **kwargs):

        # Set defaults
        self.controller = []
        self.switch = []
        self.other = []

        # Check if images is one of the valid structures and
        # load into a consolidated structure
        ImageLoader.load(self, images)

        # Temp workaround for XPRESSO
        if self.controller:
            self.controller = [self.controller[0].replace('file://', '')]
        if self.switch:
            self.switch = [self.switch[0].replace('file://', '')]

        if hasattr(self, 'other'):
            self.other = [x.replace('file://', '') for x in self.other]

        super().__init__(device, images, *args, **kwargs)


    def update_image_references(self, section):
        if 'image_mapping' in section.parameters:

            for index, image in enumerate(self.controller):
                # change the saved image to the new image name/path
                self.controller[index] = section.parameters['image_mapping'].get(
                    image, self.controller[index])

            for index, image in enumerate(self.switch):
                # change the saved image to the new image name/path
                self.switch[index] = section.parameters['image_mapping'].get(
                    image, self.switch[index])

            if hasattr(self, 'other'):
                for index,image in enumerate(self.other):
                    self.other[index] = section.parameters['image_mapping'].get(image, self.other[index])

    def update_copy_to_linux(self, number=''):
        '''Update clean section 'copy_to_linux' with image information'''
        files = self.device.clean.setdefault('copy_to_linux'+number, {}).\
            setdefault('origin', {}).setdefault('files', [])

        # Update the same object id
        files.clear()
        files.extend(self.controller + self.switch + self.other)

    def update_copy_to_device(self, number=''):
        '''Update clean stage 'copy_to_device' with image information'''
        files = self.device.clean.setdefault('copy_to_device'+number, {}).\
            setdefault('origin', {}).setdefault('files', [])

        # Update the same object id
        files.clear()
        files.extend(self.controller + self.switch + self.other)

    def update_fabric_upgrade(self, number=''):
        '''Update clean stage 'fabric_upgrade' with image information'''

        fabric_upgrade = self.device.clean.setdefault('fabric_upgrade'+number, {})
        fabric_upgrade.update({'controller_image': self.controller})
        fabric_upgrade.update({'switch_image': self.switch})

