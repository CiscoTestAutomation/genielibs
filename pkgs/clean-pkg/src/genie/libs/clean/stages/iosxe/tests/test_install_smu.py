import logging
import unittest

from unittest.mock import Mock, MagicMock, call, ANY

from genie.libs.clean.stages.iosxe.stages import InstallSmu
from genie.libs.clean.stages.tests.utils import create_test_device


from pyats.aetest.steps import Steps
from pyats.results import Passed, Skipped

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Installimage(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallSmu()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_iosxe_install_image_pass(self):
        steps = Steps()
        cls = InstallSmu()
        cls.history = MagicMock()

        device = Mock()
        device.reload = Mock()
        device.parse = Mock(return_value=
                            {'location': {'Switch 1': {'pkg_state': 
                            {1: {'type': 'IMG', 'state': 'C', 'filename_version': '17.17.01.0.207986'},
                             2: {'type': 'SMU', 'state': 'I', 'filename_version': 'flash:cat9k_iosxe.BLD_POLARIS_DEV_LATEST_20240908_003038.0.NODEFECT.SSA.smu.bin'}},
                             'auto_abort_timer': 'inactive'}}})

        cls.install_smu(steps=steps, device=device, images=['sftp://server/image.smu.bin'])

        device.reload.assert_has_calls([
            call('install activate file sftp://server/image.smu.bin', reply=ANY,
                 reload_creds='default', prompt_recovery=True, error_pattern=['FAILED:.*?$'],
                 timeout=500, device_recovery=False)
        ])
        self.assertEqual(Passed, steps.details[0].result)

    def test_iosxe_install_smu_image_skip(self):
        steps = Steps()
        cls = InstallSmu()
        cls.history = MagicMock()
        device = Mock()
        # skip the stage if the provide image is not a smu image
        cls.install_smu(steps=steps, device=device, images=['sftp://server/image.bin'])
        self.assertEqual(Skipped, steps.details[0].result)