import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.interface.configure import configure_scale_subintfs_via_tftp


class TestConfigureScaleSubintfsViaTftp(TestCase):

    def test_configure_scale_subintfs_via_tftp(self):
        device = Mock()
        device.state_machine.current_state = "enable"

        testbed = {
            "myftpserver": {
                "custom": {
                    "scale_config_path": "/auto/tftp-sjc-users4/siwwu/",
                },
                "dynamic": True,
                "protocol": "ftp",
            }
        }

        result = configure_scale_subintfs_via_tftp(
            device,
            testbed,
            "GigabitEthernet5",
            2,
            1,
            5,
            "10.2.2.1",
            "0.0.1.0",
            "255.255.255.0",
            "sparse-mode",
            False,
            False,
        )

        expected_output = (
            "\n"
            "            interface GigabitEthernet5.2\n"
            "                encapsulation dot1q 2\n"
            "                ip address 10.2.2.1 255.255.255.0\n"
            "                ip pim sparse-mode\n"
            "            exit\n"
            "            \n"
            "            interface GigabitEthernet5.3\n"
            "                encapsulation dot1q 3\n"
            "                ip address 10.2.3.1 255.255.255.0\n"
            "                ip pim sparse-mode\n"
            "            exit\n"
            "            \n"
            "            interface GigabitEthernet5.4\n"
            "                encapsulation dot1q 4\n"
            "                ip address 10.2.4.1 255.255.255.0\n"
            "                ip pim sparse-mode\n"
            "            exit\n"
            "            \n"
            "            interface GigabitEthernet5.5\n"
            "                encapsulation dot1q 5\n"
            "                ip address 10.2.5.1 255.255.255.0\n"
            "                ip pim sparse-mode\n"
            "            exit\n"
            "            \n"
            "            interface GigabitEthernet5.6\n"
            "                encapsulation dot1q 6\n"
            "                ip address 10.2.6.1 255.255.255.0\n"
            "                ip pim sparse-mode\n"
            "            exit\n"
            "            "
        )

        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()