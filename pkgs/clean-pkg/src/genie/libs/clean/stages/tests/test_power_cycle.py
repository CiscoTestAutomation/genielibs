import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.stages import PowerCycle
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Powercycle(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = PowerCycle()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_power_cycle_device api to be mocked with device console output.
        # To simulate pass case
        self.device.api.execute_power_cycle_device = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.powercycle(
            steps=steps, device=self.device, sleep_after_power_off=0
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_do_powercycle(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_power_cycle_device api to raise an exception when called.
        # To simulate fail case
        self.device.api.execute_power_cycle_device = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.powercycle(
                steps=steps, device=self.device, sleep_after_power_off=0
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class Reconnect(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = PowerCycle()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the connect method to be mocked with device console output.
        # To simulate pass case
        self.device.connect = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.reconnect(
            steps=steps, device=self.device, boot_timeout=5
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_reconnect(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the connect method to raise an exception when called.
        # To simulate fail case
        self.device.connect = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.reconnect(
                steps=steps, device=self.device, boot_timeout=5
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

