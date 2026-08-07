import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.ipsec.configure import (
    configure_ikev2_profile_pre_share,
)


class TestConfigureIkev2ProfilePreShare(TestCase):

    def test_configure_ikev2_profile_pre_share(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ikev2_profile_pre_share(
            device,
            "scale_ikev2_profile_v4_phy",
            "pre-share",
            "pre-share",
            "ikev2_key_v4_phy",
            "19.1.1.0",
            "255.255.255.0",
            "ipv4",
            None,
            "2",
            "periodic",
            None,
            None,
            "TenGigabitEthernet1/0/1",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "crypto ikev2 profile scale_ikev2_profile_v4_phy",
                "match identity remote address 19.1.1.0 255.255.255.0",
                "authentication local pre-share",
                "authentication remote pre-share",
                "keyring local ikev2_key_v4_phy",
                "match address local interface TenGigabitEthernet1/0/1",
            ],
        )


if __name__ == "__main__":
    unittest.main()