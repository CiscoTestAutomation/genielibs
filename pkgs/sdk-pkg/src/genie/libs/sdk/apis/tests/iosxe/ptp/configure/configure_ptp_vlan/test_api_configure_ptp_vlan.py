import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    configure_ptp_vlan
)


class TestConfigurePtpVlan(unittest.TestCase):

    def test_configure_ptp_vlan(self):
        device = Mock()

        result = configure_ptp_vlan(
            device,
            'GigabitEthernet1/1/0/1',
            '101'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface GigabitEthernet1/1/0/1',
              'ptp vlan 101'],)
        )