from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ike.configure import configure_crypto_isakmp_enable
from unicon.core.errors import SubCommandFailure


class TestConfigureCryptoIsakmpEnable(TestCase):

    def test_configure_crypto_isakmp_enable(self):
        self.device = Mock()
        configure_crypto_isakmp_enable(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('crypto isakmp enable',)
        )

    def test_configure_crypto_isakmp_enable_failure(self):
        self.device = Mock()
        self.device.name = "Device1"
        self.device.configure.side_effect = SubCommandFailure("configuration error")
        with self.assertRaises(SubCommandFailure):
            configure_crypto_isakmp_enable(self.device)
