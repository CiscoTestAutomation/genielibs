from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_macro_auto_fallback
from unittest.mock import Mock


class TestUnconfigureMacroAutoFallback(TestCase):

    def test_unconfigure_macro_auto_fallback(self):
        self.device = Mock()
        result = unconfigure_macro_auto_fallback(self.device, 'fallback', 'cdp')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no macro auto global processing fallback cdp'],)
        )
