from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_action_string


class TestConfigureActionString(TestCase):

    def test_configure_action_string(self):
        device = Mock()
        result = configure_action_string(
            device,
            'Test',
            '5.1',
            'force-switchover'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['event manager applet Test', 'action 5.1 force-switchover'],)
        )