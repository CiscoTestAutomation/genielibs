from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_crypto_mib_ipsec_flowmib_history_failure_size


class TestConfigureCryptoMibIpsecFlowmibHistoryFailureSize(TestCase):

    def test_configure_crypto_mib_ipsec_flowmib_history_failure_size(self):
        self.device = Mock()
        size = '256'
        configure_crypto_mib_ipsec_flowmib_history_failure_size(self.device, size=size)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto mib ipsec flowmib history failure size 256'],)
        )
