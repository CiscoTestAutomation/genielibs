import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_ip_name_server_vrf


class TestConfigureIpNameServerVrf(unittest.TestCase):

    def test_configure_ip_name_server_vrf(self):
        device = Mock()

        result = configure_ip_name_server_vrf(device, 'test1', '10.168.0.55')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('ip name-server vrf test1 10.168.0.55',)
        )