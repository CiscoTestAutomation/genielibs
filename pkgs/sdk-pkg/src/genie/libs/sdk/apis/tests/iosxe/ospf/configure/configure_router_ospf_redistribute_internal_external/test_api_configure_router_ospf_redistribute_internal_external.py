from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_router_ospf_redistribute_internal_external


class TestConfigureRouterOspfRedistributeInternalExternal(TestCase):

    def test_configure_router_ospf_redistribute_internal_external(self):
        device = Mock()
        result = configure_router_ospf_redistribute_internal_external(
            device,
            '2',
            'external',
            '1',
            '2'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                'router ospf 2',
                'redistribute ospf 2 match internal external             1 external 2'
            ],)
        )