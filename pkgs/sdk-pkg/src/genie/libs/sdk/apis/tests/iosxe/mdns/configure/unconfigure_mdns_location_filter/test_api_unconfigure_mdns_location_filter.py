import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    unconfigure_mdns_location_filter,
)


class TestUnconfigureMdnsLocationFilter(TestCase):

    def test_unconfigure_mdns_location_filter(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_mdns_location_filter(device, "filter_1")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["no mdns-sd location-filter filter_1"]
        )


if __name__ == "__main__":
    unittest.main()
