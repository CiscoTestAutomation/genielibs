import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_global_apply


class TestConfigureMacroGlobalApply(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          C9300CR-matrix:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat900
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['C9300CR-matrix']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_macro_global_apply(self):
        result = configure_macro_global_apply(self.device, 'm-qos', '$interface', '"range gi1/0/1-48"', 60)
        expected_output = None
        self.assertEqual(result, expected_output)
