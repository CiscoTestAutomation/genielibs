import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.macsec.configure import (
    config_mka_policy,
)


class TestConfigMkaPolicy(TestCase):

    def test_config_mka_policy(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = config_mka_policy(
            device=device,
            global_level=True,
            interface="TwentyFiveGigE 1/0/7",
            cipher="GCM-AES-128",
            send_secure_announcements="",
            sak_rekey_int=180,
            key_server_priority=255,
            sak_rekey_on_live_peer_loss=True,
            conf_offset=30,
            policy_name="MKA_policy1",
            delay_protection=True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "mka policy MKA_policy1",
                "macsec-cipher-suite GCM-AES-128",
                "sak-rekey interval 180",
                "key-server priority 255",
                "confidentiality-offset 30",
                "sak-rekey on-live-peer-loss",
                "delay-protection",
                "interface TwentyFiveGigE 1/0/7",
                "mka policy MKA_policy1",
            ],
        )


if __name__ == "__main__":
    unittest.main()
