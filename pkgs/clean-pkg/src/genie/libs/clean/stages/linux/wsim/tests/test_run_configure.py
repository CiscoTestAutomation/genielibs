import logging
import unittest

from unittest.mock import Mock
from genie.libs.clean.stages.linux.wsim.stages import RunConfigure
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.core.errors import SubCommandFailure


class TestRunConfigure(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = RunConfigure()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('Wsim1', os='linux', platform='wsim')

    def test_pass_run_configure(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the configure apis to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.run_configure(steps=steps, device=self.device, )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_run_configure(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # This simulates the Fail case.
        self.device.execute = Mock(side_effect=Exception)

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.run_configure(steps=steps, device=self.device, )

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)
