from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv4_ogacl_service

class TestConfigureIpv4OgaclService(TestCase):

    def test_configure_ipv4_ogacl_service(self):
        device = Mock()
        result = configure_ipv4_ogacl_service(
            device, 'ogacl_policy_in', 'permit', 'ogacl_service', 'any', 'any'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'ip access-list extended ogacl_policy_in',
                'permit object-group ogacl_service any any'
            ],)
        )