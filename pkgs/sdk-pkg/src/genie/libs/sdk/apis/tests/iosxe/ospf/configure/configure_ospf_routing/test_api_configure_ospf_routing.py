from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_routing
from unittest.mock import Mock


class TestConfigureOspfRouting(TestCase):

    def test_configure_ospf_routing(self):
        self.device = Mock()
        result = configure_ospf_routing(self.device, '1', None, False, None, None, None, None, None, None, False, 'area 0 mpls', 'per-prefix ti-lfa', 'avoidance segment-routing', '128', 'advertise-definition', True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router ospf 1', 'segment-routing area 0 mpls', 'fast-reroute per-prefix ti-lfa', 'microloop avoidance segment-routing', 'flex-algo 128', 'advertise-definition', 'bfd all-interfaces'],)
        )
