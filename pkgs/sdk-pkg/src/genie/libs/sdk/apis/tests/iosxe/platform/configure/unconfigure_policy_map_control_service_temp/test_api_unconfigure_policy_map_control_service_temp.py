import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import unconfigure_policy_map_control_service_temp



class TestUnconfigurePolicyMapControlServiceTemp(unittest.TestCase):

    def test_unconfigure_policy_map_control_service_temp(self):
        device = Mock()

        result = unconfigure_policy_map_control_service_temp(
            device,
            'DOT1X-MUST-SECURE-UPLINK'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no policy-map type control subscriber DOT1X-MUST-SECURE-UPLINK',)
        )