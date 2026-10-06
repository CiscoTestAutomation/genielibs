import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mld_snooping.configure import (
    configure_ipv6_mld_snooping_querier_version,
)


class TestConfigureIpv6MldSnoopingQuerierVersion(TestCase):

    def test_configure_ipv6_mld_snooping_querier_version(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_ipv6_mld_snooping_querier_version(device, 2)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            "ipv6 mld snooping querier version 2"
        )


if __name__ == "__main__":
    unittest.main()
