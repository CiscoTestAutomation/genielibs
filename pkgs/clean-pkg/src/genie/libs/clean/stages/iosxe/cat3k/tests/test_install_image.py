import logging
import unittest
from unittest.mock import Mock, MagicMock, call, ANY
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.cat3k.stages import InstallImage
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device


from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)

class Deactivate_manual_boot(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe',  platform='cat3k')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # This simulates the pass case.
        self.cls.deactivate_manual_boot(steps=steps, device=self.device)
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_delete_boot_variables(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the configure method to raise an exception when called.
        # This simulates the device rejecting a config.
        self.device.configure = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.deactivate_manual_boot(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
class Installimage(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = InstallImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='cat3k')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        images = ['/auto/some-location/that-this/image/stay-isr-image.bin']
        self.cls.new_boot_var = 'flash:cat9k_iosxe.BLD_V173_999.SSA.bin'
        self.cls.history = OrderedDict()
        self.cls.mock_value = OrderedDict()
        setattr(self.cls.mock_value, 'parameters', {})
        self.cls.history.update({'InstallImage': self.cls.mock_value})
        self.cls.history['InstallImage'].parameters =  OrderedDict()

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.reload = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.install_image(
            steps=steps, device=self.device, images=images
        )
        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_install_image(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        images = ['/auto/some-location/that-this/image/stay-isr-image.bin']
        self.cls.history = {}

        # And we want the verify_boot_variable api to be mocked.
        # This simulates the fail case.
        self.device.execute = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.install_image(
                steps=steps, device=self.device, images=images
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
class TestInstallImage(unittest.TestCase):

    def test_iosxe_install_image(self):
        steps = Steps()
        cls = InstallImage()
        cls.history = MagicMock()
        cls.new_boot_var = 'image.bin'

        device = Mock()
        device.reload = Mock()

        cls.install_image(steps=steps, device=device, images=['sftp://server/image.bin'])
        device.reload.assert_has_calls([
            call('install add file sftp://server/image.bin activate commit', reply=ANY, timeout=500, append_error_pattern=['FAILED:.* '])])

        self.assertEqual(Passed, steps.details[0].result)