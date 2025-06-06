# import os
# import unittest
# from pyats.topology import loader
# from genie.libs.sdk.apis.iosxe.acl.configure import configure_mac_access_group_mac_acl_in_out


# class TestConfigureMacAccessGroupMacAclInOut(unittest.TestCase):

#     @classmethod
#     def setUpClass(self):
#         testbed = f"""
#         devices:
#           n08HA:
#             connections:
#               defaults:
#                 class: unicon.Unicon
#               a:
#                 command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
#                 protocol: unknown
#             os: iosxe
#             platform: c9500
#             type: c9500
#         """
#         self.testbed = loader.load(testbed)
#         self.device = self.testbed.devices['n08HA']
#         self.device.connect(
#             learn_hostname=True,
#             init_config_commands=[],
#             init_exec_commands=[]
#         )

#     def test_configure_mac_access_group_mac_acl_in_out(self):
#         result = configure_mac_access_group_mac_acl_in_out(self.device, 'g1/1/1', 'MAC-acl', 'in')
#         expected_output = None
#         self.assertEqual(result, expected_output)

from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.acl.configure import configure_mac_access_group_mac_acl_in_out


class TestConfigureMacAccessGroupMacAclInOut(TestCase):

    def test_configure_mac_access_group_mac_acl_in_out(self):
        self.device = Mock()
        configure_mac_access_group_mac_acl_in_out(self.device, 'g1/1/1', 'MAC-acl', 'in')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface g1/1/1', 'mac access-group MAC-acl in'] ,)
        )
