import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import unconfigure_mdns_trust


class TestUnconfigureMdnsTrust(TestCase):

    def test_unconfigure_mdns_trust(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_mdns_trust(
            device,
            "TwentyFiveGigE1/0/9",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "interface TwentyFiveGigE1/0/9",
                "no mdns-sd trust",
            ]
        )


if __name__ == "__main__":
    unittest.main()
