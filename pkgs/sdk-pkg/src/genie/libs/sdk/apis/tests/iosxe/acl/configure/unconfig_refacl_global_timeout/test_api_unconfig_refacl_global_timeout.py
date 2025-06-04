from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import unconfig_refacl_global_timeout


class TestUnconfigRefaclGlobalTimeout(TestCase):

    def test_configure_mac_acl(self):
        self.device = Mock()
        unconfig_refacl_global_timeout(self.device, '300')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip reflexive-list timeout 300' ,)
        )
