import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    unconfigure_ptp_announce_transmit
)


class TestUnconfigurePtpAnnounceTransmit(unittest.TestCase):

    def test_unconfigure_ptp_announce_transmit(self):
        device = Mock()

        result = unconfigure_ptp_announce_transmit(
            device,
            'HundredGigE1/0/48'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface HundredGigE1/0/48',
              'no ptp announce transmit'],)
        )