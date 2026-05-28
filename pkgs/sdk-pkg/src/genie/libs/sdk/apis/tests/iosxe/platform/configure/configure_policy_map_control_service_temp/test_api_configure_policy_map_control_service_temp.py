import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.platform.configure import configure_policy_map_control_service_temp


class TestConfigurePolicyMapControlServiceTemp(unittest.TestCase):

    def test_configure_policy_map_control_service_temp(self):
        device = Mock()

        result = configure_policy_map_control_service_temp(
            device,
            'DOT1X-MUST-SECURE-UPLINK',
            'DEFAULT_LINKSEC_POLICY_MUST_SECURE',
            'MACSEC-UPLINK',
            'EAP-PROFILE'
        )

        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'policy-map type control subscriber DOT1X-MUST-SECURE-UPLINK',
                'event session-started match-all',
                '10 class always do-until-failure',
                '10 authenticate using dot1x aaa authc-list MACSEC-UPLINK authz-list MACSEC-UPLINK both',
                'event authentication-failure match-all',
                '10 class always do-until-failure',
                '10 terminate dot1x',
                '20 authentication-restart 10',
                'event authentication-success match-all',
                '10 class always do-until-failure',
                '10 activate service-template DEFAULT_LINKSEC_POLICY_MUST_SECURE'
            ],),
            device.configure.mock_calls[0].args,
        )