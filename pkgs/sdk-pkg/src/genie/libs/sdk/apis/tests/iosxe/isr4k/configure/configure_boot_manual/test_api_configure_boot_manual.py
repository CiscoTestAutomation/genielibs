from unittest import TestCase
from genie.libs.sdk.apis.iosxe.isr4k.configure import configure_boot_manual
from unittest.mock import Mock


class TestConfigureBootManual(TestCase):

    def test_configure_boot_manual(self):
        self.device = Mock()
        configure_boot_manual(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('config-reg 0x0',)
        )
