from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import unconfigure_scada_dnp3_ip_channel
from unittest.mock import Mock


class TestUnconfigureScadaDnp3IpChannel(TestCase):

    def test_unconfigure_scada_dnp3_ip_channel(self):
        self.device = Mock()
        result = unconfigure_scada_dnp3_ip_channel(self.device, 'dnp3_ip_channel_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol dnp3-ip', 'no channel dnp3_ip_channel_1'],)
        )
