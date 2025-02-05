import logging
import unittest

from unittest.mock import Mock, MagicMock, call, ANY, patch
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.cat9k.stages import InstallImage
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device
from genie.libs.clean.exception import StackMemberConfigException


from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Skipped
from pyats.aetest.signals import TerminateStepSignal, AEtestSkippedSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)

class TestInstallImage(unittest.TestCase):

    def test_iosxe_install_image_pass(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.chassis_type = 'stack' 
        device.sendline = Mock()
        # device.api.get_running_image.return_value = 'sftp://server/image.bin'

        with patch(
            "genie.libs.clean.stages.iosxe.cat9k.stages.StackUtils") as stack_mock:
            with patch(
                "genie.libs.clean.stages.iosxe.cat9k.stages.Dialog") as dialog_mock:
                cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])

        device.sendline.assert_has_calls([
            call('install add file sftp://server/image.bin activate commit')])
        self.assertEqual(Passed, steps.details[0].result)

    def test_iosxe_install_image_skip(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        device = Mock()
        device.chassis_type = 'stack' 
        device.api.get_running_image.return_value = 'sftp://server/image.bin'
        with self.assertRaises(TerminateStepSignal):
            with patch(
            "genie.libs.clean.stages.iosxe.cat9k.stages.StackUtils") as stack_mock:
                with patch(
                "genie.libs.clean.stages.iosxe.cat9k.stages.Dialog.process") as dialog_mock:
                    dialog_mock.side_effect = Exception
                    cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])
        self.assertEqual(Failed, steps.details[0].result)

