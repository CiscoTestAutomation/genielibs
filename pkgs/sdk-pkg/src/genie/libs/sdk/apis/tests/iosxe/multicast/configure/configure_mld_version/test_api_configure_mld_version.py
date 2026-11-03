import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_mld_version,
)


class TestConfigureMldVersion(TestCase):

    def test_configure_mld_version(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mld_version(device, 202, 2)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "int vlan 202",
                "ipv6 mld version 2",
            ],
        )


if __name__ == "__main__":
    unittest.main()
