import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_query_response_mode,
)


class TestConfigureMdnsQueryResponseMode(TestCase):

    def test_configure_mdns_query_response_mode(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_query_response_mode(device, "recurring")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd gateway",
                "query-response mode recurring",
            ]
        )


if __name__ == "__main__":
    unittest.main()
