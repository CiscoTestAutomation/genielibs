import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ipv6_mld_join_group_acl,
)


class TestConfigureIpv6MldJoinGroupAcl(TestCase):

    def test_configure_ipv6_mld_join_group_acl(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_mld_join_group_acl(
            device,
            "FF3E:6::1",
            "Loopback1",
            "ssm_source",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface Loopback1",
                "ipv6 mld join-group FF3E:6::1 source-list ssm_source",
            ],
        )


if __name__ == "__main__":
    unittest.main()
