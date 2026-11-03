import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ipv6_mld_access_group,
)


class TestConfigureIpv6MldAccessGroup(TestCase):

    def test_configure_ipv6_mld_access_group(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_mld_access_group(device, "te1/0/1", None)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "int te1/0/1",
                "ipv6 mld access-group None",
            ],
        )


if __name__ == "__main__":
    unittest.main()
