import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    configure_ptp_modes
)


class TestConfigurePtpModes(unittest.TestCase):

    def test_configure_ptp_modes(self):
        device = Mock()

        result = configure_ptp_modes(
            device,
            'g8275bc',
            'tenGigabitEthernet 1/0/1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ptp profile 8275.1 clock-mode boundary',
              'interface tenGigabitEthernet 1/0/1',
              'ptp destination-mac non-forwardable'],)
        )