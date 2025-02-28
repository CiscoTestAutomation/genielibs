from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import configure_scada_enable
from unittest.mock import Mock


class TestConfigureScadaEnable(TestCase):

    def test_configure_scada_enable(self):
        self.device = Mock()
        result = configure_scada_enable(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw enable'],)
        )
