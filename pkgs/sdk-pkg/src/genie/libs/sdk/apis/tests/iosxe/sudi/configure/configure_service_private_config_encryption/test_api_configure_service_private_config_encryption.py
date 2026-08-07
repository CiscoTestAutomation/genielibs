from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sudi.configure import configure_service_private_config_encryption


class TestConfigureServicePrivateConfigEncryption(TestCase):

    def test_configure_service_private_config_encryption(self):
        device = Mock()

        result = configure_service_private_config_encryption(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'service private-config-encryption'
        )
