from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.pki.configure import configure_trustpoint


class TestConfigureTrustpoint(TestCase):

    def test_configure_trustpoint(self):
        device = Mock()

        configure_trustpoint(
            device=device,
            revoke_check="none",
            tp_name="CTS_Trustpoint",
        )

        self.assertEqual(
            device.configure.mock_calls[0].args,
            (
                [
                    "crypto pki trustpoint CTS_Trustpoint",
                    "revocation-check none",
                ],
            ),
        )

        self.assertEqual(
            device.configure.mock_calls[0].kwargs,
            {
                "error_pattern": [
                    "The command you have entered is available in the IOS.sh",
                    "% Authorization list  does not exist",
                    "is not a valid subject name",
                    "Explicit device name must be specified",
                    "% Enrollment profile test does not exist",
                    "CRYPTO_PKI: There should be atleast one '.' [other than the trailing '.'] in the domain name",
                ]
            },
        )
