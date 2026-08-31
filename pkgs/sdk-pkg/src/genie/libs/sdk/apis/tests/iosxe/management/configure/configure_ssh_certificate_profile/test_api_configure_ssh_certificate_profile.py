import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.management.configure import (
    configure_ssh_certificate_profile,
)


class TestConfigureSshCertificateProfile(TestCase):

    def test_configure_ssh_certificate_profile(self):
        device = Mock()
        device.state_machine.current_state = "enable"
        device.configure.return_value = None

        result = configure_ssh_certificate_profile(
            device,
            "CISCO_IDEVID_SUDI",
            True,
            True,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()

        sent_commands = device.configure.call_args.args[0]
        self.assertIsInstance(sent_commands, list)
        self.assertEqual(
            sent_commands,
            [
                "ip ssh server certificate profile",
                "server",
                "trustpoint sign CISCO_IDEVID_SUDI",
                "user",
                "trustpoint verify CISCO_IDEVID_SUDI",
            ],
        )


if __name__ == "__main__":
    unittest.main()
