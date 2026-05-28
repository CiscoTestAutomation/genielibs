from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.system.configure import configure_system_mode_insecure


class TestConfigureSystemModeInsecure(TestCase):

    def test_configure_system_mode_insecure(self):
        self.device = Mock()
        configure_system_mode_insecure(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('system mode insecure',)
        )
