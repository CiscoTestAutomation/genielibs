from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.debug.configure import disable_debug


class TestDisableDebug(TestCase):
    def test_disable_debug(self):
        device = Mock()
        result = disable_debug(device, 'all')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('no debug all',)
        )