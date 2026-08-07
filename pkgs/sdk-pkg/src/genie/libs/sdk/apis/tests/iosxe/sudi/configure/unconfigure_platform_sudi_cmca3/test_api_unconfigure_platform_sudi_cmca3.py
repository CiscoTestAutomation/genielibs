from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.sudi.configure import unconfigure_platform_sudi_cmca3


class TestUnconfigurePlatformSudiCmca3(TestCase):

    def test_unconfigure_platform_sudi_cmca3(self):
        device = Mock()

        result = unconfigure_platform_sudi_cmca3(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no platform sudi cmca3')
