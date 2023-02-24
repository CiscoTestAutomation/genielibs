import logging
import unittest

from unittest.mock import Mock
from genie.libs.clean.stages.linux.wsim.stages import VerifyApRunState
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from unicon.core.errors import SubCommandFailure


class TestRunConfigure(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = VerifyApRunState()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('Wsim1', os='linux', platform='wsim')

    def test_pass_verify_ap_run_state(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the configure apis to be mocked.
        # This simulates the pass case.
        data = {'show ap status | grep APs:': '1 APs: 1 Run'}
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        self.cls.verify_ap_run_state(steps=steps, device=self.device, ap_count='1',max_time=30)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_verify_ap_run_state(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the configure apis to be mocked.
        # This simulates the pass case.
        data = {'show ap status | grep APs:': '1 APs: 0 Run'}
        self.device.execute = Mock(side_effect=lambda x: data[x])
        #self.device.api.verify_ap_associate = Mock(side_effect=SubCommandFailure)
        

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_ap_run_state(steps=steps, device=self.device,ap_count='1',max_time=3)

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)

        
