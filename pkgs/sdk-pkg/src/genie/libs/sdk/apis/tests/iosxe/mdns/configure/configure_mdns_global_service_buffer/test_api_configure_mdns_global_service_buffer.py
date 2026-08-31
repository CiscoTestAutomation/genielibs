import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_global_service_buffer,
)


class TestConfigureMdnsGlobalServiceBuffer(TestCase):

    def test_configure_mdns_global_service_buffer(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_global_service_buffer(
            device,
            "test",
            "enable",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "service-export mdns-sd controller test",
                "global-service-buffer enable",
            ]
        )


if __name__ == "__main__":
    unittest.main()
