'''Common OS: Image Handler Class'''

# Python
import os
import random

class ImageHandler(object):


    def __init__(self, device, images, *args, **kwargs):
        self.device = device
        self.images = images
        self.ctl_files = []
        self.ctd_files = []
        # Save 'append_hostname' (if provided)
        self.append_hostname = self.device.clean.get('copy_to_linux', {}).\
                                                 get('append_hostname')
        # Save 'unique_file_name' (if provided)
        self.unique_filename = self.device.clean.get('copy_to_linux', {}).\
                                                  get('unique_file_name')


    def add_hostname(self, file):
        '''Adds hostname to the given file'''

        image_name, image_ext = os.path.splitext(file)
        return ''.join([image_name, '_', self.device.name, image_ext])


    def add_unique_filename(self, file):
        '''Adds unique random number generated to the given file'''

        # Check if user has provided any unique number
        unique_num = self.device.clean.get('copy_to_linux', {}).\
                                       get('unique_number', None)

        # Generate random number to file
        if not unique_num:
            unique_num = random.randint(100000, 999999)

        # Set random number generated into section
        self.device.clean.get('copy_to_linux', {}).\
                          setdefault('unique_number', unique_num)

        image_name, image_ext = os.path.splitext(file)
        return ''.join([image_name, '_', str(unique_num), image_ext])
