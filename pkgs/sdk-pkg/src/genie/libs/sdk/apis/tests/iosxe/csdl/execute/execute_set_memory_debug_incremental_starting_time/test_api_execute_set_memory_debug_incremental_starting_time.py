from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.csdl.execute import execute_set_memory_debug_incremental_starting_time


class TestExecuteSetMemoryDebugIncrementalStartingTime(TestCase):
    def test_execute_set_memory_debug_incremental_starting_time(self):
        device = Mock()
        result = execute_set_memory_debug_incremental_starting_time(device, None)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('set memory debug incremental starting-time',)
        )