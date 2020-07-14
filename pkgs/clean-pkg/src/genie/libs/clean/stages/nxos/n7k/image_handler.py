'''NXOS N7K: Image Handler Class'''

# Python
import os

# Genie
from genie.libs.clean.stages.image_handler import ImageHandler as CommonImageHandler


class ImageHandler(CommonImageHandler):


    def __init__(self, device, images, *args, **kwargs):
        super().__init__(device, images, *args, **kwargs)

        # Set 'kickstart' and 'system' images
        if self.images:
            if isinstance(self.images, dict):
                for key, value in self.images.items():
                    try:
                        assert key in ['kickstart', 'system']
                    except AssertionError:
                        raise Exception("Invalid key '{}' provided for N7K images"
                                        "\nValid keys are 'kickstart' and 'system'")

                    # incase the file key is used
                    if isinstance(value, dict):
                        image_list = value['file']
                    else:
                        image_list = value

                    if len(image_list) > 1:
                        raise Exception("Found more than 1 image for '{}' image".\
                                        format(key))

                    setattr(self, key, image_list[0])
            elif isinstance(self.images, list) and len(self.images)==2:
                # Set 'kickstart'
                setattr(self, 'kickstart', self.images[0])
                # Set 'system'
                setattr(self, 'system', self.images[1])
            else:
                raise Exception("Expecting 'kickstart' and 'system' images for "
                                "NXOS N7K platform provided under 'images' "
                                "key as a list or dictionary")
        else:
            raise Exception("'images' list or dictionary not provided and is "
                            "expected for 'nxos'")

    def update_tftp_boot(self):
        '''Update clean section 'tftp_boot' with image information'''

        # Init 'tftp_boot' defaults
        self.tftp_boot_images = self.device.clean.setdefault('tftp_boot', {}).\
                                                  setdefault('image', [])

        # Add images to key 'files' in section tftp_boot
        for file in [self.kickstart, self.system]:
            self.tftp_boot_images.append(file)


    def update_copy_to_linux(self):
        '''Update clean section 'copy_to_linux' with image information'''

        # Init 'copy_to_linux' defaults
        self.ctl_files = self.device.clean.setdefault('copy_to_linux', {}).\
                                           setdefault('origin', {}).\
                                           setdefault('files', [])

        # Add images to key 'files' in section copy_to_linux
        for file in [self.kickstart, self.system]:
            self.ctl_files.append(file)


    def update_copy_to_device(self):
        '''Update clean stage 'copy_to_device' with image information'''

        # Init 'copy_to_device' defaults
        self.ctd_files = self.device.clean.setdefault('copy_to_device', {}).\
                                           setdefault('origin', {}).\
                                           setdefault('files', [])

        if not self.ctl_files:
            # 'copy_to_linux' is not executed before 'copy_to_device'
            for file in [self.kickstart, self.system]:
                self.ctd_files.append(file)
        else:
            # 'copy_to_linux' is executed before 'copy_to_device'
            # Get destination director of 'copy_to_linux'
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

                # Add hostname
                if self.append_hostname:
                    filename = self.add_hostname(filename)

                # Add unique number to filename
                if self.unique_filename:
                    filename = self.add_unique_filename(filename)

                # Set filename after linux copy
                filename_on_linux = os.path.join(ctl_dest_dir, filename)

                # Add file to 'files' key under 'copy_to_device'
                self.ctd_files.append(filename_on_linux)


    def update_change_boot_variable(self):
        '''Update clean stage 'change_boot_variable' with image information'''

        if not self.ctd_files:
            # 'copy_to_device' was not executed before 'change_boot_variable'

            # Set 'kickstart' 'images'
            self.device.clean.setdefault('change_boot_variable', {}).\
                              setdefault('images', {}).\
                              setdefault('kickstart', self.kickstart)

            # Set 'system' 'images'
            self.device.clean.setdefault('change_boot_variable', {}).\
                              setdefault('images', {}).\
                              setdefault('system', self.system)
        else:
            # 'copy_to_device' is executed before 'change_boot_variable'
            # Get destination director of 'copy_to_device'
            ctd_dest_dir = self.device.clean.get('copy_to_device', {}).\
                                             get('destination', {}).\
                                             get('directory')
            if not ctd_dest_dir:
                raise Exception("Clean section 'copy_to_device' missing "
                                "mandatory key 'destination' or 'directory'")

            # Get kickstart base filename
            kickstart_filename = os.path.basename(self.kickstart)
            if self.append_hostname:
                kickstart_filename = self.add_hostname(kickstart_filename)

            # Set 'kickstart' 'images'
            self.device.clean.setdefault('change_boot_variable', {}).\
                              setdefault('images', {}).\
                              setdefault('kickstart', \
                                os.path.join(ctd_dest_dir, kickstart_filename))

            # Get system base filename
            system_filename = os.path.basename(self.system)
            if self.append_hostname:
                system_filename = self.add_hostname(system_filename)

            # Set 'system' 'images'
            self.device.clean.setdefault('change_boot_variable', {}).\
                              setdefault('images', {}).\
                              setdefault('system', \
                                os.path.join(ctd_dest_dir, system_filename))


    def update_verify_running_image(self):
        '''Update clean stage 'verify_running_image' with image information'''

        # Init 'verify_running_image' defaults
        vrv_images = self.device.clean.setdefault('verify_running_image', {}).\
                                       setdefault('images', [])

        if not self.ctd_files:
            # 'copy_to_device' was not executed before 'verify_running_image'
            vrv_images.append(self.system)
            vrv_images.append(self.kickstart)
        else:
            # 'copy_to_device' is executed before 'verify_running_image'
            # Get destination director of 'copy_to_device'
            ctd_dest_dir = self.device.clean.get('copy_to_device', {}).\
                                             get('destination', {}).\
                                             get('directory')
            if not ctd_dest_dir:
                raise Exception("Clean section 'copy_to_device' missing "
                                "mandatory key 'destination' or 'directory'")

            for file in [self.kickstart, self.system]:

                # Get base filename
                filename = os.path.basename(file)
                if self.append_hostname:
                    filename = self.add_hostname(filename)

                # Set filename on device
                filename_on_device = os.path.join(ctd_dest_dir, filename)

                # Add file to 'images' key under 'verify_running_image'
                vrv_images.append(filename_on_device)

