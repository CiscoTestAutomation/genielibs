import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.health.health import health_core


class TestHealthCore(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R3_nx:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir mock_data --state connect
                protocol: unknown
            os: nxos
            platform: n9k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R3_nx']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_health_core(self):
        result = health_core(self.device)
        expected_output = {'health_data': {'corefiles': [], 'num_of_cores': 1}}
        self.assertEqual(result, expected_output)
