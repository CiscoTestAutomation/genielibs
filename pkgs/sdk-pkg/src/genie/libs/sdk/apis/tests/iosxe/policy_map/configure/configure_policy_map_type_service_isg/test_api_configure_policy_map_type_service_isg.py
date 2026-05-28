import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_type_service_isg
from unicon.core.errors import SubCommandFailure


class TestConfigurePolicyMapTypeServiceIsg(unittest.TestCase):

    def test_configure_with_accounting(self):
        device = Mock()
        configure_policy_map_type_service_isg(
            device, 'service3', 'NONTC',
            actions=['accounting aaa list ACCT_LIST']
        )
        device.configure.assert_called_once_with([
            'policy-map type service service3',
            ' class type traffic NONTC',
            '  accounting aaa list ACCT_LIST',
        ])

    def test_configure_with_timeout_idle(self):
        device = Mock()
        configure_policy_map_type_service_isg(
            device, 'service4', 'Local8_TC',
            actions=['timeout idle 180']
        )
        device.configure.assert_called_once_with([
            'policy-map type service service4',
            ' class type traffic Local8_TC',
            '  timeout idle 180',
        ])

    def test_configure_with_timeout_idle_inbound(self):
        device = Mock()
        configure_policy_map_type_service_isg(
            device, 'service5', 'NONTC1',
            actions=['timeout idle 60 inbound']
        )
        device.configure.assert_called_once_with([
            'policy-map type service service5',
            ' class type traffic NONTC1',
            '  timeout idle 60 inbound',
        ])

    def test_configure_with_redirect(self):
        device = Mock()
        configure_policy_map_type_service_isg(
            device, 'L4_REDIRECT_V4', 'Local8_TC',
            actions=['redirect to group REDIR_GRP_V4']
        )
        device.configure.assert_called_once_with([
            'policy-map type service L4_REDIRECT_V4',
            ' class type traffic Local8_TC',
            '  redirect to group REDIR_GRP_V4',
        ])

    def test_configure_with_drop(self):
        device = Mock()
        configure_policy_map_type_service_isg(
            device, 'L4_REDIRECT_V4', 'default in-out',
            actions=['drop']
        )
        device.configure.assert_called_once_with([
            'policy-map type service L4_REDIRECT_V4',
            ' class type traffic default in-out',
            '  drop',
        ])

    def test_configure_with_police(self):
        device = Mock()
        configure_policy_map_type_service_isg(
            device, 'V4DRL', 'Local8_TC',
            actions=[
                'accounting aaa list ACCT_LIST',
                'police input 8000 1000 2000',
                'police output 8000 1000 2000',
            ]
        )
        device.configure.assert_called_once_with([
            'policy-map type service V4DRL',
            ' class type traffic Local8_TC',
            '  accounting aaa list ACCT_LIST',
            '  police input 8000 1000 2000',
            '  police output 8000 1000 2000',
        ])

    def test_configure_failure(self):
        device = Mock()
        device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_service_isg(
                device, 'service3', 'NONTC',
                actions=['accounting aaa list ACCT_LIST']
            )


if __name__ == '__main__':
    unittest.main()
