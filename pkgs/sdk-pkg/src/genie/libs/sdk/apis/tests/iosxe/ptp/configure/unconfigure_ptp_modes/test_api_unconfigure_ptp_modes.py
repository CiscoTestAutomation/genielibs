import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    unconfigure_ptp_modes
)


class TestUnconfigurePtpModes(unittest.TestCase):

    def test_unconfigure_ptp_modes(self):
        device = Mock()

        result = unconfigure_ptp_modes(
            device,
            'bcdelay'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['no ptp mode boundary delay-req'],)
        )