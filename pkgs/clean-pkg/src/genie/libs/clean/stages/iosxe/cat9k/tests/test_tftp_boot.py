import logging
import unittest

from unittest.mock import Mock, MagicMock

from genie.libs.clean.stages.iosxe.cat9k.stages import TftpBoot
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.eal.dialogs import Statement, Dialog

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Tftpboot(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = TftpBoot()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='cat9k')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_no_boot_variable api to be mocked.
        # This simulates the pass case.
        self.device.api.execute_no_boot_variable = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.delete_boot_variables(
            steps=steps, device=self.device, timeout=0
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_tftp_boot(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_no_boot_variable api to be mocked to raise an 
        # exception when called. This simulates the fail case.
        self.device.api.execute_no_boot_variable = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.delete_boot_variables(
                steps=steps, device=self.device, timeout=0
        )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

