# import os
# import unittest
# from pyats.topology import loader
# from genie.libs.sdk.apis.iosxe.cts.configure import enable_cts_enforcement_vlan_list


# class TestEnableCtsEnforcementVlanList(unittest.TestCase):

#     @classmethod
#     def setUpClass(self):
#         testbed = f"""
#         devices:
#           A1:
#             connections:
#               defaults:
#                 class: unicon.Unicon
#               a:
#                 command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
#                 protocol: unknown
#             os: iosxe
#             platform: cat9k
#             type: single_rp
#         """
#         self.testbed = loader.load(testbed)
#         self.device = self.testbed.devices['A1']
#         self.device.connect(
#             learn_hostname=True,
#             init_config_commands=[],
#             init_exec_commands=[]
#         )

#     def test_enable_cts_enforcement_vlan_list(self):
#         result = enable_cts_enforcement_vlan_list(self.device, '1-2047')
#         expected_output = None
#         self.assertEqual(result, expected_output)
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import enable_cts_enforcement_vlan_list
from unittest.mock import Mock

class TestEnableCtsEnforcementVlanList(TestCase):
    
    def test_enable_cts_enforcement_vlan_list(self):
        self.device = Mock()
        result = enable_cts_enforcement_vlan_list(self.device, '1-2047')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['cts role-based enforcement vlan-list 1-2047'],)
        )