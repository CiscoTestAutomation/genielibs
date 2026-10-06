import unittest
from unittest.mock import Mock, patch

from genie.conf.base import Device
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.verify import (
    verify_tx_power,
)


SHOW_AP_DOT11_SUMMARY = '''* global assignment

AP Name              Mac Address     Slot Admin State Oper State Width Txpwr          Channel    Mode
------------------------------------------------------------------------------------------------------
AP002C.C862.E708     002c.c88a.fd20  1    Disabled    Down       40    {tx_power}/8 (20 dBm) (161,157)* Local
AP188B.4500.44C8     188b.4501.7c60  1    Disabled    Down       40    1/8 (22 dBm) (157,161)* Local
AP188B.4500.5EE8     188b.4501.e4e0  1    Disabled    Down       40    *1/8 (23 dBm) (161,157)* Local
APCC16.7EDB.4168     a0e0.af91.9e60  1    Enabled     Up         40    *1/8 (22 dBm) (36,40) Local
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
class TestVerifyTxPower(unittest.TestCase):

    def create_device(self, tx_power):
        device = Device(
            'WLC1', os='iosxe', platform='cat9k', model='c9800')
        device.is_connected = Mock(return_value=True)
        device.cli = device
        output = SHOW_AP_DOT11_SUMMARY.format(tx_power=tx_power)
        device.execute = Mock(
            side_effect=lambda command: {
                'show ap dot11 5ghz summary': output,
            }[command])
        return device

    def test_verify_tx_power(self):
        device = self.create_device('1')

        self.assertTrue(verify_tx_power(device, 'AP002C.C862.E708', '1'))
        device.execute.assert_called_once_with('show ap dot11 5ghz summary')

    def test_verify_tx_power_mismatch(self):
        device = self.create_device('2')

        self.assertFalse(verify_tx_power(device, 'AP002C.C862.E708', '1'))
