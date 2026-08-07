import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipv6.configure import (
    configure_ipv6_flow_monitor_sampler,
)


class TestConfigureIpv6FlowMonitorSampler(TestCase):

    def test_configure_ipv6_flow_monitor_sampler(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ipv6_flow_monitor_sampler(
            device,
            "Port-channel10",
            "input",
            "ipv6_monitor_in",
            "sampler_random",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface Port-channel10",
                "ipv6 flow monitor ipv6_monitor_in sampler sampler_random input",
                "end",
            ],
        )


if __name__ == "__main__":
    unittest.main()
