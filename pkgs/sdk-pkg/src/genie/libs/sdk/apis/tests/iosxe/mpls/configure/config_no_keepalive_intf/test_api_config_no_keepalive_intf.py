import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mpls.configure import (
    config_no_keepalive_intf,
)


class TestConfigNoKeepaliveIntf(TestCase):

    def test_config_no_keepalive_intf(self):
        device = Mock()
        device.configure.return_value = None

        result = config_no_keepalive_intf(
            device,
            "GigabitEthernet1/0/6",
            "100",
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "interface GigabitEthernet1/0/6",
                "no keepalive 100",
            ]
        )


if __name__ == "__main__":
    unittest.main()
