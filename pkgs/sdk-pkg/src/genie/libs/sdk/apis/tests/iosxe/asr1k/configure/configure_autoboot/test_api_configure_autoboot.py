import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.asr1k.configure import configure_autoboot


class TestConfigureAutoboot(unittest.TestCase):

    def test_configure_autoboot(self):
        self.device = Mock()
        configure_autoboot(self.device)
        self.device.configure.assert_called_once_with(
            'config-reg 0x2102'
        )
