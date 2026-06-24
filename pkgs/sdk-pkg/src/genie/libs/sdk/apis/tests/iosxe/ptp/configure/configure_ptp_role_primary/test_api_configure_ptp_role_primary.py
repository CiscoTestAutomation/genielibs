import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ptp.configure import (
    configure_ptp_role_primary
)


class TestConfigurePtpRolePrimary(unittest.TestCase):

    def test_configure_ptp_role_primary(self):
        device = Mock()

        result = configure_ptp_role_primary(
            device,
            ['te1/0/33']
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface te1/0/33',
              'ptp role primary'],)
        )