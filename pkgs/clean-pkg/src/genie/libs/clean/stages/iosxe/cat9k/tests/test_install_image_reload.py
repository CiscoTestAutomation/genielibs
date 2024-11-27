import logging
import unittest

from unittest.mock import Mock, MagicMock, call, patch

from genie.libs.clean.stages.iosxe.cat9k.stages import InstallImage

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

logging.disable(logging.CRITICAL)

class TestInstallImage(unittest.TestCase):

    def test_iosxe_install_image_reload_pass(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.chassis_type = 'stack' 
        device.reload = Mock()

        with patch(
            "genie.libs.clean.stages.iosxe.cat9k.stages.StackUtils") as stack_mock:
            with patch(
                "genie.libs.clean.stages.iosxe.cat9k.stages.Dialog") as dialog_mock:
                cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])

        device.reload([
            call('install add file sftp://server/image.bin activate commit')])
        self.assertEqual(Passed, steps.details[0].result)

    def test_iosxe_install_image_reload_fail(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = {}

        device = Mock()
        device.chassis_type = 'stack' 
        device.reload = Mock(side_effect=Exception)

        with self.assertRaises(TerminateStepSignal):
            with patch(
            "genie.libs.clean.stages.iosxe.cat9k.stages.StackUtils") as stack_mock:
                with patch(
                "genie.libs.clean.stages.iosxe.cat9k.stages.Dialog.process") as dialog_mock:
                    dialog_mock.side_effect = Exception
                    cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])
                    
        self.assertEqual(Failed, steps.details[0].result)