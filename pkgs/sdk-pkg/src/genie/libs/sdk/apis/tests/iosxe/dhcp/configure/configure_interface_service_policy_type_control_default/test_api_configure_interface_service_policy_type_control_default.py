from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_interface_service_policy_type_control_default
from unittest.mock import Mock


class TestConfigureInterfaceServicePolicyTypeControlDefault(TestCase):

    def test_configure_interface_service_policy_type_control_default(self):
        self.device = Mock()
        result = configure_interface_service_policy_type_control_default(self.device, 'GigabitEthernet0', 'TAL_DEFAULT')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet0', 'service-policy type control default TAL_DEFAULT'],)
        )
