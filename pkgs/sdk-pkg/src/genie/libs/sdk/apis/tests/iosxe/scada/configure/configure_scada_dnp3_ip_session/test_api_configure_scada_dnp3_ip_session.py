from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_dnp3_ip_session
from unittest.mock import Mock


class TestConfigureScadaDnp3IpSession(TestCase):

    def test_configure_scada_dnp3_ip_session(self):
        self.device = Mock()
        result = configure_scada_dnp3_ip_session(self.device, 'dnp3_ip_session_1', 'dnp3_ip_channel_1', 7, 'dnp3_serial_session_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol dnp3-ip', 'session dnp3_ip_session_1', 'attach-to-channel dnp3_ip_channel_1', 'link-addr source 7', 'map-to-session dnp3_serial_session_1'],)
        )
