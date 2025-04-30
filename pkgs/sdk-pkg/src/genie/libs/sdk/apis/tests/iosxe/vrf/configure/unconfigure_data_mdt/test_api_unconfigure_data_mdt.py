from unittest import TestCase
from genie.libs.sdk.apis.iosxe.vrf.configure import unconfigure_data_mdt
from unittest.mock import Mock


class TestUnconfigureDataMdt(TestCase):

    def test_unconfigure_data_mdt(self):
        self.device = Mock()
        result = unconfigure_data_mdt(self.device, 'Red', 'ipv4', '231.1.1.1', '0.0.0.35', '100')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['vrf definition Red', 'address-family ipv4', 'no mdt data 231.1.1.1 0.0.0.35 threshold 100'],)
        )
