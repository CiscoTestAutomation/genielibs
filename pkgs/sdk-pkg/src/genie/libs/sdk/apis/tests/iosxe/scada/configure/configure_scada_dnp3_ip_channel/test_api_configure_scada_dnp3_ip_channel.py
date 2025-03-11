from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_dnp3_ip_channel
from unittest.mock import Mock


class TestConfigureScadaDnp3IpChannel(TestCase):

    def test_configure_scada_dnp3_ip_channel(self):
        self.device = Mock()
        result = configure_scada_dnp3_ip_channel(self.device, 'dnp3_ip_channel_1', 13, 8001, 'any')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol dnp3-ip', 'channel dnp3_ip_channel_1', 'link-addr dest 13', 'tcp-connection local-port 8001            remote-ip any'],)
        )
