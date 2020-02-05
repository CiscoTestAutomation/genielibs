# Python
import unittest

# ATS
from pyats.topology import Device

# Genie
from genie.libs.ops.route_policy.iosxr.route_policy import RoutePolicy
from genie.libs.ops.route_policy.iosxr.tests.route_policy_output import \
    RoutePolicyOutput

# iosxr show_rpl
from genie.libs.parser.iosxr.show_rpl import ShowRplRoutePolicy


class test_route_policy(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxr'
        self.device.mapping={}

    def test_sample(self):

        f = RoutePolicy(device=self.device)

        f.maker.outputs[ShowRplRoutePolicy] = \
            {'':RoutePolicyOutput.showRplRoutePolicy}

        f.learn()

        self.assertEqual(f.info, RoutePolicyOutput.RoutePolicy['info'])

    def test_missing_attributes(self):
        f = RoutePolicy(device=self.device)

        f.maker.outputs[ShowRplRoutePolicy] = \
            {'':RoutePolicyOutput.showRplRoutePolicy}

        f.learn()
        with self.assertRaises(KeyError):
            vlan_access_map_value=(f.info['test3']['statements']\
                ['20']['actions']['set_as_path_prepend']['100'])

    def test_ignored(self):

        f = RoutePolicy(device=self.device)
        g = RoutePolicy(device=self.device)


        f.maker.outputs[ShowRplRoutePolicy] = \
            {'':RoutePolicyOutput.showRplRoutePolicy}

        g.maker.outputs[ShowRplRoutePolicy] = \
            {'':RoutePolicyOutput.showRplRoutePolicy}

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

        f.maker.outputs[ShowRplRoutePolicy] = \
            {'':RoutePolicyOutput.showRplRoutePolicy}

        f.learn()

        self.assertIn(10, f.info['aspath']['statements'])
        self.assertNotIn('20', f.info['as-path']['statements'])

    def test_empty_output(self):

        f = RoutePolicy(device=self.device)

        f.maker.outputs[ShowRplRoutePolicy] = {'':''}

        # Learn the feature
        f.learn()

        # Check no attribute not found
        # info - description
        with self.assertRaises(AttributeError):
            description = (f.info['NO-EXPORT']['description'])


if __name__ == '__main__':
    unittest.main()
