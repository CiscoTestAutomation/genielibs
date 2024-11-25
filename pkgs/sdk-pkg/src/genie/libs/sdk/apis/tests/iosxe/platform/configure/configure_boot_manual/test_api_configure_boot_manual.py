import os
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_boot_manual
from unittest.mock import Mock

class TestConfigureBootManual(TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_boot_manual(self):
        result = configure_boot_manual(self.device)
        self.device.configure.assert_called_with('boot manual')
