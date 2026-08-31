import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_remote_cache_enable,
)


class TestConfigureMdnsRemoteCacheEnable(TestCase):

    def test_configure_mdns_remote_cache_enable(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_remote_cache_enable(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "mdns-sd gateway",
                "remote-cache-enable",
            ]
        )


if __name__ == "__main__":
    unittest.main()
