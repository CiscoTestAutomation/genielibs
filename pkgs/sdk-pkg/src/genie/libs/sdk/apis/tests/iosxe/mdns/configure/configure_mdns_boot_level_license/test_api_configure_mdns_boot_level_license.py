import unittest
from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.mdns.configure import (
    configure_mdns_boot_level_license,
)


class TestConfigureMdnsBootLevelLicense(TestCase):

    def test_configure_mdns_boot_level_license(self):
        device = Mock()
        device.configure.return_value = None

        result = configure_mdns_boot_level_license(
            device,
            "dna-advantage",
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                "license boot level network-advantage addon dna-advantage",
                "do write memory",
            ]
        )


if __name__ == "__main__":
    unittest.main()
