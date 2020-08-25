'''IOSXE: Image Handler Class'''

# Genie
from genie.libs.clean.stages.image_handler import BaseImageHandler


class ImageHandler(BaseImageHandler):

    EXPECTED_IMAGE_STRUCTURE_MSG = """
-----------------------------------------------------------------------
Expected one of the following structures for 'images' in the clean yaml
-----------------------------------------------------------------------
images:
- /path/to/image.bin
- /path/to/package1
- /path/to/package2

images:
  image:
  - /path/to/image.bin
  packages:
  - /path/to/package1
  - /path/to/package2
  
images:
  image:
    file:
    - /path/to/image.bin
  packages:
    file:
    - /path/to/package1
    - /path/to/package2

-------------------------
Images structure provided
-------------------------
{}"""

    def __init__(self, device, images, *args, **kwargs):

        if isinstance(images, list) and len(images) >= 1:
            self.images = images[:1]
            self.packages = images[1:]

        elif isinstance(images, dict):
            try:
                if isinstance(images['image'], list):
                    self.images = images['image'][:1]
                else:
                    self.images = images['image']['file'][:1]

                # Because 'packages' is optional
                if 'packages' in images:
                    if isinstance(images['packages'], list):
                        self.packages = images['packages']
                    else:
                        self.packages = images['packages']['file']
                else:
                    self.packages = []

            except (KeyError, TypeError):
                self.exception = {'images': images}
        else:
            self.exception = {'images': images}

        # Raises an exception if the 'images' structure is invalid
        # otherwise initializes common variables
        super().__init__(device, *args, **kwargs)

        # Temp workaround for XPRESSO
        self.images = [self.images[0].replace('file://', '')]
        self.packages = [x.replace('file://', '') for x in self.packages]

    def update_image_references(self, section):
        # section.parameters['image_mapping'] shall be saved in any
        # stage that modifies the image name/path
        if 'image_mapping' in section.parameters:

            for index, image in enumerate(self.images):
                # change the saved image to the new image name/path
                self.images[index] = section.parameters['image_mapping'].get(image, image)

            for index, package in enumerate(self.packages):
                # change the saved package to the new package name/path
                self.packages[index] = section.parameters['image_mapping'].get(package, package)

    def update_tftp_boot(self):
        '''Update clean section 'tftp_boot' with image information'''

        tftp_boot = self.device.clean.setdefault('tftp_boot', {})
        tftp_boot.update({'image': self.images})

    def update_copy_to_linux(self):
        '''Update clean section 'copy_to_linux' with image information'''

        origin = self.device.clean.setdefault('copy_to_linux', {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.images + self.packages})

    def update_copy_to_device(self):
        '''Update clean stage 'copy_to_device' with image information'''

        origin = self.device.clean.setdefault('copy_to_device', {}).\
                                   setdefault('origin', {})
        origin.update({'files': self.images + self.packages})

    def update_change_boot_variable(self):
        '''Update clean stage 'change_boot_variable' with image information'''

        change_boot_variable = self.device.clean.setdefault('change_boot_variable', {})
        change_boot_variable.update({'images': self.images})

    def update_verify_running_image(self):
        '''Update clean stage 'verify_running_image' with image information'''

        verify_running_image = self.device.clean.setdefault('verify_running_image', {})
        verify_running_image.update({'images': self.images})

    def update_install_image(self):
        '''Update clean stage 'install_image' with image information'''

        install_image = self.device.clean.setdefault('install_image', {})
        install_image.update({'images': self.images})

    def update_install_packages(self):
        '''Update clean stage 'install_packages' with package information'''

        install_packages = self.device.clean.setdefault('install_packages', {})
        install_packages.update({'packages': self.packages})