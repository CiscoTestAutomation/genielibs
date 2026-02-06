'''
NXOS N9K specific clean stages
'''
import time
import logging
from genie.libs.clean import BaseStage
from genie.metaparser.util.schemaengine import Optional
from genie.libs.sdk.libs.abstracted_libs.nxos.subsection import get_default_dir
from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)


class InstallImage(BaseStage):
    """This stage installs a provided image onto the device using the install CLI.
Stage Schema
------------
install_image:
    images (list): Image to install
    install_timeout (int, optional): Maximum time in seconds to wait for install
        process to finish. Defaults to 750.

reload_timeout (int, optional): Maximum time in seconds to wait for reload
            process to finish. Defaults to 300.

ascii_config_processing_time (int, optional): Time in seconds to wait for
            ASCII configuration processing to complete after reload. Defaults to 60.

Example
-------
install_image:
    images:
      - bootflash:nxos.9.3.5.bin
    install_timeout: 500
    reload_timeout: 300
    ascii_config_processing_time: 90
"""
    # =================
    # Argument Defaults
    # =================
    INSTALL_TIMEOUT = 750
    RELOAD_TIMEOUT = 300
    ASCII_CONFIG_PROCESSING_TIME = 60

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('install_timeout'): int,
        Optional('reload_timeout'): int,
        Optional('ascii_config_processing_time'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'install_image',
    ]

    def install_image(self, steps, device, images, install_timeout=INSTALL_TIMEOUT, reload_timeout=RELOAD_TIMEOUT,
                      ascii_config_processing_time=ASCII_CONFIG_PROCESSING_TIME):
        with steps.start(f"Installing image '{images[0]}'") as step:

            install_add_one_shot_dialog = Dialog([
                Statement(pattern=r".*Do you want to continue with the installation \(y\/n\)\?\s*\[n\]\s+$",
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False),
                Statement(pattern=r"Waiting for standby to come online",
                          action=None, 
                          loop_continue=True, 
                          continue_timer=True),
            ])

            try:
                device.execute('install all nxos {}'.format(images[0]),
                               reply=install_add_one_shot_dialog,
                               append_error_pattern=['Failed'],
                               timeout=install_timeout)
            except Exception as e:
                step.failed("Failed to install the image", from_exception=e)

            def wait_ascii_process():
                log.info(f"Reload completed. waiting for {ascii_config_processing_time} secs to ASCII configuration processing completed. ")
                time.sleep(ascii_config_processing_time)

            # After image install, device may auto reload in some cases
            # so we have to detect auto reload and wait device to reload
            check_reload_dialog = Dialog([
                    Statement(
                        pattern=r"(Finishing the upgrade, switch will reboot in)",
                        action=None,
                        loop_continue=True,
                        continue_timer=True
                    ),

                    Statement(
                    pattern=r"CISCO MODULE|BIOS Ver|Booting from|Security Lock",
                    loop_continue=True,
                    continue_timer=True
                    ),

    
                    Statement(
                        pattern=r"System is coming up|Configuration mode is blocked",
                        loop_continue=True,
                        continue_timer=True
                    ),

                    Statement(
                        pattern=r"%ASCII-CFG-2-CONFIG_REPLAY_STATUS",
                        loop_continue=True,
                        continue_timer=True
                    ),

                    Statement(
                        pattern=r"Thirdparty RPMs installation succeeded",
                        action=wait_ascii_process,
                        loop_continue=False,
                        continue_timer=False
                    ),
                                ])

            try:
                check_reload_dialog.process(device.spawn, timeout=reload_timeout)
                log.info("Reload prompt detected after install command.")
            except Exception:
                log.info("No reload prompt detected after install command.")

