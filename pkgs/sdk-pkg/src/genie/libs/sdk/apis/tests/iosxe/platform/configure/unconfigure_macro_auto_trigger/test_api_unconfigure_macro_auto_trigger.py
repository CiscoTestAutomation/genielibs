from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_macro_auto_trigger
from unittest.mock import Mock


class TestUnconfigureMacroAutoTrigger(TestCase):

    def test_unconfigure_macro_auto_trigger(self):
        self.device = Mock()
        result = unconfigure_macro_auto_trigger(self.device, 'trigger_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no macro auto trigger trigger_1'],)
        )
