import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_service_instance


class TestConfigureServiceInstance(TestCase):

    def test_configure_service_instance(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_service_instance(
            device,
            "GigabitEthernet0/0/0",
            "30",
            "30",
            "ingress tag pop 1 symmetric",
            "20",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "interface GigabitEthernet0/0/0",
                "service instance 30 ethernet",
                "encapsulation dot1q 30",
                "rewrite ingress tag pop 1 symmetric",
                "bridge-domain 20",
            ],
        )


if __name__ == "__main__":
    unittest.main()