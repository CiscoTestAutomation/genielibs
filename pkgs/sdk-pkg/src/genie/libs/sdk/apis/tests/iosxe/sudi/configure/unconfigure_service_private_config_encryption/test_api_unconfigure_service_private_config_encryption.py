from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sudi.configure import unconfigure_service_private_config_encryption


class TestUnconfigureServicePrivateConfigEncryption(TestCase):

    def test_unconfigure_service_private_config_encryption(self):
        device = Mock()

        result = unconfigure_service_private_config_encryption(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            'no service private-config-encryption'
        )
