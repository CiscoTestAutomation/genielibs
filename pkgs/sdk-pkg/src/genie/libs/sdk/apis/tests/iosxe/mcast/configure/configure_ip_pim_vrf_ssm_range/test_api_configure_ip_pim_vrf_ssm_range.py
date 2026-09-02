import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mcast.configure import (
    configure_ip_pim_vrf_ssm_range,
)


class TestConfigureIpPimVrfSsmRange(TestCase):

    def test_configure_ip_pim_vrf_ssm_range(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ip_pim_vrf_ssm_range(
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
            "ip pim vrf red ssm range test",
        )


if __name__ == "__main__":
    unittest.main()
