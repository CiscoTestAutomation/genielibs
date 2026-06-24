import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    configure_ptp_source
)


class TestConfigurePtpSource(unittest.TestCase):

    def test_configure_ptp_source(self):
        device = Mock()

        result = configure_ptp_source(
            device,
            '18.1.1.1'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ptp transport ipv4 udp', 'ptp mode p2ptransparent', 'ptp source 18.1.1.1'],)
        )