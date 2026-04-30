from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_hw_module_slot_breakout


class TestConfigureHwModuleSlotBreakout(TestCase):

    def test_configure_hw_module_slot_breakout(self):
        device = Mock()
        result = configure_hw_module_slot_breakout(
            device,
            5,
            5
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('hw-module slot 5 breakout 5',)
        )