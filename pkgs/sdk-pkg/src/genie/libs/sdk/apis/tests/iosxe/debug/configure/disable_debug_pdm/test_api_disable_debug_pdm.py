import unittest
from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.debug.configure import disable_debug_pdm


class TestDisableDebugPdm(TestCase):

    def test_disable_debug_pdm(self):
        device = Mock()
        result = disable_debug_pdm(device, 'steering-policy', 'all')
        expected_output = None
        self.assertEqual(result, expected_output)
        
        # Verify execute was called with the correct command
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('no debug pdm steering-policy all',)
        )


if __name__ == '__main__':
    unittest.main()