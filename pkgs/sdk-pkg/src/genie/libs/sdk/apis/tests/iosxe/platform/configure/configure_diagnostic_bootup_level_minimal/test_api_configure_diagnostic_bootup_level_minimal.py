from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_diagnostic_bootup_level_minimal


class TestConfigureDiagnosticBootupLevelMinimal(TestCase):

    def test_configure_diagnostic_bootup_level_minimal(self):
        device = Mock()
        result = configure_diagnostic_bootup_level_minimal(device)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('diagnostic bootup level minimal',)
        )