import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_hw_switch_switch_logging_onboard_temperature


class TestUnconfigureHwSwitchSwitchLoggingOnboardTemperature(unittest.TestCase):

    def test_unconfigure_hw_switch_switch_logging_onboard_temperature(self):
        device = Mock()

        result = unconfigure_hw_switch_switch_logging_onboard_temperature(device, '1')

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no hw-switch switch 1 logging onboard temperature',)
        )