import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.multicast.configure import (
    configure_pim_register_source,
)


class TestConfigurePimRegisterSource(TestCase):

    def test_configure_pim_register_source(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_pim_register_source(
            device,
            "Loopback101",
            "red",
            False,
        )

        self.assertIsNone(result)
        device.configure.assert_called_once()
        commands = device.configure.call_args.args[0]
        self.assertIsInstance(commands, list)
        self.assertEqual(
            commands,
            [
                "ip pim vrf red register-source Loopback101",
            ],
        )


if __name__ == "__main__":
    unittest.main()
