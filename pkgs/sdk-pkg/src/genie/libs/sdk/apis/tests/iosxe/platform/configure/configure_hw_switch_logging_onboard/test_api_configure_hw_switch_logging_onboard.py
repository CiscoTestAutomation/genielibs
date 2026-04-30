from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_hw_switch_logging_onboard


class TestConfigureHwSwitchLoggingOnboard(TestCase):

    def test_configure_hw_switch_logging_onboard(self):
        device = Mock()
        result = configure_hw_switch_logging_onboard(
            device,
            '1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('hw-switch switch 1 logging onboard',)
        )