import logging
import unittest

from unittest.mock import Mock, MagicMock

from genie.libs.clean.stages.apic.stages import NodeRegistration
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.eal.dialogs import Statement, Dialog

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class RegisterNodes(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = NodeRegistration()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='apic')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_register_nodes method to be mocked.
        # This simulates the pass case.
        self.device.api.execute_register_nodes = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.register_nodes(
            steps=steps, device=self.device, nodes=['Spine1', 'Spine2']
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_register_nodes(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute_register_nodes method to raise an exception when called.
        # This simulates the fail case.
        self.device.api.execute_register_nodes = Mock(return_value=None)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.register_nodes(
                steps=steps, device=self.device, nodes=['Spine1', 'Spine2']
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class VerifyNodes(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = NodeRegistration()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = MagicMock('PE1', os='apic')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.device.testbed = MagicMock()
        self.device.testbed.devices = {'Spine1': MagicMock(), 'Spine2': MagicMock()}
        self.device.api = MagicMock()
        self.device.api.verify_aci_registered_nodes_in_state.return_value=True

        # Call the method to be tested (clean step inside class)
        self.cls.verify_nodes(
            steps=steps, device=self.device, nodes=['Spine1', 'Spine2']
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_verify_nodes(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.device.testbed = MagicMock()
        self.device.testbed.devices = {'Spine1': MagicMock(), 'Spine2': MagicMock()}
        self.device.api = MagicMock()

        # And we want the execute method to raise an exception when called.
        # This simulates the fail case.
        self.device.api.verify_aci_registered_nodes_in_state.return_value = {}

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_nodes(
                steps=steps, device=self.device, nodes=['Spine1', 'Spine2']
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

