import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    unconfigure_mdns_gateway_globally,
)


class TestUnconfigureMdnsGatewayGlobally(TestCase):

    def test_unconfigure_mdns_gateway_globally(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_mdns_gateway_globally(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(["no mdns-sd gateway"])


if __name__ == "__main__":
    unittest.main()
