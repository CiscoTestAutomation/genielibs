from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_clear_logging_onboard_switch_environment


class TestConfigureClearLoggingOnboardSwitchEnvironment(TestCase):

    def test_configure_clear_logging_onboard_switch_environment(self):
        device = Mock()
        result = configure_clear_logging_onboard_switch_environment(
            device,
            1
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.execute.mock_calls[0].args,
            ('clear  logging  onboard  switch 1 environment',)
        )