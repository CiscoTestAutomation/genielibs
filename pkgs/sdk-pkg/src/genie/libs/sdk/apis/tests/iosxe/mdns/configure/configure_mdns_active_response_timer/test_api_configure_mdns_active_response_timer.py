import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_active_response_timer,
)


class TestConfigureMdnsActiveResponseTimer(TestCase):

    def test_configure_mdns_active_response_timer(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_active_response_timer(device, 20)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd gateway",
                "active-response timer 20",
            ]
        )


if __name__ == "__main__":
    unittest.main()
