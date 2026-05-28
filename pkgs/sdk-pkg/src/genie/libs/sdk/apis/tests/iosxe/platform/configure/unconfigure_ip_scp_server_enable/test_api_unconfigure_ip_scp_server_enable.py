import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_ip_scp_server_enable


class TestUnconfigureIpScpServerEnable(unittest.TestCase):

    def test_unconfigure_ip_scp_server_enable(self):
        device = Mock()

        result = unconfigure_ip_scp_server_enable(device)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no ip scp server enable',)
        )