import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mpls.configure import (
    unconfigure_ldp_discovery_targeted_hello_accept,
)


class TestUnconfigureLdpDiscoveryTargetedHelloAccept(TestCase):

    def test_unconfigure_ldp_discovery_targeted_hello_accept(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ldp_discovery_targeted_hello_accept(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            ["no mpls ldp discovery targeted-hello accept"]
        )


if __name__ == "__main__":
    unittest.main()
