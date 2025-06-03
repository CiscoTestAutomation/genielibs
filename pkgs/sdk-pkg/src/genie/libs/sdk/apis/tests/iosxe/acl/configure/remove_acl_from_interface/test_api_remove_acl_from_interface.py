from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import remove_acl_from_interface


class TestRemoveAclFromInterface(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        remove_acl_from_interface(self.device, "TenGigabitEthernet0/0/0.10", "DELETE_ME")
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
             ('interface TenGigabitEthernet0/0/0.10\nno ip access-group DELETE_ME in',)
        )
