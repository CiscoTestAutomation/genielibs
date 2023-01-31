import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.health.health import health_memory


class TestHealthMemory(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: csr1000v
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_health_memory(self):
        result = health_memory(self.device)
        expected_output = {'health_data': []}
        self.assertEqual(result, expected_output)
