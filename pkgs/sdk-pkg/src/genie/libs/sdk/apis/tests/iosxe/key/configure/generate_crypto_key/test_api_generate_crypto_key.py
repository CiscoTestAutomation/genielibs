import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.key.configure import generate_crypto_key


class TestGenerateCryptoKey(TestCase):

    def assert_generate_crypto_key(
        self,
        key_type,
        key_label,
        modulus,
        key_size,
        exportable,
        expected_command,
    ):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = generate_crypto_key(
            device,
            key_type,
            key_label,
            modulus,
            key_size,
            exportable,
            30,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_command = device.configure.call_args.args[0]
        self.assertIsInstance(sent_command, str)
        self.assertEqual(sent_command, expected_command)

        sent_kwargs = device.configure.call_args.kwargs
        self.assertIn("reply", sent_kwargs)
        self.assertEqual(
            sent_kwargs["error_pattern"],
            ["% Please define a domain-name first."],
        )
        self.assertEqual(sent_kwargs["timeout"], 30)

    def test_generate_crypto_key(self):
        self.assert_generate_crypto_key(
            key_type="ec",
            key_label="ECKEYS",
            modulus=None,
            key_size="521",
            exportable=True,
            expected_command=(
                "crypto key generate ec keysize 521 "
                "exportable label ECKEYS"
            ),
        )

    def test_generate_crypto_key_1(self):
        self.assert_generate_crypto_key(
            key_type="ec",
            key_label="ECKEYS",
            modulus=None,
            key_size="256",
            exportable=False,
            expected_command=(
                "crypto key generate ec keysize 256 label ECKEYS"
            ),
        )

    def test_generate_crypto_key_2(self):
        self.assert_generate_crypto_key(
            key_type="ec",
            key_label=None,
            modulus=None,
            key_size="384",
            exportable=True,
            expected_command=(
                "crypto key generate ec keysize 384 exportable"
            ),
        )

    def test_generate_crypto_key_3(self):
        self.assert_generate_crypto_key(
            key_type="ec",
            key_label=None,
            modulus=None,
            key_size="521",
            exportable=False,
            expected_command="crypto key generate ec keysize 521",
        )

    def test_generate_crypto_key_4(self):
        self.assert_generate_crypto_key(
            key_type="rsa",
            key_label="RSAKEYS",
            modulus="4096",
            key_size=None,
            exportable=True,
            expected_command=(
                "crypto key generate rsa label RSAKEYS "
                "modulus 4096 exportable"
            ),
        )

    def test_generate_crypto_key_5(self):
        self.assert_generate_crypto_key(
            key_type="rsa",
            key_label=None,
            modulus="4096",
            key_size=None,
            exportable=True,
            expected_command=(
                "crypto key generate rsa modulus 4096 exportable"
            ),
        )

    def test_generate_crypto_key_6(self):
        self.assert_generate_crypto_key(
            key_type="rsa",
            key_label=None,
            modulus=None,
            key_size=None,
            exportable=True,
            expected_command="crypto key generate rsa exportable",
        )

    def test_generate_crypto_key_7(self):
        self.assert_generate_crypto_key(
            key_type="rsa",
            key_label="RSAKEYS",
            modulus=None,
            key_size=None,
            exportable=True,
            expected_command=(
                "crypto key generate rsa label RSAKEYS exportable"
            ),
        )

    def test_generate_crypto_key_8(self):
        self.assert_generate_crypto_key(
            key_type="rsa",
            key_label=None,
            modulus="4096",
            key_size=None,
            exportable=False,
            expected_command="crypto key generate rsa modulus 4096",
        )

    def test_generate_crypto_key_9(self):
        self.assert_generate_crypto_key(
            key_type="rsa",
            key_label=None,
            modulus=None,
            key_size=None,
            exportable=False,
            expected_command="crypto key generate rsa",
        )

    def test_generate_crypto_key_10(self):
        self.assert_generate_crypto_key(
            key_type="rsa",
            key_label="RSAKEYS",
            modulus=None,
            key_size=None,
            exportable=False,
            expected_command="crypto key generate rsa label RSAKEYS",
        )

    def test_generate_crypto_key_11(self):
        self.assert_generate_crypto_key(
            key_type="rsa",
            key_label="RSAKEYS",
            modulus="4096",
            key_size=None,
            exportable=False,
            expected_command=(
                "crypto key generate rsa label RSAKEYS modulus 4096"
            ),
        )


if __name__ == "__main__":
    unittest.main()
