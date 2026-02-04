from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.debug.configure import enable_debug_pdm


class TestEnableDebugPdm(TestCase):
    def test_enable_debug_pdm(self):
        device = Mock()
        result = enable_debug_pdm(device, 'steering-policy', 'all')
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('debug pdm steering-policy all',)
        )