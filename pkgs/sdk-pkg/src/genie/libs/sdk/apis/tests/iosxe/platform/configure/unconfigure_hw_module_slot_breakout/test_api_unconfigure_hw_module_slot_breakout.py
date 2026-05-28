import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_hw_module_slot_breakout


class TestUnconfigureHwModuleSlotBreakout(unittest.TestCase):

    def test_unconfigure_hw_module_slot_breakout(self):
        device = Mock()

        result = unconfigure_hw_module_slot_breakout(device, 5, 5)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no hw-module slot 5 breakout 5',)
        )