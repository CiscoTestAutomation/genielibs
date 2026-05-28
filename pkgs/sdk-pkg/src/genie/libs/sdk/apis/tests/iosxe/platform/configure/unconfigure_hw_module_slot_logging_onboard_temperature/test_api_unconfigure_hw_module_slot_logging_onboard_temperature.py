import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_hw_module_slot_logging_onboard_temperature


class TestUnconfigureHwModuleSlotLoggingOnboardTemperature(unittest.TestCase):

    def test_unconfigure_hw_module_slot_logging_onboard_temperature(self):
        device = Mock()

        result = unconfigure_hw_module_slot_logging_onboard_temperature(device, 2)

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no hw-module slot 2 logging onboard temperature',)
        )