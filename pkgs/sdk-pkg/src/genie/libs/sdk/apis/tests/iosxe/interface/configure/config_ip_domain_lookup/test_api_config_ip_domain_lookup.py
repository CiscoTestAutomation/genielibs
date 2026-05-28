import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import config_ip_domain_lookup


class TestConfigIpDomainLookup(TestCase):

    def test_config_ip_domain_lookup(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_ip_domain_lookup(device, "Hu1/0/7", "14")

        self.assertIsNone(result)
        self.assertEqual(device.configure.call_count, 2)

        sent_commands = [
            call.args[0] for call in device.configure.call_args_list
        ]

        for command in sent_commands:
            self.assertIsInstance(command, str)

        self.assertIn(
            "ip domain lookup source-interface Hu1/0/7",
            sent_commands,
        )
        self.assertIn(
            "ip domain lookup source-interface vlan 14",
            sent_commands,
        )


if __name__ == "__main__":
    unittest.main()