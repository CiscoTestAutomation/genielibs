import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.custom_template.configure import configure_sdm_prefer_core


class TestConfigureSdmPreferCore(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SG-SVL:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SG-SVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_sdm_prefer_core(self):
        result = configure_sdm_prefer_core(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
