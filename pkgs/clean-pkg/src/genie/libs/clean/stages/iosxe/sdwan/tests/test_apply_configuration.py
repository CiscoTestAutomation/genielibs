import logging
import unittest

from unittest.mock import Mock, MagicMock, patch
from collections import OrderedDict

from genie.libs.clean.stages.iosxe.sdwan.stages import ApplyConfiguration
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.parameters import ParameterDict

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal, AEtestPassedSignal


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Applyconfiguration(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = ApplyConfiguration()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='sdwan')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the configure method to be mocked.
        # This simulates the pass case.
        self.device.configure = Mock()
        
        # Call the method to be tested (clean step inside class)
        with self.assertRaises(AEtestPassedSignal):
            self.cls.apply_configuration(
                steps=steps, device=self.device, config_stable_time=0
            )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
    
    
    def test_fail_to_apply_configuration(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        configuration = '''
            configuration: |
            interface ethernet2/1
            no shutdown
        '''

        # And we want the configure method to be mocked.
        # This simulates the fail case.
        self.device.configure = Mock(side_effect=Exception)
        
        # Call the method to be tested (clean step inside class)
        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.apply_configuration(
                steps=steps, device=self.device, config_stable_time=2,\
                configuration=configuration, file="test.cfg"
            )
        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)
    
