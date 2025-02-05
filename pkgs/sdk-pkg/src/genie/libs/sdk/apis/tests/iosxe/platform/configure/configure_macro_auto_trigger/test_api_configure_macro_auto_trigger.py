from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_auto_trigger
from unittest.mock import Mock


class TestConfigureMacroAutoTrigger(TestCase):

    def test_configure_macro_auto_trigger(self):
        self.device = Mock()
        result = configure_macro_auto_trigger(self.device, 'test_trigger', 'phone', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['macro auto trigger test_trigger', 'device phone'],)
        )
