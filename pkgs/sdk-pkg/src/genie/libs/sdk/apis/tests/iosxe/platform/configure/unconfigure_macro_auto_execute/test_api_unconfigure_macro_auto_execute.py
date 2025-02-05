from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_macro_auto_execute
from unittest.mock import Mock


class TestUnconfigureMacroAutoExecute(TestCase):

    def test_unconfigure_macro_auto_execute(self):
        self.device = Mock()
        result = unconfigure_macro_auto_execute(self.device, 'test_trigger')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no macro auto execute test_trigger'],)
        )
