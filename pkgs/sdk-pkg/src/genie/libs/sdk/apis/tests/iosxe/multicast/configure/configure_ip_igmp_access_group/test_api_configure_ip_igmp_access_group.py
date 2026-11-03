import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ip_igmp_access_group,
)


class TestConfigureIpIgmpAccessGroup(TestCase):

    def test_configure_ip_igmp_access_group(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ip_igmp_access_group(
            device,
            "te1/0/1",
            "test2",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface te1/0/1",
                "ip igmp access-group test2",
            ],
        )


if __name__ == "__main__":
    unittest.main()
