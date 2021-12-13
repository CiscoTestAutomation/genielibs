import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.stages import PingServer
from genie.libs.clean.stages.tests.utils import CommonStageTests, create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed, Skipped
from pyats.aetest.signals import TerminateStepSignal
from unicon.core.errors import SubCommandFailure


# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class Pingserver(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = PingServer()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()        
        data = '''
            Success rate is 80 percent (4/5)
            5 packets transmitted, 5 packets received, 0.00% packet loss
        '''
        
        # And we want the ping method to be mocked
        # To simulate pass case
        self.device.ping = Mock(return_value=data)

        # Call the method to be tested (clean step inside class)
        self.cls.ping_server(
            steps=steps, device=self.device, server='server-1'
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)


    def test_fail_to_ping(self):
       # Make sure we have a unique Steps() object for result verification
        steps = Steps()

        # And we want the ping method to be mocked
        # To simulate fail case
        self.device.ping = Mock(side_effect=SubCommandFailure)

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.ping_server(
                steps=steps, device=self.device, server='server-1', timeout=2, 
                interval=1, max_attempts=1
             )

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)


    def test_fail_minimum_success_rate(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = '''
            Success rate is 80 percent (4/5)
            5 packets transmitted, 3 packets received, 0.00% packet loss
        '''
        
        # And we want the ping method to be mocked
        self.device.ping = Mock(return_value=data)

        # Call the method to be tested (clean step inside class)
        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.ping_server(
                steps=steps, device=self.device, server='server-1', timeout=2,
                min_success_rate=100, interval=1, 
                max_attempts=1
            )

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)

