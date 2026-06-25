from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_service_policy_type_control
from unittest.mock import Mock
from unicon.core.errors import SubCommandFailure


class TestConfigureInterfaceServicePolicyTypeControl(TestCase):

    def test_configure_interface_service_policy_type_control(self):
        self.device = Mock()
        configure_interface_service_policy_type_control(
            self.device, 'GigabitEthernet0/0/1', 'TAL'
        )
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                'interface GigabitEthernet0/0/1',
                'service-policy type control TAL',
            ],)
        )

    def test_configure_interface_service_policy_type_control_failure(self):
        self.device = Mock()
        self.device.configure.side_effect = SubCommandFailure('bad config')
        with self.assertRaises(SubCommandFailure):
            configure_interface_service_policy_type_control(
                self.device, 'GigabitEthernet0/0/1', 'TAL'
            )
