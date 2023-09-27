import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vdsl.configure import configure_controller_shutdown


class TestConfigureControllerShutdown(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Elixir_01:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Elixir_01']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_controller_shutdown(self):
        result = configure_controller_shutdown(self.device, '0/0/0', False)
        expected_output = None
        self.assertEqual(result, expected_output)
