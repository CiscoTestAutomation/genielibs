# Python
import unittest

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.route_policy.ios.route_policy import RoutePolicy
from genie.libs.ops.route_policy.ios.tests.route_policy_output import \
    RoutePolicyOutput

# iosxe show_route_map
from genie.libs.parser.ios.show_route_map import ShowRouteMapAll


class test_route_policy(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'ios'
        self.device.custom['abstraction'] = {'order':['os']}
        self.device.mapping={}

    def test_sample(self):

        f = RoutePolicy(device=self.device)

        f.maker.outputs[ShowRouteMapAll] = \
            {'':RoutePolicyOutput.showRouteMapAll}

        f.learn()

        self.assertEqual(f.info, RoutePolicyOutput.RoutePolicy['info'])

    def test_missing_attributes(self):
        f = RoutePolicy(device=self.device)

        f.maker.outputs[ShowRouteMapAll] = \
            {'':RoutePolicyOutput.showRouteMapAll}

        f.learn()
        with self.assertRaises(KeyError):
            vlan_access_map_value=(f.info['test']['statements']\
                ['20']['actions']['clause']['True'])

    def test_ignored(self):

        f = RoutePolicy(device=self.device)
        g = RoutePolicy(device=self.device)


        f.maker.outputs[ShowRouteMapAll] = \
            {'':RoutePolicyOutput.showRouteMapAll}

        g.maker.outputs[ShowRouteMapAll] = \
            {'':RoutePolicyOutput.showRouteMapAll}

        f.learn()
        g.learn()

        f.s = 2

        self.assertNotEqual(f,g)
        # Verify diff now
        diff = f.diff(g)
        sorted_diff = str(diff)
        sorted_result = ('+s: 2')
        self.assertEqual(sorted_diff,sorted_result)

    def test_selective_attribute(self):

        f = RoutePolicy(device=self.device, attributes=['info[(.*)][statements]'])

        f.maker.outputs[ShowRouteMapAll] = \
            {'':RoutePolicyOutput.showRouteMapAll}

        f.learn()

        self.assertIn('10', f.info['test']['statements'])
        self.assertNotIn('20', f.info['test']['statements'])

if __name__ == '__main__':
    unittest.main()