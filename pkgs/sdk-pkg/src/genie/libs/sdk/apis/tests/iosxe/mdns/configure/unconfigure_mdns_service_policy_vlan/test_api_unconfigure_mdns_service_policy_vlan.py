import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    unconfigure_mdns_service_policy_vlan,
)


class TestUnconfigureMdnsServicePolicyVlan(TestCase):

    def test_unconfigure_mdns_service_policy_vlan(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_mdns_service_policy_vlan(
            device,
            77,
            "policy1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "vlan configuration 77",
                "mdns-sd gateway",
                "no service-policy policy1",
            ]
        )


if __name__ == "__main__":
    unittest.main()
