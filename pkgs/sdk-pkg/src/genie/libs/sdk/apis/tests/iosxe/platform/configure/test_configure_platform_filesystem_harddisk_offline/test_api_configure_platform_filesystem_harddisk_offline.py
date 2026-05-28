from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_platform_filesystem_harddisk_offline


class TestConfigurePlatformFilesystemHarddiskOffline(TestCase):

    def test_configure_platform_filesystem_harddisk_offline(self):
        self.device = Mock()
        configure_platform_filesystem_harddisk_offline(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('request platform hardware filesystem harddisk: offline',)
        )
