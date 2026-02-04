from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.debug.configure import debug_vdsl_controller_slot_dump_internal


class TestDebugVdslControllerSlotDumpInternal(TestCase):
    def test_debug_vdsl_controller_slot_dump_internal(self):
        device = Mock()
        result = debug_vdsl_controller_slot_dump_internal(device, '0/0/1', 'sfp_test.dump', 900)
        expected_output = None
        self.assertEqual(result, expected_output)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('debug vdsl controller 0/0/1 dump internal sfp_test.dump',)
        )