import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_igmp_version,
)


class TestConfigureIgmpVersion(TestCase):

    def test_configure_igmp_version(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_igmp_version(device, "loopback3001", "3")

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, str)
        self.assertEqual(
            commands,
            "interface loopback3001\n ip igmp version 3",
        )


if __name__ == "__main__":
    unittest.main()
