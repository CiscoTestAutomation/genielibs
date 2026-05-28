import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_scp_server_enable


class TestConfigureIpScpServerEnable(unittest.TestCase):

    def test_configure_ip_scp_server_enable(self):
        device = Mock()

        result = configure_ip_scp_server_enable(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip scp server enable',)
        )