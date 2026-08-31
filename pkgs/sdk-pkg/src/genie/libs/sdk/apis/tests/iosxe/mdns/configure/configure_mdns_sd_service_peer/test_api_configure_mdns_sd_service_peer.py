import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_sd_service_peer,
)


class TestConfigureMdnsSdServicePeer(TestCase):

    def test_configure_mdns_sd_service_peer(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_sd_service_peer(
            device,
            "10",
            "10.10.10.1",
            "30",
            "60",
            "10",
            "100",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd gateway",
                "mode service-peer",
                "source-interface vlan 10",
                "sdg-agent 10.10.10.1",
                "active-response timer 30",
                "service-announcement-timer periodicity 60",
                "service-announcement-count 10",
                "service-query-timer periodicity 60",
                "service-query-count 10",
                "rate-limit 100",
            ]
        )


if __name__ == "__main__":
    unittest.main()
