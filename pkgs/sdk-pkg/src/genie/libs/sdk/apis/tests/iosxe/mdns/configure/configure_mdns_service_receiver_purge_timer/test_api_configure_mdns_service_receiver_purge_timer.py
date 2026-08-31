import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_service_receiver_purge_timer,
)


class TestConfigureMdnsServiceReceiverPurgeTimer(TestCase):

    def test_configure_mdns_service_receiver_purge_timer(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_service_receiver_purge_timer(device, 40)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd gateway",
                "service-receiver-purge timer 40",
            ]
        )


if __name__ == "__main__":
    unittest.main()
