import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import remove_acl_from_interface


class TestRemoveAclFromInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          DCS-W5:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: sdwan
            type: generic
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['DCS-W5']
        self.device.connect()

    def test_remove_acl_from_interface(self):
        result = remove_acl_from_interface(self.device, 'TenGigabitEthernet0/0/0.10', 'DELETE_ME')
        expected_output = None
        self.assertEqual(result, expected_output)
