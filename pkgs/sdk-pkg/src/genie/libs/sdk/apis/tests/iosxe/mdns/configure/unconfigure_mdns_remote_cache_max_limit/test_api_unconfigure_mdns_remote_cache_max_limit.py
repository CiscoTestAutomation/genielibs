import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    unconfigure_mdns_remote_cache_max_limit,
)


class TestUnconfigureMdnsRemoteCacheMaxLimit(TestCase):

    def test_unconfigure_mdns_remote_cache_max_limit(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_mdns_remote_cache_max_limit(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd gateway",
                "no remote-cache-max-limit",
            ]
        )


if __name__ == "__main__":
    unittest.main()
