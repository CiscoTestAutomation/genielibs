"""IOSXE ASR1K specific clean stages"""

# Python
import logging

from genie.metaparser.util.schemaengine import Optional
from genie.libs.clean.stages.stages import VerifyRunningImage as GenericVerifyRunningImage

# Logger
log = logging.getLogger(__name__)


class VerifyRunningImage(GenericVerifyRunningImage):
    """This stage verifies the current running image is the expected image.
The verification can be done by either MD5 hash comparison or by filename
comparison.

Stage Schema
------------
verify_running_image:

    images (list): Image(s) that should be running on the device. If not
        using verify_md5 then this should be the image path on the device.
        If using verify_md5 then this should be the original image location
        from the linux server.

    ignore_flash (bool, optional): Ignore flash directory names. Default True.

    verify_md5 (dict, optional): When this dictionary is defined, the image
            verification will by done by comparing the MD5 hashes of the
            running image against the expected image.

        hostname (str): Linux server that is used to generate the MD5
            hashes. This server must exist in the testbed servers block.

        timeout (int, optional): Maximum time in seconds allowed for the
            hashes to generate. Defaults to 60.

    regex_search (bool, optional): Verify image using regular expression. Default False.

Example
-------
verify_running_image:
    images:
        - test_image.bin
"""

    # =================
    # Argument Defaults
    # =================
    IGNORE_FLASH = True
    VERIFY_MD5 = False
    REGEX_SEARCH = False

    # ============
    # Stage Schema
    # ============
    schema = {
        'images': list,
        Optional('ignore_flash'): bool,
        Optional('verify_md5'): {
            'hostname': str,
            Optional('timeout'): int
        },
        Optional('regex_search'): bool,
    }

    def verify_running_image(self, steps, device, images, verify_md5=VERIFY_MD5, ignore_flash=IGNORE_FLASH,
                             regex_search=REGEX_SEARCH):
        super().verify_running_image(steps, device, images, verify_md5=verify_md5, ignore_flash=ignore_flash,
                                     regex_search=regex_search)
