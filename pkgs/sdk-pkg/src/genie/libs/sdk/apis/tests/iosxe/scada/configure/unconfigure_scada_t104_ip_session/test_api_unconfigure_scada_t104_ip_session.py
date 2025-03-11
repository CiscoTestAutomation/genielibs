from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import unconfigure_scada_t104_ip_session
from unittest.mock import Mock


class TestUnconfigureScadaT104IpSession(TestCase):

    def test_unconfigure_scada_t104_ip_session(self):
        self.device = Mock()
        result = unconfigure_scada_t104_ip_session(self.device, 't104_ip_session_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t104', 'no session t104_ip_session_1'],)
        )
