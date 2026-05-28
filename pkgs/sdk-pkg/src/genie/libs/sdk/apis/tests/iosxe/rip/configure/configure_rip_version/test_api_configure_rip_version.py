from unittest import TestCase
from genie.libs.sdk.apis.iosxe.rip.configure import configure_rip_version
from unittest.mock import Mock


class TestConfigureRipVersion(TestCase):

    def test_configure_rip_version(self):
        self.device = Mock()
        result = configure_rip_version(self.device, 2)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router rip', 'version 2'],)
        )
