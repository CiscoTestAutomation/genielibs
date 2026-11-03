import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ip_msdp_peer,
)


class TestConfigureIpMsdpPeer(TestCase):

    def test_configure_ip_msdp_peer(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ip_msdp_peer(
            device,
            "172.16.254.2",
            65001,
            "Gi3/0/21",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "ip msdp peer 172.16.254.2 connect-source Gi3/0/21 remote-as 65001",
        )

    def test_configure_ip_msdp_peer_1(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ip_msdp_peer(device, "172.16.254.2", 65001, None)

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(command, "ip msdp peer 172.16.254.2 remote-as 65001")


if __name__ == "__main__":
    unittest.main()
