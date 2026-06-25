import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    configure_no_ptp_enable_on_interface
)


class TestConfigureNoPtpEnableOnInterface(unittest.TestCase):

    def test_configure_no_ptp_enable_on_interface(self):
        device = Mock()

        result = configure_no_ptp_enable_on_interface(
            device,
            'FortyGigabitEthernet1/1/0/9'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface FortyGigabitEthernet1/1/0/9',
              'no ptp enable'],)
        )