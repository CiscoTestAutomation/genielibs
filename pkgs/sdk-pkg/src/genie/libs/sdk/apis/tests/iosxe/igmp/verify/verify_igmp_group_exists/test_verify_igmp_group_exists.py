import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.igmp.verify import verify_igmp_group_exists, \
                                                  verify_igmp_group_not_exists

class TestVerifyIgmpGroupsExist(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          PE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_igmp_group_exists(self):
        result = verify_igmp_group_exists(self.device, "Tunnel0", '225.1.1.1')
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_igmp_group_exists_with_kwargs(self):
        result = verify_igmp_group_exists(self.device, "Tunnel0", '225.1.1.1', flags='VG')
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_igmp_group_not_exists(self):
        result = verify_igmp_group_not_exists(self.device, "Tunnel0", '225.1.1.2')
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_igmp_group_not_exists_diff_intf(self):
        result = verify_igmp_group_not_exists(self.device, "Tunnel1", '225.1.1.2')
        expected_output = True
        self.assertEqual(result, expected_output)