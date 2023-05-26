import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mld.verify import verify_mld_group_exists, \
                                                  verify_mld_group_not_exists

class TestVerifyMldGroupsExist(unittest.TestCase):

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

    def test_verify_mld_group_exists(self):
        result = verify_mld_group_exists(self.device, "Tunnel0", 'FF0E::501')
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_mld_group_exists_with_kwargs(self):
        result = verify_mld_group_exists(self.device, "Tunnel0", 'FF0E::501', filter_mode='exclude')
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_mld_group_not_exists(self):
        result = verify_mld_group_not_exists(self.device, "Tunnel0", 'FF0E::502')
        expected_output = True
        self.assertEqual(result, expected_output)

    def test_verify_mld_group_not_exists_diff_intf(self):
        result = verify_mld_group_not_exists(self.device, "Tunnel1", 'FF0E::502')
        expected_output = True
        self.assertEqual(result, expected_output)