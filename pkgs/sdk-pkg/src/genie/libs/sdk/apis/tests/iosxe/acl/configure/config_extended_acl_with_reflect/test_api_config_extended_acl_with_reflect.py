import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import config_extended_acl_with_reflect


class TestConfigExtendedAclWithReflect(unittest.TestCase):

    def test_config_extended_acl_with_reflect(self):
        device = Mock()
        device.configure.return_value = ""

        result = config_extended_acl_with_reflect(
            device,
            "test2",
            "reflect",
            "R10000",
            "tcp",
            "permit",
            "1.1.1.1",
            None,
            None,
            "2.2.2.2",
            None,
            None,
            "80",
            None,
            "host",
            "50",
            "120",
            "timeout",
            "2001",
            "eq",
            None,
            None,
        )
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "ip access-list extended test2",
                "50 permit tcp host 1.1.1.1 eq 2001 host 2.2.2.2 eq 80 reflect R10000 timeout 120",
            ],)
        )