'''IOSXR: Image Handler Class'''

# Python
import os

# Genie
from genie.libs.clean.stages.image_handler import ImageHandler as CommonImageHandler

class ImageHandler(CommonImageHandler):

    def __init__(self, device, images, *args, **kwargs):
        super().__init__(device, images, *args, **kwargs)

        # Ensure 'images' provided is valid
        if isinstance(images, list):
            # set in CommonImageHandler
            pass
        elif isinstance(images.get('image', {}).get('file', {}), list):
            self.images = images['image']['file']
        else:
            raise Exception("For 'iosxr' images must be one of the following formats:\n\n"
                            "    images: [<image>]\n\n"
                            "or\n\n"
                            "    images:\n"
                            "        image:\n"
                            "            file: [<image>]")


    def update_tftp_boot(self):
        '''Update clean section 'tftp_boot' with image information'''

        # Init 'tftp_boot' defaults
        self.tftp_boot_images = self.device.clean.setdefault('tftp_boot', {}).\
                                                  setdefault('image', [])

        # Add image to key 'files' in section tftp_boot
        self.tftp_boot_images.extend(self.images)


    def update_copy_to_linux(self):
        '''Update clean section 'copy_to_linux' with image information'''

        # Init 'copy_to_linux' defaults
        self.ctl_files = self.device.clean.setdefault('copy_to_linux', {}).\
            setdefault('origin', {}).\
            setdefault('files', [])

        # Add image to key 'files' in section copy_to_linux
        self.ctl_files.extend(self.images)

    def update_copy_to_device(self):
        '''Update clean stage 'copy_to_device' with image information'''

        # Init 'copy_to_device' defaults
        self.ctd_files = self.device.clean.setdefault('copy_to_device', {}).\
            setdefault('origin', {}).\
            setdefault('files', [])

        if not self.ctl_files:
            # 'copy_to_linux' is not executed before 'copy_to_device'
            self.ctd_files.extend(self.images)
        else:
            # 'copy_to_linux' is executed before 'copy_to_device'
            # Get destination directory of 'copy_to_linux'
            ctl_dest_dir = self.device.clean.get('copy_to_linux', {}).\
                get('destination', {}).\
                get('directory')
            if not ctl_dest_dir:
                raise Exception("Clean section 'copy_to_linux' missing "
                                "mandatory key 'destination' or 'directory'")

            # Add all files from 'copy_to_linux' to 'copy_to_device'
            for file in self.ctl_files:

                # Get base filename
                filename = os.path.basename(file)
                if self.append_hostname:
                    filename = self.add_hostname(filename)

                # Set filename after linux copy
                filename_on_linux = os.path.join(ctl_dest_dir, filename)

                # Add file to 'files' key under 'copy_to_device'
                self.ctd_files.append(filename_on_linux)

    def update_change_boot_variable(self):
        '''Update clean stage 'change_boot_variable' with image information'''

        cbv_images = self.device.clean.setdefault('change_boot_variable', {}).\
            setdefault('images', [])

        if not self.ctd_files:
            # 'copy_to_device' was not executed before 'change_boot_variable'
            cbv_images.extend(self.images)
        else:
            # 'copy_to_device' is executed before 'change_boot_variable'
            # Get destination director of 'copy_to_device'
            ctd_dest_dir = self.device.clean.get('copy_to_device', {}).\
                get('destination', {}).\
                get('directory')
            if not ctd_dest_dir:
                raise Exception("Clean section 'copy_to_device' missing "
                                "mandatory key 'destination' or 'directory'")

            for file in self.images:

                # Get base filename
                filename = os.path.basename(file)
                if self.append_hostname:
                    filename = self.add_hostname(filename)

                # Set filename on device
                filename_on_device = os.path.join(ctd_dest_dir, filename)

                # Add file to 'images' key under 'change_boot_variable'
                cbv_images.append(filename_on_device)

    def update_verify_running_image(self):
        '''Update clean stage 'verify_running_image' with image information'''
        
        # Init 'verify_running_image' defaults
        vrv_images = self.device.clean.setdefault('verify_running_image', {}).\
            setdefault('images', [])

        if not self.ctd_files:
            # 'copy_to_device' was not executed before 'verify_running_image'
            vrv_images.extend(self.images)
        else:
            # 'copy_to_device' is executed before 'verify_running_image'
            # Get destination director of 'copy_to_device'
            ctd_dest_dir = self.device.clean.get('copy_to_device', {}).\
                get('destination', {}).\
                get('directory')
            if not ctd_dest_dir:
                raise Exception("Clean section 'copy_to_device' missing "
                                "mandatory key 'destination' or 'directory'")

            for file in self.images:

                # Get base filename
                filename = os.path.basename(file)
                if self.append_hostname:
                    filename = self.add_hostname(filename)

                # Set filename on device
                filename_on_device = os.path.join(ctd_dest_dir, filename)

                # Add file to 'images' key under 'verify_running_image'
                vrv_images.append(filename_on_device)
