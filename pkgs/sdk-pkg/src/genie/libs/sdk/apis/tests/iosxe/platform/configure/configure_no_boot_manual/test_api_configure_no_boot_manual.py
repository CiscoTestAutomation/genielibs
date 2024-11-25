import os
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.configure import configure_no_boot_manual
from unittest.mock import Mock

class TestConfigureNoBootManual(TestCase):

    @classmethod
    def setUpClass(self):
        self.device = Mock()

    def test_configure_no_boot_manual(self):
        result = configure_no_boot_manual(self.device)
        self.device.configure.assert_called_with('no boot manual')
