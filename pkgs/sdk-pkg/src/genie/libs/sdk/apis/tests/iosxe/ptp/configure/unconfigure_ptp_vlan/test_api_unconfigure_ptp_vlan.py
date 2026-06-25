import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    unconfigure_ptp_vlan
)


class TestUnconfigurePtpVlan(unittest.TestCase):

    def test_unconfigure_ptp_vlan(self):
        device = Mock()

        result = unconfigure_ptp_vlan(
            device,
            'tenGigabitEthernet 1/0/1',
            '10'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface tenGigabitEthernet 1/0/1',
              'no ptp vlan 10'],)
        )