import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.iosxe.c9800.stages import VerifyHaState
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class TestVerifyHaState(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = VerifyHaState()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('vidya-ewlc', os='iosxe', platform='c9800')

    def test_pass_verify_show_redundancy_states(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data= {'show redundancy states':'''my state = 13 -ACTIVE
                                        peer state = 8  -STANDBY HOT
                                                   Mode = Duplex
                                                   Unit = Primary
                                                Unit ID = 2

                                        Redundancy Mode (Operational) = sso
                                        Redundancy Mode (Configured)  = sso
                                        Redundancy State              = sso
                                             Maintenance Mode = Disabled
                                            Manual Swact = enabled
                                         Communications = Up

                                           client count = 128
                                         client_notification_TMR = 30000 milliseconds
                                                   RF debug mask = 0x0
                                        Gateway Monitoring = Enabled
                                        Gateway monitoring interval  = 8 secs'''}

        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        self.cls.verify_show_redundancy_states(device=self.device, steps=steps)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_pass_verify_show_chassis(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data= {'show chassis':'''Chassis/Stack Mac Address : 000c.295f.6203 - Local Mac Address
                                Mac persistency wait time: Indefinite
                                                                             H/W   Current
                                Chassis#   Role    Mac Address     Priority Version  State                 IP
                                -------------------------------------------------------------------------------------
                                 1       Standby  0050.568d.bf37     1      V02     Ready                169.254.62.83
                                *2       Active   000c.295f.6203     2      V02     Ready                169.254.62.82 '''}

        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        self.cls.verify_show_chassis(device=self.device, steps=steps)

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_verify_show_redundancy_states(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data= {'show redundancy states':'''my state = 13 -ACTIVE
                                                   Mode = Duplex
                                                   Unit = Primary
                                                Unit ID = 2

                                        Redundancy Mode (Operational) = sso
                                        Redundancy Mode (Configured)  = sso
                                        Redundancy State              = sso
                                             Maintenance Mode = Disabled
                                            Manual Swact = enabled
                                         Communications = Up

                                           client count = 128
                                         client_notification_TMR = 30000 milliseconds
                                                   RF debug mask = 0x0
                                        Gateway Monitoring = Enabled
                                        Gateway monitoring interval  = 8 secs'''}

        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_show_redundancy_states(device=self.device, steps=steps, timeout=5, interval=1)

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)

    def test_fail_verify_show_chassis(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data= {'show chassis':'''Chassis/Stack Mac Address : 000c.295f.6203 - Local Mac Address
                                Mac persistency wait time: Indefinite
                                                                             H/W   Current
                                Chassis#   Role    Mac Address     Priority Version  State                 IP
                                -------------------------------------------------------------------------------------
                                *2       Active   000c.295f.6203     2      V02     Ready                169.254.62.82 '''}

        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_show_chassis(device=self.device, steps=steps,timeout=5, interval=1)

        # Check that the result is expected
        self.assertEqual(Failed, steps.details[0].result)