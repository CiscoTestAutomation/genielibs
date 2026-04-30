from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import config_extended_acl
from unittest.mock import Mock


class TestConfigExtendedAcl(TestCase):

    def test_config_extended_acl(self):
        self.device = Mock()
        result = config_extended_acl(self.device, 'ACL_EXT_1', 'permit', 'tcp', None, None, None, None, None, None, None, None, None, '10', None, None, None, '1000 2000', '3000 4000', None, 'any', 'any')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended ACL_EXT_1', '10 permit tcp any range 1000 2000 any range 3000 4000'],)
        )
