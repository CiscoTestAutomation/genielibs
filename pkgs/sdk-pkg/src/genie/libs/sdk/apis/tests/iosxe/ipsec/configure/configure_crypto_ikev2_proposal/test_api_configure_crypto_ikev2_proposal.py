from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_crypto_ikev2_proposal
from unittest.mock import Mock


class TestConfigureCryptoIkev2Proposal(TestCase):

    def test_configure_crypto_ikev2_proposal(self):
        self.device = Mock()
        result = configure_crypto_ikev2_proposal(self.device, 'pqc-no-optional', 'aes-cbc-256', 'sha512 sha384', '19 14 21', None, 'mlkem768 mlkem1024')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['crypto ikev2 proposal pqc-no-optional', 'encryption aes-cbc-256', 'integrity sha512 sha384', 'group 19 14 21', 'pqc mlkem768 mlkem1024'],)
        )
