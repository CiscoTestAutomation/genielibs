import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    config_ip_multicast_routing_vrf_distributed,
)


class TestConfigIpMulticastRoutingVrfDistributed(TestCase):

    def test_config_ip_multicast_routing_vrf_distributed(self):
        device = Mock()
        device.configure.return_value = None

        result = config_ip_multicast_routing_vrf_distributed(device, "20")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "ip multicast-routing vrf 20 distributed"
        )


if __name__ == "__main__":
    unittest.main()
