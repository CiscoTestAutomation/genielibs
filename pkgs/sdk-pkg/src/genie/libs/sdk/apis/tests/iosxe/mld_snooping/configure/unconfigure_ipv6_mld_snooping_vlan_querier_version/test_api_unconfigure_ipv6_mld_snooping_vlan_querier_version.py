import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.configure import (
    unconfigure_ipv6_mld_snooping_vlan_querier_version,
)


class TestUnconfigureIpv6MldSnoopingVlanQuerierVersion(TestCase):

    def test_unconfigure_ipv6_mld_snooping_vlan_querier_version(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ipv6_mld_snooping_vlan_querier_version(
            device,
            100,
            2,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "no ipv6 mld snooping vlan 100 querier version 2"
        )


if __name__ == "__main__":
    unittest.main()
