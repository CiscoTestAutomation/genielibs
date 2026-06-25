from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import configure_policy_map_type_control


class TestConfigurePolicyMapTypeControl(TestCase):

    def test_configure_policy_map_type_control_with_actions(self):
        self.device = Mock()
        configure_policy_map_type_control(
            self.device, 'IT',
            classes=[{
                'event': 'session-start',
                'actions': [
                    '5 service-policy type service name IT_V4_TRAFFIC',
                    '7 service-policy type service name IT_V6_TRAFFIC',
                    '9 authorize identifier mac-address',
                ],
            }]
        )
        self.device.configure.assert_called_once_with(
            [
                "policy-map type control IT",
                " class type control always event session-start",
                "  5 service-policy type service name IT_V4_TRAFFIC",
                "  7 service-policy type service name IT_V6_TRAFFIC",
                "  9 authorize identifier mac-address",
            ]
        )

    def test_configure_policy_map_type_control_multiple_events(self):
        self.device = Mock()
        configure_policy_map_type_control(
            self.device, 'TAL',
            classes=[
                {
                    'event': 'session-start',
                    'actions': ['10 authorize identifier mac-address'],
                },
                {
                    'event': 'session-restart',
                    'actions': ['20 authorize identifier mac-address'],
                },
            ]
        )
        self.device.configure.assert_called_once_with(
            [
                "policy-map type control TAL",
                " class type control always event session-start",
                "  10 authorize identifier mac-address",
                " class type control always event session-restart",
                "  20 authorize identifier mac-address",
            ]
        )

    def test_configure_policy_map_type_control_with_error_pattern(self):
        self.device = Mock()
        configure_policy_map_type_control(
            self.device, 'ACCT_LOGON',
            classes=[{
                'event': 'session-start',
                'actions': ['5 service local'],
            }],
            error_pattern=[]
        )
        self.device.configure.assert_called_once_with(
            [
                "policy-map type control ACCT_LOGON",
                " class type control always event session-start",
                "  5 service local",
            ],
            error_pattern=[]
        )

    def test_configure_policy_map_type_control_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_control(self.device, 'IT')
