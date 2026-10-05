import unittest
from unittest.mock import Mock, patch

from genie.conf.base import Device
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import (
    verify_unused_channel,
)


SHOW_CHANNELS = '''Leader Automatic Channel Assignment
Channel Assignment Mode                    : AUTO
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
  Unused Channel List                      : {unused_channels}
'''


class OneAttemptTimeout:
    def __init__(self, max_time, interval_time):
        self.iterations = 0

    def iterate(self):
        self.iterations += 1
        return self.iterations == 1

    def sleep(self):
        return None


class TestVerifyUnusedChannel(unittest.TestCase):

    def setUp(self):
        self.device = Device(
            'WLC1', os='iosxe', platform='cat9k', model='c9800')
        self.device.is_connected = Mock(return_value=True)
        self.device.cli = self.device

    def set_unused_channels(self, channels):
        output = SHOW_CHANNELS.format(unused_channels=','.join(channels))
        self.device.execute = Mock(
            side_effect=lambda command: {
                'show ap dot11 5ghz channel': output,
            }[command])

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_unused_channel(self):
        expected = [
            '52', '56', '60', '64', '100', '104', '108', '112', '116',
            '120', '124', '128', '132', '136', '140', '144',
        ]
        self.set_unused_channels(expected)

        self.assertTrue(verify_unused_channel(self.device, expected))
        self.device.execute.assert_called_once_with(
            'show ap dot11 5ghz channel')

    @patch(
        'genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify.Timeout',
        OneAttemptTimeout,
    )
    def test_verify_unused_channel_missing_channels(self):
        self.set_unused_channels([
            '52', '56', '60', '64', '116', '120', '124', '128', '132',
            '136', '140', '144',
        ])

        self.assertFalse(verify_unused_channel(
            self.device, ['100', '104', '108', '112']))
