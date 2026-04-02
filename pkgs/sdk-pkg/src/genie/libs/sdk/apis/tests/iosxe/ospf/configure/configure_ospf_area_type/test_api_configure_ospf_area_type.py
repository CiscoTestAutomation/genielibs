from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_area_type


class TestConfigureOspfAreaType(TestCase):

    def test_configure_ospf_area_type(self):
        device = Mock()
        result = configure_ospf_area_type(
            device,
            1,
            5,
            'nssa',
            'translate',
            'suppress-fa'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 1', 'area 5 nssa translate type7 suppress-fa'],)
        )