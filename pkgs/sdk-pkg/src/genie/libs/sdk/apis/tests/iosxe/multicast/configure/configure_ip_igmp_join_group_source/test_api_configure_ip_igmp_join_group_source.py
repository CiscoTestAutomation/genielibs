import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ip_igmp_join_group_source,
)


class TestConfigureIpIgmpJoinGroupSource(TestCase):

    def test_configure_ip_igmp_join_group_source(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ip_igmp_join_group_source(
            device,
            "te1/0/1",
            "226.1.1.1",
            "",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "interface te1/0/1",
                "ip igmp join-group 226.1.1.1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
