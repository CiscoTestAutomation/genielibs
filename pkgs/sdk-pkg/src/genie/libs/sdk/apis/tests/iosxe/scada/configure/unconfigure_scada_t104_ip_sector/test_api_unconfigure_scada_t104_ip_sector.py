from unittest import TestCase
from genie.libs.sdk.apis.iosxe.scada.configure import unconfigure_scada_t104_ip_sector
from unittest.mock import Mock


class TestUnconfigureScadaT104IpSector(TestCase):

    def test_unconfigure_scada_t104_ip_sector(self):
        self.device = Mock()
        result = unconfigure_scada_t104_ip_sector(self.device, 't104_ip_sector_1')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['scada-gw protocol t104', 'no sector t104_ip_sector_1'],)
        )
