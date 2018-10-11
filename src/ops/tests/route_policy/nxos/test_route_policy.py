# Python
import unittest

# ATS
from ats.topology import Device

# Genie
from genie.libs.ops.route_policy.nxos.route_policy import RoutePolicy
from genie.libs.ops.route_policy.nxos.tests.route_policy_output import \
    RoutePolicyOutput

# nxos show_route_map
from genie.libs.parser.nxos.show_route_map import ShowRouteMap


class test_route_policy(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'nxos'
        self.device.mapping={}

    def test_sample(self):

        f = RoutePolicy(device=self.device)

        f.maker.outputs[ShowRouteMap] = \
            {'':RoutePolicyOutput.showRouteMap}

        f.learn()

        self.assertEqual(f.info, RoutePolicyOutput.RoutePolicy['info'])

    def test_missing_attributes(self):
        f = RoutePolicy(device=self.device)

        f.maker.outputs[ShowRouteMap] = \
            {'':RoutePolicyOutput.showRouteMap}

        f.learn()
        with self.assertRaises(KeyError):
            vlan_access_map_value=(f.info['BGPPeers']['statements']\
                ['20']['actions']['clause']['True'])

    def test_ignored(self):

        f = RoutePolicy(device=self.device)
        g = RoutePolicy(device=self.device)


        f.maker.outputs[ShowRouteMap] = \
            {'':RoutePolicyOutput.showRouteMap}

        g.maker.outputs[ShowRouteMap] = \
            {'':RoutePolicyOutput.showRouteMap}

        f.learn()
        g.learn()

        f.diff_ignore.append('info[BGPPeers][statements][10][actions][set_route_origin][origin]')

        self.assertNotEqual(f,g)
        # Verify diff now
        diff = f.diff(g)
        sorted_diff = str(diff)
        sorted_result = ('''+diff_ignore: deque(['maker', 'callables', 'device', 'info[BGPPeers][statements][10][actions][set_route_origin][origin]'])\n-diff_ignore: deque(['maker', 'callables', 'device'])''')
        self.assertEqual(sorted_diff,sorted_result)

    def test_selective_attribute(self):

        f = RoutePolicy(device=self.device, attributes=['info[(.*)][statements]'])

        f.maker.outputs[ShowRouteMap] = \
            {'':RoutePolicyOutput.showRouteMap}

        f.learn()

        self.assertIn('10', f.info['BGPPeers']['statements'])
        self.assertNotIn('20', f.info['bgp-to-rib']['statements'])

if __name__ == '__main__':
    unittest.main()
