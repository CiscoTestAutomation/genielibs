import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mcast.configure import (
    unconfigure_ip_pim_vrf_ssm_range,
)


class TestUnconfigureIpPimVrfSsmRange(TestCase):

    def test_unconfigure_ip_pim_vrf_ssm_range(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = unconfigure_ip_pim_vrf_ssm_range(
            device,
            "red",
            "test",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, str)
        self.assertEqual(
            sent_commands,
            "no ip pim vrf red ssm range test",
        )


if __name__ == "__main__":
    unittest.main()
