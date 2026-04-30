from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_crypto_mib_ipsec_flowmib_history_tunnel_size


class TestConfigureCryptoMibIpsecFlowmibHistoryTunnelSize(TestCase):

    def test_configure_crypto_mib_ipsec_flowmib_history_tunnel_size(self):
        self.device = Mock()
        size = '200'
        configure_crypto_mib_ipsec_flowmib_history_tunnel_size(self.device, size=size)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto mib ipsec flowmib history tunnel size 200'],)
        )
