import unittest

from unittest.mock import Mock
from genie.libs.clean.stages.linux.wsim.stages import StartApContainers
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal


class TestStartApContainers(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = StartApContainers()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('Wsim1', os='linux', platform='wsim')

    def test_pass_start_ap_containers(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # Simulate both APIs successfully configuring and starting the APs.
        self.device.api.configure_ap_client_count = Mock()
        self.device.api.simulate_ap_container = Mock(return_value=True)

        # Call the method to be tested (clean step inside class)
        self.cls.start_ap_containers(steps=steps, device=self.device, )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(Passed, steps.details[1].result)
        self.device.api.configure_ap_client_count.assert_called_once_with(
            ap_count='1', client_count='1')
        self.device.api.simulate_ap_container.assert_called_once_with(
            ap_count='1', timeout=600)

    def test_fail_start_ap_containers(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # Simulate configuration succeeding but AP startup failing.
        self.device.api.configure_ap_client_count = Mock()
        self.device.api.simulate_ap_container = Mock(return_value=False)

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.start_ap_containers(steps=steps, device=self.device, )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.assertEqual(Failed, steps.details[1].result)
        self.device.api.configure_ap_client_count.assert_called_once_with(
            ap_count='1', client_count='1')
        self.device.api.simulate_ap_container.assert_called_once_with(
            ap_count='1', timeout=600)
