'''
NXOS N9K specific clean stages
'''

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
Example
-------
install_image:
    images:
      - bootflash:nxos.9.3.5.bin
    install_timeout: 500
"""
    # =================
    # Argument Defaults
    # =================
    INSTALL_TIMEOUT = 750

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('images'): list,
        Optional('install_timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'install_image',
    ]

    def install_image(self, steps, device, images, install_timeout=INSTALL_TIMEOUT):
        with steps.start(f"Installing image '{images[0]}'") as step:

            install_add_one_shot_dialog = Dialog([
                Statement(pattern=r".*Do you want to continue with the installation \(y\/n\)\?\s*\[n\]\s+$",
                          action='sendline(y)',
                          loop_continue=True,
                          continue_timer=False),
            ])

            try:
                device.execute('install all nxos {}'.format(images[0]),
                               reply=install_add_one_shot_dialog,
                               append_error_pattern=['Failed'],
                               timeout=install_timeout)
            except Exception as e:
                step.failed("Failed to install the image", from_exception=e)

