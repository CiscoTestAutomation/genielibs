from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_vrf_lite


class TestConfigureOspfVrfLite(TestCase):

    def test_configure_ospf_vrf_lite(self):
        device = Mock()
        result = configure_ospf_vrf_lite(
            device,
            '11',
            'vrf1'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 11 vrf vrf1', 'capability vrf-lite'],)
        )