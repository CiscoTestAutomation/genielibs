import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.c8kv.configure import configure_no_boot_manual


class TestConfigureNoBootManual(unittest.TestCase):

    def test_configure_no_boot_manual(self):
        self.device = Mock()
        configure_no_boot_manual(self.device)
        self.device.api.configure_autoboot.assert_called_once_with()
