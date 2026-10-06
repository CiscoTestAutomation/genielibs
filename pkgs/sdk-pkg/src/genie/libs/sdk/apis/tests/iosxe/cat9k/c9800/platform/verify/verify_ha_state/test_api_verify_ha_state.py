import unittest
from unittest.mock import Mock, call, patch

from genie.conf.base import Device
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import (
    verify_ha_state,
)


SHOW_REDUNDANCY_STANDBY_HOT = '''my state = 13 -ACTIVE
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
Gateway monitoring interval  = 8 secs
'''

SHOW_REDUNDANCY_WITHOUT_PEER = '''my state = 13 -ACTIVE
           Mode = Duplex
           Unit = Primary
        Unit ID = 2

Redundancy Mode (Operational) = sso
Redundancy Mode (Configured)  = sso
Redundancy State              = sso
     Maintenance Mode = Disabled
        Manual Swact = enabled
     Communications = Up
'''

SHOW_CHASSIS_READY = '''Chassis/Stack Mac Address : 000c.295f.6203 - Local Mac Address
Mac persistency wait time: Indefinite
                                             H/W   Current
Chassis#   Role    Mac Address     Priority Version  State                 IP
-------------------------------------------------------------------------------------
 1       Standby  0050.568d.bf37     1      V02     Ready                169.254.62.83
*2       Active   000c.295f.6203     2      V02     Ready                169.254.62.82
'''

SHOW_CHASSIS_ACTIVE_ONLY = '''Chassis/Stack Mac Address : 000c.295f.6203 - Local Mac Address
Mac persistency wait time: Indefinite
                                             H/W   Current
Chassis#   Role    Mac Address     Priority Version  State                 IP
-------------------------------------------------------------------------------------
*2       Active   000c.295f.6203     2      V02     Ready                169.254.62.82
'''


class OneAttemptTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations == 1

    def sleep(self):
        return None


class TestVerifyHaState(unittest.TestCase):

    def setUp(self):
        self.device = Device(
            'WLC1', os='iosxe', platform='cat9k', model='c9800')
        self.device.is_connected = Mock(return_value=True)
        self.device.cli = self.device

    def set_outputs(self, outputs):
        self.device.execute = Mock(
            side_effect=lambda command: outputs[command])

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_ha_state(self):
        self.set_outputs({
            'show redundancy states': SHOW_REDUNDANCY_STANDBY_HOT,
            'show chassis': SHOW_CHASSIS_READY,
        })

        result = verify_ha_state(self.device)

        self.assertTrue(result)
        self.device.execute.assert_has_calls([
            call('show redundancy states'),
            call('show chassis'),
        ])

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_ha_state_redundancy_not_ready(self):
        self.set_outputs({
            'show redundancy states': SHOW_REDUNDANCY_WITHOUT_PEER,
        })

        result = verify_ha_state(self.device)

        self.assertFalse(result)
        self.device.execute.assert_called_once_with('show redundancy states')

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_ha_state_chassis_not_ready(self):
        self.set_outputs({
            'show redundancy states': SHOW_REDUNDANCY_STANDBY_HOT,
            'show chassis': SHOW_CHASSIS_ACTIVE_ONLY,
        })

        result = verify_ha_state(self.device)

        self.assertFalse(result)
