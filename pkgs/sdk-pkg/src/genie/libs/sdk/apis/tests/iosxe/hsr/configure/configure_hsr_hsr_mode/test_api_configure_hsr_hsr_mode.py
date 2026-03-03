from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hsr.configure import configure_hsr_hsr_mode
from unittest.mock import Mock


class TestConfigureHsrHsrMode(TestCase):

    def test_configure_hsr_hsr_mode(self):
        self.device = Mock()
        result = configure_hsr_hsr_mode(self.device, 'copper', 'yes')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('hsr-hsr-mode enable pair copper',)
        )
