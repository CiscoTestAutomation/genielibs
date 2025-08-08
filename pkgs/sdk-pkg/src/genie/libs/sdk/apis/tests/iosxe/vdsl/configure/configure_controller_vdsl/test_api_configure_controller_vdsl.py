from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vdsl.configure import configure_controller_vdsl
from unittest.mock import Mock


class TestConfigureControllerVdsl(TestCase):

    def test_configure_controller_vdsl(self):
        self.device = Mock()
        result = configure_controller_vdsl(self.device, '0/3/0', 'description test', 'operating mode auto', 'no sra', False, 'no firmware phy filename', 'training log filename bootflash:test.log', 'modem aldi', 'no diagnostics DELT')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['controller VDSL 0/3/0', 'description test', 'operating mode auto', 'no sra', 'no firmware phy filename', 'training log filename bootflash:test.log', 'modem aldi', 'no diagnostics DELT'],)
        )
