import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    unconfigure_match_service_type_mdns_service_list,
)


class TestUnconfigureMatchServiceTypeMdnsServiceList(TestCase):

    def test_unconfigure_match_service_type_mdns_service_list(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_match_service_type_mdns_service_list(
            device,
            "policie88",
            "IN",
            ["apple-tv"],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd service-list policie88 IN",
                "no match apple-tv",
            ]
        )


if __name__ == "__main__":
    unittest.main()
