from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_auto_fallback
from unittest.mock import Mock


class TestConfigureMacroAutoFallback(TestCase):

    def test_configure_macro_auto_fallback(self):
        self.device = Mock()
        result = configure_macro_auto_fallback(self.device, 'fallback', 'cdp')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['macro auto global processing fallback cdp'],)
        )
