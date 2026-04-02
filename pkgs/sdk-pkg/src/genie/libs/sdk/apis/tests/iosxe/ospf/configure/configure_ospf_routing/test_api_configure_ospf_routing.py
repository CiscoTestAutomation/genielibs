from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_routing


class TestConfigureOspfRouting(TestCase):

    def test_configure_ospf_routing(self):
        device = Mock()
        result = configure_ospf_routing(
            device,
            200,
            None,
            False,
            True,
            'cisco',
            True,
            'debug detail',
            None,
            None,
            True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['router ospf 200', 'nsf cisco', 'nsr debug detail', 'log-adjacency-changes'],)
        )