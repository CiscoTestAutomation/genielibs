import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_service_policy_type_queueing_on_interface


class TestConfigureServicePolicyTypeQueueingOnInterface(TestCase):

    def test_configure_service_policy_type_queueing_on_interface(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_service_policy_type_queueing_on_interface(
            device,
            "GigabitEthernet1/0/10",
            "output",
            "3p1q",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet1/0/10",
                "service-policy type queueing output 3p1q",
            ],
        )


if __name__ == "__main__":
    unittest.main()