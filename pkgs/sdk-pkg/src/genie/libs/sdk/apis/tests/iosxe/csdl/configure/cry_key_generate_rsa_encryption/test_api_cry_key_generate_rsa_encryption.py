from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.csdl.configure import cry_key_generate_rsa_encryption


class TestCryKeyGenerateRsaEncryption(TestCase):
    def test_cry_key_generate_rsa_encryption(self):
        device = Mock()
        result = cry_key_generate_rsa_encryption(device, '2048', 'BillRSAkey1')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['cry key generate rsa encryption mod 2048 label BillRSAkey1'],)
        )