from unittest import TestCase
from genie.libs.sdk.apis.iosxe.server.configure import configure_radius_server_dtls_ip
from unittest.mock import Mock


class TestConfigureRadiusServerDtlsIp(TestCase):

    def test_configure_radius_server_dtls_ip(self):
        self.device = Mock()
        result = configure_radius_server_dtls_ip(self.device, 'TMP_NAME', 'vlan 199')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['radius server TMP_NAME', 'dtls', 'ip radius source-interface vlan 199', 'exit'],)
        )
