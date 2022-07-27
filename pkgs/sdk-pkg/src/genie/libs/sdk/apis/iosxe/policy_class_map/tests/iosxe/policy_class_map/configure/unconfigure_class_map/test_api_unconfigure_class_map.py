import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_class_map.configure import unconfigure_class_map


class TestUnconfigureClassMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Startek:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Startek']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_class_map(self):
        result = unconfigure_class_map(self.device, 'test1', 'match-all')
        expected_output = None
        self.assertEqual(result, expected_output)
