"""IIOT specific clean stages"""

# Python
import logging

# Genie
from genie.libs.clean.stages.iosxe.ie3k.stages import (
    RommonBoot as Ie3kRommonBoot,
    InstallImage as Ie3kInstallImage,
    WriteErase as Ie3kWriteErase,
)

# Logger
log = logging.getLogger(__name__)


class RommonBoot(Ie3kRommonBoot):
    """This stage boots an image onto the device through rommon.

IE9k is similar to IE3k, hence reusing IE3k's implementation.

Stage Schema
------------
rommon_boot:

    image (list): Image to boot with

    save_system_config (bool, optional): Whether or not to save the
        system config if it was modified. Defaults to True.

    timeout (int, optional): Max time allowed for the booting process.
        Defaults to 600.

    reconnect_timeout (int, optional): Timeout to reconnect the device after booting. Default to 120 sec.

Example
-------
rommon_boot:
    image:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    save_system_config: False
    timeout: 600
"""
    pass


class InstallImage(Ie3kInstallImage):
    """This stage installs a provided image onto the device using the install
CLI. It also handles the automatic reloading of your device after the
install is complete.

IE9k is similar to IE3k, hence reusing IE3k's implementation.

Stage Schema
------------
install_image:
    images (list): Image to install

    directory (str): directory where packages.conf is created
    save_system_config (bool, optional): Whether or not to save the system
        config if it was modified. Defaults to False.

    install_timeout (int, optional): Maximum time in seconds to wait for install
        process to finish. Defaults to 500.

    reload_timeout (int, optional): Maximum time in seconds to wait for reload
        process to finish. Defaults to 800.

    skip_boot_variable (bool, optional): 
    
    skip_save_running_config (bool, optional): Skip the step to save the the running
                                        configuration to the startup config.

    issu (bool, optional): set the issu for installing image.
        Defaults to False 

    verify_running_image (bool, optional): Compare the image filename with the running
        image version on device. If a match is found, the stage will be skipped.
        Defaults to True.
    
    stack_member_timeout(optional, int): maximum time to to wait for all the members of a stack device 
        to be ready. Default to 180 seconds

    stack_member_interval(optional, int): the interval to check if all the members of a stack device 
        are ready. Default to 30 seconds

    reload_service_args (optional):

        reload_creds (str, optional): The credential to use after the reload is
            complete. The credential name comes from the testbed yaml file.
            Defaults to the 'default' credential.

        prompt_recovery (bool, optional): Enable or disable the prompt recovery
            feature of unicon. Defaults to True.

        error_pattern (list, optional): List of regex strings to check for errors.
            Default: [r"FAILED:.*?$",]
        
        post_reload_wait(int, optional): the time after for before buffer to settle down.
            . Default to 30 seconds

        post_reload_timeout(int, optional): maximum time before accessing the device after
            reload. Default to 60 seconds.
        <Key>: <Value>
            Any other arguments that the Unicon reload service supports

Example
-------
install_image:
    images:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    save_system_config: True
    install_timeout: 1000
    reload_timeout: 1000

"""
    pass


class WriteErase(Ie3kWriteErase):
    """ This stage executes 'write erase' on the device & removes the `nvram_config`
files from the optional filesystems provided.

IE9k is similar to IE3k, hence reusing IE3k's implementation.

Stage Schema
------------
write_erase:

    timeout (int, optional): Max time allowed for 'write erase'command to complete.
        Defaults to 300 seconds.

    nvram_filesystems (list, optional): List of optional filesystems to remove
        nvram_config files. Defaults to ['sdflash:', 'usbflash0:', 'usbflash1:'].

Example
-------
write_erase:
    timeout: 100
    nvram_filesystems:
    - 'sdflash:'
"""
    pass
