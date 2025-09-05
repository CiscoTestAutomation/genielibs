import unittest
from unittest.mock import Mock, patch

from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.platform.execute import hardware_qfp_active_feature_alg_statistics_sip_clear


class TestHardwareQfpActiveStatisticsSipClear(unittest.TestCase):

    def test_hardware_qfp_active_feature_alg_statistics_sip_clear(self):
        device = Mock()
        device.execute = Mock()

        result = hardware_qfp_active_feature_alg_statistics_sip_clear(device)
        self.assertIsNone(result)
        device.execute.assert_called_with("show platform hardware qfp active feature alg statistics sip clear")

        device.execute.reset_mock()
        device.execute.side_effect = SubCommandFailure("Mocked error")

        with patch('genie.libs.sdk.apis.iosxe.platform.execute.log') as mock_log:
            with self.assertRaises(SubCommandFailure):
                hardware_qfp_active_feature_alg_statistics_sip_clear(device)
            device.execute.assert_called_with("show platform hardware qfp active feature alg statistics sip clear")
            mock_log.error.assert_called_once()
