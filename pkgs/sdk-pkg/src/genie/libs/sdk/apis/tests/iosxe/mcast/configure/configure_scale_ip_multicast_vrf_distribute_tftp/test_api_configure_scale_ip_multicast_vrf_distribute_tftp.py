import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mcast.configure import (
    configure_scale_ip_multicast_vrf_distribute_tftp,
)


class TestConfigureScaleIpMulticastVrfDistributeTftp(TestCase):

    def test_configure_scale_ip_multicast_vrf_distribute_tftp(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_scale_ip_multicast_vrf_distribute_tftp(
            device,
            {
                "myftpserver": {
                    "custom": {
                        "scale_config_path": "/auto/tftp-sjc-users4/siwwu/",
                    },
                    "dynamic": True,
                    "protocol": "ftp",
                },
            },
            2,
            1,
            10,
            False,
            False,
        )

        expected_output = (
            "\n"
            "         ip multicast-routing vrf 2 distributed\n"
            "        \n"
            "         ip multicast-routing vrf 3 distributed\n"
            "        \n"
            "         ip multicast-routing vrf 4 distributed\n"
            "        \n"
            "         ip multicast-routing vrf 5 distributed\n"
            "        \n"
            "         ip multicast-routing vrf 6 distributed\n"
            "        \n"
            "         ip multicast-routing vrf 7 distributed\n"
            "        \n"
            "         ip multicast-routing vrf 8 distributed\n"
            "        \n"
            "         ip multicast-routing vrf 9 distributed\n"
            "        \n"
            "         ip multicast-routing vrf 10 distributed\n"
            "        \n"
            "         ip multicast-routing vrf 11 distributed\n"
            "        "
        )

        self.assertEqual(result, expected_output)
        device.configure.assert_not_called()


if __name__ == "__main__":
    unittest.main()
