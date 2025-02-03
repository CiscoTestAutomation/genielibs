from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_shell_trigger
from unittest.mock import Mock


class TestUnconfigureShellTrigger(TestCase):

    def test_unconfigure_shell_trigger(self):
        self.device = Mock()
        result = unconfigure_shell_trigger(self.device, 'trigger_1', 'trigger desc')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no shell trigger trigger_1 trigger desc',)
        )
