from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.cpp.execute import execute_clear_control_plane


class TestExecuteClearControlPlane(TestCase):
    def test_execute_clear_control_plane(self):
        device = Mock()
        result = execute_clear_control_plane(device)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear control-plane *',)
        )