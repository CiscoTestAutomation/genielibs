from unittest import TestCase
from genie.libs.sdk.apis.iosxe.hardware.configure import configure_hw_module_breakout
from unittest.mock import Mock


class TestConfigureHwModuleBreakout(TestCase):

    def test_configure_hw_module_breakout(self):
        self.device = Mock()
        result = configure_hw_module_breakout(self.device, None, None, '1', '1', '1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['hw-module breakout module 1 port 1 switch 1'],)
        )
