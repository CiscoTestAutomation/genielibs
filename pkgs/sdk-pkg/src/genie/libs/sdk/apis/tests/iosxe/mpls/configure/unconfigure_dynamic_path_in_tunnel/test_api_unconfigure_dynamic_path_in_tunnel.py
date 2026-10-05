import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mpls.configure import (
    unconfigure_dynamic_path_in_tunnel,
)


class TestUnconfigureDynamicPathInTunnel(TestCase):

    def test_unconfigure_dynamic_path_in_tunnel(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_dynamic_path_in_tunnel(
            device,
            "Tunnel100",
            "100",
            False,
            "vis",
            "vis",
            True,
            "igp",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "interface Tunnel100",
                (
                    "no tunnel mpls traffic-eng path-option 100 "
                    "explicit name vis"
                ),
                (
                    "no tunnel mpls traffic-eng path-option 100 "
                    "explicit name vis attributes vis"
                ),
                "no tunnel mpls traff path-option 100 dynamic lockdown",
                "no tunnel mpls traffic-eng path-selection metric igp",
            ]
        )


if __name__ == "__main__":
    unittest.main()
