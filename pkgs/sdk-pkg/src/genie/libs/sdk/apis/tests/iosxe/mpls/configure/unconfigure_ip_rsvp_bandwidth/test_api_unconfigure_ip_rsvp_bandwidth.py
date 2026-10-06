import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mpls.configure import (
    unconfigure_ip_rsvp_bandwidth,
)


class TestUnconfigureIpRsvpBandwidth(TestCase):

    def test_unconfigure_ip_rsvp_bandwidth(self):
        device = Mock()
        device.configure.return_value = None

        result = unconfigure_ip_rsvp_bandwidth(
            device,
            "Te3/0/5",
            "1000",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "interface Te3/0/5",
                "no ip rsvp bandwidth",
                "no ip rsvp bandwidth 1000",
            ]
        )


if __name__ == "__main__":
    unittest.main()
