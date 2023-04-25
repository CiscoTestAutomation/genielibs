import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nve.verify import verify_nve_vni_no_entry

class TestVerifyNveVniNoEntry(unittest.TestCase):

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

    def test_verify_nve_vni_no_entry(self):
        result = verify_nve_vni_no_entry(self.device)
        expected_output = True
        self.assertEqual(result, expected_output)
