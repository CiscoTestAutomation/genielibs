from unittest import TestCase
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server_with_dtls_ipv6
from unittest.mock import Mock


class TestConfigureRadiusServerWithDtlsIpv6(TestCase):

    def test_configure_radius_server_with_dtls_ipv6(self):
        self.device = Mock()
        result = configure_radius_server_with_dtls_ipv6(self.device, 'TMP_NAME', 'vlan 199')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['radius server TMP_NAME', 'dtls ipv6 radius source-interface vlan 199'],)
        )
