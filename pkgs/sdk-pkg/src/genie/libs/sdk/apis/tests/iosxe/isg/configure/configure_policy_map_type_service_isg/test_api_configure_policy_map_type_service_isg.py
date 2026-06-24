from unittest import TestCase
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure
from genie.libs.sdk.apis.iosxe.isg.configure import configure_policy_map_type_service_isg


class TestConfigurePolicyMapTypeServiceIsg(TestCase):

    def test_configure_policy_map_type_service_isg_with_accounting(self):
        self.device = Mock()
        configure_policy_map_type_service_isg(
            self.device, 'service3',
            classes=[{
                'class_name': 'NONTC',
                'sub_commands': ['accounting aaa list acct1'],
            }]
        )
        self.device.configure.assert_called_once_with(
            [
                "policy-map type service service3",
                " class type traffic NONTC",
                "  accounting aaa list acct1",
            ]
        )

    def test_configure_policy_map_type_service_isg_with_timeout_and_accounting(self):
        self.device = Mock()
        configure_policy_map_type_service_isg(
            self.device, 'GOLD',
            classes=[{
                'class_name': 'Local8_TC',
                'sub_commands': ['timeout idle 75', 'accounting aaa list acct1'],
            }]
        )
        self.device.configure.assert_called_once_with(
            [
                "policy-map type service GOLD",
                " class type traffic Local8_TC",
                "  timeout idle 75",
                "  accounting aaa list acct1",
            ]
        )

    def test_configure_policy_map_type_service_isg_with_redirect(self):
        self.device = Mock()
        configure_policy_map_type_service_isg(
            self.device, 'L4_REDIRECT_V4',
            classes=[
                {
                    'class_name': 'Local8_TC',
                    'sub_commands': ['redirect to group REDIRECT_V4'],
                },
                {
                    'class_name': 'default in-out',
                    'sub_commands': ['drop'],
                },
            ]
        )
        self.device.configure.assert_called_once_with(
            [
                "policy-map type service L4_REDIRECT_V4",
                " class type traffic Local8_TC",
                "  redirect to group REDIRECT_V4",
                " class type traffic default in-out",
                "  drop",
            ]
        )

    def test_configure_policy_map_type_service_isg_with_police(self):
        self.device = Mock()
        configure_policy_map_type_service_isg(
            self.device, 'V4DRL',
            classes=[{
                'class_name': 'Local8_TC',
                'sub_commands': [
                    'accounting aaa list acct1',
                    'police input 8000 1000 2000',
                    'police output 8000 1000 2000',
                ],
            }]
        )
        self.device.configure.assert_called_once_with(
            [
                "policy-map type service V4DRL",
                " class type traffic Local8_TC",
                "  accounting aaa list acct1",
                "  police input 8000 1000 2000",
                "  police output 8000 1000 2000",
            ]
        )

    def test_configure_policy_map_type_service_isg_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('error')
        with self.assertRaises(SubCommandFailure):
            configure_policy_map_type_service_isg(self.device, 'service3')
