import unittest
from unittest import TestCase
from unittest.mock import Mock, call

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    unconfig_mka_policy,
)


class TestUnconfigMkaPolicy(TestCase):

    def test_unconfig_mka_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfig_mka_policy(
            device,
            "TwentyFiveGigE 1/0/7",
            "MKA_policy1",
            True,
        )

        self.assertIsNone(result)

        self.assertEqual(device.configure.call_count, 2)
        device.configure.assert_has_calls(
            [
                call(
                    [
                        "interface TwentyFiveGigE 1/0/7",
                        "no mka policy MKA_policy1",
                    ]
                ),
                call(
                    [
                        "no mka policy MKA_policy1",
                    ]
                ),
            ]
        )


if __name__ == "__main__":
    unittest.main()
