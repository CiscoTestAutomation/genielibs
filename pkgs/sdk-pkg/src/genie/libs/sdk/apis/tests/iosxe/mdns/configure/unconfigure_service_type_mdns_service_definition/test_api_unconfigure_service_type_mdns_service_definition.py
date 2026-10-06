import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    unconfigure_service_type_mdns_service_definition,
)


class TestUnconfigureServiceTypeMdnsServiceDefinition(TestCase):

    def test_unconfigure_service_type_mdns_service_definition(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_service_type_mdns_service_definition(
            device,
            "custom3",
            ["_ftp._tcp.local"],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd service-definition custom3",
                "no service-type _ftp._tcp.local",
            ]
        )


if __name__ == "__main__":
    unittest.main()
