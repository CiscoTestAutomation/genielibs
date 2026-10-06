import unittest
from unittest.mock import Mock, patch

from genie.conf.base import Device
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import (
    verify_assignment_mode,
)


SHOW_CHANNELS = '''Leader Automatic Channel Assignment
Channel Assignment Mode                    : {assignment_mode}
Channel Update Interval                    : 600 seconds
Anchor time (Hour of the day)              : 0
Channel Update Contribution
  Noise                                    : Enable
  Interference                             : Enable
  Load                                     : Disable
  Device Aware                             : Disable
CleanAir Event-driven RRM option           : Disabled
Zero Wait DFS                              : Disabled
Channel Assignment Leader                  : vidya-ewlc-5 (9.4.62.51) (2001:9:4:62::51)
Last Run                                   : 267 seconds ago

DCA Sensitivity Level                      : MEDIUM : 15 dB
DCA 802.11n/ac Channel Width               : best
DBS Max Channel Width                      : 40 MHz
DCA Minimum Energy Limit                   : -95 dBm
Channel Energy Levels
  Minimum                                  : -72 dBm
  Average                                  : 13 dBm
  Maximum                                  : -72 dBm
Channel Dwell Times
  Minimum                                  : 9 days 0 hour 24 minutes 18 seconds
  Average                                  : 21 days 17 hours 21 minutes 42 seconds
  Maximum                                  : 26 days 20 hours 18 minutes 7 seconds
802.11a 5 GHz Auto-RF Channel List
  Allowed Channel List                     : 36,40,44,48,149,153,157,161
  Unused Channel List                      : 52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,144
'''


class OneAttemptTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations == 1

    def sleep(self):
        return None


@patch(
    'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
    OneAttemptTimeout,
)
class TestVerifyAssignmentMode(unittest.TestCase):

    def create_device(self, assignment_mode):
        device = Device(
            'WLC1', os='iosxe', platform='cat9k', model='c9800')
        device.is_connected = Mock(return_value=True)
        device.cli = device
        output = SHOW_CHANNELS.format(assignment_mode=assignment_mode)
        device.execute = Mock(
            side_effect=lambda command: {
                'show ap dot11 5ghz channel': output,
            }[command])
        return device

    def test_verify_assignment_mode(self):
        device = self.create_device('AUTO')

        self.assertTrue(verify_assignment_mode(device, 'AUTO'))
        device.execute.assert_called_once_with('show ap dot11 5ghz channel')

    def test_verify_assignment_mode_mismatch(self):
        device = self.create_device('MANUAL')

        self.assertFalse(verify_assignment_mode(device, 'AUTO'))
