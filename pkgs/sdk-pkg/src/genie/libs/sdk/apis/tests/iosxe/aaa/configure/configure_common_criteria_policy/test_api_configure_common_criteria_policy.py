import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_common_criteria_policy


class TestConfigureCommonCriteriaPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          VTP-PK1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VTP-PK1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_common_criteria_policy(self):
        result = configure_common_criteria_policy(self.device, 'ABCD', 5, 0, 0, 1, 1, 20, 8, 0, 1, 5, True, 1)
        expected_output = None
        self.assertEqual(result, expected_output)
