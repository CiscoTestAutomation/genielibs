from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import config_refacl_global_timeout
from unittest.mock import Mock

class TestConfigRefaclGlobalTimeout(TestCase):

    def test_config_refacl_global_timeout(self):
        self.device = Mock()
        config_refacl_global_timeout(self.device, '300')
        self.device.configure.assert_called_with('ip reflexive-list timeout 300')
