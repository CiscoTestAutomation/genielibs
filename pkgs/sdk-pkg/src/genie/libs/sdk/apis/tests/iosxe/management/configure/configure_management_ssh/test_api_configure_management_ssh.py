from unittest import TestCase
from genie.libs.sdk.apis.iosxe.management.configure import configure_management_ssh
from unittest.mock import Mock


class TestConfigureManagementSsh(TestCase):

    def test_configure_management_ssh(self):
        self.device = Mock()
        result = configure_management_ssh(self.device, None, None, None, 'cisco.com', 'GigabitEthernet0/0')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip domain name cisco.com',
            'ip ssh source-interface GigabitEthernet0/0',
            f'crypto key generate rsa'],)
        )
