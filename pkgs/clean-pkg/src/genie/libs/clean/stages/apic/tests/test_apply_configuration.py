import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.apic.stages import ApplyConfiguration
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.eal.dialogs import Statement, Dialog

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Apply_Configuration(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ApplyConfiguration()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='apic')
        self.device.rest = Mock()

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the connect method to be mocked.
        # This simulates the pass case.
        self.device.connect = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.apply_configuration(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_apply_configuration(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the connect method to raise an exception when called.
        # This simulates the device rejecting a config.
        self.device.connect = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.apply_configuration(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

