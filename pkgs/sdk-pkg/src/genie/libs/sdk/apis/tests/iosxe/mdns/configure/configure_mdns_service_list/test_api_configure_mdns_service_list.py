import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_service_list,
)


class TestConfigureMdnsServiceList(TestCase):

    def test_configure_mdns_service_list(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_service_list(
            device,
            "policie88",
            "IN",
            ["apple-tv"],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd service-list policie88 IN",
                "match apple-tv",
            ]
        )


if __name__ == "__main__":
    unittest.main()
