import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.wsim.execute import simulate_ap_container


class TestSimulateApContainer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          wsim4ca14d90:~$:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os linux --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: linux
            platform: wsim
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['wsim4ca14d90:~$']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_simulate_ap_container(self):
        result = simulate_ap_container(self.device, '1', '600')
        expected_output = None
        self.assertEqual(result, expected_output)
