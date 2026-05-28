import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_scp_username


class TestConfigureIpScpUsername(unittest.TestCase):

    def test_configure_ip_scp_username(self):
        device = Mock()

        result = configure_ip_scp_username(device, 'root')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip scp username root',)
        )