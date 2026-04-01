from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_extended_acl

class TestConfigureNatExtendedAcl(TestCase):

    def test_configure_nat_extended_acl(self):
        device = Mock()
        result = configure_nat_extended_acl(
            device,
            'acl_testing',
            'permit',
            '172.16.0.0',
            '0.0.255.255',
            '198.16.0.0',
            '0.0.255.255'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'ip access-list extended acl_testing',
                'permit ip 172.16.0.0 0.0.255.255 198.16.0.0 0.0.255.255'
            ],)
        )