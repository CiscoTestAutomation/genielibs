from unittest import TestCase
from genie.libs.sdk.apis.iosxe.acl.configure import config_extended_acl
from unittest.mock import Mock


class TestConfigExtendedAcl(TestCase):

    def test_config_extended_acl(self):
        self.device = Mock()
        result = config_extended_acl(self.device, 'test', 'permit', 'tcp', '1.1.1.1', None, None, '2.2.2.2', None, None, '800', None, 'host', '10', 'log', None, 'eq')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['ip access-list extended test', '10 permit tcp host 1.1.1.1 host 2.2.2.2 eq 800 log'],)
        )
