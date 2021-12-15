import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.stages import WriteErase
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Write_Erase(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = WriteErase()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    
    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(return_value='[OK]')
        self.device.execute.error_pattern = '.*'

        # Call the method to be tested (clean step inside class)
        self.cls.write_erase(
            steps=steps, device=self.device
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
    
    
    def test_fail_to_write_erase(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        
        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(return_value='[No]')
        self.device.execute.error_pattern = '.*'

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.write_erase(
                steps=steps, device=self.device
            )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)

