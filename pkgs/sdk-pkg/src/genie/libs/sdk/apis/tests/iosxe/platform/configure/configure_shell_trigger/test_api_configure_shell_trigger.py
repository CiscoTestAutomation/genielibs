from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_shell_trigger
from unittest.mock import Mock


class TestConfigureShellTrigger(TestCase):

    def test_configure_shell_trigger(self):
        self.device = Mock()
        result = configure_shell_trigger(self.device, 'trigger_1', 'trigger desc')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('shell trigger trigger_1 trigger desc',)
        )
