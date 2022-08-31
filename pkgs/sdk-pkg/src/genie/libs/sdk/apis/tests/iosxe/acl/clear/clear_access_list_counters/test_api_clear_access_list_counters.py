import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.clear import clear_access_list_counters


class TestClearAccessListCounters(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Cat9600-SVL_CGW:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Cat9600-SVL_CGW']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_access_list_counters(self):
        result = clear_access_list_counters(self.device, '')
        expected_output = None
        self.assertEqual(result, expected_output)
