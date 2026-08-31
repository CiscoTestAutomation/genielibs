import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vpdn.configure import (
    unconfigure_vpdn_group,
    unconfigure_vpdn_group_initiate_to_entries,
    unconfigure_vpdn_l2tp_attribute_initial_received_lcp_confreq,
)


class TestUnconfigureVpdnGroup(unittest.TestCase):

    def test_unconfigure_vpdn_group(self):
        device = Mock()

        result = unconfigure_vpdn_group(device, '11')

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'no vpdn-group 11',
            ]
        )

    def test_unconfigure_vpdn_group_initiate_to_entries(self):
        device = Mock()

        result = unconfigure_vpdn_group_initiate_to_entries(
            device,
            '1',
            ['10.1.1.1', '10.1.1.2'],
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'vpdn-group 1',
                'no initiate-to ip 10.1.1.1',
                'no initiate-to ip 10.1.1.2',
            ]
        )

    def test_unconfigure_vpdn_l2tp_attribute_initial_received_lcp_confreq(self):
        device = Mock()

        result = unconfigure_vpdn_l2tp_attribute_initial_received_lcp_confreq(
            device
        )

        self.assertIsNone(result)
        device.configure.assert_called_once_with(
            [
                'no vpdn l2tp attribute initial-received-lcp-confreq',
            ]
        )
