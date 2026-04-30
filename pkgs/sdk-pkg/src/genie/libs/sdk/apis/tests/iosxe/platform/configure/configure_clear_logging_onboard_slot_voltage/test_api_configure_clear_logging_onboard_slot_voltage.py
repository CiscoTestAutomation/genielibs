from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_clear_logging_onboard_slot_voltage


class TestConfigureClearLoggingOnboardSlotVoltage(TestCase):

    def test_configure_clear_logging_onboard_slot_voltage(self):
        device = Mock()
        result = configure_clear_logging_onboard_slot_voltage(
            device,
            2
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear  logging  onboard  slot 2 voltage',)
        )