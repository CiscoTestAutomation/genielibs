from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import configure_data_mdt
from unittest.mock import Mock


class TestConfigureDataMdt(TestCase):

    def test_configure_data_mdt(self):
        self.device = Mock()
        result = configure_data_mdt(self.device, 'VRF1', 'ipv4', '239.1.1.1', '0.0.0.255', 1000)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vrf definition VRF1', 'address-family ipv4', 'mdt data 239.1.1.1 0.0.0.255 threshold 1000'],)
        )
