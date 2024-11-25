import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_group


class TestConfigureRadiusGroup(unittest.TestCase):

    def test_configure_radius_group(self):
        self.device = Mock()
        result = configure_radius_group(self.device, {'server_group': 'ISEGRP2'})
        expected_output = ['aaa group server radius ISEGRP2']
        self.assertEqual(
            self.device.configure.call_args_list[0][0][0],
            ['aaa group server radius ISEGRP2',])
        self.assertEqual(result, expected_output)

    def test_configure_radius_group_1(self):
        self.device = Mock()
        result = configure_radius_group(self.device, {'dscp_acct': '32', 'dscp_auth': '40', 'server_group': 'ISEGRP2'})
        expected_output = ['aaa group server radius ISEGRP2', 'dscp auth 40', 'dscp acct 32']
        self.assertEqual(
            self.device.configure.call_args_list[0][0][0],
            ['aaa group server radius ISEGRP2', 'dscp auth 40', 'dscp acct 32'])
        self.assertEqual(result, expected_output)
