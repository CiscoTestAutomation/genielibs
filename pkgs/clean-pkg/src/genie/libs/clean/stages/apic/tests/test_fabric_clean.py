import logging
import unittest

from unittest.mock import Mock, MagicMock, patch

from genie.libs.clean.stages.apic.stages import FabricClean
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.eal.dialogs import Statement, Dialog


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Fabricclean(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = FabricClean()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='apic')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock()

        # Call the method to be tested (clean step inside class)
        self.cls.fabric_clean(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_to_do_fabric_clean(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to raise an exception when called.
        # This simulates the fail case
        self.device.execute = Mock(side_effect=Exception)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.fabric_clean(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


class Reload(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = FabricClean()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='apic')
        self.device.hostname = 'PE1'

    @patch.object(Dialog, 'process', Mock(return_value=''))
    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.device.sendline = Mock()
        self.device.spawn = MagicMock()

        # And we want the connect method to be mocked.
        # This simulates the pass case
        self.device.connect = Mock()
       
        # Call the method to be tested (clean step inside class)
        self.cls.reload(
            steps=steps, device=self.device, reload_timeout=3, sleep_after_reload=1
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    
    @patch.object(Dialog, 'process', Mock(return_value=''))
    def test_fail_to_do_reload(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        self.device.sendline = Mock()
        self.device.spawn = MagicMock()

        # And we want the connect method to be mocked.
        # This simulates the pass case
        self.device.connect = Mock(side_effect=Exception)
       
        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.reload(
                steps=steps, device=self.device, reload_timeout=3, sleep_after_reload=1
            )

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)

