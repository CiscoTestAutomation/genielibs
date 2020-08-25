'''NXOS N7K: Image Handler Class'''

# Genie
from genie.libs.clean.stages.image_handler import BaseImageHandler


class ImageHandler(BaseImageHandler):

    EXPECTED_IMAGE_STRUCTURE_MSG = """
-----------------------------------------------------------------------
Expected one of the following structures for 'images' in the clean yaml
-----------------------------------------------------------------------
images:
- /path/to/kickstart.bin
- /path/to/system.bin

images:
  kickstart:
  - /path/to/kickstart.bin
  system:
  - /path/to/system.bin

images:
  kickstart:
    file:
    - /path/to/kickstart.bin
  system:
    file:
    - /path/to/system.bin

-------------------------
Images structure provided
-------------------------
{}"""

    def __init__(self, device, images, *args, **kwargs):

        if isinstance(images, list) and len(images) >= 2:
            setattr(self, 'kickstart', [images[0]])
            setattr(self, 'system', [images[1]])

        elif isinstance(images, dict):
            try:
                if isinstance(images['kickstart'], list):
                    kickstart = images['kickstart']
                else:
                    kickstart = images['kickstart']['file']

                if isinstance(images['system'], list):
                    system = images['system']
                else:
                    system = images['system']['file']

                setattr(self, 'kickstart', [kickstart[0]])
                setattr(self, 'system', [system[0]])

            except KeyError:
                self.exception = {'images': images}
        else:
            self.exception = {'images': images}

        # Raises an exception if the 'images' structure is invalid
        # otherwise initializes common variables
        super().__init__(device, *args, **kwargs)

        # Temp workaround for XPRESSO
        self.system = [self.system[0].replace('file://', '')]
        self.kickstart = [self.kickstart[0].replace('file://', '')]

    def update_image_references(self, section):
        # section.parameters['image_mapping'] shall be saved in any
        # stage that modifies the image name/path
        if 'image_mapping' in section.parameters:

            for index,image in enumerate(self.system):
                # change the saved image to the new image name/path
                self.system[index] = section.parameters['image_mapping'].get(image, self.system[index])

            for index,image in enumerate(self.kickstart):
                # change the saved image to the new image name/path
                self.kickstart[index] = section.parameters['image_mapping'].get(image, self.kickstart[index])

    def update_tftp_boot(self):
        '''Update clean section 'tftp_boot' with image information'''

        tftp_boot = self.device.clean.setdefault('tftp_boot', {})
        tftp_boot.update({'image': self.kickstart + self.system})

    def update_copy_to_linux(self):
        '''Update clean section 'copy_to_linux' with image information'''

        # Init 'copy_to_linux' defaults
        origin = self.device.clean.setdefault('copy_to_linux', {}).\
                                          setdefault('origin', {})
        origin.update({'files': self.kickstart + self.system})

    def update_copy_to_device(self):
        '''Update clean stage 'copy_to_device' with image information'''

        origin = self.device.clean.setdefault('copy_to_device', {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.kickstart + self.system})


    def update_change_boot_variable(self):
        '''Update clean stage 'change_boot_variable' with image information'''

        images = self.device.clean.setdefault('change_boot_variable', {}).\
                          setdefault('images', {})
        images.update({'kickstart': self.kickstart})
        images.update({'system': self.system})

    def update_verify_running_image(self):
        '''Update clean stage 'verify_running_image' with image information'''

        verify_running_image = self.device.clean.setdefault('verify_running_image', {})
        verify_running_image.update({'images': self.kickstart + self.system})

