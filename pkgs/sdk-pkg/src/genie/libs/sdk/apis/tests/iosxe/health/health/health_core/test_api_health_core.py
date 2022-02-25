import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.health.health import health_core


class TestHealthCore(unittest.TestCase):

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

    def test_health_core(self):
        result = health_core(self.device)
        expected_output = {'health_data': {'corefiles': [], 'num_of_cores': 0}}
        self.assertEqual(result, expected_output)
