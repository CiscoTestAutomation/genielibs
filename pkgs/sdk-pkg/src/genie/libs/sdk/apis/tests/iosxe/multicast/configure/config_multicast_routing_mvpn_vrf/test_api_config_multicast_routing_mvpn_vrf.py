import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    config_multicast_routing_mvpn_vrf,
)


class TestConfigMulticastRoutingMvpnVrf(TestCase):

    def test_config_multicast_routing_mvpn_vrf(self):
        device = Mock()
        device.configure.return_value = None

        result = config_multicast_routing_mvpn_vrf(device, "vrf3001")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "ip multicast-routing vrf vrf3001"
        )


if __name__ == "__main__":
    unittest.main()
