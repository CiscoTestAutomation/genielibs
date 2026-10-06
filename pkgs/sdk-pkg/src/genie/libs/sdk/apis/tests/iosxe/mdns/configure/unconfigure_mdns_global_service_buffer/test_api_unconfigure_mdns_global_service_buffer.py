import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    unconfigure_mdns_global_service_buffer,
)


class TestUnconfigureMdnsGlobalServiceBuffer(TestCase):

    def test_unconfigure_mdns_global_service_buffer(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_mdns_global_service_buffer(device, "test")

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "service-export mdns-sd controller test",
                "no global-service-buffer",
            ]
        )


if __name__ == "__main__":
    unittest.main()
