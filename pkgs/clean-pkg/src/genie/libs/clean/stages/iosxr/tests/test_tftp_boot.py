import logging
import unittest

from unittest.mock import Mock, MagicMock

from genie.libs.clean.stages.iosxr.stages import TftpBoot
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.eal.dialogs import Statement, Dialog

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Tftp_Boot(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = TftpBoot()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxr')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the admin_execute method to be mocked.
        # This simulates the pass case.
        self.device.admin_execute = True

        # Call the method to be tested (clean step inside class)
        self.cls.go_to_rommon(
            steps=steps, device=self.device, device_reload_sleep=0
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_tftp_boot(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the admin_execute method to raise an exception when called.
        # This simulates the fail case.
        self.device.admin_execute = Mock()

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.go_to_rommon(
                steps=steps, device=self.device, device_reload_sleep=0
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
        
