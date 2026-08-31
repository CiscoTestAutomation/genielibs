import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_remote_cache_max_limit,
)


class TestConfigureMdnsRemoteCacheMaxLimit(TestCase):

    def test_configure_mdns_remote_cache_max_limit(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_remote_cache_max_limit(device, 1000)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd gateway",
                "remote-cache-max-limit 1000",
            ]
        )


if __name__ == "__main__":
    unittest.main()
