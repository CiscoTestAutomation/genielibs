import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_type_control_isg
from unicon.core.errors import SubCommandFailure


class TestConfigurePolicyMapTypeControlIsg(unittest.TestCase):

    def test_configure_session_start_single_event(self):
        device = Mock()
        configure_policy_map_type_control_isg(
            device, 'IT', 'session-start',
            actions=[
                '5 service-policy type service name IT_V4_TRAFFIC',
                '7 service-policy type service name IT_V6_TRAFFIC',
                '9 authorize identifier mac-address',
            ]
        )
        device.configure.assert_called_once_with([
            'policy-map type control IT',
            'class type control always event session-start',
            '5 service-policy type service name IT_V4_TRAFFIC',
            '7 service-policy type service name IT_V6_TRAFFIC',
            '9 authorize identifier mac-address',
        ])

    def test_configure_session_start_authorize_only(self):
        device = Mock()
        configure_policy_map_type_control_isg(
            device, 'TAL', 'session-start',
            actions=['10 authorize identifier mac-address']
        )
        device.configure.assert_called_once_with([
            'policy-map type control TAL',
            'class type control always event session-start',
            '10 authorize identifier mac-address',
        ])

    def test_configure_session_restart(self):
        device = Mock()
        configure_policy_map_type_control_isg(
            device, 'TAL', 'session-restart',
            actions=['20 authorize identifier mac-address']
        )
        device.configure.assert_called_once_with([
            'policy-map type control TAL',
            'class type control always event session-restart',
            '20 authorize identifier mac-address',
        ])

    def test_configure_account_logon(self):
        device = Mock()
        configure_policy_map_type_control_isg(
            device, 'L4_R', 'account-logon',
            actions=[
                '10 authenticate aaa list AUTHEN_LIST',
                '20 service-policy type service unapply name L4_REDIRECT_V4',
                '30 service-policy type service unapply name L4_REDIRECT_V6',
            ]
        )
        device.configure.assert_called_once_with([
            'policy-map type control L4_R',
            'class type control always event account-logon',
            '10 authenticate aaa list AUTHEN_LIST',
            '20 service-policy type service unapply name L4_REDIRECT_V4',
            '30 service-policy type service unapply name L4_REDIRECT_V6',
        ])

    def test_configure_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_control_isg(
                device, 'IT', 'session-start',
                actions=['9 authorize identifier mac-address']
            )


if __name__ == '__main__':
    unittest.main()
