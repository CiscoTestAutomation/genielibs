'''Common OS: Image Handler Class'''

# Python
import os

class ImageHandler(object):


    def __init__(self, device, images, *args, **kwargs):
        self.device = device
        self.images = images
        self.ctl_files = []
        self.ctd_files = []
        # Save 'append_hostname' (if provided)
        self.append_hostname = self.device.clean.get('copy_to_linux', {}).\
                                                 get('append_hostname')


    def add_hostname(self, file):
        '''Adds hostname to the given file'''

        image_name, image_ext = os.path.splitext(file)
        return ''.join([image_name, '_', self.device.name, image_ext])

