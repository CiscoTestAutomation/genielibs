import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_ip_scp_password


class TestUnconfigureIpScpPassword(unittest.TestCase):

    def test_unconfigure_ip_scp_password(self):
        device = Mock()

        result = unconfigure_ip_scp_password(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip scp password',)
        )