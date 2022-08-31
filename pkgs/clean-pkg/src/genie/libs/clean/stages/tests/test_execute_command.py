import logging
from socket import timeout
import unittest

from unittest.mock import Mock, call

from genie.libs.clean.stages.stages import ExecuteCommand
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Executecommand(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ExecuteCommand()
        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')
        self.commands=['show version', 'show boot']

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        self.device.execute = Mock()
        # To simulate pass case
        # Call the method to be tested (clean step inside class)
        self.cls.execute_command(
            steps=steps, device=self.device, commands=self.commands, sleep_time=0
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        
        calls = [call('show boot', timeout=60), call('show version', timeout=60), ]
        self.device.execute.assert_has_calls(calls, any_order=True)

    def test_fail_to_execute_command(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # To simulate fail case
        self.device.execute = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.execute_command(
                steps=steps, device=self.device, commands=self.commands, sleep_time=0
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)