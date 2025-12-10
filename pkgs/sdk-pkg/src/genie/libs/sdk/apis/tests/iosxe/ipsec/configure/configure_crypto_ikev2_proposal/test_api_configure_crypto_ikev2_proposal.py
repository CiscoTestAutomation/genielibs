from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_crypto_ikev2_proposal
from unittest.mock import Mock


class TestConfigureCryptoIkev2Proposal(TestCase):

    def test_configure_crypto_ikev2_proposal(self):
        self.device = Mock()
        result = configure_crypto_ikev2_proposal(self.device, 'my_ikev2_proposal', 'aes-cbc-256', 'sha256', 14, 'sha256')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 proposal my_ikev2_proposal', 'encryption aes-cbc-256', 'integrity sha256', 'prf sha256', 'group 14'],)
        )
