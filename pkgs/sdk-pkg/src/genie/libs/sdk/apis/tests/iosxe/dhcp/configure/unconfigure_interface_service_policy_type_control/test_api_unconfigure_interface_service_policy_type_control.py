from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_interface_service_policy_type_control
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure


class TestUnconfigureInterfaceServicePolicyTypeControl(TestCase):

    def test_unconfigure_interface_service_policy_type_control(self):
        self.device = Mock()
        unconfigure_interface_service_policy_type_control(
            self.device, 'GigabitEthernet0/0/1'
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet0/0/1',
                'no service-policy type control',
            ],)
        )

    def test_unconfigure_interface_service_policy_type_control_with_name(self):
        self.device = Mock()
        unconfigure_interface_service_policy_type_control(
            self.device, 'GigabitEthernet0/0/1', policy_name='TAL'
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet0/0/1',
                'no service-policy type control TAL',
            ],)
        )

    def test_unconfigure_interface_service_policy_type_control_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('bad config')
        with self.assertRaises(SubCommandFailure):
            unconfigure_interface_service_policy_type_control(
                self.device, 'GigabitEthernet0/0/1'
            )
