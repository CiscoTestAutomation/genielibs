import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_service_peer_group,
)


class TestConfigureMdnsServicePeerGroup(TestCase):

    def test_configure_mdns_service_peer_group(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_service_peer_group(
            device,
            3,
            "policy44",
            "20.0.0.20",
            4096,
            "bonjour",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd service-peer group",
                "peer-group 3",
                "service-policy policy44",
                (
                    "service-peer 20.0.0.20 location-group 4096 "
                    "role bonjour"
                ),
            ]
        )


if __name__ == "__main__":
    unittest.main()
