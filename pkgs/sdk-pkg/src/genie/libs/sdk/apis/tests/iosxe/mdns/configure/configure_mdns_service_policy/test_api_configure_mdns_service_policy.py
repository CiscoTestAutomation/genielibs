import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_service_policy,
)


class TestConfigureMdnsServicePolicy(TestCase):

    def test_configure_mdns_service_policy(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_service_policy(
            device,
            "policy1",
            "policie1",
            "IN",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd service-policy policy1",
                "service-list policie1 IN",
            ]
        )


if __name__ == "__main__":
    unittest.main()
