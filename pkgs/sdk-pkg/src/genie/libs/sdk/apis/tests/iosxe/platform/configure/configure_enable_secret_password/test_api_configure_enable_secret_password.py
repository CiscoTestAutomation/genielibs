from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_enable_secret_password


class TestConfigureEnableSecretPassword(TestCase):

    def test_configure_enable_secret_password(self):
        device = Mock()
        result = configure_enable_secret_password(
            device,
            'cisco@123',
            5
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['enable secret level 5 cisco@123'],)
        )