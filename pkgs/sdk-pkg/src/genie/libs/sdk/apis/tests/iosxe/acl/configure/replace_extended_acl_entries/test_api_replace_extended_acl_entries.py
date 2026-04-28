from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.acl.configure import replace_extended_acl_entries


class TestReplaceExtendedAclEntries(TestCase):

    def test_replace_extended_acl_entries(self):
        device = Mock()
        result = replace_extended_acl_entries(
            device,
            acl_name="acl_pbr",
            acl_entries=[
                " 10 permit ip any 200.1.1.0 0.0.0.255",
                " 20 permit ip any 201.1.1.0 0.0.0.255",
            ],
            timeout=60,
        )
        device.configure.assert_called_with(
            [
                "no ip access-list extended acl_pbr",
                "ip access-list extended acl_pbr",
                "10 permit ip any 200.1.1.0 0.0.0.255",
                "20 permit ip any 201.1.1.0 0.0.0.255",
            ],
            timeout=60,
        )
        self.assertEqual(result, None)
