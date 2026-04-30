from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_hw_module_slot_logging_onboard_voltage


class TestConfigureHwModuleSlotLoggingOnboardVoltage(TestCase):

    def test_configure_hw_module_slot_logging_onboard_voltage(self):
        device = Mock()
        result = configure_hw_module_slot_logging_onboard_voltage(
            device,
            2
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('hw-module slot 2 logging onboard voltage',)
        )