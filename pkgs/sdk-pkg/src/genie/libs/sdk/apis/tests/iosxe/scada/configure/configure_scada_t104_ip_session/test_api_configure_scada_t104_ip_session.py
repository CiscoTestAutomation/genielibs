from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_t104_ip_session
from unittest.mock import Mock


class TestConfigureScadaT104IpSession(TestCase):

    def test_configure_scada_t104_ip_session(self):
        self.device = Mock()
        result = configure_scada_t104_ip_session(self.device, 't104_ip_session_1', 't104_ip_channel_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t104', 'session t104_ip_session_1', 'attach-to-channel t104_ip_channel_1'],)
        )
