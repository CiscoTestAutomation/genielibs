import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    configure_ptp_priority
)


class TestConfigurePtpPriority(unittest.TestCase):

    def test_configure_ptp_priority(self):
        device = Mock()

        result = configure_ptp_priority(
            device,
            20,
            128
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ptp priority1 20',
              'ptp priority2 128'],)
        )

    def test_configure_ptp_priority_1(self):
        device = Mock()

        result = configure_ptp_priority(
            device,
            29,
            None
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ptp priority1 29'],)
        )

    def test_configure_ptp_priority_2(self):
        device = Mock()

        result = configure_ptp_priority(
            device,
            None,
            98
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['ptp priority2 98'],)
        )