from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import unconfigure_scada_enable
from unittest.mock import Mock


class TestUnconfigureScadaEnable(TestCase):

    def test_unconfigure_scada_enable(self):
        self.device = Mock()
        result = unconfigure_scada_enable(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['no scada-gw enable'],)
        )
