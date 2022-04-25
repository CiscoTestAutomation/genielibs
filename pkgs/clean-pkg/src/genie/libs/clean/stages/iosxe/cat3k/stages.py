'''
IOSXE cat3k specific clean stages
'''
# Genie
from genie.metaparser.util.schemaengine import Optional
from genie.libs.clean.stages.iosxe.stages import (
    InstallImage as IOSXEInstallImage)

# Unicon
from unicon.eal.dialogs import Statement, Dialog

class InstallImage(IOSXEInstallImage):
    """This stage installs a provided image onto the device using the install
CLI. It also handles the automatic reloading of your device after the
install is complete.

Stage Schema
------------
install_image:
    images (list): Image to install

    save_system_config (bool, optional): Whether or not to save the system
        config if it was modified. Defaults to False.

    install_timeout (int, optional): Maximum time in seconds to wait for install
        process to finish. Defaults to 500.

    reload_timeout (int, optional): Maximum time in seconds to wait for reload
        process to finish. Defaults to 800.

Example
-------
install_image:
    images:
      - /auto/some-location/that-this/image/stay-isr-image.bin
    save_system_config: True
    install_timeout: 1000
    reload_timeout: 1000

"""
    # =================
    # Argument Defaults
    # =================
    SAVE_SYSTEM_CONFIG = False
    INSTALL_TIMEOUT = 500
    RELOAD_TIMEOUT = 800

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('save_system_config'): bool,
        Optional('install_timeout'): int,
        Optional('reload_timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'delete_boot_variable',
        'set_boot_variable',
        'deactivate_manual_boot',
        'save_running_config',
        'verify_boot_variable',
        'install_image',
        'wait_for_reload'
    ]

    def deactivate_manual_boot(self,steps,device):
        with steps.start("deactivate boot manual") as step:
            try:
                device.configure('no boot manual')
            except Exception as e:
                step.failed("Failed to deactivate boot manual",
                            from_exception=e)

    def install_image(self, steps, device, images, save_system_config=SAVE_SYSTEM_CONFIG,
                      install_timeout=INSTALL_TIMEOUT):
        with steps.start(f"Installing image '{images[0]}'") as step:

            install_add_one_shot_dialog = Dialog([
                Statement(pattern=r".*Press Quit\(q\) to exit, you may save "
                                  r"configuration and re-enter the command\. "
                                  r"\[y\/n\/q\]",
                          action='sendline(y)' if save_system_config else 'sendline(n)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r".*Please confirm you have changed boot config "
                                  r"to \S+ \[y\/n\]",
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r".*reload of the system\. "
                                  r"Do you want to proceed\? \[y\/n\]",
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False),

                Statement(pattern='Press RETURN to get started.*',
                          action='sendline()',
                          args=None,
                          loop_continue=False,
                          continue_timer=False),  
                Statement(pattern=r"FAILED:.* ",
                          action=None,
                          loop_continue=False,
                          continue_timer=False),
            ])

            try:
                device.reload('install add file {} activate commit'.format(images[0]),
                               reply=install_add_one_shot_dialog,
                               append_error_pattern=['FAILED:.* '],
                               timeout=install_timeout)
            except Exception as e:
                step.failed("Failed to install the image", from_exception=e)

            image_mapping = self.history['InstallImage'].parameters.setdefault(
                'image_mapping', {})
            image_mapping.update({images[0]: self.new_boot_var})
