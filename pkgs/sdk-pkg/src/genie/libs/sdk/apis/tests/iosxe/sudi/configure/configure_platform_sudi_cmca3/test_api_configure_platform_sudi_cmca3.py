from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sudi.configure import configure_platform_sudi_cmca3


class TestConfigurePlatformSudiCmca3(TestCase):

    def test_configure_platform_sudi_cmca3(self):
        device = Mock()

        result = configure_platform_sudi_cmca3(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('platform sudi cmca3')
