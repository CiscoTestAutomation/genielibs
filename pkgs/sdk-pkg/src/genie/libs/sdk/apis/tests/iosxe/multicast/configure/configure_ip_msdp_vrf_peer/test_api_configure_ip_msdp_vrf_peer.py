import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_ip_msdp_vrf_peer,
)


class TestConfigureIpMsdpVrfPeer(TestCase):

    def test_configure_ip_msdp_vrf_peer(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ip_msdp_vrf_peer(
            device,
            "6.6.6.1",
            "red",
            "loopback1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        command = device.configure.call_args.args[0]
        self.assertIsInstance(command, str)
        self.assertEqual(
            command,
            "ip msdp vrf red peer 6.6.6.1 connect-source loopback1",
        )


if __name__ == "__main__":
    unittest.main()
