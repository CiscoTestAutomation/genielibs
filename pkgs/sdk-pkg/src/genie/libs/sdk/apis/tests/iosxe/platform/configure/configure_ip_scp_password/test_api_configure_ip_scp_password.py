import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_scp_password


class TestConfigureIpScpPassword(unittest.TestCase):

    def test_configure_ip_scp_password(self):
        device = Mock()

        result = configure_ip_scp_password(device, 'cisco')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip scp password cisco',)
        )