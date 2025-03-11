from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import unconfigure_scada_t104_ip_channel
from unittest.mock import Mock


class TestUnconfigureScadaT104IpChannel(TestCase):

    def test_unconfigure_scada_t104_ip_channel(self):
        self.device = Mock()
        result = unconfigure_scada_t104_ip_channel(self.device, 't104_ip_channel_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t104', 'no channel t104_ip_channel_1'],)
        )
