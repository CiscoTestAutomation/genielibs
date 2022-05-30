import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_on_device


class TestConfigPolicyMapOnDevice(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
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
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_policy_map_on_device(self):
        result = configure_policy_map_on_device(self.device, 'test-shape', 'class-default', '500000')
        expected_output = None
        self.assertEqual(result, expected_output)
