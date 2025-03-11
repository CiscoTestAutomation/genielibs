from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_t104_ip_channel
from unittest.mock import Mock


class TestConfigureScadaT104IpChannel(TestCase):

    def test_configure_scada_t104_ip_channel(self):
        self.device = Mock()
        result = configure_scada_t104_ip_channel(self.device, 't104_ip_channel_1', 12, 8, 30, 15, 10, 30, 0, 8002, 'any')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t104', 'channel t104_ip_channel_1', 'k-value 12', 'w-value 8', 't0-timeout 30', 't1-timeout 15', 't2-timeout 10', 't3-timeout 30', 'tcp-connection 0          local-port 8002          remote-ip any'],)
        )
