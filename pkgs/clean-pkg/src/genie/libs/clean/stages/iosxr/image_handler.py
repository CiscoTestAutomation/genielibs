'''IOSXR: Image Handler Class'''

# Genie
from genie.libs.clean.stages.iosxe.image_handler import ImageHandler as IosxeImageHandler


class ImageHandler(IosxeImageHandler):

    def __init__(self, device, images, *args, **kwargs):
        super().__init__(device, images, *args, **kwargs)

    def update_install_image_and_packages(self, number=''):
        ''' Update clean stage 'install_image_and_packages' with
            package information
        '''
        install_packages = self.device.clean.setdefault('install_image_and_packages'+number, {})
        install_packages.update({'image': self.image})
        install_packages.update({'packages': self.packages})
